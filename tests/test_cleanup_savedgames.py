"""Tests for the SavedGames cleanup utility."""

from __future__ import annotations

import os
import time
from pathlib import Path

from tools.cleanup_savedgames import apply_cleanup, list_snapshots, select_candidates


def _write_snapshot(path: Path, seconds_ago: int) -> None:
    path.write_text("snapshot", encoding="utf-8")
    now = time.time()
    timestamp = now - seconds_ago
    os.utime(path, (timestamp, timestamp))


def test_list_snapshots_sorts_newest_first(tmp_path: Path) -> None:
    iterations = tmp_path / "iterations"
    iterations.mkdir()
    _write_snapshot(iterations / "old.gguf", seconds_ago=60)
    _write_snapshot(iterations / "new.gguf", seconds_ago=10)

    snapshots = list_snapshots(iterations)

    assert [path.name for path in snapshots] == ["new.gguf", "old.gguf"]


def test_select_candidates_respects_keep_and_age(tmp_path: Path) -> None:
    iterations = tmp_path / "iterations"
    iterations.mkdir()
    _write_snapshot(iterations / "new.gguf", seconds_ago=60)
    _write_snapshot(iterations / "mid.gguf", seconds_ago=60 * 60 * 24 * 5)
    _write_snapshot(iterations / "old.gguf", seconds_ago=60 * 60 * 24 * 40)

    snapshots = list_snapshots(iterations)
    candidates = select_candidates(snapshots, keep=1, min_age_days=30)

    assert [path.name for path in candidates] == ["old.gguf"]


def test_apply_cleanup_archives_files(tmp_path: Path) -> None:
    iterations = tmp_path / "iterations"
    archive = tmp_path / "archive"
    iterations.mkdir()
    _write_snapshot(iterations / "keep.gguf", seconds_ago=10)
    target = iterations / "move.gguf"
    _write_snapshot(target, seconds_ago=60)

    apply_cleanup([target], archive_dir=archive, dry_run=False)

    assert not target.exists()
    assert (archive / "move.gguf").exists()
