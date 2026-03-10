"""Tests for deterministic objective rotation and reset behavior."""

from __future__ import annotations

from datetime import datetime, timezone

from hololive_coliseum.objective_manager import ObjectiveManager
from hololive_coliseum.time_provider import FixedTimeProvider


def test_daily_and_weekly_rotation_is_deterministic() -> None:
    provider = FixedTimeProvider(datetime(2026, 3, 10, tzinfo=timezone.utc))
    manager = ObjectiveManager(
        time_provider=provider,
        progression_level_provider=lambda: 8,
    )
    manager.ensure_region_objectives(
        {
            "name": "Frost Rim",
            "recommended_level": 4,
            "radius": 3,
            "auto_dev": {"hazard_challenge": {"hazard": "ice", "target": 5}},
        }
    )

    initial_daily = {
        objective.objective_type: objective.target
        for objective in manager.objectives.values()
        if objective.period == "daily"
    }
    initial_weekly = {
        objective.objective_type: objective.target
        for objective in manager.objectives.values()
        if objective.period == "weekly"
    }

    assert initial_daily
    assert initial_weekly
    assert set(initial_daily).isdisjoint(initial_weekly)
    assert len(initial_daily) == len(set(initial_daily))
    assert len(initial_weekly) == len(set(initial_weekly))

    assert all(target > 0 for target in initial_daily.values())
    assert all(target > 0 for target in initial_weekly.values())

    provider.advance(days=1)
    manager.refresh()
    next_daily = {
        objective.objective_type
        for objective in manager.objectives.values()
        if objective.period == "daily"
    }
    assert next_daily
    assert next_daily != set(initial_daily)

    provider.advance(weeks=1)
    manager.refresh()
    next_weekly = {
        objective.objective_type
        for objective in manager.objectives.values()
        if objective.period == "weekly"
    }
    assert next_weekly
    assert next_weekly != set(initial_weekly)
