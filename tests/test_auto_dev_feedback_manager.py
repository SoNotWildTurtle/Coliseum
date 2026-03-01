"""Tests for auto dev feedback manager."""

import json

import pytest

from hololive_coliseum.auto_dev_feedback_manager import AutoDevFeedbackManager


def test_feedback_manager_collects_and_persists(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    manager = AutoDevFeedbackManager()
    manager.start_match("Gawr Gura", "Default")
    manager.record_hazard("spike")
    manager.record_hazard("spike")
    manager.record_hazard("lava")
    entry = manager.finalize("victory", 900, 120, "player1")

    assert entry["hazards"]["spike"] == 2
    assert manager.get_trending_hazard() == "spike"
    assert manager.get_favorite_character() == "Gawr Gura"
    assert manager.get_average_score() == pytest.approx(900)
    assert manager.get_average_duration() == pytest.approx(120)
    recommended = manager.estimate_recommended_level()
    assert recommended >= 1

    data = json.loads((tmp_path / "auto_dev_feedback.json").read_text(encoding="utf-8"))
    assert data[0]["result"] == "victory"

    # Loading again should rebuild aggregates from disk
    manager_reload = AutoDevFeedbackManager()
    insight = manager_reload.region_insight()
    assert insight["trending_hazard"] == "spike"
    assert manager_reload.estimate_recommended_level() == recommended
    challenge = manager_reload.hazard_challenge()
    assert challenge is not None
    assert challenge["hazard"] == "spike"
    assert challenge["target"] >= 3
    assert insight["hazard_challenge"]["hazard"] == "spike"
