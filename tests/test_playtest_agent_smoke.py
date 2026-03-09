"""Smoke tests for one-pass playtest agent analysis."""

from __future__ import annotations

import json
from pathlib import Path

from hololive_coliseum.tools.playtest_agent import run_agent_once


def _write_jsonl(path: Path, entries: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, sort_keys=True) + "\n")


def test_playtest_agent_one_pass_outputs_advice(tmp_path) -> None:
    session = tmp_path / "session_01"
    events = [
        {
            "type": "damage",
            "t": 1000,
            "frame": 10,
            "payload": {"amount": 12, "target_id": "PlayerA"},
        },
        {
            "type": "hazard_damage",
            "t": 2000,
            "frame": 20,
            "payload": {"amount": 8, "source": "hazard:lava", "target_id": "PlayerA"},
        },
        {
            "type": "objective_progress",
            "t": 2500,
            "frame": 25,
            "payload": {"objective": "defeat_enemies", "progress": 1, "target": 5},
        },
        {
            "type": "xp_delta",
            "t": 3000,
            "frame": 30,
            "payload": {"delta": 5},
        },
    ]
    _write_jsonl(session / "events" / "events_1.jsonl", events)
    snaps_dir = session / "snapshots"
    snaps_dir.mkdir(parents=True, exist_ok=True)
    (snaps_dir / "snap_00000010.json").write_text(
        json.dumps(
            {
                "frame": 10,
                "ticks": 1000,
                "state": "playing",
                "player": {"hp": 20, "max_hp": 100},
                "world": {"enemy_count": 4, "nearest_enemy_distance": 50},
            }
        ),
        encoding="utf-8",
    )
    (snaps_dir / "snap_00000020.json").write_text(
        json.dumps(
            {
                "frame": 20,
                "ticks": 2000,
                "state": "playing",
                "player": {"hp": 18, "max_hp": 100},
                "world": {"enemy_count": 5, "nearest_enemy_distance": 45},
            }
        ),
        encoding="utf-8",
    )

    output_path = session / "advice.json"
    report = run_agent_once(session, output=output_path)
    assert isinstance(report, dict)
    assert "metrics" in report
    assert "suggestions" in report
    assert isinstance(report["suggestions"], list)
    assert output_path.exists()
    assert output_path.with_suffix(".md").exists()
