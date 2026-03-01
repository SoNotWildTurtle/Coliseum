"""Tests for auto dev intelligence manager."""

from hololive_coliseum.auto_dev_intelligence_manager import AutoDevIntelligenceManager
from hololive_coliseum.auto_dev_network_manager import AutoDevNetworkManager


def test_intelligence_manager_compiles_signals() -> None:
    manager = AutoDevIntelligenceManager(utilisation_ceiling=50.0)
    monsters = [
        {
            "name": "Lava Vanguard",
            "hazard": "lava",
            "threat": 1.3,
            "elite": True,
            "role": "assault",
            "ai_focus": "aggressive",
            "spawn_synergy": "reinforcement",
        }
    ]
    spawn_plan = {
        "danger": 1.4,
        "group_count": 2,
        "groups": ({"size": 3}, {"size": 2}),
        "interval": 6.0,
        "lanes": ("north", "south"),
        "formation": "onslaught",
        "reinforcement_curve": (6.0, 7.5),
        "tempo": "furious",
    }
    mob_ai = {
        "directives": [
            {
                "monster": "Lava Vanguard",
                "behaviour": "ambush",
                "hazard": "lava",
                "adapts": True,
                "ai_focus": "aggressive",
            }
        ],
        "learning": True,
        "training_modules": ("Lava counter drills",),
    }
    boss_plan = {"name": "Lava Sovereign", "hazard": "lava", "threat": 1.6}
    quests = [
        {
            "title": "Support the forge",
            "trade_skill": "Smithing",
            "objective": "Craft lava shields",
            "supports_boss": False,
            "difficulty": "standard",
            "tags": ("smithing", "lava"),
        },
        {
            "title": "Challenge Lava Sovereign",
            "trade_skill": "Combat",
            "objective": "Defeat the Lava Sovereign in single combat",
            "supports_boss": True,
            "difficulty": "heroic",
            "tags": ("combat", "boss"),
        },
    ]
    research = {
        "utilization_percent": 30.0,
        "latest_sample_percent": 35.0,
        "raw_utilization_percent": 35.0,
        "intelligence_focus": "Analyse arena telemetry",
    }
    guidance = {
        "directives": ("Focus lava counters",),
        "processing_utilization_percent": 35.0,
    }
    evolution = {
        "summary": "Priority high evolution",
        "next_objectives": ("Promote trade skill: Smithing",),
        "processing_utilization_percent": 35.0,
    }
    network_manager = AutoDevNetworkManager()
    network = network_manager.assess_network(
        nodes=[
            {
                "name": "central_relay",
                "role": "relay",
                "latency_ms": 52.0,
                "uptime_ratio": 0.91,
                "trusted": True,
            },
            {
                "name": "south_relay",
                "role": "relay",
                "latency_ms": 74.0,
                "uptime_ratio": 0.89,
                "trusted": False,
            },
            {
                "name": "core_hub",
                "role": "core",
                "latency_ms": 28.0,
                "uptime_ratio": 0.99,
                "trusted": True,
            },
        ],
        bandwidth_samples=[6.5, 8.2, 11.5],
        security_events=[
            {"severity": "high", "type": "void_surge"},
            {"severity": "medium", "type": "priority_throttle"},
        ],
        research=research,
        auto_dev_load=guidance["processing_utilization_percent"],
    )
    summary = manager.synthesise(
        monsters=monsters,
        spawn_plan=spawn_plan,
        mob_ai=mob_ai,
        boss_plan=boss_plan,
        quests=quests,
        research=research,
        guidance=guidance,
        evolution=evolution,
        network=network,
    )
    assert summary["processing_utilization_percent"] == 35.0
    assert summary["raw_processing_percent"] == 35.0
    assert summary["load_state"] in {"balanced", "elevated", "saturated", "critical"}
    assert summary["encounter_alignment"]["hazards"] == ["lava"]
    assert summary["encounter_alignment"]["boss"] == "Lava Sovereign"
    assert summary["quest_alignment"]["quest_count"] == 2
    assert "Focus lava counters" in summary["strategic_directives"]
    blueprint = summary["encounter_blueprint"]
    assert blueprint["boss_synergy"] is True
    assert blueprint["average_group_size"] >= 0.0
    synergy = summary["quest_synergy"]
    assert synergy["boss_supporting_quest"] is True
    assert synergy["trade_skill_focus"] == ["Combat", "Smithing"]
    research = summary["research_utilization"]
    assert research["raw_percent"] == 35.0
    backend = summary["backend_guidance"]
    assert backend["priority"]
    assert backend["action_items"]
    assert backend["directive_count"] >= 1
    assert backend["trade_focus"]
    monster_catalog = summary["monster_catalog"]
    assert monster_catalog["count"] == 1
    assert "lava" in monster_catalog["hazards"]
    assert monster_catalog["elite_count"] == 1
    assert "aggressive" in monster_catalog["ai_focuses"]
    assert "reinforcement" in monster_catalog["spawn_synergies"]
    spawn_overview = summary["spawn_overview"]
    assert spawn_overview["group_count"] >= 2
    assert spawn_overview["total_enemies"] >= 5
    assert spawn_overview["formation"] in {"onslaught", "staggered", "burst"}
    ai_development = summary["mob_ai_development"]
    assert ai_development["directive_count"] == 1
    assert ai_development["hazard_focus"] == "lava"
    assert ai_development["adaptive"] is True
    assert ai_development["training_modules"]
    assert ai_development["ai_focuses"]
    boss_outlook = summary["boss_outlook"]
    assert boss_outlook["name"] == "Lava Sovereign"
    assert boss_outlook["supporting_quests"] >= 1
    quest_matrix = summary["quest_matrix"]
    assert quest_matrix["skills"]["Smithing"] == 1
    assert quest_matrix["skills"]["Combat"] == 1
    mutation = summary["monster_mutation_paths"]
    assert mutation["mutation_ready"] is False
    assert mutation["paths"]
    group_support = summary["group_spawn_support"]
    assert group_support["supporting_quests"] >= 1
    ai_modularity = summary["ai_modularity_map"]
    assert ai_modularity["module_count"] == 1
    alerts = summary["boss_spawn_alerts"]
    assert alerts["hazard"] == "lava"
    dependencies = summary["quest_trade_dependencies"]
    assert "Smithing" in dependencies["skills"]
    benchmarking = summary["research_benchmarking"]
    assert benchmarking["raw_percent"] == 35.0
    guidance_map = summary["managerial_guidance_map"]
    assert guidance_map["recommended_action"]
    actions = summary["self_evolution_actions"]
    assert isinstance(actions, tuple)
    comp = summary["competitive_research_pressure"]
    assert comp["other_games_percent"] >= 0.0
    assert "tracked_games" in comp
    security_overview = summary["network_security_overview"]
    assert security_overview["risk"] in {"low", "medium", "high", "critical"}
    signal_health = summary["holographic_signal_health"]
    assert signal_health["anchor_quality"] >= 0.0
    dashboard = summary["self_evolution_dashboard"]
    assert "pipeline_steps" in dashboard
    assert quest_matrix["quest_total"] == 2
    assert quest_matrix["difficulty_breakdown"]
    assert summary["signals_considered"] >= 7
    mechanics = summary["group_mechanics"]
    assert mechanics["total_enemies"] == 5
    assert mechanics["peak_group_size"] == 3
    assert mechanics["hazard_focus"] == ("lava",)
    assert mechanics["formation"] in {"onslaught", "staggered", "burst"}
    assert mechanics["synergy_breakdown"]
    training = summary["mob_ai_training"]
    assert training["hazards_supported"] == ("lava",)
    assert training["coordination_window"] > 0.0
    assert training["training_focus"] == ()
    assert training["training_modules"]
    boss_pressure = summary["boss_pressure"]
    assert boss_pressure["pressure_rating"] in {"intense", "overwhelming", "manageable"}
    assert boss_pressure["supporting_monster_ratio"] >= 1.0
    quest_dependency = summary["quest_dependency"]
    assert "Combat" in quest_dependency["skills"]
    assert "Combat" in quest_dependency["boss_linked_skills"]
    processing_overview = summary["processing_overview"]
    assert processing_overview["current_percent"] == 35.0
    assert processing_overview["raw_percent"] == 35.0
    assert "primary_source" in processing_overview
    channels = summary["processing_channels"]
    assert channels["channels"]["research"] == 35.0
    assert channels["channels"]["network"] == network["processing_utilization_percent"]
    assert channels["primary"] in {"research", "guidance", "evolution", "network"}
    assert channels["total"] >= channels["channels"]["network"] + channels["channels"]["research"]
    evolution_alignment = summary["evolution_alignment"]
    assert evolution_alignment["guidance_priority"]
    pipeline = summary["orchestration_pipeline"]
    assert pipeline["stages"]
    assert 0.0 <= pipeline["ready_ratio"] <= 1.0
    assert pipeline["next_focus"] in {
        "stabilise",
        "monster_design",
        "group_spawning",
        "mob_ai",
        "boss_selection",
        "quest_generation",
        "research_intelligence",
    }
    playbook = summary["management_playbook"]
    assert playbook["pipeline_focus"] in {
        "stabilise",
        "monster_design",
        "group_spawning",
        "mob_ai",
        "boss_selection",
        "quest_generation",
        "research_intelligence",
    }
    assert "actions" in playbook
    assert playbook["raw_utilization"] == 35.0
    creation = summary["monster_creation"]
    assert creation["creation_load"] in {"stable", "active", "surging"}
    assert creation["peak_threat"] >= 1.3
    spawn_tactics = summary["spawn_tactics"]
    assert spawn_tactics["reinforcement_style"] in {"burst", "wave", "staggered", "onslaught", "incursion"}
    assert spawn_tactics["largest_group_size"] >= 3
    assert spawn_tactics["reinforcement_curve"]
    ai_plan = summary["ai_development_plan"]
    assert ai_plan["iteration_mode"] in {"steady", "continuous", "accelerated"}
    assert "hazards_covered" in ai_plan
    boss_strategy = summary["boss_spawn_strategy"]
    assert boss_strategy["recommended_group"] in {"solo", "party", "raid"}
    assert boss_strategy["interval"] >= 0.0
    assert boss_strategy["strategies"]
    assert boss_strategy["threat"] >= 1.0
    quest_generation = summary["quest_generation"]
    assert quest_generation["quests_available"] == 2
    assert "Combat" in quest_generation["skills_supported"]
    assert quest_generation["difficulty_breakdown"]
    assert quest_generation["tags"]
    competitive = summary["competitive_research"]
    assert competitive["raw_percent"] >= 0.0
    forge = summary["monster_forge"]
    assert forge["status"] in {"idle", "stable", "active", "surging"}
    assert forge["count"] == len(monsters)
    group_detail = summary["group_spawn_mechanics_detail"]
    assert group_detail["groups"] >= spawn_plan["group_count"]
    assert group_detail["pattern"] in {"burst", "laned", "staggered"}
    mob_ai_plan = summary["mob_ai_innovation_plan"]
    assert mob_ai_plan["directive_count"] == 1
    assert mob_ai_plan["iteration_mode"] in {"baseline", "continuous", "accelerated"}
    boss_matrix = summary["boss_spawn_matrix"]
    assert boss_matrix["name"] == boss_plan["name"]
    assert boss_matrix["supporting_quests"] >= 1
    quest_tradecraft = summary["quest_tradecraft"]
    assert "Smithing" in quest_tradecraft["skills"]
    assert quest_tradecraft["boss_support"] >= 1
    research_pressure = summary["research_pressure"]
    assert research_pressure["competitive_raw_percent"] >= 0.0
    managerial_alignment = summary["managerial_alignment"]
    assert managerial_alignment["alignment"] in {"balanced", "divergent", "escalating"}
    group_coord = summary["group_spawn_coordination"]
    assert group_coord["group_count"] >= spawn_plan["group_count"]
    ai_innovation = summary["ai_innovation"]
    assert ai_innovation["directive_count"] == 1
    boss_readiness = summary["boss_spawn_readiness"]
    assert boss_readiness["hazard"] == boss_plan["hazard"]
    quest_alignment = summary["quest_trade_alignment"]
    assert "Smithing" in quest_alignment["skills"]
    automation = summary["network_security_automation"]
    assert automation["automation_score"] == network["security_automation"]["automation_score"]
    assert automation["playbooks"]
    assert automation["automation_tiers"]
    holographic = summary["holographic_transmission"]
    assert holographic["layer_count"] == network["holographic_channels"]["layer_count"]
    assert holographic["encrypted_channels"] is True
    assert holographic["channel_map"]
    assert holographic["channel_map"]["redundancy"] in {"baseline", "elevated"}
    verification_layers = summary["network_verification_layers"]
    assert verification_layers["layers"] == network["verification_layers"]["layers"]
    assert verification_layers["integrity"] in {"stable", "harden", "reinforce"}
    managerial = summary["managerial_overview"]
    assert managerial["raw_processing_percent"] == 35.0
    assert managerial["network_status"] == summary["network_health"]["status"]
    assert isinstance(managerial["relay_needs"], bool)
    assert managerial["security_automation_score"] == automation["automation_score"]
    assert managerial["holographic_anchor_quality"] == holographic["anchor_quality"]
    assert managerial["verification_layers"] == verification_layers["layers"]
    net_health = summary["network_health"]
    assert net_health["score"] >= 0.0
    assert net_health["status"]
    net_security = summary["network_security"]
    assert net_security["risk"] in {"low", "medium", "high", "critical"}
    upgrade = summary["network_upgrade_plan"]
    assert upgrade["relays"] >= 0
    assert isinstance(upgrade["needs_redundancy"], bool)
    assert "Add trusted relay coverage" in network["recommendations"]
    assert "Increase security monitoring" in network["recommendations"]
    net_processing = summary["network_processing"]
    assert net_processing["processing_percent"] == network["processing_utilization_percent"]
    assert net_processing["raw_percent"] == network["raw_processing_percent"]


def test_boss_strategy_populates_defaults_without_hints() -> None:
    manager = AutoDevIntelligenceManager(utilisation_ceiling=40.0)
    boss_plan = {"name": "Aurora Titan", "threat": 1.1}
    spawn_plan = {"interval": 12.0}
    quests = (
        {"objective": "Challenge the Aurora Titan", "title": "Face the Titan"},
    )
    result = manager._boss_spawn_strategy(boss_plan, spawn_plan, quests)
    assert result["strategies"], "Expected fallback strategies when none provided"
    assert "solo_opportunity" in result["strategies"] or "exploit_openings" in result["strategies"]


def test_intelligence_manager_handles_empty_inputs() -> None:
    manager = AutoDevIntelligenceManager()
    assert manager.synthesise() == {}
