"""Smoke test for deterministic balance sweep tooling."""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest


def test_balance_sweep_smoke(tmp_path) -> None:
    pytest.importorskip("pygame")
    output_path = tmp_path / "summary.json"
    env = dict(os.environ)
    env["PYGAME_HEADLESS"] = "1"
    env["SDL_VIDEODRIVER"] = "dummy"
    env["SDL_AUDIODRIVER"] = "dummy"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hololive_coliseum.tools.balance_sweep",
            "--seeds",
            "100-101",
            "--frames",
            "30",
            "--output",
            str(output_path),
        ],
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert output_path.exists()
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert "damage_dealt" in payload
    assert "damage_taken" in payload
    assert "per_seed_signatures" in payload
    assert payload["seed_count"] == 2
