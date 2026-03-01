"""MMO hub logic helpers extracted from the main game class."""

from __future__ import annotations

import random
import time

from .mmo_world_state_manager import MMOWorldStateManager

from .weather_forecast_manager import WeatherForecastManager


class GameMMOLogic:
    """Logic helper mixin for MMO hub simulation and state."""

    @staticmethod
    def _mmo_time_ms() -> int:
        return int(time.time() * 1000)

    def _mmo_touch_entry(
        self,
        entry: dict[str, object],
        now: int,
        *,
        prefix: str,
        key_fields: tuple[str, ...],
    ) -> None:
        if "id" not in entry:
            key = ":".join(str(entry.get(field, "")) for field in key_fields)
            entry["id"] = f"{prefix}:{key}"
        entry["updated_at"] = int(now)
        entry.setdefault("origin", self.mmo_player_id)

    def _mmo_record_tombstone(
        self,
        kind: str,
        entry: dict[str, object],
        now: int,
    ) -> None:
        entry_id = entry.get("id")
        if entry_id is None:
            return
        for tombstone in self.mmo_world_tombstones:
            if (
                tombstone.get("kind") == kind
                and tombstone.get("id") == entry_id
            ):
                tombstone["updated_at"] = int(now)
                tombstone["origin"] = self.mmo_player_id
                tombstone["shard"] = self.mmo_shard_id
                return
        self.mmo_world_tombstones.append(
            {
                "kind": kind,
                "id": entry_id,
                "updated_at": int(now),
                "origin": self.mmo_player_id,
                "shard": self.mmo_shard_id,
            }
        )

    def _mmo_prune_tombstones(self, now: int) -> None:
        ttl = int(self.mmo_world_tombstone_ttl_ms)
        if ttl <= 0:
            return
        cutoff = int(now) - ttl
        self.mmo_world_tombstones = [
            tombstone
            for tombstone in self.mmo_world_tombstones
            if int(tombstone.get("updated_at", 0) or 0) >= cutoff
        ]

    def _mmo_nearest_region(self, pos: tuple[float, float]) -> dict[str, object] | None:
        regions = self.world_generation_manager.region_manager.get_regions()
        if not regions:
            return None
        best = None
        best_dist = None
        for region in regions:
            rpos = region.get("position")
            if not rpos or len(rpos) != 2:
                continue
            dx = float(rpos[0]) - pos[0]
            dy = float(rpos[1]) - pos[1]
            dist = dx * dx + dy * dy
            if best_dist is None or dist < best_dist:
                best_dist = dist
                best = region
        return best

    def _mmo_regions(self) -> list[dict[str, object]]:
        regions = self.world_generation_manager.region_manager.get_regions()
        if self.mmo_biome_filter != "all":
            regions = [
                region
                for region in regions
                if str(region.get("biome", "")).lower() == self.mmo_biome_filter
            ]
        if self.mmo_sort_mode == "distance":
            player_pos = self.world_player_manager.get_position(self.mmo_player_id)
            return sorted(
                regions,
                key=lambda r: self._mmo_region_distance(r, player_pos),
            )
        if self.mmo_sort_mode == "level":
            return sorted(
                regions,
                key=lambda r: int(r.get("recommended_level", 0) or 0),
            )
        if self.mmo_sort_mode == "biome":
            return sorted(
                regions,
                key=lambda r: (
                    str(r.get("biome", "")),
                    str(r.get("name", "")),
                ),
            )
        if self.mmo_sort_mode == "threat":
            return sorted(
                regions,
                key=lambda r: self._mmo_region_threat(r),
                reverse=True,
            )
        return sorted(regions, key=lambda r: str(r.get("name", "")))

    def _mmo_selected_region(self) -> dict[str, object] | None:
        regions = self._mmo_regions()
        if not regions:
            return None
        self.mmo_region_index = max(
            0, min(self.mmo_region_index, len(regions) - 1)
        )
        return regions[self.mmo_region_index]

    def _mmo_find_region(self, name: str) -> dict[str, object] | None:
        regions = self.world_generation_manager.region_manager.get_regions()
        for region in regions:
            if str(region.get("name", "")).lower() == name.lower():
                return region
        return None

    def _mmo_region_distance(
        self,
        region: dict[str, object],
        player_pos: tuple[float, float],
    ) -> float:
        pos = region.get("position")
        if not pos or len(pos) != 2:
            return float("inf")
        dx = float(pos[0]) - player_pos[0]
        dy = float(pos[1]) - player_pos[1]
        return dx * dx + dy * dy

    def _mmo_region_threat(self, region: dict[str, object]) -> float:
        level = float(region.get("recommended_level", 1) or 1)
        feature = region.get("feature") or {}
        feature_bonus = 1.5 if isinstance(feature, dict) and feature else 0.0
        auto_dev = region.get("auto_dev", {}) if isinstance(region, dict) else {}
        plan_summary = auto_dev.get("auto_dev_plan_summary", {})
        hazard_focus = str(plan_summary.get("hazards") or "")
        hazard_bonus = 1.5 if hazard_focus else 0.0
        events = self._mmo_region_events(str(region.get("name", "")))
        event_bonus = 0.0
        if events:
            severity = str(events[0].get("severity", "low")).lower()
            if severity == "high":
                event_bonus = 2.0
            elif severity == "medium":
                event_bonus = 1.0
        return level + feature_bonus + hazard_bonus + event_bonus

    def _mmo_region_weather(
        self,
        region: dict[str, object],
        now: int,
    ) -> tuple[str, list[str]]:
        seed = str(region.get("seed") or region.get("name") or "region")
        schedule = self.mmo_weather_cache.get(seed)
        if not schedule:
            manager = WeatherForecastManager(seed, weather_types=[
                "clear",
                "rain",
                "snow",
                "wind",
                "storm",
            ])
            schedule = manager.forecast(12)
            self.mmo_weather_cache[seed] = schedule
        if not schedule:
            return "clear", []
        index = int(now / 8000) % len(schedule)
        upcoming = [
            schedule[(index + step) % len(schedule)]
            for step in range(1, self.mmo_weather_forecast_steps + 1)
        ]
        return schedule[index], upcoming

    def _mmo_threat_trend(self, region_name: str) -> str:
        series = self.mmo_threat_history.get(region_name, [])
        if len(series) < 2:
            return "Stable"
        delta = float(series[-1]) - float(series[0])
        if abs(delta) < 0.3:
            return "Stable"
        return "Rising" if delta > 0 else "Falling"

    def _mmo_heatmap_threat(self, region: dict[str, object]) -> float:
        name = str(region.get("name", "region"))
        series = self.mmo_threat_history.get(name, [])
        if series:
            return sum(float(value) for value in series) / len(series)
        return float(self._mmo_region_threat(region))

    def _mmo_cycle_sort(self) -> None:
        idx = self.mmo_sort_modes.index(self.mmo_sort_mode)
        self.mmo_sort_mode = self.mmo_sort_modes[(idx + 1) % len(self.mmo_sort_modes)]
        self.mmo_message = f"Sort: {self.mmo_sort_mode.title()}"

    def _mmo_region_resources(self, region: dict[str, object]) -> tuple[str, int]:
        seed = str(region.get("seed") or region.get("name") or "region")
        cached = self.mmo_resource_cache.get(seed)
        if cached:
            return cached
        rng = random.Random(seed)
        resource = rng.choice(
            ["Aether Ore", "Sunsteel", "Crystal", "Runic Wood", "Tide Salt"]
        )
        richness = rng.randint(1, 5)
        self.mmo_resource_cache[seed] = (resource, richness)
        return resource, richness

    def _mmo_infra_items(self) -> list[dict[str, object]]:
        items: list[dict[str, object]] = []
        for outpost in self.mmo_outposts:
            items.append(
                {
                    "kind": "outpost",
                    "region": outpost.get("region", "region"),
                    "data": outpost,
                }
            )
        for route in self.mmo_trade_routes:
            items.append(
                {
                    "kind": "route",
                    "origin": route.get("origin", ""),
                    "destination": route.get("destination", ""),
                    "data": route,
                }
            )
        return items

    def _mmo_patrol_entries(self) -> list[dict[str, object]]:
        entries: list[dict[str, object]] = []
        player_pos = self.world_player_manager.get_position(self.mmo_player_id)
        for agent in self.mmo_auto_agents:
            pos = agent.get("pos") or [0.0, 0.0]
            dx = float(pos[0]) - player_pos[0]
            dy = float(pos[1]) - player_pos[1]
            dist = (dx * dx + dy * dy) ** 0.5
            entries.append(
                {
                    "kind": "agent",
                    "id": agent.get("id"),
                    "distance": dist,
                    "target": agent.get("target"),
                    "assignment": agent.get("assignment"),
                }
            )
        for player_id, pos in self.mmo_remote_positions.items():
            dx = pos[0] - player_pos[0]
            dy = pos[1] - player_pos[1]
            dist = (dx * dx + dy * dy) ** 0.5
            entries.append(
                {
                    "kind": "remote",
                    "id": player_id,
                    "distance": dist,
                }
            )
        return entries

    def _mmo_set_waypoint_for_region(self, region_name: str) -> None:
        region = self._mmo_find_region(region_name)
        if not region:
            self.mmo_message = "Region unavailable."
            return
        self.mmo_waypoint = {
            "name": region.get("name", "region"),
            "position": region.get("position"),
            "biome": region.get("biome", "n/a"),
        }
        self._mmo_log_event(f"Waypoint set: {self.mmo_waypoint['name']}")

    def _mmo_collect_resource(self, resource: str, amount: int) -> None:
        if not resource:
            return
        current = int(self.mmo_stockpile.get(resource, 0))
        self.mmo_stockpile[resource] = current + max(0, int(amount))

    def _mmo_supply_tick(self) -> None:
        focus = self.mmo_strategy.get("focus", "resources")
        for outpost in self.mmo_outposts:
            region = self._mmo_find_region(str(outpost.get("region", "")))
            if not region:
                continue
            resource, richness = self._mmo_region_resources(region)
            level = int(outpost.get("level", 1))
            gain = max(1, richness + level - 1)
            if focus == "resources":
                gain += 1
            self._mmo_collect_resource(resource, gain)

    def _mmo_survey_items(self) -> list[dict[str, object]]:
        items: list[dict[str, object]] = []
        for region in self._mmo_regions():
            resource, richness = self._mmo_region_resources(region)
            items.append(
                {
                    "region": region.get("name", "region"),
                    "resource": resource,
                    "richness": richness,
                }
            )
        return sorted(items, key=lambda item: item["richness"], reverse=True)

    def _mmo_region_influence(self, region: dict[str, object]) -> tuple[str, int]:
        biome = str(region.get("biome", "plains")).lower()
        faction_map = {
            "plains": "Celestial Guard",
            "forest": "Verdant Coalition",
            "desert": "Forge Guild",
            "tundra": "Tide Watch",
        }
        faction = faction_map.get(biome, "Skyward Circuit")
        base = self.reputation_manager.get(faction)
        bonus = int(self._mmo_region_threat(region))
        return faction, base + bonus

    def _mmo_add_shipment(self, resource: str, amount: int) -> None:
        if amount <= 0:
            return
        destination = None
        if self.mmo_waypoint:
            destination = self.mmo_waypoint.get("name")
        if not destination:
            region = self._mmo_nearest_region(
                self.world_player_manager.get_position(self.mmo_player_id)
            )
            destination = region.get("name") if region else "Frontier"
        risk = random.choice(["Low", "Medium", "High"])
        shipment = {
            "resource": resource,
            "amount": amount,
            "destination": destination,
            "eta": random.randint(4, 9),
            "eta_total": 0,
            "status": "in_transit",
            "escorted": False,
            "risk": risk,
        }
        shipment["eta_total"] = int(shipment["eta"])
        self.mmo_shipments.append(shipment)
        self._mmo_log_event(
            f"Shipment dispatched: {amount} {resource} -> {destination}."
        )

    def _mmo_recipes(self) -> list[dict[str, object]]:
        return [
            {
                "name": "Aether Ingot",
                "inputs": {"Aether Ore": 3},
                "outputs": {"Aether Ingot": 1},
                "eta": 3,
            },
            {
                "name": "Sunsteel Plate",
                "inputs": {"Sunsteel": 2, "Crystal": 1},
                "outputs": {"Sunsteel Plate": 1},
                "eta": 4,
            },
            {
                "name": "Runic Core",
                "inputs": {"Runic Wood": 2, "Crystal": 2},
                "outputs": {"Runic Core": 1},
                "eta": 5,
            },
            {
                "name": "Tide Catalyst",
                "inputs": {"Tide Salt": 3, "Aether Ore": 1},
                "outputs": {"Tide Catalyst": 1},
                "eta": 4,
            },
        ]

    def _mmo_can_craft(self, recipe: dict[str, object]) -> bool:
        inputs = recipe.get("inputs", {})
        if not isinstance(inputs, dict):
            return False
        for resource, needed in inputs.items():
            if int(self.mmo_stockpile.get(resource, 0)) < int(needed):
                return False
        return True

    def _mmo_start_craft(self, recipe: dict[str, object]) -> None:
        if not self._mmo_can_craft(recipe):
            self.mmo_message = "Insufficient materials."
            return
        for resource, needed in recipe.get("inputs", {}).items():
            self.mmo_stockpile[resource] = int(self.mmo_stockpile.get(resource, 0)) - int(needed)
        entry = {
            "name": recipe.get("name", "Craft"),
            "outputs": recipe.get("outputs", {}),
            "eta": int(recipe.get("eta", 3)),
            "eta_total": int(recipe.get("eta", 3)),
            "status": "in_progress",
        }
        self.mmo_crafting_queue.append(entry)
        self._mmo_log_event(f"Craft started: {entry['name']}.")

    def _mmo_market_tick(self) -> None:
        for order in list(self.mmo_market_orders):
            if order.get("status") != "open":
                continue
            if "expires_in" not in order:
                order["expires_in"] = int(order.get("eta", 0)) + 5
            order["eta"] = max(0, int(order.get("eta", 0)) - 1)
            order["expires_in"] = max(0, int(order.get("expires_in", 0)) - 1)
            if order["expires_in"] <= 0:
                order["status"] = "expired"
                kind = order.get("kind", "sell")
                qty = int(order.get("quantity", 0))
                price = int(order.get("price", 0))
                resource = order.get("resource", "resource")
                if kind == "sell":
                    self._mmo_collect_resource(resource, qty)
                else:
                    self.mmo_credits += qty * price
                self._mmo_log_event(f"Order expired: {kind} {resource}.")
                self._mmo_record_stat("orders_expired")
                continue
            if order["eta"] <= 0:
                order["status"] = "filled"
                kind = order.get("kind", "sell")
                qty = int(order.get("quantity", 0))
                price = int(order.get("price", 0))
                resource = order.get("resource", "resource")
                if kind == "sell":
                    self.mmo_credits += qty * price
                    self._mmo_log_event(f"Sold {qty} {resource}.")
                else:
                    self._mmo_collect_resource(resource, qty)
                    self._mmo_log_event(f"Bought {qty} {resource}.")
                self._mmo_record_stat("orders_filled")

    def _mmo_cancel_open_order(self) -> None:
        for order in reversed(self.mmo_market_orders):
            if order.get("status") != "open":
                continue
            order["status"] = "cancelled"
            kind = order.get("kind", "sell")
            qty = int(order.get("quantity", 0))
            price = int(order.get("price", 0))
            resource = order.get("resource", "resource")
            if kind == "sell":
                self._mmo_collect_resource(resource, qty)
            else:
                self.mmo_credits += qty * price
            self._mmo_log_event(f"Order cancelled: {kind} {resource}.")
            self._mmo_record_stat("orders_cancelled")
            return
        self.mmo_message = "No open orders to cancel."

    def _mmo_crafting_tick(self) -> None:
        for craft in list(self.mmo_crafting_queue):
            if craft.get("status") != "in_progress":
                continue
            craft["eta"] = max(0, int(craft.get("eta", 0)) - 1)
            if craft["eta"] <= 0:
                craft["status"] = "complete"
                outputs = craft.get("outputs", {})
                if isinstance(outputs, dict):
                    for resource, amount in outputs.items():
                        self._mmo_collect_resource(str(resource), int(amount))
                self._mmo_log_event(f"Craft complete: {craft.get('name', 'Craft')}.")
                self._mmo_record_stat("crafts_completed")

    def _mmo_post_order(self, resource: str, *, kind: str = "sell") -> None:
        price = self.economy_manager.get_price(resource)
        quantity = 5
        if kind == "sell":
            available = int(self.mmo_stockpile.get(resource, 0))
            if available < quantity:
                self.mmo_message = "Insufficient stock for order."
                return
            self.mmo_stockpile[resource] = available - quantity
        else:
            cost = quantity * price
            if self.mmo_credits < cost:
                self.mmo_message = "Insufficient credits."
                return
            self.mmo_credits -= cost
        order = {
            "resource": resource,
            "kind": kind,
            "quantity": quantity,
            "price": price,
            "status": "open",
            "eta": random.randint(3, 7),
            "expires_in": random.randint(6, 12),
        }
        order["expires_total"] = int(order["expires_in"])
        self.mmo_market_orders.append(order)
        self._mmo_log_event(f"Order posted: {kind} {quantity} {resource}.")

    def _mmo_record_stat(self, key: str, amount: int = 1) -> None:
        current = int(self.mmo_stats.get(key, 0))
        self.mmo_stats[key] = current + max(0, int(amount))

    def _mmo_campaigns(self) -> list[dict[str, object]]:
        return [
            {
                "name": "Frontier Relief",
                "stat": "shipments_delivered",
                "target": 5,
                "reward": 50,
            },
            {
                "name": "Stability Initiative",
                "stat": "events_responded",
                "target": 4,
                "reward": 40,
            },
            {
                "name": "Guild Contracts",
                "stat": "contracts_accepted",
                "target": 4,
                "reward": 35,
            },
            {
                "name": "Market Surge",
                "stat": "orders_filled",
                "target": 6,
                "reward": 60,
            },
            {
                "name": "Research Sprint",
                "stat": "crafts_completed",
                "target": 4,
                "reward": 45,
            },
        ]

    def _mmo_update_campaigns(self) -> None:
        for campaign in self._mmo_campaigns():
            name = str(campaign.get("name", "Campaign"))
            if self.mmo_campaign_status.get(name):
                continue
            stat_key = str(campaign.get("stat", ""))
            target = int(campaign.get("target", 0))
            current = int(self.mmo_stats.get(stat_key, 0))
            if target > 0 and current >= target:
                reward = int(campaign.get("reward", 0))
                self.mmo_credits += reward
                self.mmo_campaign_status[name] = True
                self._mmo_log_event(f"Campaign complete: {name} (+{reward}g).")

    def _mmo_timeline_items(self, now: int) -> list[dict[str, object]]:
        items: list[dict[str, object]] = []
        for event in self.mmo_world_events:
            remaining = max(0, int((event.get("expires_at", 0) - now) / 1000))
            items.append(
                {
                    "type": "Event",
                    "name": event.get("name", "Event"),
                    "region": event.get("region", "region"),
                    "remaining": remaining,
                }
            )
        for contract in self.mmo_contracts:
            items.append(
                {
                    "type": "Contract",
                    "name": contract.get("name", "Contract"),
                    "region": contract.get("region", "region"),
                    "remaining": int(contract.get("eta", 0)),
                    "status": contract.get("status", "active"),
                }
            )
        for op in self.mmo_operations:
            items.append(
                {
                    "type": "Operation",
                    "name": op.get("name", "Operation"),
                    "region": op.get("region", "region"),
                    "remaining": int(op.get("eta", 0)),
                    "status": op.get("status", "active"),
                }
            )
        return sorted(items, key=lambda item: (item.get("remaining", 0), item["type"]))

    def _mmo_region_events(self, region_name: str) -> list[dict[str, object]]:
        return [
            event
            for event in self.mmo_world_events
            if str(event.get("region", "")).lower() == region_name.lower()
        ]

    def _mmo_region_contracts(self, region_name: str) -> list[dict[str, object]]:
        return [
            contract
            for contract in self.mmo_contracts
            if str(contract.get("region", "")).lower() == region_name.lower()
        ]

    def _mmo_seed_economy(self) -> None:
        """Seed a lightweight MMO market board."""
        rng = random.Random(self.mmo_ai_seed)
        items = [
            "Aether Ore",
            "Crystal Shards",
            "Sunsteel Ingot",
            "Tide Pearls",
            "Forest Resin",
            "Sky Relic",
        ]
        self.mmo_market_items = list(items)
        for item in items:
            base = rng.randint(35, 160)
            variance = rng.randint(-12, 18)
            self.economy_manager.set_price(item, max(12, base + variance))

    def _mmo_queue_match(self, size: int | None = None) -> None:
        if self.network_manager is None:
            self.mmo_message = "Network offline."
            return
        size = int(size or self.mmo_match_queue_size)
        self.network_manager.send_match_join(
            size=size,
            shard=self.mmo_shard_id,
        )
        self.mmo_match_status = "queued"
        self.mmo_message = f"Queued for match ({size}v{size})."

    def _mmo_leave_match(self) -> None:
        if self.network_manager is None:
            self.mmo_message = "Network offline."
            return
        self.network_manager.send_match_leave(
            size=self.mmo_match_queue_size,
            shard=self.mmo_shard_id,
        )
        self.mmo_match_status = "idle"
        self.mmo_message = "Left matchmaking."

    def _mmo_accept_match(self) -> None:
        if self.network_manager is None:
            self.mmo_message = "Network offline."
            return
        if not self.mmo_match_id:
            self.mmo_message = "No match to accept."
            return
        self.network_manager.send_match_accept(
            self.mmo_match_id,
            shard=self.mmo_shard_id,
        )
        self.mmo_match_status = "accepted"
        self.mmo_message = "Match accepted."

    def _mmo_decline_match(self) -> None:
        if self.network_manager is None:
            self.mmo_message = "Network offline."
            return
        if not self.mmo_match_id:
            self.mmo_message = "No match to decline."
            return
        self.network_manager.send_match_decline(
            self.mmo_match_id,
            shard=self.mmo_shard_id,
        )
        self.mmo_match_status = "idle"
        self.mmo_match_group = None
        self.mmo_match_id = None
        self.mmo_message = "Match declined."

    def _mmo_launch_match(self) -> None:
        if self.mmo_match_status != "ready":
            self.mmo_message = "Match is not ready."
            return
        self.mmo_match_status = "launching"
        self.mmo_message = "Match launch queued."

    def _select_mmo_shard(self) -> None:
        if self.mmo_shard_mode != "auto" or self.mmo_shard_selected:
            return
        shard = self._mmo_choose_shard()
        self.mmo_shard_id = shard
        self.mmo_shard_selected = True
        self.mmo_message = f"Shard selected: {self.mmo_shard_id}."

    def _announce_mmo_shard(self, now: int) -> None:
        if self.network_manager is None:
            return
        if now - self.mmo_last_shard_announce < self.mmo_shard_announce_interval:
            return
        self.mmo_last_shard_announce = now
        load = max(1, len(self.mmo_remote_positions) + 1)
        payload = {
            "type": "mmo_shard_announce",
            "shard": self.mmo_shard_id,
            "load": load,
        }
        self.network_manager.send_reliable(payload, importance=1)

    def _mmo_choose_shard(self) -> str:
        shards = [f"shard-{idx + 1}" for idx in range(self.mmo_shard_count)]
        if self.mmo_shard_stats:
            candidates = [
                (shard, self.mmo_shard_stats.get(shard, 10 ** 9))
                for shard in shards
            ]
            candidates.sort(key=lambda item: (item[1], item[0]))
            return candidates[0][0] if candidates else "public"
        import hashlib

        seed = str(self.account_id or self.mmo_player_id)
        digest = hashlib.sha256(seed.encode()).hexdigest()
        idx = int(digest[:8], 16) % max(1, self.mmo_shard_count)
        return shards[idx] if shards else "public"

    def _mmo_cache_world_state(self) -> None:
        shard = str(self.mmo_shard_id)
        if not shard:
            return
        now = self._mmo_time_ms()
        state = dict(self.mmo_world_state.state)
        self.mmo_world_state_cache[shard] = {
            "state": state,
            "seq": self.mmo_world_state.current_sequence(),
            "tombstones": list(self.mmo_world_tombstones),
            "cached_at": now,
        }

    def _mmo_restore_world_state(self, shard: str) -> bool:
        entry = self.mmo_world_state_cache.get(str(shard))
        if not isinstance(entry, dict):
            return False
        snapshot = entry.get("state")
        if not isinstance(snapshot, dict):
            return False
        ttl = int(getattr(self, "mmo_shard_cache_ttl_ms", 0) or 0)
        cached_at = entry.get("cached_at")
        if ttl > 0 and isinstance(cached_at, int):
            age = self._mmo_time_ms() - cached_at
            if age > ttl:
                return False
        self.mmo_world_state = MMOWorldStateManager(verifier=self.mmo_verifier)
        seq = entry.get("seq")
        state = self.mmo_world_state.load_snapshot(
            snapshot,
            sequence=int(seq) if isinstance(seq, int) else None,
        )
        tombstones = entry.get("tombstones")
        self.mmo_world_tombstones = (
            [dict(item) for item in tombstones if isinstance(item, dict)]
            if isinstance(tombstones, list)
            else []
        )
        self._apply_mmo_world_state(state)
        return True

    def _mmo_prune_shard_cache(self) -> None:
        ttl = int(getattr(self, "mmo_shard_cache_ttl_ms", 0) or 0)
        if ttl <= 0:
            return
        now = self._mmo_time_ms()
        expired = [
            shard
            for shard, entry in self.mmo_world_state_cache.items()
            if isinstance(entry, dict)
            and isinstance(entry.get("cached_at"), int)
            and now - int(entry["cached_at"]) > ttl
        ]
        for shard in expired:
            self.mmo_world_state_cache.pop(shard, None)

    def _mmo_clear_world_state(self) -> None:
        self.world_generation_manager.region_manager.set_regions([])
        self.mmo_influence = {}
        self.mmo_world_events = []
        self.mmo_outposts = []
        self.mmo_operations = []
        self.mmo_trade_routes = []
        self.mmo_directives = []
        self.mmo_bounties = []
        self.mmo_world_tombstones = []

    def _mmo_switch_shard(self, target: str, *, reason: str) -> None:
        if target == self.mmo_shard_id:
            self.mmo_message = "Already on that shard."
            return
        self._mmo_cache_world_state()
        self._mmo_leave_match()
        self._mmo_network_leave()
        self.mmo_shard_id = target
        self.mmo_shard_selected = True
        self.mmo_presence.positions.clear()
        self.mmo_presence.last_seen.clear()
        self.mmo_remote_states.clear()
        restored = self._mmo_restore_world_state(target)
        if not restored:
            self.mmo_world_state = MMOWorldStateManager(verifier=self.mmo_verifier)
            self._mmo_clear_world_state()
        self.mmo_match_group = None
        self.mmo_match_status = "idle"
        self.mmo_match_id = None
        self._mmo_network_join()
        self._request_mmo_snapshot()
        self._request_mmo_world_snapshot()
        self.mmo_message = f"{reason} {self.mmo_shard_id}."

    def _mmo_migrate_shard(self) -> None:
        if self.mmo_shard_mode != "auto":
            self.mmo_message = "Shard is fixed."
            return
        target = self._mmo_choose_shard()
        if target == self.mmo_shard_id:
            self.mmo_message = "Already on best shard."
            return
        self._mmo_switch_shard(target, reason="Migrated to")

    def _mmo_cycle_shard_choice(self) -> None:
        if self.mmo_shard_mode != "auto":
            self.mmo_message = "Shard is fixed."
            return
        shards = [f"shard-{idx + 1}" for idx in range(self.mmo_shard_count)]
        if not shards:
            self.mmo_message = "No shards available."
            return
        self.mmo_shard_choice_index = (
            self.mmo_shard_choice_index + 1
        ) % len(shards)
        self.mmo_message = f"Selected shard: {shards[self.mmo_shard_choice_index]}."

    def _mmo_confirm_shard_choice(self) -> None:
        if self.mmo_shard_mode != "auto":
            self.mmo_message = "Shard is fixed."
            return
        shards = [f"shard-{idx + 1}" for idx in range(self.mmo_shard_count)]
        if not shards:
            self.mmo_message = "No shards available."
            return
        target = shards[self.mmo_shard_choice_index % len(shards)]
        if target == self.mmo_shard_id:
            self.mmo_message = "Already on that shard."
            return
        self._mmo_switch_shard(target, reason="Switched to")

    def _mmo_auto_migrate_shard(self, now: int) -> None:
        if self.mmo_shard_mode != "auto":
            return
        if not self.mmo_shard_stats:
            return
        if now - self.mmo_last_shard_migration < self.mmo_shard_migrate_cooldown_ms:
            return
        current_load = self.mmo_shard_stats.get(self.mmo_shard_id)
        if current_load is None:
            return
        best_shard, best_load = min(
            self.mmo_shard_stats.items(),
            key=lambda item: (item[1], item[0]),
        )
        if current_load - best_load < self.mmo_shard_migrate_threshold:
            return
        self.mmo_last_shard_migration = now
        if best_shard != self.mmo_shard_id:
            self._mmo_migrate_shard()

    def _mmo_update_matchmaking(self, now: int) -> None:
        if self.mmo_match_status != "found":
            return
        if self.mmo_match_found_at is None:
            return
        deadline = self.mmo_match_found_at + self.mmo_match_timeout_ms
        if now >= deadline:
            self._mmo_decline_match()

    def _mmo_seed_operations(self) -> None:
        """Seed MMO operations when none exist."""
        if self.mmo_operations:
            return
        regions = self._mmo_regions()
        region_map = {
            str(region.get("name", "Frontier")): region for region in regions
        }
        names = [r.get("name", "Frontier") for r in regions[:3]]
        if not names:
            names = ["Frontier", "Outer Rim", "Unknown Reach"]
        now = pygame.time.get_ticks()
        for idx, name in enumerate(names, start=1):
            region = region_map.get(str(name), {})
            threat = float(self._mmo_region_threat(region)) if region else 0.0
            if threat >= 7.0:
                priority = "High"
                risk = "High"
            elif threat >= 4.0:
                priority = "Medium"
                risk = "Medium"
            else:
                priority = "Low"
                risk = "Low"
            entry = {
                "name": f"Operation {idx}",
                "region": name,
                "status": "scouting",
                "priority": priority,
                "risk": risk,
                "eta": random.randint(3, 9),
            }
            self._mmo_touch_entry(
                entry,
                now,
                prefix="operation",
                key_fields=("name", "region"),
            )
            self.mmo_operations.append(entry)

    def _mmo_append_operation(self) -> None:
        regions = self._mmo_regions()
        if not regions:
            return
        idx = len(self.mmo_operations) + 1
        region = random.choice(regions)
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
        entry = {
            "name": f"Operation {idx}",
            "region": region.get("name", "Frontier"),
            "status": "scouting",
            "priority": priority,
            "risk": risk,
            "eta": random.randint(3, 9),
        }
        self._mmo_touch_entry(
            entry,
            pygame.time.get_ticks(),
            prefix="operation",
            key_fields=("name", "region"),
        )
        self.mmo_operations.append(entry)

    def _mmo_seed_guilds(self) -> None:
        """Sync guild reputation into the reputation manager."""
        if not self.mmo_guilds:
            return
        for guild in self.mmo_guilds:
            name = str(guild.get("name", "Guild"))
            influence = int(guild.get("influence", 0))
            if name not in self.reputation_manager.rep:
                self.reputation_manager.modify(name, influence)

    def _mmo_seed_contracts(self) -> None:
        """Seed baseline contracts for MMO operations."""
        if self.mmo_contracts:
            return
        regions = self._mmo_regions()
        rng = random.Random(self.mmo_ai_seed + 9)
        for idx, region in enumerate(regions[:3], start=1):
            name = str(region.get("name", "Frontier"))
            threat = float(self._mmo_region_threat(region))
            if threat >= 7.0:
                difficulty = "Hard"
            elif threat >= 4.0:
                difficulty = "Medium"
            else:
                difficulty = "Easy"
            self.mmo_contracts.append(
                {
                    "name": f"Contract {idx}",
                    "region": name,
                    "objective": rng.choice(
                        ["Secure Relic", "Clear Hazard", "Escort Caravan"]
                    ),
                    "difficulty": difficulty,
                    "reward": rng.randint(20, 60),
                    "eta": rng.randint(2, 6),
                    "status": "active",
                }
            )

    def _mmo_append_contract(self) -> None:
        regions = self._mmo_regions()
        if not regions:
            return
        rng = random.Random(self.mmo_ai_seed + len(self.mmo_contracts) * 11)
        region = rng.choice(regions)
        idx = len(self.mmo_contracts) + 1
        threat = float(self._mmo_region_threat(region))
        if threat >= 7.0:
            difficulty = "Hard"
        elif threat >= 4.0:
            difficulty = "Medium"
        else:
            difficulty = "Easy"
        self.mmo_contracts.append(
            {
                "name": f"Contract {idx}",
                "region": region.get("name", "Frontier"),
                "objective": rng.choice(
                    ["Secure Relic", "Clear Hazard", "Escort Caravan"]
                ),
                "difficulty": difficulty,
                "reward": rng.randint(25, 70),
                "eta": rng.randint(2, 6),
                "status": "active",
            }
        )

    def _mmo_seed_events(self) -> None:
        """Ensure the world event list is populated."""
        if len(self.mmo_world_events) >= 3:
            return
        for _ in range(3 - len(self.mmo_world_events)):
            self._mmo_spawn_world_event()

    def _mmo_spawn_world_event(self) -> None:
        regions = self._mmo_regions()
        if not regions:
            return
        rng = random.Random(
            self.mmo_ai_seed + len(self.mmo_world_events) * 11
        )
        region = rng.choice(regions)
        name = str(region.get("name", "Frontier"))
        now = pygame.time.get_ticks()
        event = {
            "name": rng.choice(
                ["Storm Surge", "Rift Bloom", "Raid Warning", "Supply Drop"]
            ),
            "region": name,
            "severity": rng.choice(["Low", "Medium", "High"]),
            "expires_at": now + rng.randint(12000, 24000),
        }
        self._mmo_touch_entry(
            event,
            now,
            prefix="event",
            key_fields=("name", "region", "expires_at"),
        )
        self.mmo_world_events.append(event)
        self._mmo_log_event(f"World event: {event['name']} at {name}.")

        severity = str(event.get("severity", "low")).lower()
        if severity in {"high", "medium"}:
            level = "warn" if severity == "medium" else "error"
            self._mmo_add_alert(
                f"{event['name']} near {name} ({severity.title()}).",
                level=level,
            )

    def _mmo_roster_entries(self) -> list[dict[str, object]]:
        entries: list[dict[str, object]] = []
        player_pos = self.world_player_manager.get_position(self.mmo_player_id)
        entries.append(
            {
                "name": self.mmo_player_id,
                "role": "Commander",
                "status": "active",
                "pos": list(player_pos),
            }
        )
        for name, pos in self.mmo_remote_positions.items():
            entries.append(
                {
                    "name": name,
                    "role": "Remote",
                    "status": "online",
                    "pos": list(pos),
                }
            )
        assigned = {
            member
            for expedition in self.mmo_expeditions
            for member in expedition.get("team", [])
            if expedition.get("status") not in {"complete", "idle"}
        }
        for agent in self.mmo_auto_agents:
            name = str(agent.get("id", "agent"))
            status = "expedition" if name in assigned else "patrolling"
            entries.append(
                {
                    "name": name,
                    "role": "Agent",
                    "status": status,
                    "pos": list(agent.get("pos") or [0.0, 0.0]),
                }
            )
        return entries

    def _mmo_seed_expeditions(self) -> None:
        if self.mmo_expeditions:
            return
        regions = self._mmo_regions()
        if not regions:
            return
        roster = self._mmo_roster_entries()
        candidates = [
            entry["name"]
            for entry in roster
            if entry.get("role") in {"Agent", "Remote"}
        ]
        if not candidates:
            candidates = [self.mmo_player_id]
        rng = random.Random(self.mmo_ai_seed + 31)
        for idx, region in enumerate(regions[:3], start=1):
            team_size = min(2, len(candidates))
            team = rng.sample(candidates, k=team_size)
            resource, richness = self._mmo_region_resources(region)
            self.mmo_expeditions.append(
                {
                    "name": f"Expedition {idx}",
                    "region": region.get("name", "Frontier"),
                    "status": "en_route",
                    "eta": rng.randint(2, 6),
                    "eta_total": 0,
                    "team": team,
                    "reward": rng.randint(25, 70) + richness * 5,
                    "resource": resource,
                    "richness": richness,
                    "risk": rng.choice(["Low", "Medium", "High"]),
                }
            )
            self.mmo_expeditions[-1]["eta_total"] = int(
                self.mmo_expeditions[-1]["eta"]
            )

    def _mmo_redeploy_expedition(
        self, expedition: dict[str, object], now: int
    ) -> None:
        regions = self._mmo_regions()
        if not regions:
            self.mmo_message = "No regions available for expeditions."
            return
        rng = random.Random(self.mmo_ai_seed + int(now / 1000))
        region = rng.choice(regions)
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
            f"{expedition.get('name', 'Expedition')} redeployed to "
            f"{expedition.get('region', 'region')}."
        )

    def _mmo_update_expeditions(self, now: int) -> None:
        if not self.mmo_expeditions:
            return
        rng = random.Random(self.mmo_ai_seed + int(now / 1000))
        for expedition in self.mmo_expeditions:
            status = str(expedition.get("status", "idle"))
            if status in {"complete", "idle"}:
                continue
            expedition["eta"] = max(0, int(expedition.get("eta", 0)) - 1)
            if expedition["eta"] > 0:
                continue
            region_name = str(expedition.get("region", "Frontier"))
            region = self._mmo_find_region(region_name) or {}
            if status == "en_route":
                expedition["status"] = "exploring"
                expedition["eta"] = rng.randint(2, 5)
                expedition["eta_total"] = int(expedition["eta"])
                self._mmo_log_event(
                    f"{expedition.get('name', 'Expedition')} reached "
                    f"{region_name}."
                )
            elif status == "exploring":
                expedition["status"] = "returning"
                expedition["eta"] = rng.randint(2, 4)
                expedition["eta_total"] = int(expedition["eta"])
                resource, richness = self._mmo_region_resources(region)
                expedition["resource"] = resource
                expedition["richness"] = richness
                self._mmo_log_event(
                    f"{expedition.get('name', 'Expedition')} secured {resource}."
                )
            elif status == "returning":
                expedition["status"] = "complete"
                reward = int(expedition.get("reward", 0))
                resource = str(expedition.get("resource", "Supplies"))
                richness = int(expedition.get("richness", 1))
                self.mmo_credits += max(0, reward)
                self._mmo_collect_resource(resource, max(1, richness))
                self._mmo_log_event(
                    f"{expedition.get('name', 'Expedition')} returned with "
                    f"{resource} +{reward}g."
                )
                self._mmo_flash_notice(
                    f"{expedition.get('name', 'Expedition')} complete.",
                    color=(180, 230, 200),
                )

    def _mmo_add_alert(self, message: str, *, level: str = "warn") -> None:
        if not message:
            return
        now = pygame.time.get_ticks()
        if now - self.mmo_last_alert_time < 1500:
            return
        self.mmo_last_alert_time = now
        duration = 16000 if level == "warn" else 24000
        if level == "info":
            duration = 12000
        self.mmo_alerts.append(
            {
                "text": message,
                "level": level,
                "time": now,
                "expires_at": now + duration,
            }
        )
        if len(self.mmo_alerts) > 12:
            self.mmo_alerts = self.mmo_alerts[-12:]

    def _mmo_flash_notice(
        self,
        message: str,
        *,
        color: tuple[int, int, int] = (220, 240, 255),
        duration: int = 3500,
    ) -> None:
        if not message:
            return
        now = pygame.time.get_ticks()
        self.mmo_flash_messages.append(
            {
                "text": message,
                "color": color,
                "expires_at": now + max(800, duration),
            }
        )
        if len(self.mmo_flash_messages) > 6:
            self.mmo_flash_messages = self.mmo_flash_messages[-6:]

    def _mmo_prune_alerts(self, now: int) -> None:
        if not self.mmo_alerts:
            return
        self.mmo_alerts = [
            alert
            for alert in self.mmo_alerts
            if alert.get("expires_at", 0) > now
        ]

    def _mmo_idle_agents(self) -> list[str]:
        assigned = {
            directive.get("assignee")
            for directive in self.mmo_directives
            if directive.get("status") == "active"
        }
        for expedition in self.mmo_expeditions:
            status = expedition.get("status")
            if status in {"complete", "idle"}:
                continue
            for member in expedition.get("team", []):
                assigned.add(member)
        idle: list[str] = []
        for agent in self.mmo_auto_agents:
            name = str(agent.get("id", "agent"))
            if name not in assigned:
                idle.append(name)
        return idle

    def _mmo_seed_directives(self) -> None:
        if self.mmo_directives:
            return
        regions = self._mmo_regions()
        if not regions:
            return
        rng = random.Random(self.mmo_ai_seed + 53)
        kinds = ["Recon", "Patrol", "Escort", "Recovery"]
        for _ in range(min(5, len(regions))):
            region = rng.choice(regions)
            resource, richness = self._mmo_region_resources(region)
            directive = {
                "id": f"D-{self.mmo_directive_sequence:03d}",
                "kind": rng.choice(kinds),
                "region": region.get("name", "Frontier"),
                "status": "open",
                "eta": rng.randint(3, 7),
                "eta_total": 0,
                "assignee": None,
                "reward": rng.randint(20, 80) + richness * 4,
                "resource": resource,
            }
            directive["eta_total"] = int(directive["eta"])
            self._mmo_touch_entry(
                directive,
                pygame.time.get_ticks(),
                prefix="directive",
                key_fields=("id",),
            )
            self.mmo_directive_sequence += 1
            self.mmo_directives.append(directive)

    def _mmo_assign_directive(self, directive: dict[str, object]) -> None:
        if directive.get("status") != "open":
            return
        idle_agents = self._mmo_idle_agents()
        assignee = idle_agents[0] if idle_agents else self.mmo_player_id
        directive["assignee"] = assignee
        directive["status"] = "active"
        directive["eta"] = max(1, int(directive.get("eta", 3)))
        self._mmo_touch_entry(
            directive,
            pygame.time.get_ticks(),
            prefix="directive",
            key_fields=("id",),
        )
        self._mmo_log_event(
            f"{directive.get('id', 'Directive')} assigned to {assignee}."
        )

    def _mmo_update_directives(self, now: int) -> None:
        if not self.mmo_directives:
            return
        for directive in self.mmo_directives:
            if directive.get("status") != "active":
                continue
            directive["eta"] = max(0, int(directive.get("eta", 0)) - 1)
            if directive["eta"] > 0:
                self._mmo_touch_entry(
                    directive,
                    now,
                    prefix="directive",
                    key_fields=("id",),
                )
                continue
            directive["status"] = "complete"
            directive["retire_at"] = now + 6000
            self._mmo_touch_entry(
                directive,
                now,
                prefix="directive",
                key_fields=("id",),
            )
            reward = int(directive.get("reward", 0))
            resource = str(directive.get("resource", "Supplies"))
            self.mmo_credits += max(0, reward)
            self._mmo_collect_resource(resource, 1)
            self._mmo_log_event(
                f"{directive.get('id', 'Directive')} completed (+{reward}g)."
            )
            self._mmo_flash_notice(
                f"{directive.get('id', 'Directive')} completed.",
                color=(200, 220, 255),
            )
            self._mmo_record_stat("directives_completed")
            self._mmo_add_alert(
                f"{directive.get('id', 'Directive')} ready to archive.",
                level="info",
            )
        for directive in list(self.mmo_directives):
            if directive.get("status") != "complete":
                continue
            if now >= int(directive.get("retire_at", 0)):
                self._mmo_record_tombstone("directive", directive, now)
                self.mmo_directives.remove(directive)

    def _mmo_seed_bounties(self) -> None:
        if len(self.mmo_bounties) >= 4:
            return
        regions = self._mmo_regions()
        if not regions:
            return
        rng = random.Random(self.mmo_ai_seed + 67)
        titles = [
            "Void Marauder",
            "Rift Stalker",
            "Storm Reaver",
            "Abyssal Warden",
            "Iron Talon",
        ]
        while len(self.mmo_bounties) < 4:
            region = rng.choice(regions)
            resource, richness = self._mmo_region_resources(region)
            reward = rng.randint(40, 120) + richness * 6
            entry = {
                "id": f"B-{self.mmo_bounty_sequence:03d}",
                "name": rng.choice(titles),
                "region": region.get("name", "Frontier"),
                "status": "open",
                "eta": rng.randint(3, 7),
                "eta_total": 0,
                "assignee": None,
                "reward": reward,
                "resource": resource,
                "threat": rng.choice(["Low", "Medium", "High"]),
            }
            entry["eta_total"] = int(entry["eta"])
            self._mmo_touch_entry(
                entry,
                pygame.time.get_ticks(),
                prefix="bounty",
                key_fields=("id",),
            )
            self.mmo_bounty_sequence += 1
            self.mmo_bounties.append(entry)

    def _mmo_assign_bounty(self, bounty: dict[str, object]) -> None:
        if bounty.get("status") != "open":
            return
        idle_agents = self._mmo_idle_agents()
        assignee = idle_agents[0] if idle_agents else self.mmo_player_id
        bounty["assignee"] = assignee
        bounty["status"] = "active"
        bounty["eta"] = max(1, int(bounty.get("eta", 3)))
        self._mmo_touch_entry(
            bounty,
            pygame.time.get_ticks(),
            prefix="bounty",
            key_fields=("id",),
        )
        self._mmo_log_event(
            f"{bounty.get('id', 'Bounty')} assigned to {assignee}."
        )

    def _mmo_update_bounties(self, now: int) -> None:
        if not self.mmo_bounties:
            return
        for bounty in self.mmo_bounties:
            if bounty.get("status") != "active":
                continue
            bounty["eta"] = max(0, int(bounty.get("eta", 0)) - 1)
            if bounty["eta"] > 0:
                self._mmo_touch_entry(
                    bounty,
                    now,
                    prefix="bounty",
                    key_fields=("id",),
                )
                continue
            bounty["status"] = "complete"
            bounty["retire_at"] = now + 6000
            self._mmo_touch_entry(
                bounty,
                now,
                prefix="bounty",
                key_fields=("id",),
            )
            reward = int(bounty.get("reward", 0))
            resource = str(bounty.get("resource", "Supplies"))
            self.mmo_credits += max(0, reward)
            self._mmo_collect_resource(resource, 1)
            self._mmo_log_event(
                f"{bounty.get('name', 'Bounty')} neutralized (+{reward}g)."
            )
            self._mmo_flash_notice(
                f"{bounty.get('name', 'Bounty')} resolved.",
                color=(240, 190, 190),
            )
            self._mmo_record_stat("bounties_completed")
            self._mmo_add_alert(
                f"{bounty.get('id', 'Bounty')} ready to archive.",
                level="info",
            )
        for bounty in list(self.mmo_bounties):
            if bounty.get("status") != "complete":
                continue
            if now >= int(bounty.get("retire_at", 0)):
                self._mmo_record_tombstone("bounty", bounty, now)
                self.mmo_bounties.remove(bounty)

    def _mmo_project_catalog(self) -> list[dict[str, object]]:
        return [
            {
                "name": "Outpost Upgrade",
                "kind": "outpost_upgrade",
                "credits": 60,
                "resources": {"Aether Ore": 3, "Sunsteel": 2},
                "eta": 4,
            },
            {
                "name": "Influence Boost",
                "kind": "influence_boost",
                "credits": 45,
                "resources": {"Runic Wood": 2, "Crystal": 2},
                "eta": 3,
            },
            {
                "name": "Market Expansion",
                "kind": "market_boost",
                "credits": 70,
                "resources": {"Tide Salt": 3, "Aether Ore": 2},
                "eta": 5,
            },
        ]

    def _mmo_training_catalog(self) -> list[dict[str, object]]:
        return [
            {
                "name": "Tactics Drill",
                "kind": "tactics",
                "credits": 35,
                "eta": 3,
            },
            {
                "name": "Recon Course",
                "kind": "recon",
                "credits": 30,
                "eta": 2,
            },
            {
                "name": "Logistics Clinic",
                "kind": "logistics",
                "credits": 25,
                "eta": 2,
            },
        ]

    def _mmo_seed_projects(self) -> None:
        if len(self.mmo_projects) >= 4:
            return
        regions = self._mmo_regions()
        if not regions:
            return
        rng = random.Random(self.mmo_ai_seed + 73)
        catalog = self._mmo_project_catalog()
        while len(self.mmo_projects) < 4:
            region = rng.choice(regions)
            template = rng.choice(catalog)
            entry = {
                "id": f"P-{self.mmo_project_sequence:03d}",
                "name": template["name"],
                "kind": template["kind"],
                "region": region.get("name", "Frontier"),
                "status": "open",
                "eta": template["eta"],
                "eta_total": template["eta"],
                "credits": template["credits"],
                "resources": dict(template["resources"]),
            }
            self.mmo_project_sequence += 1
            self.mmo_projects.append(entry)

    def _mmo_append_project(self) -> None:
        regions = self._mmo_regions()
        if not regions:
            return
        catalog = self._mmo_project_catalog()
        if not catalog:
            return
        rng = random.Random(self.mmo_ai_seed + self.mmo_project_sequence * 3)
        region = rng.choice(regions)
        template = rng.choice(catalog)
        entry = {
            "id": f"P-{self.mmo_project_sequence:03d}",
            "name": template["name"],
            "kind": template["kind"],
            "region": region.get("name", "Frontier"),
            "status": "open",
            "eta": template["eta"],
            "eta_total": template["eta"],
            "credits": template["credits"],
            "resources": dict(template["resources"]),
        }
        self.mmo_project_sequence += 1
        self.mmo_projects.append(entry)

    def _mmo_seed_training(self) -> None:
        if len(self.mmo_training_queue) >= 3:
            return
        rng = random.Random(self.mmo_ai_seed + 79)
        catalog = self._mmo_training_catalog()
        while len(self.mmo_training_queue) < 3:
            template = rng.choice(catalog)
            entry = {
                "id": f"T-{self.mmo_training_sequence:03d}",
                "name": template["name"],
                "kind": template["kind"],
                "status": "open",
                "eta": template["eta"],
                "eta_total": template["eta"],
                "credits": template["credits"],
            }
            self.mmo_training_sequence += 1
            self.mmo_training_queue.append(entry)

    def _mmo_append_training(self) -> None:
        catalog = self._mmo_training_catalog()
        if not catalog:
            return
        rng = random.Random(self.mmo_ai_seed + self.mmo_training_sequence * 5)
        template = rng.choice(catalog)
        entry = {
            "id": f"T-{self.mmo_training_sequence:03d}",
            "name": template["name"],
            "kind": template["kind"],
            "status": "open",
            "eta": template["eta"],
            "eta_total": template["eta"],
            "credits": template["credits"],
        }
        self.mmo_training_sequence += 1
        self.mmo_training_queue.append(entry)

    def _mmo_start_training(self, training: dict[str, object]) -> None:
        if training.get("status") != "open":
            return
        credits = int(training.get("credits", 0))
        if self.mmo_credits < credits:
            self.mmo_message = "Insufficient credits."
            return
        self.mmo_credits -= credits
        training["status"] = "active"
        training["eta"] = max(1, int(training.get("eta", 1)))
        training["eta_total"] = int(training.get("eta_total", training["eta"]))
        self._mmo_log_event(
            f"{training.get('name', 'Training')} started."
        )
        self._mmo_record_stat("training_started")

    def _mmo_apply_training_reward(self, training: dict[str, object]) -> None:
        kind = training.get("kind")
        if kind == "tactics":
            self.mmo_ai_level = min(10, self.mmo_ai_level + 1)
        elif kind == "recon":
            self.mmo_ai_radius = min(0.15, self.mmo_ai_radius + 0.01)
        elif kind == "logistics":
            resources = [
                "Aether Ore",
                "Sunsteel",
                "Crystal",
                "Runic Wood",
                "Tide Salt",
            ]
            resource = random.choice(resources)
            self._mmo_collect_resource(resource, 3)
        self._mmo_record_stat("training_completed")

    def _mmo_update_training(self, now: int) -> None:
        if not self.mmo_training_queue:
            return
        for training in self.mmo_training_queue:
            if training.get("status") != "active":
                continue
            training["eta"] = max(0, int(training.get("eta", 0)) - 1)
            if training["eta"] > 0:
                continue
            training["status"] = "complete"
            self._mmo_apply_training_reward(training)
            self._mmo_flash_notice(
                f"{training.get('name', 'Training')} complete.",
                color=(170, 210, 240),
            )
            self._mmo_add_alert(
                f"{training.get('id', 'Training')} ready to archive.",
                level="info",
            )

    def _mmo_can_start_project(self, project: dict[str, object]) -> bool:
        credits = int(project.get("credits", 0))
        if self.mmo_credits < credits:
            return False
        resources = project.get("resources", {})
        if not isinstance(resources, dict):
            return False
        for resource, needed in resources.items():
            if int(self.mmo_stockpile.get(resource, 0)) < int(needed):
                return False
        return True

    def _mmo_start_project(self, project: dict[str, object]) -> None:
        if project.get("status") != "open":
            return
        if not self._mmo_can_start_project(project):
            self.mmo_message = "Insufficient materials."
            return
        credits = int(project.get("credits", 0))
        self.mmo_credits -= credits
        for resource, needed in project.get("resources", {}).items():
            self.mmo_stockpile[resource] = int(
                self.mmo_stockpile.get(resource, 0)
            ) - int(needed)
        project["status"] = "active"
        project["eta"] = max(1, int(project.get("eta", 1)))
        project["eta_total"] = int(project.get("eta_total", project["eta"]))
        self._mmo_log_event(
            f"{project.get('name', 'Project')} started in {project.get('region')}."
        )
        self._mmo_record_stat("projects_started")

    def _mmo_apply_project_reward(self, project: dict[str, object]) -> None:
        region_name = str(project.get("region", "Frontier"))
        kind = project.get("kind")
        if kind == "outpost_upgrade":
            outpost = next(
                (
                    entry
                    for entry in self.mmo_outposts
                    if entry.get("region") == region_name
                ),
                None,
            )
            if outpost:
                level = int(outpost.get("level", 1))
                outpost["level"] = min(5, level + 1)
                self._mmo_touch_entry(
                    outpost,
                    pygame.time.get_ticks(),
                    prefix="outpost",
                    key_fields=("region",),
                )
                self.mmo_backend.upsert_outpost(outpost)
            else:
                self._mmo_build_outpost(
                    self._mmo_find_region(region_name) or {}
                )
        elif kind == "influence_boost":
            self._mmo_adjust_influence(region_name, 8)
        elif kind == "market_boost":
            self.mmo_credits += 20
        self._mmo_record_stat("projects_completed")

    def _mmo_update_projects(self, now: int) -> None:
        if not self.mmo_projects:
            return
        for project in self.mmo_projects:
            if project.get("status") != "active":
                continue
            project["eta"] = max(0, int(project.get("eta", 0)) - 1)
            if project["eta"] > 0:
                continue
            project["status"] = "complete"
            self._mmo_apply_project_reward(project)
            self._mmo_log_event(
                f"{project.get('name', 'Project')} completed."
            )
            self._mmo_flash_notice(
                f"{project.get('name', 'Project')} complete.",
                color=(180, 220, 190),
            )
            self._mmo_add_alert(
                f"{project.get('id', 'Project')} ready to archive.",
                level="info",
            )

    def _mmo_adjust_influence(self, region_name: str, delta: int) -> None:
        if not region_name or delta == 0:
            return
        current = int(self.mmo_influence.get(region_name, 0))
        target = max(0, min(100, current + int(delta)))
        self.mmo_influence[region_name] = target

    def _mmo_influence_value(self, region: dict[str, object]) -> int:
        name = str(region.get("name", ""))
        current = int(self.mmo_influence.get(name, 0))
        if current <= 0:
            faction, base = self._mmo_region_influence(region)
            current = max(10, min(90, int(base)))
            self.mmo_influence[name] = current
        return current

    def _mmo_influence_entries(self) -> list[dict[str, object]]:
        regions = self._mmo_regions()
        return sorted(
            regions,
            key=lambda region: self._mmo_influence_value(region),
            reverse=True,
        )

    def _mmo_update_influence(self, now: int) -> None:
        regions = self._mmo_regions()
        if not regions:
            return
        for region in regions:
            name = str(region.get("name", ""))
            faction, base = self._mmo_region_influence(region)
            baseline = max(10, min(90, int(base)))
            current = int(self.mmo_influence.get(name, baseline))
            if current < baseline:
                current = min(baseline, current + 1)
            elif current > baseline:
                current = max(baseline, current - 1)
            if now % 5000 < 100 and faction:
                current = max(0, current - 1)
            self.mmo_influence[name] = current

    def _mmo_toggle_shipment_escort(self, shipment: dict[str, object]) -> None:
        status = shipment.get("status")
        if status != "in_transit":
            self.mmo_message = "Shipment already resolved."
            return
        if shipment.get("escorted"):
            self.mmo_message = "Escort already assigned."
            return
        cost = 15
        if self.mmo_credits < cost:
            self.mmo_message = "Insufficient credits."
            return
        self.mmo_credits -= cost
        shipment["escorted"] = True
        shipment["eta"] = max(1, int(shipment.get("eta", 1)) - 1)
        destination = shipment.get("destination", "Frontier")
        self._mmo_log_event(f"Escort assigned to {destination}.")
        self._mmo_record_stat("shipments_escorted")

