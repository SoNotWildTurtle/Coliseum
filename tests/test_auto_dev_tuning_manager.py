"""Tests for auto dev tuning manager."""

import json

import pytest


@pytest.fixture(autouse=True)
def _set_save_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    yield


def test_tuning_reduces_defensive_spawn_delays():
    from hololive_coliseum.auto_dev_feedback_manager import AutoDevFeedbackManager
    from hololive_coliseum.auto_dev_tuning_manager import AutoDevTuningManager

    feedback = AutoDevFeedbackManager()
    feedback.start_match("Gawr Gura", "Arena")
    for _ in range(4):
        feedback.record_hazard("fire")
    feedback.finalize("loss", 2500, 180)
    tuning = AutoDevTuningManager(feedback)
    base = {
        "shield": 9000,
        "defense": 10500,
        "heal": 5000,
    }
    adjusted = tuning.recommend_spawn_timers(base)
    assert adjusted["shield"] < base["shield"]
    assert adjusted["defense"] < base["defense"]
    plan = tuning.support_plan()
    assert plan is not None
    assert plan["hazard"] == "fire"
    assert "shield" in plan["recommended_powerups"]
    # Ensure the file persisted the telemetry for future runs
    with open(feedback.path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    assert data[-1]["hazards"]["fire"] >= 4


def test_adaptive_tuning_adjusts_mob_spawn_config():
    from hololive_coliseum.auto_dev_tuning_manager import AutoDevTuningManager

    tuning = AutoDevTuningManager()
    tuning.apply_adaptive_tuning(
        {"focus": "innovation", "risk_budget": "aggressive"}
    )
    base = {"interval": 4000, "wave": 2, "max": 8}
    updated = tuning.adjust_mob_spawn_config(base)
    assert updated["interval"] <= base["interval"]
    assert updated["wave"] >= base["wave"]
    assert updated["max"] >= base["max"]
