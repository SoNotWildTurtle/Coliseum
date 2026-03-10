"""Tests for objective progress updates, rewards, and telemetry hooks."""

from __future__ import annotations

from datetime import datetime, timezone

from hololive_coliseum.objective_manager import ObjectiveManager
from hololive_coliseum.time_provider import FixedTimeProvider


def test_rewards_are_applied_once_and_events_are_emitted() -> None:
    provider = FixedTimeProvider(datetime(2026, 3, 10, tzinfo=timezone.utc))
    events: list[dict[str, object]] = []
    rewards: list[tuple[str, dict[str, int]]] = []
    manager = ObjectiveManager(
        time_provider=provider,
        reward_sink=lambda reward, objective: rewards.append(
            (objective.objective_id, dict(reward))
        ),
        event_emitter=lambda event: events.append(dict(event)),
    )
    manager.ensure_region_objectives({"name": "Arena"})

    objective = next(
        obj for obj in manager.objectives.values() if obj.objective_type == "defeat_enemies"
    )
    updates = manager.record_event(
        "enemy_defeated",
        objective.target,
        meta={"source": "test"},
    )

    assert len(updates) == 1
    update = updates[0]
    assert update.kind == "defeat_enemies"
    assert update.delta == objective.target
    assert update.completed_now is True
    assert update.progress == objective.target
    assert len(rewards) == 1
    assert rewards[0][0] == objective.objective_id

    manager.record_event("enemy_defeated", 1, meta={"source": "test"})
    assert len(rewards) == 1

    event_types = [str(event.get("type")) for event in events]
    assert "objective_progress" in event_types
    assert "objective_completed" in event_types
    assert "objective_reward" in event_types
