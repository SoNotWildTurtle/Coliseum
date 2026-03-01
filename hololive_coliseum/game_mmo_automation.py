"""MMO hub automation helpers extracted from the main game class."""

from __future__ import annotations

import math
import random

import pygame

from .shared_state_manager import SharedStateManager


class GameMMOAutomation:
    """Automation helper mixin for MMO hub flow and pipeline."""

    def _autoplay_mmo(self, now: int) -> None:
        """Drive the MMO hub automatically when autoplay is enabled."""
        if not self.autoplay:
            return
        if self.state == "mmo":
            self._autoplay_mmo_overlays(now)
        drift_x = math.cos(now / 1200) * self.mmo_speed * 0.6
        drift_y = math.sin(now / 1400) * self.mmo_speed * 0.6
        drift_scale = 1.0 + (self.mmo_ai_level - 1) * 0.04
        self.world_player_manager.move_player(
            self.mmo_player_id,
            drift_x * drift_scale,
            drift_y * drift_scale,
        )
        if now % 2400 < 50:
            self._mmo_generate_plan(now)
        if now % 1800 < 50:
            self._mmo_spawn_region()
        if now % 1200 < 50:
            self._mmo_sync_region()

    def _autoplay_mmo_overlays(self, now: int) -> None:
        """Cycle MMO overlay screens and toggles during autoplay."""
        if self.autoplay_mmo_state != "mmo":
            self.autoplay_mmo_state = "mmo"
            self.autoplay_mmo_overlay_index = 0
            self.autoplay_mmo_overlay_seen.clear()
            self.autoplay_mmo_last_step = now
            self.autoplay_mmo_toggle_index = 0
            self.autoplay_mmo_layer_index = 0
            if not self.mmo_seen_tour:
                self.mmo_show_tour = True
                self.mmo_tour_step = 0
        if now - self.autoplay_mmo_last_step < self.autoplay_menu_delay:
            return
        self.autoplay_mmo_last_step = now
        if not self.mmo_overlays:
            return
        overlay = self.mmo_overlays[
            self.autoplay_mmo_overlay_index % len(self.mmo_overlays)
        ]
        self.autoplay_mmo_overlay_index += 1
        self.autoplay_mmo_overlay_seen.add(overlay)
        self._clear_mmo_toggles()
        self.mmo_overlay_mode = overlay
        toggle_note, layer_note, help_note = self._autoplay_mmo_cycle_aux(overlay)
        notes = [f"overlay={overlay}"]
        for note in (toggle_note, layer_note, help_note):
            if note:
                notes.append(note)
        self._autoplay_trace("MMO " + " ".join(notes), now=now)
        if self.mmo_show_tour:
            self.mmo_tour_step += 1
            if self.mmo_tour_step >= 5:
                self.mmo_show_tour = False
                self.mmo_seen_tour = True
        target = len(self.mmo_overlays)
        if self.autoplay_menu_quick:
            target = max(1, min(self.autoplay_mmo_overlay_limit, target))
        if len(self.autoplay_mmo_overlay_seen) >= target:
            self.autoplay_menu_resume_state = "main_menu"
            self.autoplay_menu_resume_time = now + self.autoplay_menu_delay

    def _autoplay_mmo_cycle_aux(self, overlay: str) -> tuple[str | None, ...]:
        """Toggle MMO UI panels, layers, and help pages."""
        toggle_note = None
        layer_note = None
        help_note = None
        toggles = [
            "mmo_ui_show_panel",
            "mmo_show_minimap",
            "mmo_show_event_log",
        ]
        if toggles:
            attr = toggles[self.autoplay_mmo_toggle_index % len(toggles)]
            setattr(self, attr, not getattr(self, attr))
            self.autoplay_mmo_toggle_index += 1
            toggle_note = f"{attr}={getattr(self, attr)}"
        if overlay == "help":
            pages = len(self._mmo_help_pages())
            if pages:
                self.mmo_help_page = (self.mmo_help_page + 1) % pages
                help_note = f"help_page={self.mmo_help_page + 1}/{pages}"
        if self.mmo_layers:
            layer_keys = list(self.mmo_layers.keys())
            key = layer_keys[self.autoplay_mmo_layer_index % len(layer_keys)]
            self.mmo_layers[key] = not self.mmo_layers.get(key, True)
            self.autoplay_mmo_layer_index += 1
            layer_note = f"layer_{key}={self.mmo_layers[key]}"
        return toggle_note, layer_note, help_note

    def _autoplay_generation(self, now: int) -> None:
        """Generate MMO regions and extend playtime during autoplay."""
        if not self.autoplay:
            return
        if self.autoplay_mmo_fast:
            return
        if self.autoplay_generation_interval <= 0:
            return
        if now < self.autoplay_next_generation:
            return
        self.autoplay_next_generation = now + self.autoplay_generation_interval
        seed = f"{random.getrandbits(128):032x}"
        self.world_generation_manager.seed_manager.add_seed(seed)
        region = self.world_generation_manager.generate_region_from_seed(
            seed,
            self.mmo_player_id,
        )
        self.mmo_backend.upsert_regions([region])
        extension = max(0, self.autoplay_level_extension)
        extension = int(round(extension * (1.0 + self.mmo_ai_level * 0.05)))
        self.level_limit += extension

    def _mmo_generate_plan(self, now: int) -> None:
        """Build and persist an auto-dev plan for the MMO."""
        if now - self.mmo_last_plan < self.mmo_plan_cooldown:
            self.mmo_message = "Auto-dev plan cooling down..."
            return
        self.mmo_last_plan = now
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
        self_evolution = plan.get("self_evolution_blueprint", {})
        if isinstance(self_evolution, dict):
            adaptive = self_evolution.get("adaptive_tuning")
            if isinstance(adaptive, dict):
                self.auto_dev_tuning.apply_adaptive_tuning(adaptive)
        boss_plan = plan.get("boss_plan", {})
        boss_name = str(boss_plan.get("name", "Unknown"))
        threat = float(boss_plan.get("threat", 0.0) or 0.0)
        security_score = float(plan.get("network_security_score", 0.0))
        summary = {
            "focus": focus.get("trending_hazard", "general"),
            "boss": boss_name,
            "threat": round(threat, 2),
            "network_security_score": round(security_score, 2),
        }
        self.mmo_backend.record_plan(summary, plan)
        self.world_generation_manager.set_pipeline_bias(plan)
        self.mmo_plan_summary = (
            f"Plan: {summary['boss']} | Focus {summary['focus']}"
        )
        self.mmo_message = "Auto-dev plan refreshed."

    def _mmo_extend_pipeline(self, now: int, *, source: str) -> str:
        """Add MMO content to keep the post-arena loop active."""
        if now - self.mmo_last_pipeline_boost < self.mmo_pipeline_boost_cooldown:
            return "MMO pipeline cooling down."
        self.mmo_last_pipeline_boost = now
        self._ensure_mmo_world()
        before_ops = len(self.mmo_operations)
        before_contracts = len(self.mmo_contracts)
        before_projects = len(self.mmo_projects)
        before_training = len(self.mmo_training_queue)
        before_events = len(self.mmo_world_events)
        self._mmo_seed_operations()
        self._mmo_seed_contracts()
        self._mmo_seed_events()
        self._mmo_seed_expeditions()
        self._mmo_seed_projects()
        self._mmo_seed_training()
        self._mmo_seed_directives()
        self._mmo_seed_bounties()
        self._mmo_spawn_world_event()
        self._mmo_append_operation()
        self._mmo_append_contract()
        self._mmo_append_project()
        self._mmo_append_training()
        added = (
            (len(self.mmo_operations) - before_ops)
            + (len(self.mmo_contracts) - before_contracts)
            + (len(self.mmo_projects) - before_projects)
            + (len(self.mmo_training_queue) - before_training)
            + (len(self.mmo_world_events) - before_events)
        )
        if added <= 0:
            return "MMO pipeline already saturated."
        self.mmo_message = "MMO pipeline expanded."
        self._mmo_log_event(f"{source} pipeline expanded (+{added} tasks).")
        return f"{source}: +{added} new MMO tasks queued."

    def _mmo_award_arena_grant(self) -> str:
        """Convert arena results into MMO supplies after a victory."""
        score = int(getattr(self.score_manager, "score", 0))
        grant = max(50, min(200, 50 + score // 120))
        self.mmo_credits += grant
        resource = "Aether Ore"
        self._mmo_collect_resource(resource, 2)
        self._mmo_log_event(f"Arena grant: +{grant} credits, +2 {resource}.")
        return f"Arena grant issued (+{grant} credits, +2 {resource})."

    def _build_post_victory_report(self, now: int) -> None:
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
        self.post_victory_focus = focus
        self.post_victory_plan = plan
        boss_plan = plan.get("boss_plan", {})
        boss_name = str(boss_plan.get("name", "Unknown"))
        threat = float(boss_plan.get("threat", 0.0) or 0.0)
        security_score = float(plan.get("network_security_score", 0.0))
        summary = {
            "focus": focus.get("trending_hazard", "general"),
            "boss": boss_name,
            "threat": round(threat, 2),
            "network_security_score": round(security_score, 2),
        }
        self.mmo_backend.record_plan(summary, plan)
        self.world_generation_manager.set_pipeline_bias(plan)
        self.mmo_plan_summary = f"Plan: {summary['boss']} | Focus {summary['focus']}"

    def _mmo_remote_state(self, player_id: str) -> SharedStateManager:
        manager = self.mmo_remote_states.get(player_id)
        if manager is None:
            manager = SharedStateManager(
                tolerances={"pos_x": 0.02, "pos_y": 0.02},
                verifier=self.mmo_verifier,
            )
            self.mmo_remote_states[player_id] = manager
        return manager

    def _broadcast_mmo_state(self, delta: dict[str, object]) -> None:
        """Share MMO hub state updates with connected peers."""
        if self.network_manager is None:
            return
        packet = {
            "type": "mmo_state",
            "player_id": self.mmo_player_id,
            "shard": self.mmo_shard_id,
            "delta": dict(delta),
        }
        self.network_manager.send_reliable(packet, importance=2)

    def _mmo_sync_state(self, now: int, *, force: bool = False) -> None:
        """Persist MMO hub state snapshots at a controlled cadence."""
        if not force and now - self.mmo_last_state_sync < self.mmo_state_interval:
            return
        self.mmo_last_state_sync = now
        pos = self.world_player_manager.get_position(self.mmo_player_id)
        region = self._mmo_nearest_region(pos)
        payload = {
            "pos_x": round(pos[0], 3),
            "pos_y": round(pos[1], 3),
            "region": region.get("name") if region else None,
            "biome": region.get("biome") if region else None,
        }
        delta = self.mmo_shared_state.update(**payload)
        changed = any(k not in {"seq", "type", "verify"} for k in delta)
        if force or changed:
            seq = int(delta.get("seq", self.mmo_shared_state.current_sequence()))
            verify = delta.get("verify") or self.mmo_verifier.compute(
                self.mmo_shared_state.state
            )
            self.mmo_backend.record_snapshot(seq, self.mmo_shared_state.state, verify)
            self.mmo_backend.upsert_player(self.mmo_player_id, pos)
            self.mmo_backend.prune_snapshots(keep=200)
            self._broadcast_mmo_state(delta)

    def _mmo_region_summary(self, region: dict[str, object]) -> dict[str, object]:
        """Return a compact region summary for MMO world sync."""
        return {
            "name": region.get("name"),
            "seed": region.get("seed"),
            "biome": region.get("biome"),
            "position": region.get("position"),
            "radius": region.get("radius"),
            "recommended_level": region.get("recommended_level"),
            "feature": region.get("feature"),
            "quest": region.get("quest"),
            "updated_at": int(pygame.time.get_ticks()),
            "origin": self.mmo_player_id,
        }

    def _mmo_world_snapshot(self, now: int) -> dict[str, object]:
        regions = [
            self._mmo_region_summary(region)
            for region in self.world_generation_manager.region_manager.get_regions()
        ]
        for event in self.mmo_world_events:
            if isinstance(event, dict) and "updated_at" not in event:
                self._mmo_touch_entry(
                    event,
                    now,
                    prefix="event",
                    key_fields=("name", "region", "expires_at"),
                )
        for outpost in self.mmo_outposts:
            if isinstance(outpost, dict) and "updated_at" not in outpost:
                self._mmo_touch_entry(
                    outpost,
                    now,
                    prefix="outpost",
                    key_fields=("region",),
                )
        for op in self.mmo_operations:
            if isinstance(op, dict) and "updated_at" not in op:
                self._mmo_touch_entry(
                    op,
                    now,
                    prefix="operation",
                    key_fields=("name", "region"),
                )
        for route in self.mmo_trade_routes:
            if isinstance(route, dict) and "updated_at" not in route:
                self._mmo_touch_entry(
                    route,
                    now,
                    prefix="route",
                    key_fields=("origin", "destination"),
                )
        return self.mmo_world_state.build_snapshot(
            regions=regions,
            influence=self.mmo_influence,
            world_events=self.mmo_world_events,
            outposts=self.mmo_outposts,
            operations=self.mmo_operations,
            trade_routes=self.mmo_trade_routes,
            directives=self.mmo_directives,
            bounties=self.mmo_bounties,
            tombstones=self.mmo_world_tombstones,
            updated_at=now,
            shard=self.mmo_shard_id,
        )

    def _broadcast_mmo_world_delta(self, delta: dict[str, object]) -> None:
        if self.network_manager is None:
            return
        payload = {
            "type": "mmo_world_delta",
            "shard": self.mmo_shard_id,
            "delta": dict(delta),
        }
        self.network_manager.send_reliable(payload, importance=2)

    def _mmo_sync_world_state(self, now: int, *, force: bool = False) -> None:
        self._announce_mmo_shard(now)
        self._mmo_auto_migrate_shard(now)
        self._mmo_prune_shard_cache()
        if (
            not force
            and now - self.mmo_last_world_state_sync
            < self.mmo_world_state_interval
        ):
            return
        self.mmo_last_world_state_sync = now
        snapshot = self._mmo_world_snapshot(now)
        delta = self.mmo_world_state.update(snapshot)
        if force or self.mmo_world_state.has_payload_changes(delta):
            self._broadcast_mmo_world_delta(delta)

    def _apply_mmo_world_state(self, state: dict[str, object]) -> None:
        regions = state.get("regions")
        if isinstance(regions, list):
            self.world_generation_manager.region_manager.set_regions(
                [dict(region) for region in regions if isinstance(region, dict)]
            )
        influence = state.get("influence")
        if isinstance(influence, dict):
            self.mmo_influence = {str(k): int(v) for k, v in influence.items()}
        world_events = state.get("world_events")
        if isinstance(world_events, list):
            self.mmo_world_events = [
                dict(event) for event in world_events if isinstance(event, dict)
            ]
        outposts = state.get("outposts")
        if isinstance(outposts, list):
            self.mmo_outposts = [
                dict(outpost) for outpost in outposts if isinstance(outpost, dict)
            ]
        operations = state.get("operations")
        if isinstance(operations, list):
            self.mmo_operations = [
                dict(op) for op in operations if isinstance(op, dict)
            ]
        trade_routes = state.get("trade_routes")
        if isinstance(trade_routes, list):
            self.mmo_trade_routes = [
                dict(route) for route in trade_routes if isinstance(route, dict)
            ]
        directives = state.get("directives")
        if isinstance(directives, list):
            self.mmo_directives = [
                dict(directive)
                for directive in directives
                if isinstance(directive, dict)
            ]
        bounties = state.get("bounties")
        if isinstance(bounties, list):
            self.mmo_bounties = [
                dict(bounty) for bounty in bounties if isinstance(bounty, dict)
            ]
        tombstones = state.get("tombstones")
        if isinstance(tombstones, list):
            self.mmo_world_tombstones = [
                dict(tombstone)
                for tombstone in tombstones
                if isinstance(tombstone, dict)
            ]

