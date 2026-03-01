"""Tests for auto dev focus manager."""

from hololive_coliseum.auto_dev_focus_manager import AutoDevFocusManager


def test_analyse_combines_signals() -> None:
    manager = AutoDevFocusManager(max_focus=3)
    roadmap = {
        "focus": "lava",
        "iteration": 4,
        "priority_actions": [
            {"hazard": "lava", "title": "Stabilise lava"},
            {"hazard": "poison", "title": "Monitor poison"},
        ],
    }
    feedback = {"trending_hazard": "lava", "hazard_challenge": {"hazard": "lava"}}
    projection = {
        "matches_considered": 6,
        "focus": [
            {"hazard": "lava", "danger_score": 60},
            {"hazard": "poison", "danger_score": 20},
        ],
    }
    scenarios = [
        {"hazard": "lava"},
        {"hazard": "poison"},
    ]
    support_plan = {"hazard": "lava"}

    report = manager.analyse(
        roadmap=roadmap,
        feedback=feedback,
        projection=projection,
        scenarios=scenarios,
        support_plan=support_plan,
    )

    assert report["top_focus"] == "lava"
    hazards = {entry["hazard"]: entry for entry in report["priorities"]}
    assert hazards["lava"]["score"] > hazards["poison"]["score"]
    assert "roadmap" in hazards["lava"]["sources"]
    assert report["context"]["roadmap_iteration"] == 4
    assert report["context"]["matches_considered"] == 6
    assert report["context"]["support_plan_hazard"] == "lava"
    assert report["context"]["scenario_count"] == 2


def test_history_respects_limit() -> None:
    manager = AutoDevFocusManager(history_limit=2)
    for idx in range(3):
        manager.analyse(roadmap={"focus": f"hazard-{idx}"})
    history = manager.recent_focus()
    assert len(history) == 2
    assert history[0]["top_focus"] == "hazard-1"
    assert history[1]["top_focus"] == "hazard-2"


def test_analyse_without_signals_returns_empty() -> None:
    manager = AutoDevFocusManager()
    assert manager.analyse() == {}
    assert manager.latest() is None
