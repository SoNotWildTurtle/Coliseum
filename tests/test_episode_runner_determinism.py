"""Determinism checks for the headless episode runner."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def _run_episode(out_dir: Path, seed: int, frames: int = 60) -> dict:
    env = os.environ.copy()
    env["PYGAME_HEADLESS"] = "1"
    env["SDL_VIDEODRIVER"] = "dummy"
    env["SDL_AUDIODRIVER"] = "dummy"
    env["HOLO_TELEMETRY"] = "0"
    cmd = [
        sys.executable,
        "-m",
        "hololive_coliseum.tools.episode_runner",
        "--scenario",
        "basic",
        "--frames",
        str(frames),
        "--seed",
        str(seed),
        "--headless",
        "--output-dir",
        str(out_dir),
    ]
    result = subprocess.run(
        cmd,
        env=env,
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report_path = out_dir / "episode_report.json"
    assert report_path.exists()
    return json.loads(report_path.read_text(encoding="utf-8"))


def test_episode_runner_same_seed_same_signature(tmp_path) -> None:
    report_a = _run_episode(tmp_path / "run_a", seed=1337, frames=60)
    report_b = _run_episode(tmp_path / "run_b", seed=1337, frames=60)

    assert report_a["episode_signature"] == report_b["episode_signature"]
    assert report_a["frames_executed"] == report_b["frames_executed"] == 60


def test_episode_runner_different_seed_changes_signature_or_metrics(tmp_path) -> None:
    report_a = _run_episode(tmp_path / "run_a", seed=1337, frames=60)
    report_b = _run_episode(tmp_path / "run_b", seed=1338, frames=60)

    if report_a["episode_signature"] == report_b["episode_signature"]:
        assert report_a["outcomes"] != report_b["outcomes"]


def test_episode_runner_report_schema(tmp_path) -> None:
    report = _run_episode(tmp_path / "run_schema", seed=2026, frames=40)
    required_keys = {
        "seed",
        "scenario",
        "frames_requested",
        "frames_executed",
        "outcomes",
        "invariants",
        "episode_signature",
        "signature_version",
        "signature_inputs",
        "determinism",
    }
    assert required_keys.issubset(report.keys())
