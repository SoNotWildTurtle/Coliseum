"""Tests for auto dev roadmap manager."""

from hololive_coliseum.auto_dev_roadmap_manager import AutoDevRoadmapManager


class DummyFeedback:
    def __init__(self) -> None:
        self.total_matches = 5

    def get_trending_hazard(self) -> str:
        return "lava"

    def get_average_score(self) -> float:
        return 1500.0

    def get_average_duration(self) -> float:
        return 180.0


def test_compile_iteration_combines_sources() -> None:
    manager = AutoDevRoadmapManager()
    feedback = {
        "trending_hazard": "lava",
        "hazard_challenge": {"hazard": "lava", "target": 6},
        "average_score": 1200.0,
    }
    projection = {
        "focus": [
            {
                "hazard": "lava",
                "danger_score": 70,
                "recommended_powerups": ("shield", "defense"),
                "spawn_multiplier": 0.6,
            }
        ]
    }
    scenarios = [
        {"hazard": "lava", "danger_score": 70, "training_focus": "Counter lava"}
    ]
    support_plan = {
        "hazard": "lava",
        "target": 6,
        "recommended_powerups": ("shield",),
        "spawn_multiplier": 0.6,
    }

    entry = manager.compile_iteration(
        feedback=feedback,
        feedback_manager=DummyFeedback(),
        projection=projection,
        scenarios=scenarios,
        support_plan=support_plan,
    )

    assert entry["focus"] == "lava"
    sources = {action["source"] for action in entry["priority_actions"]}
    assert {"feedback", "projection", "tuning"}.issubset(sources)
    assert entry["support_plan"]["hazard"] == "lava"
    assert entry["projection_focus"][0]["hazard"] == "lava"
    assert entry["scenarios"][0]["hazard"] == "lava"
    assert entry["iteration"] == 1
    assert len(manager.recent_history()) == 1
    assert manager.latest() == entry


def test_history_respects_limit() -> None:
    manager = AutoDevRoadmapManager(max_history=2)
    for idx in range(3):
        manager.compile_iteration(feedback={"trending_hazard": f"h{idx}"})
    history = manager.recent_history()
    assert len(history) == 2
    assert history[0]["iteration"] == 2
    assert history[1]["iteration"] == 3


def test_compile_iteration_without_data_returns_empty() -> None:
    manager = AutoDevRoadmapManager()
    assert manager.compile_iteration() == {}
    assert manager.recent_history() == []
