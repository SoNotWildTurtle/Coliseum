"""Tests for the extended auto-dev encounter managers."""

from __future__ import annotations

from hololive_coliseum.auto_dev_monster_manager import AutoDevMonsterManager
from hololive_coliseum.auto_dev_spawn_manager import AutoDevSpawnManager
from hololive_coliseum.auto_dev_mob_ai_manager import AutoDevMobAIManager
from hololive_coliseum.auto_dev_boss_manager import AutoDevBossManager
from hololive_coliseum.auto_dev_quest_manager import AutoDevQuestManager
from hololive_coliseum.auto_dev_research_manager import AutoDevResearchManager
from hololive_coliseum.auto_dev_guidance_manager import AutoDevGuidanceManager


def _sample_scenarios() -> list[dict[str, object]]:
    return [
        {"hazard": "lava", "danger_score": 55},
        {"hazard": "poison", "danger_score": 35},
    ]


def test_monster_manager_uses_trade_skills() -> None:
    manager = AutoDevMonsterManager(max_monsters=2)
    monsters = manager.generate_monsters(
        focus={"top_focus": "lava"},
        scenarios=_sample_scenarios(),
        trade_skills=["Alchemy", "Smithing"],
    )
    assert len(monsters) == 2
    assert monsters[0]["hazard"] == "lava"
    assert monsters[0]["weakness"] in {"Alchemy", "Smithing"}
    assert "creation_blueprint" in monsters[0]
    assert monsters[0]["creation_blueprint"]["mutation_track"]
    assert monsters[0]["ai_development_path"]["stages"]


def test_spawn_manager_returns_groups() -> None:
    monsters = [
        {"name": "Lava Vanguard", "threat": 1.0, "hazard": "lava"},
        {"name": "Poison Vanguard", "threat": 0.8, "hazard": "poison"},
    ]
    manager = AutoDevSpawnManager(base_group_size=3)
    plan = manager.plan_groups(monsters, scenarios=_sample_scenarios())
    assert plan["group_count"] == 2
    assert all(group["size"] >= 1 for group in plan["groups"])
    assert plan["cohort_matrix"]
    assert plan["escalation_plan"]["mode"]
    assert plan["group_roles"]


def test_mob_ai_manager_uses_projection_powerups() -> None:
    monsters = [
        {"name": "Lava Vanguard", "hazard": "lava", "threat": 1.2},
    ]
    spawn_plan = {"danger": 1.5}
    projection = {
        "focus": [
            {
                "hazard": "lava",
                "recommended_powerups": ("shield", "resistance"),
                "spawn_multiplier": 0.9,
            }
        ]
    }
    manager = AutoDevMobAIManager()
    directives = manager.ai_directives(monsters, spawn_plan=spawn_plan, projection=projection)
    assert directives["directives"][0]["behaviour"] == "coordinated assaults"
    assert "shield" in directives["directives"][0]["abilities"]
    assert directives["coordination_matrix"]
    assert directives["evolution_threads"]


def test_boss_manager_prefers_focus_hazard() -> None:
    monsters = [
        {"name": "Lava Vanguard", "hazard": "lava"},
        {"name": "Poison Vanguard", "hazard": "poison"},
    ]
    roadmap = {"focus": "poison"}
    manager = AutoDevBossManager()
    spawn_plan = {
        "danger": 1.5,
        "lanes": ("north", "south"),
        "reinforcement_curve": (6.0, 8.0),
        "cohort_matrix": {
            "poison": {"groups": 2, "synergies": ("reinforcement",), "roles": ("vanguard",)},
        },
    }
    boss = manager.select_boss(
        monsters,
        roadmap=roadmap,
        spawn_plan=spawn_plan,
        trade_skills=["Alchemy"],
    )
    assert boss["hazard"] == "poison"
    assert "recommended_counters" in boss
    assert boss["spawn_support"]["lanes"]
    assert boss["phase_transitions"]["mode"]
    assert boss["trade_skill_hooks"]


