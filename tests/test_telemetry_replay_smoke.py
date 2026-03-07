"""Smoke test for telemetry replay/analyzer CLI."""

from __future__ import annotations

import json
import subprocess
import sys


def test_telemetry_replay_smoke(tmp_path) -> None:
    input_path = tmp_path / "events.jsonl"
    input_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "type": "damage",
                        "t": 1,
                        "frame": 1,
                        "payload": {
                            "target_id": "EnemyA",
                            "attacker_id": "Player",
                            "amount": 10,
                        },
                    }
                ),
                json.dumps(
                    {
                        "type": "heal",
                        "t": 2,
                        "frame": 2,
                        "payload": {"target_id": "Player", "amount": 3},
                    }
                ),
                json.dumps(
                    {
                        "type": "currency_delta",
                        "t": 3,
                        "frame": 3,
                        "payload": {"delta": 5, "reason": "reward"},
                    }
                ),
                json.dumps(
                    {
                        "type": "xp_delta",
                        "t": 4,
                        "frame": 4,
                        "payload": {"delta": 8},
                    }
                ),
                json.dumps(
                    {
                        "type": "achievement_unlocked",
                        "t": 5,
                        "frame": 5,
                        "payload": {"id": "First Blood"},
                    }
                ),
            ]
        ),
        encoding="utf-8",
    )
    output_path = tmp_path / "telemetry_summary.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hololive_coliseum.tools.telemetry_replay",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert output_path.exists()
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert "event_counts" in payload
    assert payload["event_counts"]["damage"] == 1
    assert "aggregates" in payload
