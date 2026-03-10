"""Smoke tests for the deterministic objective manager."""

from __future__ import annotations

from datetime import datetime, timezone

from hololive_coliseum.objective_manager import ObjectiveManager
from hololive_coliseum.time_provider import FixedTimeProvider


def test_ensure_region_creates_daily_and_weekly_objectives() -> None:
    provider = FixedTimeProvider(datetime(2026, 3, 10, tzinfo=timezone.utc))
    manager = ObjectiveManager(
        time_provider=provider,
        progression_level_provider=lambda: 6,
    )
    manager.ensure_region_objectives(
        {"name": "Glacial Front", "recommended_level": 3, "radius": 2},
        fallback_name="Glacial Front",
    )
    summary = manager.summary(limit=4)
    assert summary
    assert any(objective.period == "daily" for objective in manager.objectives.values())
    assert any(objective.period == "weekly" for objective in manager.objectives.values())


def test_record_event_rewards_only_once() -> None:
    awarded: list[dict[str, int]] = []
    provider = FixedTimeProvider(datetime(2026, 3, 10, tzinfo=timezone.utc))
    manager = ObjectiveManager(
        time_provider=provider,
        reward_sink=lambda reward, objective: awarded.append(dict(reward)),
    )
    manager.ensure_region_objectives({"name": "Arena"})
    objective = next(
        obj
        for obj in manager.objectives.values()
        if obj.objective_type in {"earn_coins", "defeat_enemies", "collect_powerups"}
    )
    event_name = {
        "earn_coins": "coins_earned",
        "defeat_enemies": "enemy_defeated",
        "collect_powerups": "powerup_collected",
    }[objective.objective_type]
    updates = manager.record_event(event_name, objective.target)
    assert updates and updates[0].completed is True
    assert len(awarded) == 1
    manager.record_event(event_name, 1)
    assert len(awarded) == 1


def test_objective_manager_round_trip() -> None:
    provider = FixedTimeProvider(datetime(2026, 3, 10, tzinfo=timezone.utc))
    manager = ObjectiveManager(time_provider=provider)
    manager.ensure_region_objectives({"name": "Frontier"})
    manager.record_event("coins_earned", 5)
    data = manager.to_dict()
    restored = ObjectiveManager(time_provider=provider)
    restored.load_from_dict(data)
    assert restored.region_name == "Frontier"
    assert restored.to_dict() == data


def test_auto_dev_hazard_objective_creation() -> None:
    provider = FixedTimeProvider(datetime(2026, 3, 10, tzinfo=timezone.utc))
    manager = ObjectiveManager(time_provider=provider)
    region = {
        "name": "Inferno Reach",
        "auto_dev": {"hazard_challenge": {"hazard": "lava", "target": 4}},
    }
    manager.ensure_region_objectives(region)
    hazard_obj = manager.objectives.get("hazard_mastery")
    assert hazard_obj is not None
    assert "lava" in hazard_obj.description
