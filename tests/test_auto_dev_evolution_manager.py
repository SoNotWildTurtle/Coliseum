"""Tests for auto dev evolution manager."""

from hololive_coliseum.auto_dev_evolution_manager import AutoDevEvolutionManager


def test_evolution_brief_collects_signals():
    manager = AutoDevEvolutionManager(horizon=4)
    guidance = {
        "priority": "high",
        "directives": ("Stabilise lava lanes",),
        "processing_utilization_percent": 42.0,
    }
    roadmap = {"priority_actions": ["Fortify lava chokepoints"]}
    focus = {"top_focus": "lava"}
    research = {"latest_sample_percent": 38.5}
    monsters = [{"threat": 1.2}, {"threat": 0.9}]
    spawn_plan = {"danger": 1.2}
    quests = [{"trade_skill": "Lava Forging"}]

    brief = manager.evolution_brief(
        guidance=guidance,
        roadmap=roadmap,
        focus=focus,
        research=research,
        monsters=monsters,
        spawn_plan=spawn_plan,
        quests=quests,
    )

    assert brief["horizon"] == 4
    assert brief["threat_tier"] == "high"
    assert brief["spawn_state"] == "rising"
    assert any("Fortify lava" in obj for obj in brief["next_objectives"])
    assert brief["resource_focus"]["quest_development"] == "active"
    assert brief["processing_utilization_percent"] == 42.0
    assert brief["confidence"] > 0


def test_evolution_brief_handles_missing_data():
    manager = AutoDevEvolutionManager()

    brief = manager.evolution_brief()

    assert brief["threat_tier"] == "low"
    assert brief["processing_utilization_percent"] == 0.0
    assert brief["next_objectives"]
    assert brief["confidence"] == 0.0
