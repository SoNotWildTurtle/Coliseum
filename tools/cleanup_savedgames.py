"""Utility to prune old SavedGames iteration snapshots."""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path


DEFAULT_KEEP = 20


def list_snapshots(iterations_dir: Path) -> list[Path]:
    """Return sorted snapshot paths (newest first)."""
    if not iterations_dir.exists():
        return []
    snapshots = sorted(
        iterations_dir.glob("*.gguf"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return snapshots


def select_candidates(
    snapshots: list[Path],
    keep: int,
    min_age_days: int | None,
) -> list[Path]:
    """Select snapshots eligible for removal or archiving."""
    keep = max(0, keep)
    candidates = snapshots[keep:]
    if min_age_days is None:
        return candidates
    cutoff = dt.datetime.now(tz=dt.timezone.utc) - dt.timedelta(days=min_age_days)
    return [
        path
        for path in candidates
        if dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.timezone.utc)
        <= cutoff
    ]


def total_size(paths: list[Path]) -> int:
    """Return total size for a list of files."""
    return sum(path.stat().st_size for path in paths)


def apply_cleanup(
    targets: list[Path],
    archive_dir: Path | None,
    dry_run: bool,
) -> None:
    """Archive or delete snapshot files."""
    if dry_run:
        return
    if archive_dir is not None:
        archive_dir.mkdir(parents=True, exist_ok=True)
        for path in targets:
            shutil.move(str(path), archive_dir / path.name)
        return
    for path in targets:
        path.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean up SavedGames iteration snapshots.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("SavedGames"),
        help="SavedGames directory (default: SavedGames).",
    )
    parser.add_argument(
        "--keep",
        type=int,
        default=DEFAULT_KEEP,
        help="Number of newest snapshots to keep.",
    )
    parser.add_argument(
        "--min-age-days",
        type=int,
        default=None,
        help="Only target snapshots older than this many days.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be removed without changing files.",
    )
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "--delete",
        action="store_true",
        help="Delete selected snapshots.",
    )
    action_group.add_argument(
        "--archive",
        type=Path,
        default=None,
        help="Move selected snapshots to the archive directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root
    iterations_dir = root / "iterations"
    snapshots = list_snapshots(iterations_dir)
    candidates = select_candidates(snapshots, args.keep, args.min_age_days)
    if not snapshots:
        print("No iteration snapshots found.")
        return 0

    total_count = len(snapshots)
    candidate_count = len(candidates)
    candidate_size = total_size(candidates)
    action = (
        "dry-run"
        if args.dry_run or (not args.delete and args.archive is None)
        else "apply"
    )
    print(f"Snapshots found: {total_count}")
    print(f"Candidates: {candidate_count}")
    print(f"Candidate size: {candidate_size} bytes")
    print(f"Mode: {action}")

    dry_run = args.dry_run or (not args.delete and args.archive is None)
    if candidates:
        apply_cleanup(candidates, args.archive, dry_run=dry_run)
        if dry_run:
            print("No changes applied (dry-run).")
        elif args.archive is not None:
            print(f"Archived to: {args.archive}")
        else:
            print("Deleted selected snapshots.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
