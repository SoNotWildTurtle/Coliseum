"""Deterministic, replayable arena episode runner for regression checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import subprocess
import sys
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _git_commit() -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        return None
    commit = out.strip()
    return commit or None


def _parse_resolution(value: str) -> tuple[int, int]:
    left, right = value.lower().split("x", 1)
    width = int(left)
    height = int(right)
    if width < 320 or height < 240:
        raise ValueError(f"resolution too small: {width}x{height}")
    return width, height


def _configure_headless(headless: bool) -> None:
    if not headless:
        return
    os.environ["PYGAME_HEADLESS"] = "1"
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")


def seed_everything(seed: int) -> dict[str, Any]:
    """Seed known randomness sources for deterministic episode playback."""

    random.seed(seed)
    report: dict[str, Any] = {
        "seed": int(seed),
        "python_random_seeded": True,
        "numpy_seeded": False,
        "global_random_instances_reseeded": 0,
    }
    try:
        import numpy as np  # type: ignore

        np.random.seed(seed)
        report["numpy_seeded"] = True
    except Exception:
        report["numpy_seeded"] = False

    reseeded = 0
    for module in list(sys.modules.values()):
        module_dict = getattr(module, "__dict__", None)
        if not isinstance(module_dict, dict):
            continue
        for value in module_dict.values():
            if isinstance(value, random.Random):
                value.seed(seed)
                reseeded += 1
    report["global_random_instances_reseeded"] = reseeded
    return report


@dataclass
class EpisodeConfig:
    seed: int
    frames: int
    seconds: float | None
    scenario: str
    headless: bool
    fixed_dt: float | None
    output_dir: Path
    trace: bool
    trace_level: str
    verbose: bool
    width: int
    height: int
    autoplay: bool
    strict: bool


def _scenario_setup(game: Any, scenario: str) -> dict[str, Any]:
    game.selected_mode = "Arcade"
    if getattr(game, "characters", None):
        index = 0 if scenario != "stress" else min(1, len(game.characters) - 1)
        game.selected_character = game.characters[index]
    if getattr(game, "maps", None):
        if scenario == "stress":
            game.selected_map = game.maps[min(1, len(game.maps) - 1)]
        elif scenario == "economy":
            game.selected_map = game.maps[-1]
        else:
            game.selected_map = game.maps[0]
    if scenario == "stress":
        game.ai_players = max(2, int(getattr(game, "ai_players", 1)))
        game.match_mobs = True
    if scenario == "economy":
        game.match_mobs = True
    return {
        "selected_character": getattr(game, "selected_character", ""),
        "selected_map": getattr(game, "selected_map", ""),
        "ai_players": int(getattr(game, "ai_players", 1)),
        "match_mobs": bool(getattr(game, "match_mobs", False)),
    }


def _allowed_trace_type(event_type: str, level: str) -> bool:
    minimal = {
        "damage",
        "hazard_damage",
        "heal",
        "status_tick",
        "achievement_unlocked",
        "currency_delta",
        "xp_delta",
        "objective_progress",
    }
    if level == "verbose":
        return True
    if level == "normal":
        return event_type in minimal or event_type.endswith("_delta")
    return event_type in minimal


def _canonical_signature_payload(
    *,
    seed: int,
    scenario: str,
    frames: int,
    outcomes: dict[str, Any],
) -> dict[str, Any]:
    return {
        "seed": int(seed),
        "scenario": str(scenario),
        "frames": int(frames),
        "outcomes": outcomes,
    }


def _sha256(data: dict[str, Any]) -> str:
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _check_invariants(
    *,
    frames_requested: int,
    frames_executed: int,
    outcomes: dict[str, Any],
) -> tuple[dict[str, dict[str, str]], bool]:
    invariants: dict[str, dict[str, str]] = {}
    has_fail = False

    def add(name: str, condition: bool, detail: str, fail: bool = False) -> None:
        nonlocal has_fail
        status = "pass" if condition else ("fail" if fail else "warn")
        invariants[name] = {"status": status, "detail": detail}
        if status == "fail":
            has_fail = True

    add(
        "frame_count_matches_request",
        frames_requested == frames_executed,
        f"requested={frames_requested} executed={frames_executed}",
        fail=True,
    )
    add(
        "kills_non_negative",
        int(outcomes.get("kills", 0)) >= 0,
        f"kills={outcomes.get('kills', 0)}",
    )
    add(
        "deaths_non_negative",
        int(outcomes.get("deaths", 0)) >= 0,
        f"deaths={outcomes.get('deaths', 0)}",
    )
    add(
        "damage_dealt_finite",
        math.isfinite(float(outcomes.get("damage_dealt", 0.0))),
        f"damage_dealt={outcomes.get('damage_dealt', 0.0)}",
    )
    add(
        "damage_taken_finite",
        math.isfinite(float(outcomes.get("damage_taken", 0.0))),
        f"damage_taken={outcomes.get('damage_taken', 0.0)}",
    )
    add(
        "currency_non_negative",
        int(outcomes.get("coins_gained", 0)) >= 0,
        f"coins_gained={outcomes.get('coins_gained', 0)}",
    )
    add(
        "xp_non_negative",
        int(outcomes.get("xp_gained", 0)) >= 0,
        f"xp_gained={outcomes.get('xp_gained', 0)}",
    )
    return invariants, has_fail


def run_episode(config: EpisodeConfig) -> tuple[int, dict[str, Any]]:
    _configure_headless(config.headless)
    if config.autoplay:
        os.environ["HOLO_AUTOPLAY"] = "1"
    elif "HOLO_AUTOPLAY" in os.environ:
        del os.environ["HOLO_AUTOPLAY"]

    import pygame
    from hololive_coliseum.game import Game

    config.output_dir.mkdir(parents=True, exist_ok=True)
    determinism_report = seed_everything(config.seed)

    frame_counter = {"value": 0}
    fixed_dt = config.fixed_dt if config.fixed_dt is not None else (1.0 / 60.0)
    fixed_ms = fixed_dt * 1000.0
    current_ms = {"value": 0.0}
    capture_frames = {"active": False}
    game_holder: dict[str, Any] = {"game": None}

    original_get_ticks = pygame.time.get_ticks
    original_flip = pygame.display.flip

    def fake_get_ticks() -> int:
        return int(current_ms["value"])

    def wrapped_flip() -> None:
        if not capture_frames["active"]:
            original_flip()
            return
        frame_counter["value"] += 1
        current_ms["value"] = frame_counter["value"] * fixed_ms
        if frame_counter["value"] >= config.frames:
            game_ref = game_holder.get("game")
            if game_ref is not None:
                game_ref.running = False
        original_flip()

    pygame.time.get_ticks = fake_get_ticks
    pygame.display.flip = wrapped_flip

    run_start = _utc_now()
    trace_path = config.output_dir / "episode_trace.jsonl"
    trace_handle = None
    game = None
    events_by_type: dict[str, int] = {}
    achievements: list[str] = []
    objective_events = 0
    outcomes: dict[str, Any] = {
        "kills": 0,
        "deaths": 0,
        "damage_dealt": 0.0,
        "damage_taken": 0.0,
        "healing_total": 0.0,
        "coins_gained": 0,
        "xp_gained": 0,
        "achievements_unlocked": [],
        "objective_events": 0,
    }
    scenario_info: dict[str, Any] = {}
    error_trace = None

    try:
        if config.trace:
            trace_handle = trace_path.open("w", encoding="utf-8")
        game = Game(width=config.width, height=config.height)
        game_holder["game"] = game
        scenario_info = _scenario_setup(game, config.scenario)
        game._setup_level()
        game._set_state("playing")
        game.level_start_time = 0
        frame_counter["value"] = 0
        current_ms["value"] = 0.0
        capture_frames["active"] = True
        player_id = game.player.__class__.__name__

        def on_event(event: dict[str, Any]) -> None:
            event_type = str(event.get("type", "unknown"))
            payload = event.get("payload", {})
            if not isinstance(payload, dict):
                payload = {}
            events_by_type[event_type] = events_by_type.get(event_type, 0) + 1

            if event_type in {"damage", "hazard_damage", "status_tick"}:
                amount = float(payload.get("amount", 0.0) or 0.0)
                attacker_id = str(payload.get("attacker_id", ""))
                target_id = str(payload.get("target_id", ""))
                if attacker_id == player_id:
                    outcomes["damage_dealt"] += amount
                if target_id == player_id:
                    outcomes["damage_taken"] += amount
            elif event_type == "heal":
                amount = float(payload.get("amount", 0.0) or 0.0)
                outcomes["healing_total"] += amount
            elif event_type == "currency_delta":
                delta = int(payload.get("delta", 0) or 0)
                if delta > 0:
                    outcomes["coins_gained"] += delta
            elif event_type == "xp_delta":
                delta = int(payload.get("delta", 0) or 0)
                if delta > 0:
                    outcomes["xp_gained"] += delta
            elif event_type == "achievement_unlocked":
                achievement_id = str(payload.get("id", ""))
                if achievement_id:
                    achievements.append(achievement_id)
            elif event_type == "objective_progress":
                nonlocal objective_events
                objective_events += 1

            if trace_handle is not None and _allowed_trace_type(event_type, config.trace_level):
                trace_handle.write(
                    json.dumps(
                        {
                            "frame": int(event.get("frame", frame_counter["value"])),
                            "t": int(event.get("t", fake_get_ticks())),
                            "event_type": event_type,
                            "payload": payload,
                        },
                        sort_keys=True,
                    )
                    + "\n"
                )

        game.event_bus.subscribe("*", on_event)
        game.run()

        outcomes["kills"] = int(getattr(game, "kills", 0))
        lives = int(getattr(game, "match_lives", 0))
        player_lives = int(getattr(game.player, "lives", 0))
        outcomes["deaths"] = max(0, lives - player_lives)
        outcomes["achievements_unlocked"] = sorted(set(achievements))
        outcomes["objective_events"] = int(objective_events)
    except Exception:
        error_trace = traceback.format_exc()
    finally:
        if trace_handle is not None:
            trace_handle.close()
        pygame.time.get_ticks = original_get_ticks
        pygame.display.flip = original_flip
        try:
            pygame.quit()
        except Exception:
            pass

    invariants, has_fail = _check_invariants(
        frames_requested=config.frames,
        frames_executed=frame_counter["value"],
        outcomes=outcomes,
    )

    signature_inputs = {
        "seed": config.seed,
        "scenario": config.scenario,
        "frames": config.frames,
        "outcome_fields": [
            "kills",
            "deaths",
            "damage_dealt",
            "damage_taken",
            "healing_total",
            "coins_gained",
            "xp_gained",
            "achievements_unlocked",
            "objective_events",
        ],
    }
    signature_payload = _canonical_signature_payload(
        seed=config.seed,
        scenario=config.scenario,
        frames=config.frames,
        outcomes=outcomes,
    )
    episode_signature = _sha256(signature_payload)

    report = {
        "timestamp_utc": run_start,
        "seed": int(config.seed),
        "scenario": config.scenario,
        "frames_requested": int(config.frames),
        "frames_executed": int(frame_counter["value"]),
        "seconds_requested": config.seconds,
        "fixed_dt": float(fixed_dt),
        "resolution": {"width": config.width, "height": config.height},
        "python_version": sys.version.split()[0],
        "pygame_version": pygame.version.ver,
        "git_commit": _git_commit(),
        "determinism": {
            **determinism_report,
            "fixed_ticks_patched": True,
            "fixed_display_flip_guard": True,
        },
        "scenario_info": scenario_info,
        "outcomes": outcomes,
        "event_counts": events_by_type,
        "invariants": invariants,
        "signature_version": 1,
        "signature_inputs": signature_inputs,
        "episode_signature": episode_signature,
        "error": error_trace,
    }
    (config.output_dir / "episode_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    if not config.trace and trace_path.exists():
        trace_path.unlink()

    if error_trace:
        return 1, report
    if has_fail and config.strict:
        return 2, report
    return 0, report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run deterministic arena episode replay.")
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--frames", type=int, default=None)
    parser.add_argument("--seconds", type=float, default=10.0)
    parser.add_argument("--res", default="1280x720")
    parser.add_argument("--scenario", choices=["basic", "stress", "economy"], default="basic")
    parser.add_argument("--headless", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--fixed-dt", type=float, default=1.0 / 60.0)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--trace", action="store_true")
    parser.add_argument(
        "--trace-level",
        choices=["minimal", "normal", "verbose"],
        default="minimal",
    )
    parser.add_argument("--autoplay", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    width, height = _parse_resolution(args.res)
    frames = int(args.frames) if args.frames is not None else max(
        1,
        int(float(args.seconds) / float(args.fixed_dt)),
    )
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_dir = Path("SavedGames") / "episodes" / f"run_{stamp}"
    config = EpisodeConfig(
        seed=int(args.seed),
        frames=int(frames),
        seconds=float(args.seconds),
        scenario=str(args.scenario),
        headless=bool(args.headless) or (os.environ.get("PYGAME_HEADLESS") == "1"),
        fixed_dt=float(args.fixed_dt),
        output_dir=output_dir,
        trace=bool(args.trace),
        trace_level=str(args.trace_level),
        verbose=bool(args.verbose),
        width=width,
        height=height,
        autoplay=bool(args.autoplay),
        strict=bool(args.strict),
    )
    code, report = run_episode(config)
    if config.verbose:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif code != 0:
        print(f"episode_runner failed with code={code}")
        if report.get("error"):
            print(report["error"])
    return code


if __name__ == "__main__":
    raise SystemExit(main())
