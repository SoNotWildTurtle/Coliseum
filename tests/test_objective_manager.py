"""Tests for objective manager."""

from hololive_coliseum.objective_manager import ObjectiveManager


def test_ensure_region_creates_objectives():
    manager = ObjectiveManager()
    manager.ensure_region_objectives(
        {"name": "Glacial Front", "recommended_level": 3, "radius": 2},
        fallback_name="Glacial Front",
    )
    summary = manager.summary(limit=4)
    assert summary and "Glacial Front" in summary[0]


def test_record_event_rewards_only_once():
    manager = ObjectiveManager()
    manager.ensure_region_objectives({"name": "Arena"})
    target = manager.objectives["defeat_enemies"].target
    rewards = manager.record_event("enemy_defeated", target)
    assert rewards  # reward granted on completion
    assert not manager.record_event("enemy_defeated", 1)


def test_objective_manager_round_trip():
    manager = ObjectiveManager()
    manager.ensure_region_objectives({"name": "Frontier"})
    manager.record_event("coin_collected", 5)
    data = manager.to_dict()
    restored = ObjectiveManager()
    restored.load_from_dict(data)
    assert restored.region_name == "Frontier"
    assert restored.objectives["collect_coins"].progress == 5


def test_auto_dev_hazard_objective_creation():
    manager = ObjectiveManager()
    region = {
        "name": "Inferno Reach",
        "auto_dev": {"hazard_challenge": {"hazard": "lava", "target": 4}},
    }
    manager.ensure_region_objectives(region)
    hazard_obj = manager.objectives.get("hazard_mastery")
    assert hazard_obj is not None
    assert "lava" in hazard_obj.description
    rewards = manager.record_event("hazard_logged", hazard_obj.target)
    assert rewards
