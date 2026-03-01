"""Tests for the auto-dev scenario manager."""

from __future__ import annotations

from typing import Any, Dict, List

from hololive_coliseum.auto_dev_scenario_manager import AutoDevScenarioManager
from hololive_coliseum.objective_manager import ObjectiveManager


class DummyProjection:
    """Return predetermined focus entries for tests."""

    def __init__(self, focus: List[Dict[str, Any]]) -> None:
        self.focus = focus
        self.calls = 0

    def projection_summary(self, limit: int = 3) -> Dict[str, Any]:
        self.calls += 1
        return {
            "matches_considered": 4,
            "focus": self.focus[:limit],
        }


def build_objective_manager() -> ObjectiveManager:
    manager = ObjectiveManager()
    manager.ensure_region_objectives(
        {
            "name": "Test",
            "seed": "abc123",
            "radius": 2,
            "recommended_level": 5,
        }
    )
    return manager


def test_scenario_briefs_include_counter_plan_and_objectives() -> None:
    projection = DummyProjection(
        [
            {
                "hazard": "lava",
                "danger_score": 55,
                "recommended_powerups": ("shield", "defense"),
                "spawn_multiplier": 0.6,
            }
        ]
    )
    manager = AutoDevScenarioManager(projection, build_objective_manager())
    briefs = manager.scenario_briefs(limit=2)
    assert briefs
    primary = briefs[0]
    assert primary["hazard"] == "lava"
    assert primary["danger_score"] == 55
    plan = primary["counter_plan"]
    assert plan["powerups"] == ("shield", "defense")
    assert primary["recommended_objectives"]
    assert projection.calls == 1


def test_scenario_briefs_fallback_to_objectives_when_no_projection() -> None:
    manager = AutoDevScenarioManager(None, build_objective_manager())
    briefs = manager.scenario_briefs()
    assert briefs
    fallback = briefs[0]
    assert fallback["hazard"] == "general"
    assert fallback["recommended_objectives"]