def test_quest_manager_links_trade_skills_and_boss() -> None:
    manager = AutoDevQuestManager(max_quests=2)
    quests = manager.generate_quests(
        ["Alchemy", "Smithing"],
        boss_plan={"name": "Lava Sovereign", "hazard": "lava"},
        spawn_plan={"danger": 2.0},
    )
    assert any(q["trade_skill"] == "Alchemy" for q in quests)
    assert any(q["title"].startswith("Challenge") for q in quests)
    assert all("spawn_dependency" in q for q in quests)
    assert all("trade_synergy" in q for q in quests)
    assert any(q["support_threads"] for q in quests)


def test_research_manager_reports_average() -> None:
    manager = AutoDevResearchManager(default_percent=10.0)
    manager.record_utilization(30.0, source="auto_dev")
    manager.update_from_intensity(0.25, source="mining")
    manager.record_competitive_research(18.0, game="RealmQuest")
    summary = manager.intelligence_brief()
    assert summary["utilization_percent"] >= 20.0
    assert summary["primary_source"] in {"auto_dev", "mining", "baseline"}
    assert summary["recommendation"]
    assert isinstance(summary["raw_samples"], list)
    assert "latest_sample_percent" in summary
    assert summary["raw_utilization_percent"] == summary["latest_sample_percent"]
    assert summary["raw_percentage"] == summary["latest_sample_percent"]
    competitive = summary["competitive_research"]
    assert competitive["raw_percent"] >= 0.0
    assert "RealmQuest" in competitive["games"]
    assert summary["competitive_raw_percent"] >= 0.0
    assert summary["competitive_share_percent"] >= 0.0
    assert summary["volatility_percent"] >= 0.0
    assert summary["trend_direction"] in {"increasing", "decreasing", "stable"}
    assert summary["research_pressure_index"] >= 0.0
    assert summary["weakness_signals"]
    assert summary["competitive_utilization_percent"] == summary["competitive_raw_percent"]


def test_research_manager_captures_runtime(monkeypatch) -> None:
    manager = AutoDevResearchManager(default_percent=12.0)
    monkeypatch.setattr(manager, "_runtime_percent", lambda: 42.0)
    manager.record_competitive_research(10.0, game="ArenaX")
    captured = manager.capture_runtime_utilization(source="profiling")
    assert captured == 42.0
    summary = manager.intelligence_brief()
    assert summary["latest_sample_percent"] == 42.0
    assert summary["primary_source"] == "profiling"
    assert summary["raw_utilization_percent"] == 42.0
    assert summary["competitive_research"]["raw_percent"] >= 10.0
    assert summary["competitive_raw_percent"] >= 10.0
    assert summary["competitive_share_percent"] >= 0.0


def test_guidance_manager_blends_inputs() -> None:
    manager = AutoDevGuidanceManager()
    monsters = [
        {"name": "Lava Vanguard", "hazard": "lava", "threat": 1.2},
        {"name": "Poison Vanguard", "hazard": "poison", "threat": 0.8},
    ]
    spawn_plan = {"danger": 1.4}
    mob_ai = {"directives": [{"hazard": "lava"}]}
    boss_plan = {"name": "Lava Sovereign", "hazard": "lava"}
    quests = [{"title": "Alchemy support", "trade_skill": "Alchemy"}]
    research = {"utilization_percent": 25.0, "latest_sample_percent": 28.0}
    guidance = manager.compose_guidance(
        monsters=monsters,
        spawn_plan=spawn_plan,
        mob_ai=mob_ai,
        boss_plan=boss_plan,
        quests=quests,
        research=research,
    )
    assert guidance["priority"] in {"medium", "high", "critical", "low"}
    assert guidance["processing_utilization_percent"] == 28.0
    assert guidance["directives"]
    assert guidance["insight_chain"]
    assert "general_intelligence_rating" in guidance
    assert guidance["network_signal"] == 0.0
    assert guidance["managerial_threads"]
    assert "general_intelligence_score" in guidance
    assert guidance["backend_guidance_vector"]
    assert guidance["governance_outlook"]
    assert "pressure_index" in guidance["self_evolution_vector"]
    assert guidance["intelligence_breakdown"]["weights"]
    assert guidance["backend_alignment_score"] >= 0.0
    assert guidance["guidance_backbone"]
