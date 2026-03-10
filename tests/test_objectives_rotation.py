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
    assert manager.last_reset_day_key == "2026-03-10"
    assert manager.last_reset_week_key == "2026-W11"
    assert len(manager.daily_objectives) == len(initial_daily)
    assert len(manager.weekly_objectives) == len(initial_weekly)

    assert all(target > 0 for target in initial_daily.values())
    assert all(target > 0 for target in initial_weekly.values())
    assert all(":2026-03-10:" in obj.objective_id for obj in manager.daily_objectives)
    assert all(":2026-W11:" in obj.objective_id for obj in manager.weekly_objectives)

    provider.advance(days=1)
    manager.refresh()
    next_daily = {
        objective.objective_type
        for objective in manager.objectives.values()
        if objective.period == "daily"
    }
    assert next_daily
    assert next_daily != set(initial_daily)
    assert manager.last_reset_day_key == "2026-03-11"

    provider.advance(weeks=1)
    manager.refresh()
    next_weekly = {
        objective.objective_type
        for objective in manager.objectives.values()
        if objective.period == "weekly"
    }
    assert next_weekly
    assert next_weekly != set(initial_weekly)
    assert manager.last_reset_week_key == "2026-W12"
