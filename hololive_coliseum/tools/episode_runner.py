"""Deterministic headless arena episode runner."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import random
import subprocess
import sys
import traceback
from typing import Any


@dataclass(frozen=True)
class EpisodeScenario:
    """Arena setup used for deterministic episode runs."""

    name: str
    character: str
    map_name: str
    difficulty: str
    ai_players: int
    allies: int
    mobs: bool
    mob_interval: int
    mob_wave: int
    mob_max: int
    level_limit: int


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _git_commit() -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return None
    return out or None


def _parse_resolution(text: str) -> tuple[int, int]:
    value = str(text).lower().strip()
    if "x" not in value:
        raise ValueError(f"resolution must look like 1280x720, got {text!r}")
    left, right = value.split("x", 1)
    width = max(320, int(left))
    height = max(240, int(right))
    return width, height


def _scenario_library() -> dict[str, EpisodeScenario]:
    return {
        "basic": EpisodeScenario(
            name="basic",
            character="Gawr Gura",
            map_name="Default",
            difficulty="Normal",
            ai_players=1,
            allies=0,
            mobs=False,
            mob_interval=3500,
            mob_wave=2,
            mob_max=8,
            level_limit=90,
        ),
        "stress": EpisodeScenario(
            name="stress",
            character="Takanashi Kiara",
            map_name="Storm Archive",
            difficulty="Hard",
            ai_players=2,
            allies=1,
            mobs=True,
            mob_interval=1200,
            mob_wave=3,
            mob_max=12,
            level_limit=120,
        ),
        "economy": EpisodeScenario(
            name="economy",
            character="Ceres Fauna",
            map_name="Default",
            difficulty="Normal",
            ai_players=1,
            allies=0,
            mobs=True,
            mob_interval=1000,
            mob_wave=2,
            mob_max=10,
            level_limit=120,
        ),
        "micro": EpisodeScenario(
            name="micro",
            character="Gawr Gura",
            map_name="Default",
            difficulty="Normal",
            ai_players=1,
            allies=0,
            mobs=False,
            mob_interval=3500,
            mob_wave=2,
            mob_max=8,
            level_limit=45,
        ),
    }


def _configure_runtime_env(headless: bool) -> None:
    if headless:
        os.environ.setdefault("PYGAME_HEADLESS", "1")
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
    os.environ.setdefault("HOLO_AUTOPLAY_FLOW", "0")
    os.environ.setdefault("HOLO_AUTOPLAY_MMO_FAST", "1")
    os.environ.setdefault("HOLO_AUTOPLAY_TRACE", "0")
    os.environ.setdefault("HOLO_AUTOPLAY_LOG", "0")
    os.environ.setdefault("HOLO_UI_DEBUG_OVERLAY", "0")
    os.environ.setdefault("HOLO_UI_DEBUG_LOG", "0")


def _reseed_module_rngs(seed: int) -> list[str]:
    module_names = (
        "hololive_coliseum.game",
        "hololive_coliseum.ai_autoplayer",
        "hololive_coliseum.autoplay_controller",
        "hololive_coliseum.weather_forecast_manager",
    )
    reseeded: list[str] = []
    for module_name in module_names:
        module = sys.modules.get(module_name)
        if module is None:
            continue
        for attr_name in dir(module):
            try:
                value = getattr(module, attr_name)
            except Exception:
                continue
            if isinstance(value, random.Random):
                value.seed(seed)
                reseeded.append(f"{module_name}.{attr_name}")
    return reseeded


def seed_everything(seed: int) -> dict[str, Any]:
    """Seed known RNG sources and report applied controls."""

    random.seed(seed)
    numpy_present = False
    numpy_seeded = False
    try:
        import numpy as np  # type: ignore
    except Exception:
        np = None
    if np is not None:
        numpy_present = True
        np.random.seed(seed)
        numpy_seeded = True
    reseeded_rngs = _reseed_module_rngs(seed)
    return {
        "seed": int(seed),
        "numpy_present": bool(numpy_present),
        "numpy_seeded": bool(numpy_seeded),
        "reseeded_rng_instances": reseeded_rngs,
    }


class EpisodeMonitor:
    """Collect deterministic episode metrics and optional event trace."""

    def __init__(
        self,
        game: Any,
        *,
        trace_path: Path | None,
        trace_level: str,
        trace_max_events: int,
        verbose: bool = False,
    ) -> None:
        self.game = game
        self.verbose = verbose
        self.trace_level = str(trace_level)
        self.trace_max_events = max(1, int(trace_max_events))
        self.frame_count = 0
        self.current_frame = 0
        self.current_t_ms = 0
        self.trace_path = trace_path
        self._trace_handle = (
            trace_path.open("w", encoding="utf-8") if trace_path is not None else None
        )
        self.trace_event_count = 0
        self.trace_dropped = 0
        self.trace_counts: dict[str, int] = {}
        self.damage_by_attacker: dict[str, float] = {}
        self.damage_by_target: dict[str, float] = {}
        self.prev_state = str(game.state)
        self.prev_player_health = float(getattr(game.player, "health", 0.0))
        self.prev_enemy_health: dict[int, float] = {
            id(enemy): float(getattr(enemy, "health", 0.0))
            for enemy in list(getattr(game, "enemies", []))
        }
        self.prev_xp = int(getattr(game.player.experience_manager, "xp", 0))
        self.prev_coins = int(game.player.currency_manager.get_balance())
        self.initial_lives = int(getattr(game.player, "lives", 0))
        self.initial_xp = self.prev_xp
        self.initial_level = int(getattr(game.player.experience_manager, "level", 1))
        self.initial_coins = self.prev_coins
        self.initial_kills = int(getattr(game, "kills", 0))
        self.initial_achievements = set(
            getattr(game.achievement_manager, "unlocked", set())
        )
        self.player_event_ids = {
            f"{game.player.__class__.__name__}:{id(game.player)}",
            game.player.__class__.__name__,
        }
        if getattr(game.player, "name", None):
            self.player_event_ids.add(str(getattr(game.player, "name")))
        self.damage_dealt = 0.0
        self.damage_taken = 0.0
        self.healing_total = 0.0
        self.coins_gained = 0
        self.coins_spent = 0
        self.xp_gained = 0
        self.ko_events = 0
        self.player_ko_events = 0
        self.hazard_damage_total = 0.0
        self.status_tick_damage_total = 0.0
        self.combat_hook_available = False
        self.combat_events_seen = 0
        self.hp_events_seen = 0

    def attach_event_sink(self, game: Any) -> bool:
        if game is None or not hasattr(game, "event_sink"):
            return False
        game.event_sink = self.on_game_event
        self.combat_hook_available = True
        return True

    def _should_trace(self, event_type: str) -> bool:
        if self._trace_handle is None:
            return False
        minimal = {
            "damage",
            "hazard_damage",
            "status_tick",
            "heal",
            "ko",
            "reward",
        }
        normal = minimal | {"coins", "xp", "state_transition"}
        if self.trace_level == "minimal":
            return event_type in minimal
        if self.trace_level == "normal":
            return event_type in normal
        return True

    def _trace(self, frame: int, t_ms: int, event_type: str, payload: dict[str, Any]) -> None:
        self.trace_counts[event_type] = int(self.trace_counts.get(event_type, 0)) + 1
        if not self._should_trace(event_type):
            return
        if self.trace_event_count >= self.trace_max_events:
            self.trace_dropped += 1
            return
        row = {
            "frame": int(frame),
            "t": int(t_ms),
            "event_type": event_type,
            "payload": payload,
        }
        self._trace_handle.write(json.dumps(row, sort_keys=True) + "\n")
        self.trace_event_count += 1

    def _is_player_target(self, target_id: str) -> bool:
        prefix = f"{self.game.player.__class__.__name__}:"
        text = str(target_id)
        return text.startswith(prefix) or text in self.player_event_ids

    def on_game_event(self, event: dict[str, Any]) -> None:
        self.combat_events_seen += 1
        event_type = str(event.get("type", "unknown"))
        t_ms = int(event.get("t_ms", self.current_t_ms))
        frame = int(self.current_frame)
        if event_type in {"damage", "hazard_damage", "status_tick", "heal", "ko"}:
            self.hp_events_seen += 1
        if event_type in {"damage", "hazard_damage", "status_tick"}:
            amount = float(event.get("amount", 0.0))
            attacker = str(event.get("attacker_id", "unknown"))
            target = str(event.get("target_id", "unknown"))
            hp_before = float(event.get("hp_before", 0.0))
            hp_after = float(event.get("hp_after", 0.0))
            is_damage = hp_after <= hp_before
            if self._is_player_target(target):
                if is_damage:
                    self.damage_taken += max(0.0, amount)
                else:
                    self.healing_total += max(0.0, amount)
            else:
                if is_damage:
                    self.damage_dealt += max(0.0, amount)
                else:
                    self.healing_total += max(0.0, amount)
            if event_type == "hazard_damage":
                self.hazard_damage_total += max(0.0, amount)
            if event_type == "status_tick" and is_damage:
                self.status_tick_damage_total += max(0.0, amount)
            if not self._is_player_target(target):
                self.damage_by_attacker[attacker] = self.damage_by_attacker.get(
                    attacker, 0.0
                ) + max(0.0, amount)
                self.damage_by_target[target] = self.damage_by_target.get(target, 0.0) + max(
                    0.0, amount
                )
        elif event_type == "heal":
            amount = float(event.get("amount", 0.0))
            self.healing_total += max(0.0, amount)
            target = str(event.get("target_id", "unknown"))
            if not self._is_player_target(target):
                self.damage_by_target[target] = self.damage_by_target.get(target, 0.0)
        if event_type == "ko":
            self.ko_events += 1
            target = str(event.get("target_id", ""))
            if self._is_player_target(target):
                self.player_ko_events += 1
        self._trace(frame, t_ms, event_type, dict(event))

    def _fallback_health_deltas(self, frame: int, t_ms: int) -> None:
        player = self.game.player
        player_health = float(getattr(player, "health", 0.0))
        player_delta = player_health - self.prev_player_health
        if player_delta < 0:
            amount = float(-player_delta)
            self.damage_taken += max(0.0, amount)
            self._trace(frame, t_ms, "damage", {"target_id": "player", "amount": amount})
        elif player_delta > 0:
            amount = float(player_delta)
            self.healing_total += amount
            self._trace(frame, t_ms, "healing", {"target_id": "player", "amount": amount})
        self.prev_player_health = player_health

        enemy_health_now: dict[int, float] = {
            id(enemy): float(getattr(enemy, "health", 0.0))
            for enemy in list(getattr(self.game, "enemies", []))
        }
        for enemy_id, prev_hp in self.prev_enemy_health.items():
            current_hp = enemy_health_now.get(enemy_id)
            if current_hp is None:
                if prev_hp <= 0:
                    self.ko_events += 1
                    self._trace(frame, t_ms, "ko", {"target_id": f"enemy:{enemy_id}"})
                continue
            delta = current_hp - prev_hp
            if delta < 0:
                amount = float(-delta)
                self.damage_dealt += amount
                self._trace(frame, t_ms, "damage", {"target_id": f"enemy:{enemy_id}", "amount": amount})
        self.prev_enemy_health = enemy_health_now

    def on_frame(self, frame: int, t_ms: int) -> None:
        self.frame_count += 1
        self.current_frame = int(frame)
        self.current_t_ms = int(t_ms)
        state = str(getattr(self.game, "state", "unknown"))
        if state != self.prev_state:
            self._trace(frame, t_ms, "state_transition", {"from": self.prev_state, "to": state})
            self.prev_state = state
        if not (self.combat_hook_available and self.hp_events_seen > 0):
            self._fallback_health_deltas(frame, t_ms)
        coins = int(self.game.player.currency_manager.get_balance())
        if coins != self.prev_coins:
            delta = coins - self.prev_coins
            if delta > 0:
                self.coins_gained += int(delta)
                self._trace(frame, t_ms, "reward", {"kind": "coins", "amount": int(delta)})
            else:
                self.coins_spent += int(-delta)
            self._trace(frame, t_ms, "coins", {"delta": int(delta), "value": coins})
            self.prev_coins = coins
        xp = int(getattr(self.game.player.experience_manager, "xp", 0))
        if xp != self.prev_xp:
            delta = xp - self.prev_xp
            if delta > 0:
                self.xp_gained += int(delta)
                self._trace(frame, t_ms, "reward", {"kind": "xp", "amount": int(delta)})
            self._trace(frame, t_ms, "xp", {"delta": int(delta), "value": xp})
            self.prev_xp = xp
        if self.trace_level == "verbose" and frame % 30 == 0:
            self._trace(
                frame,
                t_ms,
                "ai_snapshot",
                {
                    "enemies": len(list(getattr(self.game, "enemies", []))),
                    "projectiles": len(list(getattr(self.game, "projectiles", []))),
                    "combo": int(getattr(self.game.score_manager, "combo", 0)),
                },
            )

    def trace_summary(self) -> dict[str, Any]:
        top_damage_dealers = sorted(
            self.damage_by_attacker.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:5]
        top_targets = sorted(
            self.damage_by_target.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:5]
        return {
            "event_counts": dict(sorted(self.trace_counts.items())),
            "events_written": int(self.trace_event_count),
            "events_dropped": int(self.trace_dropped),
            "total_heal": int(self.healing_total),
            "hazard_damage_total": int(self.hazard_damage_total),
            "status_tick_damage_total": int(self.status_tick_damage_total),
            "top_damage_dealers": [
                {"id": key, "damage": int(value)} for key, value in top_damage_dealers
            ],
            "top_targets": [
                {"id": key, "damage": int(value)} for key, value in top_targets
            ],
            "combat_hook_available": bool(self.combat_hook_available),
            "combat_events_seen": int(self.combat_events_seen),
            "hp_events_seen": int(self.hp_events_seen),
        }

    def close(self) -> None:
        if self._trace_handle is not None:
            self._trace_handle.close()
            self._trace_handle = None


class DeterministicRuntime:
    """Patch pygame timing/event hooks for deterministic fixed-step runs."""

    def __init__(
        self,
        pygame_mod: Any,
        game: Any,
        *,
        frame_limit: int,
        dt_ms: int,
        monitor: EpisodeMonitor,
    ) -> None:
        self.pygame = pygame_mod
        self.game = game
        self.frame_limit = max(1, int(frame_limit))
        self.dt_ms = max(1, int(dt_ms))
        self.monitor = monitor
        self.current_ms = 0
        self.frame_counter = 0
        self._orig_get_ticks = None
        self._orig_event_get = None
        self._orig_flip = None

    def __enter__(self) -> "DeterministicRuntime":
        self._orig_get_ticks = self.pygame.time.get_ticks
        self._orig_event_get = self.pygame.event.get
        self._orig_flip = self.pygame.display.flip

        def _get_ticks() -> int:
            return int(self.current_ms)

        def _event_get(*_args: Any, **_kwargs: Any) -> list[Any]:
            self.frame_counter += 1
            self.current_ms = self.frame_counter * self.dt_ms
            return []

        def _flip(*args: Any, **kwargs: Any) -> Any:
            self.monitor.on_frame(self.frame_counter, self.current_ms)
            result = self._orig_flip(*args, **kwargs)
            if self.frame_counter >= self.frame_limit:
                self.game.running = False
            return result

        self.pygame.time.get_ticks = _get_ticks
        self.pygame.event.get = _event_get
        self.pygame.display.flip = _flip
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self._orig_get_ticks is not None:
            self.pygame.time.get_ticks = self._orig_get_ticks
        if self._orig_event_get is not None:
            self.pygame.event.get = self._orig_event_get
        if self._orig_flip is not None:
            self.pygame.display.flip = self._orig_flip


def _invariant(name: str, passed: bool, detail: str, strict: bool) -> dict[str, Any]:
    if passed:
        status = "pass"
    else:
        status = "fail" if strict else "warn"
    return {"name": name, "status": status, "detail": detail}


def _validate_invariants(
    game: Any,
    now_ms: int,
    monitor: EpisodeMonitor,
    *,
    strict: bool,
    frames_requested: int,
    inject_violation: bool = False,
) -> list[dict[str, Any]]:
    player = game.player
    cooldowns = player.cooldown_status(int(now_ms))
    cooldown_ok = all(float(item.get("remaining_ms", 0.0)) >= -0.05 for item in cooldowns)
    hp_values = [float(getattr(player, "health", 0.0))]
    hp_values.extend(float(getattr(enemy, "health", 0.0)) for enemy in list(getattr(game, "enemies", [])))
    hp_finite = all(not math.isnan(value) and not math.isinf(value) for value in hp_values)
    damage_finite = all(
        not math.isnan(value) and not math.isinf(value)
        for value in [monitor.damage_dealt, monitor.damage_taken, monitor.healing_total]
    )
    currency = float(player.currency_manager.get_balance())
    currency_ok = (not math.isnan(currency)) and (not math.isinf(currency)) and currency >= 0
    inventory_raw = getattr(player.inventory, "items", {})
    inventory_ok = isinstance(inventory_raw, dict) and all(int(count) >= 0 for count in inventory_raw.values())
    xp_ok = int(monitor.xp_gained) >= 0
    frame_ok = int(monitor.frame_count) == int(frames_requested)
    ko_ok = int(monitor.player_ko_events) <= int(max(0, monitor.initial_lives))
    checks = [
        _invariant("entity_hp_finite", hp_finite, "all hp values are finite", strict),
        _invariant("damage_metrics_finite", damage_finite, "damage/healing metrics are finite", strict),
        _invariant("cooldowns_non_negative_tolerance", cooldown_ok, "cooldowns >= -0.05ms", strict),
        _invariant("currency_non_negative_finite", currency_ok, "currency is finite and >= 0", strict),
        _invariant("inventory_non_negative", inventory_ok, "inventory counts are non-negative", strict),
        _invariant("xp_gain_non_negative", xp_ok, "xp gained is non-negative", strict),
        _invariant("frame_count_matches", frame_ok, "frames_run equals frames_requested", strict),
        _invariant("ko_once_per_life", ko_ok, "player KOs do not exceed life count", strict),
    ]
    if inject_violation:
        checks.append(_invariant("injected_violation", False, "forced failure for strict-mode test", strict))
    return checks


def _canonical_signature_payload(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "signature_version": int(report["signature_version"]),
        "scenario": report["scenario"],
        "seed": report["seed"],
        "frames_run": report["frames_run"],
        "outcomes": report["outcomes"],
        "invariant_status": {
            item["name"]: item["status"] for item in report["invariants"]
        },
    }


def _episode_signature(report: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    payload = _canonical_signature_payload(report)
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    signature = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    signature_inputs = {
        "version": "v1",
        "included_fields": sorted(payload.keys()),
        "canonical_json": "sorted_keys,separators(',',':')",
    }
    return signature, signature_inputs


def _setup_scenario(game: Any, scenario: EpisodeScenario, *, now_ms: int) -> None:
    if scenario.difficulty in game.difficulty_levels:
        game.difficulty_index = game.difficulty_levels.index(scenario.difficulty)
    game.ai_players = int(max(0, scenario.ai_players))
    game.match_allies = int(max(0, scenario.allies))
    game.match_mobs = bool(scenario.mobs)
    game.match_mob_interval = int(max(100, scenario.mob_interval))
    game.match_mob_wave = int(max(1, scenario.mob_wave))
    game.match_mob_max = int(max(1, scenario.mob_max))
    game.base_level_limit = int(max(10, scenario.level_limit))
    game.level_limit = game.base_level_limit
    game.selected_mode = "Arena"
    game.selected_chapter = None
    if scenario.character in game.characters:
        game.selected_character = scenario.character
    elif game.characters:
        game.selected_character = game.characters[0]
    if scenario.map_name in game.maps:
        game.selected_map = scenario.map_name
    elif "Default" in game.maps:
        game.selected_map = "Default"
    elif game.maps:
        game.selected_map = game.maps[0]
    game._setup_level()
    game.level_start_time = int(now_ms)
    game._set_state("playing")


def _build_report(
    *,
    seed: int,
    scenario: EpisodeScenario,
    frames_requested: int,
    dt_seconds: float,
    monitor: EpisodeMonitor,
    game: Any,
    now_ms: int,
    invariants: list[dict[str, Any]],
    determinism_controls: dict[str, Any],
    trace_enabled: bool,
) -> dict[str, Any]:
    player = game.player
    achievements_now = set(getattr(game.achievement_manager, "unlocked", set()))
    new_achievements = sorted(achievements_now - monitor.initial_achievements)
    outcomes = {
        "kills": int(getattr(game, "kills", 0)),
        "deaths": max(0, monitor.initial_lives - int(getattr(player, "lives", 0))),
        "total_damage_dealt": int(monitor.damage_dealt),
        "total_damage_taken": int(monitor.damage_taken),
        "total_healing": int(monitor.healing_total),
        "hazard_damage_total": int(monitor.hazard_damage_total),
        "status_tick_damage_total": int(monitor.status_tick_damage_total),
        "coins_start": int(monitor.initial_coins),
        "coins_end": int(player.currency_manager.get_balance()),
        "coins_gained": int(monitor.coins_gained),
        "coins_spent": int(monitor.coins_spent),
        "xp_start": int(monitor.initial_xp),
        "xp_end": int(getattr(player.experience_manager, "xp", 0)),
        "xp_gained": int(monitor.xp_gained),
        "level_start": int(monitor.initial_level),
        "level_end": int(getattr(player.experience_manager, "level", 1)),
        "achievements_unlocked": new_achievements,
        "ko_events": int(monitor.ko_events),
        "final_state": str(getattr(game, "state", "unknown")),
    }
    report: dict[str, Any] = {
        "schema_version": "1.1",
        "timestamp_utc": _utc_now(),
        "seed": int(seed),
        "scenario": scenario.name,
        "frames_requested": int(frames_requested),
        "frames_run": int(monitor.frame_count),
        "seconds_run": round(float(monitor.frame_count) * float(dt_seconds), 6),
        "python_version": sys.version.split()[0],
        "pygame_version": game.pygame.version.ver if hasattr(game, "pygame") else None,
        "git_commit": _git_commit(),
        "outcomes": outcomes,
        "invariants": invariants,
        "determinism_controls": determinism_controls,
        "trace_summary": monitor.trace_summary() if trace_enabled else None,
        "signature_version": 1,
        "signature_inputs": {},
        "episode_signature": "",
        "final_tick_ms": int(now_ms),
    }
    signature, signature_inputs = _episode_signature(report)
    report["signature_inputs"] = signature_inputs
    report["episode_signature"] = signature
    any_fail = any(item["status"] == "fail" for item in invariants)
    any_warn = any(item["status"] == "warn" for item in invariants)
    if any_fail:
        report["status"] = "invariant_failure"
    elif any_warn:
        report["status"] = "ok_with_warnings"
    else:
        report["status"] = "ok"
    return report


def _run_episode(
    *,
    seed: int,
    frames: int,
    width: int,
    height: int,
    scenario: EpisodeScenario,
    output_dir: Path,
    trace: bool,
    trace_level: str,
    trace_max_events: int,
    autoplay: bool,
    fixed_dt: float,
    strict: bool,
    inject_violation: bool,
) -> tuple[int, dict[str, Any]]:
    _configure_runtime_env(headless=True)
    from hololive_coliseum import save_manager

    run_save_root = output_dir / "savedgames"
    run_save_root.mkdir(parents=True, exist_ok=True)
    save_manager.SAVE_DIR = str(run_save_root)
    os.environ["HOLO_PROFILE_ID"] = f"episode_{scenario.name}_{seed}"
    os.environ["HOLO_AUTOPLAY"] = "1" if autoplay else "0"

    import pygame
    from hololive_coliseum.game import Game

    pygame.init()
    if os.environ.get("PYGAME_HEADLESS") == "1":
        pygame.display.init()
        pygame.display.set_mode((max(1, width), max(1, height)))
    game: Any | None = None
    monitor: EpisodeMonitor | None = None
    trace_path = output_dir / "episode_trace.jsonl" if trace else None
    report: dict[str, Any] = {}
    try:
        game = Game(width=width, height=height)
        game.pygame = pygame
        determinism = seed_everything(seed)
        determinism["fixed_ticks_patched"] = True
        determinism["fixed_dt_seconds"] = float(fixed_dt)
        game.width = int(width)
        game.height = int(height)
        game.world_width = int(width)
        game.world_height = int(height)
        game.ground_y = game.height - 50
        game.screen = game._apply_display_mode()
        game.mixer_ready = False
        _setup_scenario(game, scenario, now_ms=0)
        monitor = EpisodeMonitor(
            game,
            trace_path=trace_path,
            trace_level=trace_level,
            trace_max_events=trace_max_events,
        )
        event_hook_enabled = monitor.attach_event_sink(game)
        determinism["combat_hook_enabled"] = bool(event_hook_enabled)
        dt_ms = max(1, int(round(float(fixed_dt) * 1000.0)))
        with DeterministicRuntime(
            pygame,
            game,
            frame_limit=frames,
            dt_ms=dt_ms,
            monitor=monitor,
        ) as runtime:
            game.run()
            now_ms = runtime.current_ms
        determinism["fallback_damage_inference_used"] = not (
            monitor.combat_hook_available and monitor.hp_events_seen > 0
        )
        invariants = _validate_invariants(
            game,
            now_ms,
            monitor,
            strict=strict,
            frames_requested=frames,
            inject_violation=inject_violation,
        )
        report = _build_report(
            seed=seed,
            scenario=scenario,
            frames_requested=frames,
            dt_seconds=float(fixed_dt),
            monitor=monitor,
            game=game,
            now_ms=now_ms,
            invariants=invariants,
            determinism_controls=determinism,
            trace_enabled=trace,
        )
        code = 0 if report["status"] != "invariant_failure" else 2
    except Exception:
        report = {
            "schema_version": "1.1",
            "timestamp_utc": _utc_now(),
            "seed": int(seed),
            "scenario": scenario.name,
            "status": "error",
            "exception": traceback.format_exc(),
        }
        code = 1
    finally:
        if monitor is not None:
            monitor.close()
        try:
            pygame.quit()
        except Exception:
            pass
    return code, report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run deterministic arena episodes.")
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--frames", type=int, default=None)
    parser.add_argument("--seconds", type=float, default=10.0)
    parser.add_argument("--res", default="1280x720")
    parser.add_argument("--headless", action="store_true", default=True)
    parser.add_argument("--no-headless", action="store_true")
    parser.add_argument("--scenario", choices=sorted(_scenario_library().keys()), default="basic")
    parser.add_argument("--autoplay", action="store_true", default=True)
    parser.add_argument("--no-autoplay", action="store_true")
    parser.add_argument("--fixed-dt", type=float, default=1.0 / 60.0)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--trace-level", choices=("minimal", "normal", "verbose"), default="normal")
    parser.add_argument("--trace-max-events", type=int, default=2000)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--inject-test-violation", action="store_true", help=argparse.SUPPRESS)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    scenario = _scenario_library()[args.scenario]
    width, height = _parse_resolution(args.res)
    headless = bool(args.headless) and not bool(args.no_headless)
    if headless:
        os.environ["PYGAME_HEADLESS"] = "1"
    autoplay = bool(args.autoplay) and not bool(args.no_autoplay)
    frames = int(args.frames) if args.frames is not None else max(1, int(round(args.seconds * 60.0)))
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path("SavedGames") / "episodes" / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir.mkdir(parents=True, exist_ok=True)
    code, report = _run_episode(
        seed=int(args.seed),
        frames=frames,
        width=width,
        height=height,
        scenario=scenario,
        output_dir=output_dir,
        trace=bool(args.trace),
        trace_level=str(args.trace_level),
        trace_max_events=int(args.trace_max_events),
        autoplay=autoplay,
        fixed_dt=float(args.fixed_dt),
        strict=bool(args.strict),
        inject_violation=bool(args.inject_test_violation),
    )
    report_path = output_dir / "episode_report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    if args.verbose:
        print(f"[episode-runner] report: {report_path}")
        if report.get("episode_signature"):
            print(f"[episode-runner] signature: {report['episode_signature']}")
        if report.get("status") == "error":
            lines = str(report.get("exception", "")).splitlines()
            if lines:
                print(f"[episode-runner] error: {lines[-1]}")
    return int(code)


if __name__ == "__main__":
    raise SystemExit(main())
