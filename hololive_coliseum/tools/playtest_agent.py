"""Live playtest analyzer that tails telemetry and snapshots for advice."""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from hololive_coliseum.save_manager import SAVE_DIR


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _default_playtest_root() -> Path:
    return Path(SAVE_DIR) / "playtest"


def find_latest_session(base: Path | None = None) -> Path | None:
    root = base or _default_playtest_root()
    if not root.exists():
        return None
    sessions = [p for p in root.iterdir() if p.is_dir()]
    if not sessions:
        return None
    sessions.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return sessions[0]


def _collect_event_files(session_dir: Path) -> list[Path]:
    event_dir = session_dir / "events"
    if event_dir.exists():
        return sorted(event_dir.glob("*.jsonl"))
    return sorted(session_dir.glob("*.jsonl"))


def _collect_snapshot_files(session_dir: Path) -> list[Path]:
    snap_dir = session_dir / "snapshots"
    return sorted(snap_dir.glob("snap_*.json")) if snap_dir.exists() else []


@dataclass
class Advice:
    severity: str
    rule: str
    message: str
    code_pointer: str

    def to_dict(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "rule": self.rule,
            "message": self.message,
            "code_pointer": self.code_pointer,
        }


class SessionReader:
    """Incremental reader for playtest events and snapshots."""

    def __init__(self, session_dir: Path) -> None:
        self.session_dir = session_dir
        self._event_offsets: dict[Path, int] = {}
        self._seen_snaps: set[Path] = set()

    def poll(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        new_events: list[dict[str, Any]] = []
        for event_file in _collect_event_files(self.session_dir):
            offset = self._event_offsets.get(event_file, 0)
            with event_file.open("r", encoding="utf-8") as handle:
                handle.seek(offset)
                for raw in handle:
                    raw = raw.strip()
                    if not raw:
                        continue
                    try:
                        new_events.append(json.loads(raw))
                    except json.JSONDecodeError:
                        continue
                self._event_offsets[event_file] = handle.tell()

        new_snaps: list[dict[str, Any]] = []
        for snap_file in _collect_snapshot_files(self.session_dir):
            if snap_file in self._seen_snaps:
                continue
            self._seen_snaps.add(snap_file)
            try:
                new_snaps.append(json.loads(snap_file.read_text(encoding="utf-8")))
            except json.JSONDecodeError:
                continue
        new_snaps.sort(key=lambda item: _safe_int(item.get("frame"), 0))
        return new_events, new_snaps


def analyze_playtest(
    events: list[dict[str, Any]],
    snapshots: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compute rolling metrics and actionable advice from playtest data."""

    event_counts = Counter()
    damage_dealt = 0.0
    damage_taken = 0.0
    hazard_damage = 0.0
    status_tick_damage = 0.0
    healing_total = 0.0
    coins_delta = 0
    xp_delta = 0
    objective_progress_events = 0
    achievement_unlocks = 0
    playtest_issue_events = 0
    missing_provenance = 0
    damage_events = 0
    last_event_ticks = 0
    low_hp_samples = 0
    near_death_samples = 0
    playing_samples = 0
    recent_enemy_pressure = 0
    first_playing_ticks = None
    last_objective_ticks = None
    last_snapshot_ticks = 0
    snapshot_states = Counter()

    for event in events:
        event_type = str(event.get("type", "unknown"))
        payload = event.get("payload", {})
        if not isinstance(payload, dict):
            payload = {}
        event_counts[event_type] += 1
        ticks = _safe_int(event.get("t"), 0)
        last_event_ticks = max(last_event_ticks, ticks)

        if event_type in {"damage", "hazard_damage", "status_tick"}:
            damage_events += 1
            amount = _safe_float(payload.get("amount"), 0.0)
            target = str(payload.get("target_id", ""))
            attacker = str(payload.get("attacker_id", ""))
            source = str(payload.get("source", ""))
            if not attacker or not source:
                missing_provenance += 1
            if event_type == "hazard_damage":
                hazard_damage += amount
                damage_taken += amount
            elif event_type == "status_tick":
                status_tick_damage += amount
                damage_taken += amount
            else:
                # Best-effort attribution: when target exists treat as taken, else dealt.
                if target:
                    damage_taken += amount
                else:
                    damage_dealt += amount
        elif event_type == "heal":
            healing_total += _safe_float(payload.get("amount"), 0.0)
        elif event_type == "currency_delta":
            coins_delta += max(0, _safe_int(payload.get("delta"), 0))
        elif event_type == "xp_delta":
            xp_delta += max(0, _safe_int(payload.get("delta"), 0))
        elif event_type == "objective_progress":
            objective_progress_events += 1
            last_objective_ticks = ticks
        elif event_type == "achievement_unlocked":
            achievement_unlocks += 1
        elif event_type == "playtest_issue":
            playtest_issue_events += 1

    for snap in snapshots:
        ticks = _safe_int(snap.get("ticks"), 0)
        last_snapshot_ticks = max(last_snapshot_ticks, ticks)
        state = str(snap.get("state", "unknown"))
        snapshot_states[state] += 1
        if state == "playing":
            playing_samples += 1
            if first_playing_ticks is None:
                first_playing_ticks = ticks
            hp = _safe_float(snap.get("player", {}).get("hp"), 0.0)
            max_hp = _safe_float(snap.get("player", {}).get("max_hp"), 0.0)
            if max_hp > 0:
                ratio = hp / max_hp
                if ratio < 0.25:
                    low_hp_samples += 1
                if ratio < 0.10:
                    near_death_samples += 1
            nearest = snap.get("world", {}).get("nearest_enemy_distance")
            if nearest is not None and _safe_float(nearest, 0.0) < 75.0:
                recent_enemy_pressure += 1

    duration_ticks = max(last_snapshot_ticks, last_event_ticks)
    minutes = max(1.0 / 60.0, duration_ticks / 60000.0)
    hp_low_ratio = (low_hp_samples / playing_samples) if playing_samples else 0.0
    near_death_ratio = (near_death_samples / playing_samples) if playing_samples else 0.0
    coins_per_min = coins_delta / minutes
    xp_per_min = xp_delta / minutes
    hazard_ratio = (
        (hazard_damage / damage_taken) if damage_taken > 0 else 0.0
    )
    provenance_ratio = (
        (missing_provenance / damage_events) if damage_events else 0.0
    )
    objective_stall_ms = 0
    if first_playing_ticks is not None:
        ref = last_objective_ticks if last_objective_ticks is not None else first_playing_ticks
        objective_stall_ms = max(0, duration_ticks - ref)

    advice: list[Advice] = []

    def add(severity: str, rule: str, message: str, pointer: str) -> None:
        advice.append(Advice(severity, rule, message, pointer))

    if hp_low_ratio > 0.30:
        add("high", "low_hp_time", "Player HP spent >30% of playtime below 25%. Tune healing/drop rates or defense.", "hololive_coliseum/hazard_manager.py, hololive_coliseum/combat_manager.py")
    if near_death_ratio > 0.15:
        add("high", "near_death_spikes", "Near-death states are frequent. Consider i-frames or lower burst damage windows.", "hololive_coliseum/combat_manager.py")
    if objective_stall_ms > 60000 and snapshot_states.get("playing", 0) > 0:
        add("medium", "objective_stall", "Objective progress stalled for over 60s while playing. Revisit trigger wiring or requirements.", "hololive_coliseum/objective_manager.py, hololive_coliseum/game.py")
    if hazard_ratio > 0.60 and damage_taken > 0:
        add("high", "hazard_overweight", "Hazard damage dominates incoming damage. Rebalance hazard frequency/telegraphing.", "hololive_coliseum/hazard_manager.py")
    if status_tick_damage > max(15.0, healing_total * 1.5):
        add("medium", "status_pressure", "Status tick damage outpaces healing. Add or buff cleanse/counterplay options.", "hololive_coliseum/status_effects.py, hololive_coliseum/item_manager.py")
    if coins_per_min < 5 and minutes > 2:
        add("medium", "economy_flat_coins", "Coins per minute are low over sustained play. Consider reward scaling hooks.", "hololive_coliseum/game.py:_award_currency")
    if xp_per_min < 10 and minutes > 2:
        add("medium", "economy_flat_xp", "XP gain rate is low/flat. Review XP multipliers and enemy reward formulas.", "hololive_coliseum/game.py:_xp_for_enemy")
    if provenance_ratio > 0.20:
        add("medium", "missing_provenance", "Many damage events lack attacker/source attribution. Improve provenance in emitters.", "hololive_coliseum/combat_manager.py, hololive_coliseum/hazard_manager.py, hololive_coliseum/status_effects.py")
    if recent_enemy_pressure > 0 and damage_dealt < damage_taken * 0.4:
        add("medium", "pressure_without_output", "Player remains under close enemy pressure with low outgoing damage. Check hitbox/hurtbox or weapon tuning.", "hololive_coliseum/combat_manager.py, hololive_coliseum/player.py")
    if snapshot_states.get("playing", 0) > 0 and damage_events == 0:
        add("high", "combat_silence", "No damage events recorded during active play. Verify collision/event bus hooks.", "hololive_coliseum/game.py:_publish_event")
    if objective_progress_events > 0 and achievement_unlocks == 0 and minutes > 3:
        add("low", "achievement_pacing", "Objectives progressed without achievement unlocks. Validate progression pacing and thresholds.", "hololive_coliseum/achievement_manager.py")
    if event_counts.get("heal", 0) == 0 and hp_low_ratio > 0.20:
        add("medium", "healing_absent", "Sustained low HP with no heal events detected. Consider heal pickup cadence.", "hololive_coliseum/game.py:_handle_powerup_collision")
    if playtest_issue_events >= 8:
        add("high", "runtime_issue_markers", "Frequent runtime issue markers detected during playtest. Inspect recent snapshots and telemetry markers.", "hololive_coliseum/playtest_snapshot.py")

    severe_count = sum(1 for item in advice if item.severity == "high")
    return {
        "timestamp_utc": _utc_now(),
        "metrics": {
            "duration_minutes": round(minutes, 3),
            "damage_dealt": round(damage_dealt, 3),
            "damage_taken": round(damage_taken, 3),
            "hazard_damage": round(hazard_damage, 3),
            "status_tick_damage": round(status_tick_damage, 3),
            "healing_total": round(healing_total, 3),
            "coins_per_min": round(coins_per_min, 3),
            "xp_per_min": round(xp_per_min, 3),
            "objective_progress_events": int(objective_progress_events),
            "achievement_unlocks": int(achievement_unlocks),
            "playtest_issue_events": int(playtest_issue_events),
            "hp_low_ratio": round(hp_low_ratio, 4),
            "near_death_ratio": round(near_death_ratio, 4),
            "provenance_missing_ratio": round(provenance_ratio, 4),
            "event_counts": dict(sorted(event_counts.items())),
            "snapshot_states": dict(sorted(snapshot_states.items())),
        },
        "suggestions": [item.to_dict() for item in advice],
        "severe_count": severe_count,
    }


def _write_outputs(report: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    md_path = output_path.with_suffix(".md")
    lines = [
        "# Playtest Agent Advice",
        "",
        f"Generated: {report.get('timestamp_utc', '')}",
        "",
        "## Suggestions",
    ]
    for item in report.get("suggestions", []):
        lines.append(
            f"- [{item.get('severity', 'info')}] {item.get('rule', '')}: "
            f"{item.get('message', '')} ({item.get('code_pointer', '')})"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_agent_once(
    input_dir: Path,
    *,
    output: Path | None = None,
    tail_events: bool = False,
) -> dict[str, Any]:
    reader = SessionReader(input_dir)
    events, snapshots = reader.poll()
    report = analyze_playtest(events, snapshots)
    if tail_events:
        event_tail = events[-20:]
        print(json.dumps(event_tail, indent=2, sort_keys=True))
    if output is not None:
        _write_outputs(report, output)
    return report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Tail playtest session and emit advice.")
    parser.add_argument("--input", default=None, help="Session directory; defaults to latest.")
    parser.add_argument("--interval", type=float, default=5.0, help="Polling/report interval.")
    parser.add_argument("--tail-events", action="store_true")
    parser.add_argument("--output", default=None, help="Write advice JSON/MD to this path.")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero on severe anomalies.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    session_dir = Path(args.input) if args.input else find_latest_session()
    if session_dir is None or not session_dir.exists():
        print("playtest_agent: no playtest session directory found")
        return 1
    reader = SessionReader(session_dir)
    interval = max(1.0, float(args.interval))
    output = Path(args.output) if args.output else None
    cumulative_events: list[dict[str, Any]] = []
    cumulative_snaps: list[dict[str, Any]] = []
    print(f"playtest_agent: monitoring {session_dir}")
    try:
        while True:
            events, snaps = reader.poll()
            if events:
                cumulative_events.extend(events)
            if snaps:
                cumulative_snaps.extend(snaps)
            report = analyze_playtest(cumulative_events, cumulative_snaps)
            print(
                json.dumps(
                    {
                        "timestamp_utc": report["timestamp_utc"],
                        "severe_count": report["severe_count"],
                        "suggestion_count": len(report["suggestions"]),
                        "metrics": {
                            "damage_taken": report["metrics"]["damage_taken"],
                            "damage_dealt": report["metrics"]["damage_dealt"],
                            "coins_per_min": report["metrics"]["coins_per_min"],
                            "xp_per_min": report["metrics"]["xp_per_min"],
                        },
                    },
                    sort_keys=True,
                )
            )
            for suggestion in report["suggestions"][:8]:
                print(
                    f"- [{suggestion['severity']}] {suggestion['rule']}: "
                    f"{suggestion['message']}"
                )
            if args.tail_events and events:
                print("Recent events:")
                for event in events[-20:]:
                    print(json.dumps(event, sort_keys=True))
            if output is not None:
                _write_outputs(report, output)
            if args.strict and report["severe_count"] > 0:
                return 2
            time.sleep(interval)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
