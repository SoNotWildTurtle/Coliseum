"""MMO hub flow helpers extracted from the main game class."""

from __future__ import annotations

import random

import pygame


class GameMMOFlow:
    """Flow helper mixin for MMO hub state updates."""

    def _mmo_patrol_target_region(self) -> dict[str, object] | None:
        if self.mmo_world_events:
            severity_rank = {"high": 3, "medium": 2, "low": 1}
            sorted_events = sorted(
                self.mmo_world_events,
                key=lambda event: severity_rank.get(
                    str(event.get("severity", "low")).lower(),
                    0,
                ),
                reverse=True,
            )
            for event in sorted_events:
                region = self._mmo_find_region(str(event.get("region", "")))
                if region:
                    return region
        if self.mmo_contracts:
            for contract in self.mmo_contracts:
                status = str(contract.get("status", "active"))
                if status in {"active", "accepted"}:
                    region = self._mmo_find_region(str(contract.get("region", "")))
                    if region:
                        return region
        return None

    def _mmo_dispatch_patrols(self, now: int) -> None:
        if now - self.mmo_last_patrol_dispatch < self.mmo_patrol_dispatch_interval:
            return
        self.mmo_last_patrol_dispatch = now
        region = self._mmo_patrol_target_region()
        if not region:
            return
        self._mmo_assign_patrol(region)

    def _mmo_update_threat_history(self) -> None:
        regions = self._mmo_regions()
        if not regions:
            return
        history = self.mmo_threat_history
        window = max(2, int(self.mmo_threat_history_window))
        for region in regions:
            name = str(region.get("name", "region"))
            threat = float(self._mmo_region_threat(region))
            series = history.get(name, [])
            series.append(threat)
            if len(series) > window:
                series = series[-window:]
            history[name] = series

    def _mmo_assign_patrol(self, region: dict[str, object]) -> None:
        pos = region.get("position")
        if not pos or len(pos) != 2:
            self.mmo_message = "Selected region missing position."
            return
        if not self.mmo_auto_agents:
            self.mmo_auto_agents.append(
                {
                    "id": f"agent_{len(self.mmo_auto_agents) + 1}",
                    "pos": [float(pos[0]), float(pos[1])],
                    "dir": [0.0, 0.0],
                    "cooldown": 0,
                }
            )
        best_agent = None
        best_dist = None
        target = [float(pos[0]), float(pos[1])]
        for agent in self.mmo_auto_agents:
            agent_pos = agent.get("pos") or [0.0, 0.0]
            dx = float(agent_pos[0]) - target[0]
            dy = float(agent_pos[1]) - target[1]
            dist = dx * dx + dy * dy
            if best_dist is None or dist < best_dist:
                best_dist = dist
                best_agent = agent
        if not best_agent:
            self.mmo_message = "No patrol agents available."
            return
        best_agent["target"] = target
        best_agent["assignment"] = str(region.get("name", "region"))
        label = best_agent.get("id", "agent")
        self.mmo_message = f"Patrol assigned: {label}."
        self._mmo_log_event(
            f"Patrol {label} assigned to {best_agent['assignment']}."
        )

    def _update_mmo_world(self, now: int) -> None:
        """Update MMO world events, contracts, and operation timers."""
        if now - self.mmo_last_world_tick < self.mmo_world_tick_interval:
            return
        self.mmo_last_world_tick = now
        self._mmo_update_threat_history()
        expired_events = [
            event
            for event in self.mmo_world_events
            if event.get("expires_at", 0) <= now
        ]
        for event in expired_events:
            if isinstance(event, dict):
                self._mmo_record_tombstone("world_event", event, now)
        self.mmo_world_events = [
            event for event in self.mmo_world_events if event not in expired_events
        ]
        self._mmo_prune_tombstones(now)
        self._mmo_prune_alerts(now)
        self._mmo_seed_events()
        self._mmo_seed_expeditions()
        self._mmo_seed_directives()
        self._mmo_seed_bounties()
        self._mmo_supply_tick()
        self._mmo_market_tick()
        self._mmo_crafting_tick()
        self._mmo_update_campaigns()
        self._mmo_update_expeditions(now)
        self._mmo_update_directives(now)
        self._mmo_update_bounties(now)
        self._mmo_update_influence(now)
        self._mmo_seed_projects()
        self._mmo_update_projects(now)
        self._mmo_seed_training()
        self._mmo_update_training(now)
        self._mmo_auto_dev_pulse(now)
        self._mmo_dispatch_patrols(now)
        if self.mmo_stockpile:
            low = [
                name
                for name, amount in self.mmo_stockpile.items()
                if int(amount) <= 2
            ]
            if low:
                self._mmo_add_alert(
                    f"Low stock: {', '.join(low[:3])}.",
                    level="warn",
                )
        for shipment in list(self.mmo_shipments):
            if shipment.get("status") != "in_transit":
                continue
            risk = str(shipment.get("risk", "low")).lower()
            escorted = bool(shipment.get("escorted"))
            if risk == "high" and not escorted:
                rng = random.Random(
                    self.mmo_ai_seed + int(now / 1000) + len(self.mmo_shipments)
                )
                if rng.random() < 0.03:
                    shipment["eta"] = int(shipment.get("eta", 0)) + 1
                    destination = shipment.get("destination", "Frontier")
                    self._mmo_add_alert(
                        f"Ambush near {destination}; shipment delayed.",
                        level="warn",
                    )
            shipment["eta"] = max(0, int(shipment.get("eta", 0)) - 1)
            if shipment["eta"] <= 0:
                shipment["status"] = "delivered"
                destination = shipment.get("destination", "Frontier")
                reward = int(shipment.get("amount", 0))
                faction, _ = self._mmo_region_influence(
                    self._mmo_find_region(str(destination)) or {}
                )
                self.reputation_manager.modify(faction, max(1, reward))
                if shipment.get("escorted"):
                    self.mmo_credits += 5
                    self._mmo_log_event("Escort bonus: +5 credits.")
                self._mmo_log_event(
                    f"Shipment delivered to {destination} for {faction}."
                )
                self._mmo_record_stat("shipments_delivered")
        for op in self.mmo_operations:
            if op.get("status") != "active":
                continue
            eta = int(op.get("eta", 0)) - 1
            op["eta"] = max(0, eta)
            if eta <= 0:
                op["status"] = "complete"
                if "retire_at" not in op:
                    op["retire_at"] = now + 6000
                self._mmo_notify(
                    f"{op.get('name', 'Operation')} completed.", level="info"
                )
            self._mmo_touch_entry(
                op,
                now,
                prefix="operation",
                key_fields=("name", "region"),
            )
        for op in list(self.mmo_operations):
            if op.get("status") == "complete" and now >= int(op.get("retire_at", 0)):
                self._mmo_record_tombstone("operation", op, now)
                self.mmo_operations.remove(op)
        for contract in self.mmo_contracts:
            if contract.get("status") != "active":
                continue
            eta = int(contract.get("eta", 0)) - 1
            contract["eta"] = max(0, eta)
            if eta <= 0:
                contract["status"] = "complete"
                reward = int(contract.get("reward", 0))
                if self.mmo_guilds:
                    guild = random.choice(self.mmo_guilds).get("name", "Guild")
                else:
                    guild = "Guild"
                self.reputation_manager.modify(str(guild), max(1, reward // 5))
                self._mmo_notify(
                    f"{contract.get('name', 'Contract')} completed.", level="info"
                )
        for route in list(self.mmo_trade_routes):
            if route.get("status") != "closed":
                continue
            if now >= int(route.get("retire_at", 0)):
                self._mmo_record_tombstone("trade_route", route, now)
                self.mmo_trade_routes.remove(route)

    def _mmo_build_outpost(self, region: dict[str, object]) -> None:
        name = str(region.get("name", "region"))
        for outpost in self.mmo_outposts:
            if outpost.get("region") == name:
                self.mmo_message = f"Outpost already built at {name}."
                return
        outpost = {
            "region": name,
            "level": 1,
            "status": "operational",
        }
        self._mmo_touch_entry(
            outpost,
            pygame.time.get_ticks(),
            prefix="outpost",
            key_fields=("region",),
        )
        self.mmo_outposts.append(outpost)
        self.mmo_backend.upsert_outpost(outpost)
        self.mmo_message = f"Outpost established at {name}."
        self._mmo_log_event(f"Outpost established at {name}.")

    def _mmo_remove_outpost(self, region: dict[str, object]) -> None:
        name = str(region.get("name", "region"))
        for outpost in list(self.mmo_outposts):
            if outpost.get("region") != name:
                continue
            now = pygame.time.get_ticks()
            self._mmo_record_tombstone("outpost", outpost, now)
            self.mmo_outposts.remove(outpost)
            self.mmo_message = f"Outpost removed from {name}."
            self._mmo_log_event(f"Outpost removed from {name}.")
            return
        self.mmo_message = "No outpost to remove."

    def _mmo_auto_dev_pulse(self, now: int) -> None:
        if now - self.mmo_last_auto_dev_tick < self.mmo_auto_dev_interval:
            return
        self.mmo_last_auto_dev_tick = now
        focus = self.auto_dev_manager.region_insight()
        scenario_manager = self.world_generation_manager.scenario_manager
        scenarios = scenario_manager.scenario_briefs() if scenario_manager else []
        crafting = self.world_generation_manager.crafting_manager
        trade_skills = []
        if crafting and crafting.generator:
            trade_skills = list(crafting.generator.list_core_skills())
        plan = self.mmo_pipeline.build_plan(
            focus=focus,
            scenarios=scenarios,
            trade_skills=trade_skills,
        )
        overview = plan.get("overview", {}) if isinstance(plan, dict) else {}
        hazards = overview.get("hazards", ()) if isinstance(overview, dict) else ()
        upgrades = overview.get("network_upgrades", ()) if isinstance(overview, dict) else ()
        focus_region = self._mmo_focus_region(plan)
        if hazards:
            region_name = (
                focus_region.get("name", "Frontier")
                if focus_region
                else "Frontier"
            )
            directive = {
                "id": f"D-{self.mmo_directive_sequence:03d}",
                "kind": "Mitigation",
                "region": region_name,
                "status": "open",
                "eta": 3,
                "eta_total": 3,
                "assignee": None,
                "reward": 55,
                "resource": "Supplies",
            }
            self.mmo_directive_sequence += 1
            self.mmo_directives.append(directive)
        if upgrades:
            self._mmo_append_project()
            self._mmo_append_training()
        if len(self.mmo_contracts) < 3:
            self._mmo_append_contract()
        if len(self.mmo_operations) < 3:
            self._mmo_append_operation()
        if plan:
            boss_plan = plan.get("boss_plan", {})
            boss_name = str(boss_plan.get("name", "Unknown"))
            threat = float(boss_plan.get("threat", 0.0) or 0.0)
            summary = f"Auto-dev pulse: {boss_name} (Threat {threat:.1f})."
            self.mmo_message = summary
            self._mmo_log_event(summary)
        if focus_region:
            self.mmo_focus_region_name = focus_region.get("name")
            self.mmo_focus_region_threat = float(
                self._mmo_region_threat(focus_region)
            )
            for expedition in self.mmo_expeditions:
                status = str(expedition.get("status", "idle"))
                if status in {"idle", "complete"}:
                    self._mmo_redeploy_expedition_to_region(
                        expedition, focus_region, now
                    )
                    break
            self._mmo_route_patrols_to_region(focus_region)
        self._mmo_auto_escort_shipments(now)
        for directive in self.mmo_directives:
            if directive.get("status") == "open":
                self._mmo_assign_directive(directive)
                break
        for bounty in self.mmo_bounties:
            if bounty.get("status") == "open":
                self._mmo_assign_bounty(bounty)
                break
        for project in self.mmo_projects:
            if project.get("status") == "open":
                self._mmo_start_project(project)
                break
        for training in self.mmo_training_queue:
            if training.get("status") == "open":
                self._mmo_start_training(training)
                break

    def _mmo_focus_region(self, plan: dict[str, object]) -> dict[str, object] | None:
        regions = self._mmo_regions()
        if not regions:
            return None
        overview = plan.get("overview", {}) if isinstance(plan, dict) else {}
        preferred_biome = None
        if isinstance(overview, dict):
            preferred_biome = overview.get("preferred_biome")
        if not preferred_biome:
            boss_plan = plan.get("boss_plan", {}) if isinstance(plan, dict) else {}
            hazard = str(boss_plan.get("hazard", ""))
            preferred_biome = self._mmo_biome_from_hazard(hazard)
        candidates = regions
        if preferred_biome:
            candidates = [
                region
                for region in regions
                if str(region.get("biome", "")).lower() == str(preferred_biome).lower()
            ] or regions
        return max(candidates, key=self._mmo_region_threat)

    @staticmethod
    def _mmo_biome_from_hazard(hazard: str) -> str | None:
        hazard = hazard.lower()
        if "ice" in hazard or "tundra" in hazard:
            return "tundra"
        if "lava" in hazard or "burn" in hazard or "desert" in hazard:
            return "desert"
        if "poison" in hazard or "forest" in hazard:
            return "forest"
        if "wind" in hazard or "storm" in hazard:
            return "plains"
        return None

    def _mmo_redeploy_expedition_to_region(
        self,
        expedition: dict[str, object],
        region: dict[str, object],
        now: int,
    ) -> None:
        rng = random.Random(self.mmo_ai_seed + int(now / 1000))
        resource, richness = self._mmo_region_resources(region)
        expedition["region"] = region.get("name", "Frontier")
        expedition["status"] = "en_route"
        expedition["eta"] = rng.randint(2, 6)
        expedition["eta_total"] = int(expedition["eta"])
        expedition["reward"] = rng.randint(25, 70) + richness * 5
        expedition["resource"] = resource
        expedition["richness"] = richness
        expedition["risk"] = rng.choice(["Low", "Medium", "High"])
        self._mmo_log_event(
            f"{expedition.get('name', 'Expedition')} rerouted to "
            f"{expedition.get('region', 'region')}."
        )

    def _mmo_route_patrols_to_region(self, region: dict[str, object]) -> None:
        pos = region.get("position")
        if not pos or len(pos) != 2:
            return
        for agent in self.mmo_auto_agents:
            agent["target"] = [float(pos[0]), float(pos[1])]

    def _mmo_auto_escort_shipments(self, now: int) -> None:
        if now - self.mmo_last_shipment_auto < self.mmo_auto_dev_shipment_cooldown:
            return
        self.mmo_last_shipment_auto = now
        focus_threat = float(self.mmo_focus_region_threat or 0.0)
        allow_medium = focus_threat >= 5.0
        for shipment in self.mmo_shipments:
            if shipment.get("status") != "in_transit":
                continue
            if shipment.get("escorted"):
                continue
            risk = str(shipment.get("risk", "low")).lower()
            if risk == "high":
                pass
            elif risk == "medium" and allow_medium:
                pass
            else:
                continue
            if self.mmo_credits < 15:
                continue
            self._mmo_toggle_shipment_escort(shipment)
            break

    def _mmo_open_trade_route(self, region: dict[str, object]) -> None:
        origin = str(region.get("name", "region"))
        target = None
        for favorite in sorted(self.mmo_favorites):
            if favorite != origin:
                target = favorite
                break
        if target is None:
            regions = self._mmo_regions()
            if len(regions) > 1:
                next_index = (self.mmo_region_index + 1) % len(regions)
                target = str(regions[next_index].get("name", "region"))
        if target is None or target == origin:
            self.mmo_message = "No valid trade route target."
            return
        route = {"origin": origin, "destination": target, "status": "active"}
        self._mmo_touch_entry(
            route,
            pygame.time.get_ticks(),
            prefix="route",
            key_fields=("origin", "destination"),
        )
        self.mmo_trade_routes.append(route)
        self.mmo_backend.record_route(route)
        self.mmo_message = f"Route opened: {origin} -> {target}."
        self._mmo_log_event(f"Trade route opened from {origin} to {target}.")

    def _mmo_close_trade_route(self, region: dict[str, object]) -> None:
        origin = str(region.get("name", "region"))
        for route in list(self.mmo_trade_routes):
            if route.get("origin") != origin:
                continue
            now = pygame.time.get_ticks()
            route["status"] = "closed"
            route["retire_at"] = now + 6000
            self._mmo_touch_entry(
                route,
                now,
                prefix="route",
                key_fields=("origin", "destination"),
            )
            self.mmo_message = f"Route closed from {origin}."
            self._mmo_log_event(f"Trade route closed from {origin}.")
            return
        self.mmo_message = "No trade route to close."

    def _mmo_dispatch_operation(self, region: dict[str, object]) -> None:
        name = str(region.get("name", "region"))
        threat = float(self._mmo_region_threat(region))
        if threat >= 7.0:
            priority = "High"
            risk = "High"
        elif threat >= 4.0:
            priority = "Medium"
            risk = "Medium"
        else:
            priority = "Low"
            risk = "Low"
        op = {
            "name": f"Ops-{len(self.mmo_operations) + 1}",
            "region": name,
            "status": "active",
            "priority": priority,
            "risk": risk,
            "eta": random.randint(2, 6),
        }
        self._mmo_touch_entry(
            op,
            pygame.time.get_ticks(),
            prefix="operation",
            key_fields=("name", "region"),
        )
        self.mmo_operations.append(op)
        self.mmo_backend.record_operation(op)
        self.mmo_message = f"Operation dispatched to {name}."
        self._mmo_log_event(f"Operation dispatched to {name}.")

