"""Tests for auto dev projection manager."""

from __future__ import annotations

import pytest

from hololive_coliseum.auto_dev_feedback_manager import AutoDevFeedbackManager
from hololive_coliseum.auto_dev_tuning_manager import AutoDevTuningManager
from hololive_coliseum.auto_dev_projection_manager import AutoDevProjectionManager


@pytest.fixture()
def feedback_manager(tmp_path):
    path = tmp_path / "feedback.json"
    manager = AutoDevFeedbackManager(path)
    return manager


def test_projection_summary_highlights_top_hazards(feedback_manager):
    tuning = AutoDevTuningManager(feedback_manager)
    for _ in range(2):
        feedback_manager.start_match("Gawr Gura", "Arena")
        for _ in range(4):
            feedback_manager.record_hazard("lava")
        feedback_manager.record_hazard("poison")
        feedback_manager.finalize("loss", 1200, 90)
    feedback_manager.start_match("Gawr Gura", "Arena")
    for _ in range(2):
        feedback_manager.record_hazard("poison")
    feedback_manager.finalize("win", 1500, 60)

    projection = AutoDevProjectionManager(feedback_manager, tuning, window=5)
    summary = projection.projection_summary()
    assert summary["matches_considered"] == 3
    focus = summary["focus"]
    assert focus[0]["hazard"] == "lava"
    assert focus[0]["danger_score"] > focus[1]["danger_score"]
    assert "recommended_powerups" in focus[0]
    assert focus[0]["spawn_multiplier"] <= 0.7


def test_projection_summary_empty_without_data():
    projection = AutoDevProjectionManager()
    assert projection.projection_summary() == {}
