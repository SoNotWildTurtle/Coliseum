"""Tests for goal analysis manager."""

from pathlib import Path

from hololive_coliseum.goal_analysis_manager import GoalAnalysisManager


def test_goal_analysis_marks_completed(tmp_path: Path) -> None:
    goals = tmp_path / "GOALS.md"
    goals.write_text("- [ ] collect coins\n- [ ] beat boss\n")
    snap1 = tmp_path / "snap1.gguf"
    snap1.write_text("collect coins")
    snap2 = tmp_path / "snap2.gguf"
    snap2.write_text("nothing here")
    mgr = GoalAnalysisManager(goals)
    result = mgr.analyze([snap1, snap2])
    assert result == {"collect coins": True, "beat boss": False}
    mgr.mark_completed(result)
    updated = goals.read_text().splitlines()
    assert "- [x] collect coins" in updated
    assert "- [ ] beat boss" in updated


def test_goal_analysis_missing_snapshot(tmp_path: Path) -> None:
    goals = tmp_path / "GOALS.md"
    goals.write_text("- [ ] win game\n")
    mgr = GoalAnalysisManager(goals)
    result = mgr.analyze([tmp_path / "nope.gguf"])
    assert result == {"win game": False}
