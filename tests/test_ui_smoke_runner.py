"""Smoke test for the headless UI smoke runner CLI."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


pytest.importorskip("pygame")


def test_ui_smoke_runner_menu_mode(tmp_path: Path) -> None:
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
        "--output-dir",
        str(tmp_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    output = f"{proc.stdout}\n{proc.stderr}"
    if proc.returncode != 0 and "No available video device" in output:
        pytest.skip("SDL dummy video driver unavailable on this platform.")
    assert proc.returncode == 0, output
    reports = sorted(tmp_path.glob("*.json"))
    assert reports, "runner did not produce a JSON report"
    report = json.loads(reports[-1].read_text(encoding="utf-8"))
    assert report.get("effective_font_scale") is not None
    assert report.get("ui_scale") is not None
    assert report.get("config", {}).get("resolution") == "1280x720"
    assert "menu" in report.get("modes_executed", [])

