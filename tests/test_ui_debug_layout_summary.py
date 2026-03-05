"""Validate that UI debug logging writes a layout summary artifact."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


pytest.importorskip("pygame")


def test_ui_debug_layout_summary(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYGAME_HEADLESS"] = "1"
    env["SDL_VIDEODRIVER"] = "dummy"
    env["SDL_AUDIODRIVER"] = "dummy"
    cmd = [
        sys.executable,
        "-m",
        "hololive_coliseum.tools.ui_smoke_runner",
        "--res",
        "1280x720",
        "--font-scale",
        "1.0",
        "--mode",
        "menu",
        "--frames",
        "10",
        "--ui-debug",
        "--output-dir",
        str(tmp_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    output = f"{proc.stdout}\n{proc.stderr}"
    if proc.returncode != 0 and "No available video device" in output:
        pytest.skip("SDL dummy video driver unavailable on this platform.")
    assert proc.returncode == 0, output
    summary = tmp_path / "ui_layout_summary.json"
    assert summary.exists(), "ui_layout_summary.json was not written"
    payload = json.loads(summary.read_text(encoding="utf-8"))
    assert "metadata" in payload
    assert "counts" in payload
    counts = payload["counts"]
    assert isinstance(counts.get("overflow_count"), int)
    assert isinstance(counts.get("collision_count"), int)
    assert isinstance(counts.get("clip_risk_count"), int)

