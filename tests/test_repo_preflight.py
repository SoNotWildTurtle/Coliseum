"""Tests for repository hygiene preflight checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_repo_preflight_clean() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "tools" / "repo_preflight.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
