"""Repository analysis helpers for tracking the game's current technical state."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class FileSnapshot:
    """Summary metadata for a single Python file."""

    path: str
    line_count: int
    has_docstring: bool


class ProjectAnalysisSkill:
    """Build a lightweight, deterministic snapshot of project health."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def analyze(self) -> dict[str, Any]:
        """Return repository metrics and actionable observations."""
        module_files = self._python_files("hololive_coliseum")
        test_files = self._python_files("tests", pattern="test_*.py")
        module_snapshots = [self._snapshot(path) for path in module_files]
        test_snapshots = [self._snapshot(path) for path in test_files]
        missing_docstrings = [
            item.path for item in module_snapshots if not item.has_docstring
        ]

        docstring_ratio = 0.0
        if module_snapshots:
            documented = sum(1 for item in module_snapshots if item.has_docstring)
            docstring_ratio = documented / len(module_snapshots)

        runtime_snapshot = self._saved_games_snapshot()
        directory_snapshot = self._directory_snapshot()
        pygame_audit = self._pygame_test_audit(test_files)
        todo_snapshot = self._todo_snapshot(module_files, test_files)
        observations = self._observations(
            module_snapshots=module_snapshots,
            test_snapshots=test_snapshots,
            docstring_ratio=docstring_ratio,
            runtime_snapshot=runtime_snapshot,
            directory_snapshot=directory_snapshot,
            pygame_audit=pygame_audit,
            todo_snapshot=todo_snapshot,
        )
        return {
            "generated_at": datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
            "module_count": len(module_snapshots),
            "test_count": len(test_snapshots),
            "auto_dev_module_count": sum(
                1 for item in module_snapshots if "auto_dev_" in Path(item.path).name
            ),
            "docstring_ratio": round(docstring_ratio, 3),
            "largest_modules": self._top_files(module_snapshots, limit=10),
            "largest_tests": self._top_files(test_snapshots, limit=10),
            "missing_docstrings": missing_docstrings[:15],
            "runtime_snapshot": runtime_snapshot,
            "directory_snapshot": directory_snapshot,
            "pygame_audit": pygame_audit,
            "todo_snapshot": todo_snapshot,
            "observations": observations,
        }

    def render_markdown(self, analysis: dict[str, Any]) -> str:
        """Render a human-readable project state report."""
        lines: list[str] = []
        lines.append("# Project State Analysis")
        lines.append("")
        lines.append(f"- Generated (UTC): `{analysis['generated_at']}`")
        lines.append(f"- Python modules (`hololive_coliseum`): {analysis['module_count']}")
        lines.append(f"- Test modules (`tests/test_*.py`): {analysis['test_count']}")
        lines.append(f"- Auto-dev modules: {analysis['auto_dev_module_count']}")
        lines.append(f"- Module docstring ratio: {analysis['docstring_ratio']:.1%}")
        lines.append("")
        lines.append("## Largest Core Modules")
        lines.append("")
        for entry in analysis["largest_modules"]:
            lines.append(f"- `{entry['path']}`: {entry['line_count']} lines")
        lines.append("")
        lines.append("## Largest Test Modules")
        lines.append("")
        for entry in analysis["largest_tests"]:
            lines.append(f"- `{entry['path']}`: {entry['line_count']} lines")
        if analysis["missing_docstrings"]:
            lines.append("")
            lines.append("## Modules Missing Docstrings (Sample)")
            lines.append("")
            for entry in analysis["missing_docstrings"]:
                lines.append(f"- `{entry}`")
        dirs = analysis["directory_snapshot"]
        lines.append("")
        lines.append("## Directory Footprint")
        lines.append("")
        for entry in dirs:
            lines.append(
                f"- `{entry['path']}`: {entry['file_count']} files, "
                f"{entry['size_mb']:.2f} MB"
            )
        runtime = analysis["runtime_snapshot"]
        lines.append("")
        lines.append("## Runtime Save Snapshot")
        lines.append("")
        lines.append(f"- JSON save files: {runtime['json_files']}")
        lines.append(f"- SQLite-related files: {runtime['db_related_files']}")
        lines.append(f"- Iteration snapshots (`.gguf`): {runtime['gguf_files']}")
        lines.append(f"- SavedGames total size: {runtime['total_size_mb']:.2f} MB")
        pygame_audit = analysis["pygame_audit"]
        lines.append("")
        lines.append("## Pygame Test Audit")
        lines.append("")
        lines.append(f"- Tests referencing pygame: {pygame_audit['pygame_tests']}")
        lines.append(
            f"- Tests missing importorskip: {pygame_audit['missing_importorskip']}"
        )
        if pygame_audit["missing_importorskip_paths"]:
            lines.append("")
            lines.append("### Missing importorskip (Sample)")
            for entry in pygame_audit["missing_importorskip_paths"]:
                lines.append(f"- `{entry}`")
        todo_snapshot = analysis["todo_snapshot"]
        lines.append("")
        lines.append("## TODO Snapshot")
        lines.append("")
        lines.append(
            f"- TODOs in modules/tests: {todo_snapshot['total_todos']}"
        )
        if todo_snapshot["sample_locations"]:
            lines.append("")
            lines.append("### TODO Locations (Sample)")
            for entry in todo_snapshot["sample_locations"]:
                lines.append(f"- `{entry}`")
        lines.append("")
        lines.append("## Key Observations")
        lines.append("")
        for item in analysis["observations"]:
            lines.append(f"- {item}")
        lines.append("")
        return "\n".join(lines)

    def _python_files(self, relative_dir: str, pattern: str = "*.py") -> list[Path]:
        base = self.root / relative_dir
        if not base.exists():
            return []
        return sorted(path for path in base.rglob(pattern) if "__pycache__" not in path.parts)

    def _snapshot(self, path: Path) -> FileSnapshot:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        rel_path = path.relative_to(self.root).as_posix()
        return FileSnapshot(
            path=rel_path,
            line_count=len(text.splitlines()),
            has_docstring=bool(ast.get_docstring(tree)),
        )

    def _top_files(self, snapshots: list[FileSnapshot], limit: int) -> list[dict[str, Any]]:
        top = sorted(snapshots, key=lambda item: item.line_count, reverse=True)[:limit]
        return [{"path": item.path, "line_count": item.line_count} for item in top]

    def _saved_games_snapshot(self) -> dict[str, Any]:
        saved_games = self.root / "SavedGames"
        if not saved_games.exists():
            return {
                "json_files": 0,
                "db_related_files": 0,
                "gguf_files": 0,
                "total_size_mb": 0.0,
            }
        files = [path for path in saved_games.rglob("*") if path.is_file()]
        json_files = sum(1 for path in files if path.suffix.lower() == ".json")
        db_related_files = sum(
            1
            for path in files
            if path.suffix.lower() in {".db", ".db-shm", ".db-wal"}
        )
        gguf_files = sum(1 for path in files if path.suffix.lower() == ".gguf")
        total_size = sum(path.stat().st_size for path in files)
        return {
            "json_files": json_files,
            "db_related_files": db_related_files,
            "gguf_files": gguf_files,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
        }

    def _directory_snapshot(self) -> list[dict[str, Any]]:
        targets = [
            "hololive_coliseum",
            "tests",
            "docs",
            "tools",
            "Images",
            "asset_pack",
            "sounds",
            "SavedGames",
        ]
        entries: list[dict[str, Any]] = []
        for name in targets:
            path = self.root / name
            if not path.exists():
                continue
            files = [item for item in path.rglob("*") if item.is_file()]
            size = sum(item.stat().st_size for item in files)
            entries.append(
                {
                    "path": name,
                    "file_count": len(files),
                    "size_mb": round(size / (1024 * 1024), 2),
                }
            )
        return entries

    def _pygame_test_audit(self, test_files: list[Path]) -> dict[str, Any]:
        pygame_tests: list[Path] = []
        missing_importorskip: list[Path] = []
        for path in test_files:
            text = path.read_text(encoding="utf-8")
            if "pygame" not in text:
                continue
            pygame_tests.append(path)
            if "importorskip(\"pygame\")" not in text:
                missing_importorskip.append(path)
        return {
            "pygame_tests": len(pygame_tests),
            "missing_importorskip": len(missing_importorskip),
            "missing_importorskip_paths": [
                path.relative_to(self.root).as_posix()
                for path in missing_importorskip[:10]
            ],
        }

    def _todo_snapshot(
        self, module_files: list[Path], test_files: list[Path]
    ) -> dict[str, Any]:
        locations: list[str] = []
        total = 0
        for path in module_files + test_files:
            lines = path.read_text(encoding="utf-8").splitlines()
            for idx, line in enumerate(lines, start=1):
                if "TODO" in line:
                    total += 1
                    if len(locations) < 12:
                        rel_path = path.relative_to(self.root).as_posix()
                        locations.append(f"{rel_path}:{idx}")
        return {"total_todos": total, "sample_locations": locations}

    def _observations(
        self,
        module_snapshots: list[FileSnapshot],
        test_snapshots: list[FileSnapshot],
        docstring_ratio: float,
        runtime_snapshot: dict[str, Any],
        directory_snapshot: list[dict[str, Any]],
        pygame_audit: dict[str, Any],
        todo_snapshot: dict[str, Any],
    ) -> list[str]:
        observations: list[str] = []
        if module_snapshots:
            tests_per_module = len(test_snapshots) / len(module_snapshots)
            observations.append(
                f"Test-file to module ratio is {tests_per_module:.2f}; coverage breadth is strong."
            )
        if docstring_ratio < 0.9:
            observations.append(
                "Module docstring coverage is below 90%; add docs to improve analyzer context."
            )
        if pygame_audit["missing_importorskip"] > 0:
            observations.append(
                "Some pygame tests lack importorskip guards; add skips for clean CI."
            )
        if todo_snapshot["total_todos"] > 0:
            observations.append(
                "TODO markers remain in modules/tests; track them before ship milestones."
            )
        largest = self._top_files(module_snapshots, limit=3)
        if largest:
            lead = ", ".join(item["path"] for item in largest)
            observations.append(f"Largest implementation hotspots: {lead}.")
        if runtime_snapshot["gguf_files"] > 50:
            observations.append(
                "SavedGames contains many iteration snapshots; archive old `.gguf` files."
            )
        codebase_analysis_doc = self.root / "docs" / "CODEBASE_ANALYSIS.md"
        if codebase_analysis_doc.exists():
            text = codebase_analysis_doc.read_text(encoding="utf-8")
            if ".venv" in text:
                observations.append(
                    "Generated codebase analysis still includes virtualenv modules."
                )
        for entry in directory_snapshot:
            if entry["path"] == "SavedGames" and entry["size_mb"] > 100:
                observations.append(
                    "SavedGames is over 100 MB; archive or prune large saves."
                )
        if not observations:
            observations.append("No immediate structural risks detected.")
        return observations
