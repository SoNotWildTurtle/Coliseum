"""Tests for analysis skill."""

from __future__ import annotations

from pathlib import Path

from tools.generate_codebase_analysis import walk_py_files
from tools.analysis_skill import ProjectAnalysisSkill


def test_project_analysis_skill_reports_basic_metrics(tmp_path: Path) -> None:
    package_dir = tmp_path / "hololive_coliseum"
    tests_dir = tmp_path / "tests"
    saved_games_dir = tmp_path / "SavedGames" / "iterations"
    docs_dir = tmp_path / "docs"
    package_dir.mkdir(parents=True)
    tests_dir.mkdir()
    saved_games_dir.mkdir(parents=True)
    docs_dir.mkdir()

    (package_dir / "module_a.py").write_text(
        '"""Example module."""\n\n\ndef run() -> int:\n    return 1\n',
        encoding="utf-8",
    )
    (package_dir / "module_b.py").write_text(
        "def run() -> int:\n    return 2\n",
        encoding="utf-8",
    )
    (tests_dir / "test_module_a.py").write_text(
        "def test_ok() -> None:\n    assert True\n",
        encoding="utf-8",
    )
    (saved_games_dir / "iteration_a.gguf").write_text("snapshot", encoding="utf-8")
    (tmp_path / "SavedGames" / "settings.json").write_text("{}", encoding="utf-8")
    (docs_dir / "CODEBASE_ANALYSIS.md").write_text(
        "contains .venv artifacts",
        encoding="utf-8",
    )

    skill = ProjectAnalysisSkill(tmp_path)
    analysis = skill.analyze()
    rendered = skill.render_markdown(analysis)

    assert analysis["module_count"] == 2
    assert analysis["test_count"] == 1
    assert analysis["docstring_ratio"] == 0.5
    assert analysis["runtime_snapshot"]["gguf_files"] == 1
    assert "Project State Analysis" in rendered
    assert (
        "Generated codebase analysis still includes virtualenv modules."
        in analysis["observations"]
    )


def test_walk_py_files_skips_virtualenv_variants(tmp_path: Path) -> None:
    (tmp_path / "hololive_coliseum").mkdir()
    (tmp_path / ".venv314" / "Lib").mkdir(parents=True)
    (tmp_path / "venv_local").mkdir()
    keep_file = tmp_path / "hololive_coliseum" / "kept.py"
    skip_hidden_venv = tmp_path / ".venv314" / "Lib" / "skip.py"
    skip_named_venv = tmp_path / "venv_local" / "skip.py"
    keep_file.write_text('"""ok"""\n', encoding="utf-8")
    skip_hidden_venv.write_text('"""skip"""\n', encoding="utf-8")
    skip_named_venv.write_text('"""skip"""\n', encoding="utf-8")

    files = walk_py_files(tmp_path)

    assert keep_file in files
    assert skip_hidden_venv not in files
    assert skip_named_venv not in files
