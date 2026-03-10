"""Tests for daily completion streak behavior."""

from __future__ import annotations

from datetime import datetime, timezone

from hololive_coliseum.objective_manager import ObjectiveManager, Objective
from hololive_coliseum.time_provider import FixedTimeProvider


def _complete_daily(manager: ObjectiveManager) -> Objective:
    daily = next(obj for obj in manager.objectives.values() if obj.period == "daily")
    event_name = {
        "defeat_enemies": "enemy_defeated",
        "collect_powerups": "powerup_collected",
        "earn_coins": "coins_earned",
        "deal_damage": "damage_dealt",
    }[daily.objective_type]
    manager.record_event(event_name, daily.target, meta={"source": "test"})
    return daily


def test_daily_streak_increments_and_resets_after_missed_day() -> None:
    provider = FixedTimeProvider(datetime(2026, 3, 10, tzinfo=timezone.utc))
    rewards: list[dict[str, int]] = []
    manager = ObjectiveManager(
        time_provider=provider,
        reward_sink=lambda reward, objective: rewards.append(dict(reward)),
    )
    manager.ensure_region_objectives({"name": "Arena"})

    first = _complete_daily(manager)
    assert first.completed is True
    assert manager.daily_streak == 1

    provider.advance(days=1)
    manager.refresh()
    second = _complete_daily(manager)
    assert second.completed is True
    assert manager.daily_streak == 2

    provider.advance(days=2)
    manager.refresh()
    assert manager.daily_streak == 0
    third = _complete_daily(manager)
    assert third.completed is True
    assert manager.daily_streak == 1
    assert len(rewards) >= 3
