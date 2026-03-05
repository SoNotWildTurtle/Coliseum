"""Determinism checks for the arena episode runner."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

pytest.importorskip("pygame")


def _run_episode(output_dir: Path, *, seed: int) -> dict:
    cmd = [
        sys.executable,
        "-m",
        "hololive_coliseum.tools.episode_runner",
        "--scenario",
        "basic",
        "--frames",
        "120",
        "--seed",
        str(seed),
        "--headless",
        "--output-dir",
        str(output_dir),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stderr or proc.stdout
    report_path = output_dir / "episode_report.json"
    assert report_path.exists(), f"missing report at {report_path}"
    return json.loads(report_path.read_text(encoding="utf-8"))


def _run_episode_raw(args: list[str]) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, "-m", "hololive_coliseum.tools.episode_runner", *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def test_same_seed_same_signature(tmp_path) -> None:
    report_a = _run_episode(tmp_path / "run_a", seed=1337)
    report_b = _run_episode(tmp_path / "run_b", seed=1337)
    assert report_a["episode_signature"] == report_b["episode_signature"]


def test_different_seed_changes_signature_or_metrics(tmp_path) -> None:
    report_a = _run_episode(tmp_path / "run_seed_1", seed=1337)
    report_b = _run_episode(tmp_path / "run_seed_2", seed=1338)
    same_signature = report_a["episode_signature"] == report_b["episode_signature"]
    same_outcomes = report_a["outcomes"] == report_b["outcomes"]
    assert not (same_signature and same_outcomes)


def test_report_schema_keys(tmp_path) -> None:
    report = _run_episode(tmp_path / "schema", seed=1337)
    required = {
        "schema_version",
        "timestamp_utc",
        "seed",
        "scenario",
        "frames_requested",
        "frames_run",
        "seconds_run",
        "python_version",
        "pygame_version",
        "outcomes",
        "invariants",
        "signature_inputs",
        "signature_version",
        "episode_signature",
        "status",
        "determinism_controls",
    }
    assert required.issubset(report.keys())
    assert isinstance(report["invariants"], list)
    assert isinstance(report["outcomes"], dict)


def test_strict_mode_returns_nonzero_on_violation(tmp_path) -> None:
    out = tmp_path / "strict_violation"
    proc = _run_episode_raw(
        [
            "--scenario",
            "basic",
            "--frames",
            "60",
            "--seed",
            "1337",
            "--headless",
            "--strict",
            "--inject-test-violation",
            "--output-dir",
            str(out),
        ]
    )
    assert proc.returncode != 0
    report = json.loads((out / "episode_report.json").read_text(encoding="utf-8"))
    assert report["status"] == "invariant_failure"


def test_trace_summary_schema_and_optional_provenance(tmp_path) -> None:
    out = tmp_path / "trace_run"
    proc = _run_episode_raw(
        [
            "--scenario",
            "basic",
            "--frames",
            "120",
            "--seed",
            "1337",
            "--headless",
            "--trace",
            "--trace-level",
            "minimal",
            "--output-dir",
            str(out),
        ]
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    report = json.loads((out / "episode_report.json").read_text(encoding="utf-8"))
    summary = report.get("trace_summary")
    assert isinstance(summary, dict)
    for key in (
        "event_counts",
        "events_written",
        "events_dropped",
        "total_heal",
        "hazard_damage_total",
        "status_tick_damage_total",
    ):
        assert key in summary
    counts = summary.get("event_counts", {})
    assert isinstance(counts, dict)
    assert "damage" in counts or "hazard_damage" in counts
