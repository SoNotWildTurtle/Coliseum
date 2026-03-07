"""Deterministic balance sweep harness for multi-seed episode aggregation."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import random
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from hololive_coliseum.game import Game


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def _parse_seed_values(seed: int | None, count: int, seeds_expr: str | None) -> list[int]:
    if seeds_expr:
        values: list[int] = []
        for chunk in seeds_expr.split(","):
            part = chunk.strip()
            if not part:
                continue
            if "-" in part:
                left, right = part.split("-", 1)
                start = int(left)
                end = int(right)
                step = 1 if end >= start else -1
                values.extend(range(start, end + step, step))
            else:
                values.append(int(part))
        return values
    base = 1337 if seed is None else int(seed)
    total = max(1, int(count))
    return [base + offset for offset in range(total)]


def _prepare_headless_env() -> None:
    os.environ.setdefault("PYGAME_HEADLESS", "1")
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    os.environ.setdefault("HOLO_TELEMETRY", "0")


def _sha256(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass
class EpisodeOutcome:
    seed: int
    scenario: str
    signature: str
    frames: int
    damage_dealt: float
    damage_taken: float
    kills: int
    deaths: int
    coins_gained: int
    xp_gained: int


def _run_episode(seed: int, scenario: str, frames: int, width: int, height: int) -> EpisodeOutcome:
    import pygame

    random.seed(seed)
    frame_state = {"frame": 0}
    dt_ms = 1000 / 60.0
    now_ms = {"value": 0.0}
    source_class = {"player": ""}
    metrics = {
        "damage_dealt": 0.0,
        "damage_taken": 0.0,
        "coins_gained": 0,
        "xp_gained": 0,
    }

    orig_get_ticks = pygame.time.get_ticks
    orig_flip = pygame.display.flip

    def fake_ticks() -> int:
        return int(now_ms["value"])

    def capped_flip() -> None:
        frame_state["frame"] += 1
        now_ms["value"] = frame_state["frame"] * dt_ms
        if frame_state["frame"] >= frames:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        orig_flip()

    pygame.time.get_ticks = fake_ticks
    pygame.display.flip = capped_flip

    game = None
    try:
        game = Game(width=width, height=height)
        game.selected_mode = "Arcade"
        if game.characters:
            game.selected_character = game.characters[0]
        if game.maps:
            if scenario == "stress" and len(game.maps) > 1:
                game.selected_map = game.maps[1]
            else:
                game.selected_map = game.maps[0]
        if scenario == "stress":
            game.ai_players = max(2, int(getattr(game, "ai_players", 1)))
        game._setup_level()
        game._set_state("playing")
        game.level_start_time = 0
        source_class["player"] = game.player.__class__.__name__

        def on_event(event: dict[str, Any]) -> None:
            event_type = event.get("type")
            payload = event.get("payload", {})
            if not isinstance(payload, dict):
                return
            if event_type == "damage":
                attacker = str(payload.get("attacker_id", ""))
                target = str(payload.get("target_id", ""))
                amount = float(payload.get("amount", 0.0) or 0.0)
                if attacker == source_class["player"]:
                    metrics["damage_dealt"] += amount
                if target == source_class["player"]:
                    metrics["damage_taken"] += amount
            elif event_type == "currency_delta":
                delta = int(payload.get("delta", 0) or 0)
                if delta > 0:
                    metrics["coins_gained"] += delta
            elif event_type == "xp_delta":
                delta = int(payload.get("delta", 0) or 0)
                if delta > 0:
                    metrics["xp_gained"] += delta

        game.event_bus.subscribe("*", on_event)
        game.run()

        deaths = max(0, int(getattr(game, "match_lives", 3)) - int(game.player.lives))
        summary = {
            "seed": int(seed),
            "scenario": str(scenario),
            "frames": int(frame_state["frame"]),
            "damage_dealt": float(metrics["damage_dealt"]),
            "damage_taken": float(metrics["damage_taken"]),
            "kills": int(getattr(game, "kills", 0)),
            "deaths": int(deaths),
            "coins_gained": int(metrics["coins_gained"]),
            "xp_gained": int(metrics["xp_gained"]),
        }
        signature = _sha256(summary)
        return EpisodeOutcome(signature=signature, **summary)
    finally:
        pygame.time.get_ticks = orig_get_ticks
        pygame.display.flip = orig_flip


def _aggregate(values: list[float]) -> dict[str, float]:
    if not values:
        return {"avg": 0.0, "min": 0.0, "max": 0.0}
    return {
        "avg": float(sum(values) / len(values)),
        "min": float(min(values)),
        "max": float(max(values)),
    }


def _write_csv(path: Path, rows: list[EpisodeOutcome]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "seed",
                "signature",
                "frames",
                "damage_dealt",
                "damage_taken",
                "kills",
                "deaths",
                "coins_gained",
                "xp_gained",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "seed": row.seed,
                    "signature": row.signature,
                    "frames": row.frames,
                    "damage_dealt": row.damage_dealt,
                    "damage_taken": row.damage_taken,
                    "kills": row.kills,
                    "deaths": row.deaths,
                    "coins_gained": row.coins_gained,
                    "xp_gained": row.xp_gained,
                }
            )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run deterministic balance sweeps.")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--seeds", default=None, help="Explicit seeds or ranges, e.g. 100-120")
    parser.add_argument("--scenario", default="basic")
    parser.add_argument("--frames", type=int, default=300)
    parser.add_argument("--res", default="1280x720")
    parser.add_argument("--output", default=None)
    parser.add_argument("--csv", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    _prepare_headless_env()
    width, height = (int(part) for part in args.res.lower().split("x", 1))
    seed_values = _parse_seed_values(args.seed, args.count, args.seeds)

    if args.output:
        summary_path = Path(args.output)
    else:
        summary_path = Path("SavedGames") / "balance_sweeps" / _utc_stamp() / "summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    outcomes: list[EpisodeOutcome] = []
    failures: list[dict[str, Any]] = []
    for seed in seed_values:
        try:
            outcome = _run_episode(seed, args.scenario, args.frames, width, height)
            outcomes.append(outcome)
        except Exception as exc:
            failures.append(
                {
                    "seed": int(seed),
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                }
            )

    summary = {
        "scenario": args.scenario,
        "frames": int(args.frames),
        "resolution": {"width": width, "height": height},
        "seed_count": len(seed_values),
        "success_count": len(outcomes),
        "failure_count": len(failures),
        "damage_dealt": _aggregate([o.damage_dealt for o in outcomes]),
        "damage_taken": _aggregate([o.damage_taken for o in outcomes]),
        "kills": _aggregate([float(o.kills) for o in outcomes]),
        "deaths": _aggregate([float(o.deaths) for o in outcomes]),
        "coins_gained": _aggregate([float(o.coins_gained) for o in outcomes]),
        "xp_gained": _aggregate([float(o.xp_gained) for o in outcomes]),
        "per_seed_signatures": [
            {"seed": o.seed, "signature": o.signature} for o in outcomes
        ],
        "failures": failures,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    if args.csv:
        _write_csv(summary_path.with_suffix(".csv"), outcomes)
    print(summary_path)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
