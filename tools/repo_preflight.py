"""Repository hygiene preflight checks for tracked local artifacts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]


def _tracked_files() -> tuple[int, list[str]]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print("repo_preflight: failed to read tracked files", file=sys.stderr)
        print(result.stderr.strip(), file=sys.stderr)
        return result.returncode, []
    return 0, [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _violations(paths: list[str]) -> list[str]:
    violations: list[str] = []
    for path in paths:
        normalized = path.replace("\\", "/")
        lower = normalized.lower()
        parts = tuple(part.lower() for part in PurePosixPath(normalized).parts)
        if ".venv" in parts:
            violations.append(path)
            continue
        if lower.endswith(".lnk"):
            violations.append(path)
            continue
        if lower == "github pull request.txt":
            violations.append(path)
    return violations


def main() -> int:
    status, tracked = _tracked_files()
    if status != 0:
        return status
    bad = _violations(tracked)
    if not bad:
        print("repo_preflight: clean")
        return 0

    print("repo_preflight: tracked local artifacts detected:")
    for path in sorted(bad):
        print(f" - {path}")
    print("Remove from index with `git rm --cached` and commit.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
