"""Tests for objective export/import and profile persistence round-trips."""

from __future__ import annotations

from datetime import datetime, timezone

from hololive_coliseum.objective_manager import ObjectiveManager
from hololive_coliseum.profile_store import ProfileStore, default_profile
from hololive_coliseum.time_provider import FixedTimeProvider


def test_objective_state_round_trips_through_export_and_profile_store(tmp_path) -> None:
    provider = FixedTimeProvider(datetime(2026, 3, 10, tzinfo=timezone.utc))
    manager = ObjectiveManager(
        time_provider=provider,
        progression_level_provider=lambda: 9,
    )
    manager.ensure_region_objectives(
        {"name": "Verdant Span", "recommended_level": 5, "radius": 2}
    )
    daily = next(obj for obj in manager.objectives.values() if obj.period == "daily")
    event_name = {
        "defeat_enemies": "enemy_defeated",
        "collect_powerups": "powerup_collected",
        "earn_coins": "coins_earned",
        "deal_damage": "damage_dealt",
    }[daily.objective_type]
    manager.record_event(event_name, max(1, min(daily.target, 3)))

    exported = manager.export_state()
    assert exported["daily_objectives"]
    assert exported["weekly_objectives"]
    assert exported["last_daily_key"] == "2026-03-10"
    assert exported["last_weekly_key"] == "2026-W11"
    restored = ObjectiveManager(time_provider=provider)
    restored.import_state(exported)
    assert restored.export_state() == exported

    store = ProfileStore(load_root=tmp_path / "profiles")
    profile = default_profile("objectives")
    profile["data"]["objectives"] = exported
    store.save("objectives", profile)

    loaded, _warnings = store.load("objectives")
    rehydrated = ObjectiveManager(time_provider=provider)
    rehydrated.import_state(loaded["data"]["objectives"])
    assert rehydrated.export_state() == exported
