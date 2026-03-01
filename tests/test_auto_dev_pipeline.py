"""Integration tests for the auto-dev orchestration pipeline."""

from __future__ import annotations

from hololive_coliseum.auto_dev_pipeline import AutoDevPipeline


def _scenarios() -> list[dict[str, object]]:
    return [
        {"hazard": "lava", "danger_score": 60},
        {"hazard": "poison", "danger_score": 40},
    ]


def _network_nodes() -> list[dict[str, object]]:
    return [
        {"latency_ms": 72.0, "uptime_ratio": 0.97, "trusted": True},
        {"latency_ms": 95.0, "uptime_ratio": 0.93, "trusted": False},
    ]


def test_pipeline_builds_comprehensive_plan() -> None:
    pipeline = AutoDevPipeline()
    plan = pipeline.build_plan(
        focus={"top_focus": "lava"},
        scenarios=_scenarios(),
        trade_skills=["Alchemy", "Smithing", "Fletching"],
        network_nodes=_network_nodes(),
        bandwidth_samples=[12.5, 16.4, 18.1],
        security_events=[{"severity": "medium", "type": "intrusion_probe"}],
        research_sample=28.0,
        research_intensity=[(0.35, "mining")],
        competitive_games={"RealmQuest": [12.0]},
        runtime_probe=True,
        codebase_snapshot=[
            {
                "name": "auto_dev_spawn_manager",
                "complexity": 14.0,
                "has_tests": True,
                "docstring": True,
                "recent_incidents": [False],
            },
            {
                "name": "auto_dev_network_manager",
                "complexity": 19.0,
                "has_tests": False,
                "docstring": True,
                "recent_incidents": [True, False],
            },
        ],
        test_snapshot=[{"name": "test_auto_dev_pipeline"}],
    )

    assert plan["monsters"]
    assert plan["spawn_plan"]["group_count"] >= 1
    assert plan["mob_ai"]["directives"]
    assert plan["boss_plan"]["hazard"] in {"lava", "poison"}
    assert plan["quests"]
    assert plan["research"]["samples"] >= 1
    assert plan["network"]["security_auto_dev"]["upgrade_paths"]
    assert plan["guidance"]["priority"] in {"low", "medium", "high", "critical"}
    assert plan["processing_utilization_percent"] == plan["guidance"]["processing_utilization_percent"]
    assert plan["processing_utilization_percent"] == plan["research"]["latest_sample_percent"]
    assert plan["managerial_general_intelligence"] == plan["guidance"]["general_intelligence_rating"]
    assert plan["managerial_general_intelligence_score"] == plan["guidance"]["general_intelligence_score"]
    assert plan["backend_guidance_vector"]
    assert plan["holographic_transmission"]["signal_matrix"]
    assert plan["holographic_transmission"]["enhancements"]
    assert plan["holographic_transmission"]["efficiency_score"] >= 0.0
    assert plan["holographic_transmission"]["phase_coherence_index"] >= 0.0
    assert plan["holographic_transmission"]["guardrails"]
    assert plan["holographic_transmission"]["integrity"]
    assert plan["overview"]["network_upgrades"]
    assert plan["weakness_analysis"]["signals"]
    assert plan["research_competitive_utilization_percent"] == plan["research"]["competitive_utilization_percent"]
    assert plan["research_raw_processing_percent"] == plan["research"]["raw_utilization_percent"]
    assert plan["governance_outlook"] == plan["guidance"]["governance_outlook"]
    assert plan["network_security_score"] == plan["network"]["network_security_score"]
    assert plan["codebase_analysis"]["status"] == "analysed"
    assert plan["codebase_analysis"]["coverage_ratio"] < 1.0
    assert plan["weakness_analysis"]["codebase"]["mitigation_plan"]
    assert plan["guidance_breakdown"]["distribution"]
    mitigation = plan["mitigation_plan"]
    assert mitigation["stability_score"] <= 100.0
    assert mitigation["codebase_tasks"]
    assert mitigation["network_tasks"]
    assert mitigation["priority"] in {"monitor", "medium", "high", "critical"}
    assert mitigation["holographic_upgrades"]
    remediation = plan["remediation_actions"]
    assert remediation["applied_fixes"]
    assert remediation["stability_projection"]["projected_security_score"] >= remediation["stability_projection"]["security_score"]
    assert plan["evolution_plan"]["summary"]
    assert plan["evolution_plan"]["processing_utilization_percent"] == plan["processing_utilization_percent"]
    calibration = plan["transmission_calibration"]
    assert calibration["compression_profile"]["algorithm"]
    assert calibration["security_layers"]["recommended_layers"] >= calibration["security_layers"]["active_layers"]
    assert calibration["phase_alignment"]["target"] >= calibration["phase_alignment"]["current"]
    assert calibration["guardrails"]["status"]
    assert calibration["lithographic_integrity"]["score"] >= 0.0
    stability = plan["stability_report"]
    assert stability["projected_security"] >= stability["baseline_security"]
    assert stability["projected_coverage"] >= stability["coverage"]
    assert stability["notes"]
    assert plan["backend_dashboard"]["alignment_score"] == plan["guidance"]["backend_alignment_score"]
    assert plan["codebase_fix_summary"]["stability_outlook"] == plan["codebase_analysis"]["stability_outlook"]
    resilience = plan["resilience_brief"]
    assert 0.0 <= resilience["resilience_index"] <= 1.0
    assert resilience["resilience_actions"]
    assert (
        resilience["network_security_focus"]["security_score"]
        == plan["network"]["network_security_score"]
    )
    intelligence_matrix = plan["managerial_intelligence_matrix"]
    assert intelligence_matrix["resilience_grade"] == resilience["grade"]
    assert (
        intelligence_matrix["network_security_score"]
        == plan["network"]["network_security_score"]
    )
    assert (
        intelligence_matrix["guardrail_status"]
        == resilience["holographic_readiness"]["status"]
    )
    continuity = plan["continuity_plan"]
    assert continuity["timeline"]
    assert plan["network_security_playbooks"]
    assert (
        plan["managerial_intelligence_matrix"]["continuity_index"]
        == continuity["continuity_index"]
    )
    assert plan["holographic_transmission_actions"]["actions"]
    waveform = plan["transmission_calibration"]["spectral_waveform"]
    assert waveform["recommended_actions"]
    security_brief = plan["security_brief"]
    assert security_brief["threat_level"]
    assert security_brief["network_security_actions"]
    assert plan["network_security_actions"] == security_brief["network_security_actions"]
    assert plan["security_threat_level"] == security_brief["threat_level"]
    lattice = plan["holographic_lattice"]
    assert lattice["density"] >= 0.2
    assert lattice["actions"]
    intelligence_matrix = plan["managerial_intelligence_matrix"]
    assert intelligence_matrix["security_projection"]["threat_level"] == plan["security_threat_level"]
    overlay = plan["transmission_calibration"]["lattice_overlay"]
    assert overlay["actions"]
    assert overlay["stability"]
    governance_brief = plan["governance_brief"]
    assert governance_brief["state"]
    assert governance_brief["oversight_actions"]
    assert (
        plan["managerial_intelligence_matrix"]["governance_state"]
        == governance_brief["state"]
    )
    assert plan["codebase_modernization_targets"]
    assert (
        plan["codebase_modernization_targets"]
        == plan["codebase_analysis"]["modernization_targets"]
    )
    blueprint = plan["self_evolution_blueprint"]
    assert blueprint["readiness_state"]
    assert blueprint["upgrade_directives"]
    assert plan["blueprint_brief"]["priority"]
    assert plan["blueprint_priority"] == plan["blueprint_brief"]["priority"]
    assert plan["managerial_intelligence_matrix"]["blueprint_priority"] == plan["blueprint_priority"]
    assert plan["functionality_gap_report"]["blueprint_gap_index"] >= 0.0
    mechanics = plan["mechanics_blueprint"]
    assert mechanics["mechanic_archetypes"]
    assert plan["mechanics_priority"] == mechanics["priority"]
    assert plan["mechanics_functionality_tracks"]
    assert plan["mechanics_gameplay_threads"]
    assert plan["mechanics_holographic_hooks"]["recommended_actions"]
    assert plan["mechanics_network_considerations"]["security_score"]
    mechanics_matrix = plan["managerial_intelligence_matrix"]
    assert mechanics_matrix["mechanics_priority"] == mechanics["priority"]
    assert mechanics_matrix["mechanics_functionality_tracks"]
    assert mechanics_matrix["mechanics_threads"]
    innovation = plan["innovation_brief"]
    assert innovation["feature_concepts"]
    assert plan["innovation_priority"] == innovation["priority"]
    assert plan["innovation_backend_actions"]
    assert plan["innovation_network_requirements"]["security_score"] == innovation[
        "network_requirements"
    ]["security_score"]
    assert plan["innovation_research_synergy"]["trend"]
    assert plan["innovation_gameplay_inspirations"]
    innovation_matrix = plan["managerial_intelligence_matrix"]
    assert innovation_matrix["innovation_priority"] == innovation["priority"]
    assert innovation_matrix["innovation_tracks"]
    assert innovation_matrix["innovation_backend_actions"]
    experience = plan["experience_brief"]
    assert experience["experience_arcs"]
    assert plan["experience_priority"] == experience["priority"]
    assert plan["experience_functionality_enhancements"]
    assert (
        plan["experience_network_blueprint"]["security_score"]
        == experience["network_blueprint"]["security_score"]
    )
    assert plan["experience_holographic_choreography"]["actions"]
    assert plan["experience_backend_directives"]
    assert plan["experience_research_implications"]["trend"]
    experience_matrix = plan["managerial_intelligence_matrix"]
    assert experience_matrix["experience_priority"] == experience["priority"]
    assert (
        experience_matrix["experience_enhancements"]
        == tuple(experience["functionality_enhancements"])
    )
    assert experience_matrix["experience_threads"]
    functionality = plan["functionality_brief"]
    assert functionality["concept_briefs"]
    assert plan["functionality_priority"] == functionality["priority"]
    assert plan["functionality_threads"]
    assert (
        plan["functionality_network_requirements"]["security_score"]
        == functionality["network_requirements"]["security_score"]
    )
    assert plan["functionality_backend_directives"]
    assert plan["functionality_research_implications"]["pressure_index"] >= 0.0
    assert plan["functionality_codebase_alignment"]["modernization_targets"]
    functionality_matrix = plan["managerial_intelligence_matrix"]
    assert (
        functionality_matrix["functionality_priority"]
        == functionality["priority"]
    )
    assert functionality_matrix["functionality_tracks"]
    assert functionality_matrix["functionality_directives"]
    dynamics = plan["dynamics_brief"]
    assert dynamics["systems_threads"]
    assert plan["dynamics_priority"] == dynamics["priority"]
    assert plan["dynamics_synergy_score"] == dynamics["synergy_score"]
    assert plan["dynamics_network_requirements"]["security_score"] >= 0.0
    assert plan["dynamics_holographic_requirements"]["recommended_actions"]
    assert plan["dynamics_backend_actions"]
    assert plan["dynamics_managerial_directives"]
    dynamics_matrix = plan["managerial_intelligence_matrix"]
    assert dynamics_matrix["dynamics_priority"] == dynamics["priority"]
    assert dynamics_matrix["dynamics_systems_tracks"]
    assert dynamics_matrix["dynamics_backend_actions"]
    playstyle = plan["playstyle_brief"]
    assert playstyle["archetypes"]
    assert plan["playstyle_priority"] == playstyle["priority"]
    assert plan["playstyle_network_requirements"]["security_score"] >= 0.0
    assert plan["playstyle_holographic_requirements"]["recommended_actions"]
    assert plan["playstyle_managerial_directives"]
    assert plan["playstyle_tracks"]
    assert plan["playstyle_risk_index"] >= 0.0
    gameplay = plan["gameplay_blueprint"]
    assert gameplay["loops"]
    assert plan["gameplay_priority"] == gameplay["priority"]
    assert plan["gameplay_network_requirements"]["security_score"] >= 0.0
    assert plan["gameplay_holographic_requirements"]["recommended_actions"]
    assert plan["gameplay_actions"]
    assert plan["gameplay_codebase_alignment"]["modernization_targets"]
    assert plan["gameplay_research_implications"]["pressure_index"] >= 0.0
    interaction = plan["interaction_brief"]
    assert interaction["interaction_score"] >= 0.0
    assert interaction["interaction_tracks"]
    assert plan["interaction_priority"] == interaction["priority"]
    assert plan["interaction_network_requirements"]["security_score"] >= 0.0
    assert plan["interaction_holographic_requirements"]["recommended_actions"]
    assert plan["interaction_gap_summary"]["functionality_gap_index"] >= 0.0
    assert plan["interaction_codebase_alignment"]["functionality_gaps"]
    assert plan["interaction_network_synergy"]["next_steps"]
    assert plan["interaction_backend_alignment"]["mitigation_focus"]
    gap_report = plan["functionality_gap_report"]
    assert gap_report["recommended_fixes"]
    assert gap_report["synergy_gap"] >= 0.0
    assert gap_report["design_focus_index"] >= 0.0
    assert gap_report["design_focus_modules"]
    assert gap_report["creation_gap_index"] >= 0.0
    assert gap_report["creation_focus_modules"]
    assert gap_report["creation_recommendations"]
    assert gap_report["synthesis_gap_index"] >= 0.0
    assert gap_report["synthesis_tracks"]
    assert gap_report["synthesis_actions"]
    assert gap_report["convergence_gap_index"] >= 0.0
    assert gap_report["convergence_tracks"]
    assert gap_report["convergence_actions"]
    assert gap_report["implementation_gap_index"] >= 0.0
    assert gap_report["implementation_tracks"]
    assert gap_report["implementation_delivery_windows"]
    assert gap_report["execution_gap_index"] >= 0.0
    assert gap_report["execution_actions"]
    assert gap_report["execution_windows"]
    playstyle_matrix = plan["managerial_intelligence_matrix"]
    assert playstyle_matrix["playstyle_priority"] == playstyle["priority"]
    assert playstyle_matrix["playstyle_directives"]
    assert playstyle_matrix["playstyle_archetypes"]
    gameplay_matrix = plan["managerial_intelligence_matrix"]
    assert gameplay_matrix["gameplay_priority"] == gameplay["priority"]
    assert gameplay_matrix["gameplay_actions"]
    assert gameplay_matrix["gameplay_loops"]
    assert gameplay_matrix["gameplay_codebase_alignment"]["modernization_targets"]
    interaction_matrix = plan["managerial_intelligence_matrix"]
    assert interaction_matrix["interaction_priority"] == interaction["priority"]
    assert interaction_matrix["interaction_tracks"]
    assert interaction_matrix["interaction_actions"]
    assert interaction_matrix["interaction_gap_index"] >= 0.0
    design = plan["design_blueprint"]
    assert design["creation_tracks"]
    assert design["prototype_threads"]
    assert plan["design_priority"] == design["priority"]
    assert plan["design_network_requirements"]["security_score"] >= 0.0
    assert plan["design_holographic_requirements"]["recommended_actions"]
    assert plan["design_codebase_alignment"]["design_focus_modules"]
    assert plan["design_gap_summary"]["focus_index"] == design["design_gap_summary"]["focus_index"]
    assert plan["design_risk_profile"]["security_gap"] >= 0.0
    design_matrix = plan["managerial_intelligence_matrix"]
    assert design_matrix["design_priority"] == design["priority"]
    assert design_matrix["design_tracks"]
    assert design_matrix["design_actions"]
    assert design_matrix["design_focus_index"] == design["design_gap_summary"]["focus_index"]
    creation = plan["creation_blueprint"]
    assert creation["creation_tracks"]
    assert creation["creation_threads"]
    assert plan["creation_priority"] == creation["priority"]
    assert plan["creation_network_requirements"]["security_score"] >= 0.0
    assert plan["creation_holographic_requirements"]["recommended_actions"]
    assert plan["creation_concept_portfolio"]
    assert plan["creation_prototype_requirements"]
    assert plan["creation_gap_summary"]["gap_index"] == creation["creation_gap_summary"]["gap_index"]
    assert plan["creation_risk_profile"]["risk_index"] >= 0.0
    assert plan["creation_mechanics_synergy_index"] == creation["mechanics_synergy_index"]
    assert plan["creation_functionality_extension_index"] == creation[
        "functionality_extension_index"
    ]
    assert plan["creation_expansion_tracks"]
    assert plan["creation_mechanics_expansion_tracks"]
    assert plan["creation_functionality_extension_tracks"]
    iteration = plan["iteration_brief"]
    assert iteration["cycles"]
    assert plan["iteration_priority"] == iteration["priority"]
    assert plan["iteration_network_requirements"]["security_score"] >= 0.0
    assert plan["iteration_holographic_requirements"]["recommended_actions"]
    assert plan["iteration_research_implications"]["utilization_percent"] >= 0.0
    assert plan["iteration_security_profile"]["threat_level"]
    synthesis = plan["synthesis_brief"]
    assert synthesis["synthesis_score"] >= 0.0
    assert plan["synthesis_priority"] == synthesis["priority"]
    assert plan["synthesis_tracks"]
    assert plan["synthesis_actions"]
    assert plan["synthesis_network_requirements"]["security_score"] >= 0.0
    assert plan["synthesis_holographic_requirements"]["recommended_actions"]
    assert plan["synthesis_research_implications"]["utilization_percent"] >= 0.0
    assert plan["synthesis_concept_threads"]
    assert plan["synthesis_codebase_alignment"]["gap_index"] >= 0.0
    convergence = plan["convergence_brief"]
    assert convergence["convergence_score"] >= 0.0
    assert plan["convergence_priority"] == convergence["priority"]
    assert plan["convergence_tracks"]
    assert plan["convergence_threads"]
    assert plan["convergence_actions"]
    assert plan["convergence_network_requirements"]["security_score"] >= 0.0
    assert plan["convergence_holographic_requirements"]["recommended_actions"]
    assert plan["convergence_research_implications"]["utilization_percent"] >= 0.0
    assert plan["convergence_codebase_alignment"]["convergence_gap_index"] >= 0.0
    implementation = plan["implementation_brief"]
    assert implementation["implementation_tracks"]
    assert implementation["implementation_actions"]
    assert plan["implementation_priority"] == implementation["priority"]
    assert plan["implementation_tracks"] == implementation["implementation_tracks"]
    assert plan["implementation_network_requirements"]["security_score"] >= 0.0
    assert plan["implementation_holographic_actions"]
    assert plan["implementation_research_implications"]["utilization_percent"] >= 0.0
    assert plan["implementation_managerial_directives"]
    iteration = plan["iteration_brief"]
    assert iteration["actions"]
    execution = plan["execution_brief"]
    assert execution["execution_tracks"]
    assert execution["execution_actions"]
    assert plan["execution_priority"] == execution["priority"]
    assert plan["execution_network_requirements"]["security_score"] == execution[
        "network_requirements"
    ]["security_score"]
    assert plan["execution_holographic_actions"]
    assert plan["execution_stability_index"] == execution["execution_stability_index"]
    creation_matrix = plan["managerial_intelligence_matrix"]
    assert creation_matrix["creation_priority"] == creation["priority"]
    assert creation_matrix["creation_tracks"]
    assert creation_matrix["creation_actions"]
    assert creation_matrix["creation_gap_index"] == creation["creation_gap_summary"]["gap_index"]
    assert creation_matrix["creation_mechanics_synergy_index"] == creation[
        "mechanics_synergy_index"
    ]
    assert creation_matrix["creation_functionality_extension_index"] == creation[
        "functionality_extension_index"
    ]
    assert creation_matrix["creation_expansion_tracks"] == tuple(
        creation.get("expansion_tracks", ())
    )
    assert creation_matrix["iteration_priority"] == iteration["priority"]
    assert creation_matrix["iteration_cycles"]
    assert creation_matrix["iteration_actions"]
    assert creation_matrix["iteration_network_requirements"]["security_score"] >= 0.0
    assert creation_matrix["iteration_holographic_actions"]
    assert (
        creation_matrix["iteration_research_implications"]["utilization_percent"]
        >= 0.0
    )
    assert creation_matrix["synthesis_priority"] == synthesis["priority"]
    assert creation_matrix["synthesis_tracks"]
    assert creation_matrix["synthesis_actions"]
    assert creation_matrix["synthesis_gap_index"] == synthesis["gap_index"]
    assert creation_matrix["synthesis_alignment_index"] >= 0.0
    assert creation_matrix["synthesis_network_requirements"]["security_score"] >= 0.0
    assert creation_matrix["synthesis_holographic_actions"]
    assert creation_matrix["synthesis_research_implications"]["utilization_percent"] >= 0.0
    assert creation_matrix["convergence_priority"] == convergence["priority"]
    assert creation_matrix["convergence_tracks"]
    assert creation_matrix["convergence_actions"]
    assert creation_matrix["convergence_gap_index"] == convergence["gap_index"]
    assert creation_matrix["convergence_network_requirements"]["security_score"] >= 0.0
    assert creation_matrix["convergence_holographic_actions"]
    assert (
        creation_matrix["convergence_research_implications"]["utilization_percent"]
        >= 0.0
    )
    assert creation_matrix["implementation_priority"] == implementation["priority"]
    assert creation_matrix["implementation_tracks"] == implementation["implementation_tracks"]
    assert creation_matrix["implementation_backlog"]
    assert creation_matrix["execution_priority"] == execution["priority"]
    assert creation_matrix["execution_actions"]
    assert (
        creation_matrix["execution_network_requirements"]["security_score"]
        == execution["network_requirements"]["security_score"]
    )
    assert creation_matrix["execution_holographic_actions"]
    gap_report = plan["functionality_gap_report"]
    assert gap_report["iteration_gap_index"] >= 0.0
    assert gap_report["iteration_cycles"]
    assert gap_report["iteration_actions"]
    systems = plan["systems_blueprint"]
    assert systems["systems_tracks"]
    assert systems["systems_actions"]
    assert plan["systems_priority"] == systems["priority"]
    assert plan["systems_network_requirements"]["security_score"] >= 0.0
    assert plan["systems_holographic_requirements"]["recommended_actions"]
    assert plan["systems_codebase_alignment"]["systems_focus_modules"]
    assert plan["systems_gap_summary"]["alignment_index"] == systems["systems_gap_summary"]["alignment_index"]
    assert plan["systems_architecture_overview"]["network_status"]
    systems_matrix = plan["managerial_intelligence_matrix"]
    assert systems_matrix["systems_priority"] == systems["priority"]
    assert systems_matrix["systems_tracks"]
    assert systems_matrix["systems_actions"]
    assert systems_matrix["systems_alignment_index"] == systems["systems_gap_summary"]["alignment_index"]
    assert systems_matrix["systems_network_requirements"]["security_score"] >= 0.0
    assert systems_matrix["systems_holographic_actions"]
    assert blueprint["holographic_directives"]
    assert blueprint["codebase_focus"]["mitigation_plan"]
    assert blueprint["research_focus"]["utilization_percent"] == plan["research"]["raw_utilization_percent"]
    assert (
        plan["managerial_intelligence_matrix"]["self_evolution_state"]
        == blueprint["readiness_state"]
    )
    assert (
        plan["managerial_intelligence_matrix"]["self_evolution_actions"]
        == blueprint["next_actions"]
    )
    network_auto_dev = plan["network_auto_dev_plan"]
    assert network_auto_dev["priority"]
    assert network_auto_dev["upgrade_tracks"]
    assert network_auto_dev["holographic_integration"]["actions"]
    assert plan["network_auto_dev_actions"] == network_auto_dev["next_steps"]
    assert (
        plan["managerial_intelligence_matrix"]["network_upgrade_priority"]
        == network_auto_dev["priority"]
    )
    modernization = plan["modernization_brief"]
    assert modernization["priority"] in {"monitor", "stabilise", "accelerate"}
    assert plan["modernization_actions"]
    assert plan["codebase_weakness_resolutions"]
    assert plan["modernization_timeline"]
    assert modernization["network_alignment"]["alignment"] in {
        "balanced",
        "requires-hardening",
        "upgrade-ready",
    }
    assert (
        plan["managerial_intelligence_matrix"]["modernization_priority"]
        == modernization["priority"]
    )
    assert (
        plan["managerial_intelligence_matrix"]["modernization_alignment"]
        == modernization["network_alignment"]["alignment"]
    )
    optimization = plan["optimization_brief"]
    assert optimization["priority"] in {"monitor", "stabilise", "accelerate"}
    assert plan["optimization_actions"]
    assert plan["optimization_priority"] == optimization["priority"]
    assert plan["optimization_fix_windows"]
    assert (
        plan["managerial_intelligence_matrix"]["optimization_priority"]
        == optimization["priority"]
    )
    assert plan["managerial_intelligence_matrix"]["optimization_focus"]
    assert (
        plan["managerial_intelligence_matrix"]["optimization_actions"]
        == tuple(optimization["optimization_actions"])
    )
    integrity = plan["integrity_report"]
    assert integrity["integrity_score"] == plan["integrity_score"]
    assert integrity["priority"] == plan["integrity_priority"]
    assert plan["integrity_restoration_actions"]
    assert plan["holographic_integrity_actions"]
    assert plan["network_hardening_actions"]
    assert (
        plan["managerial_intelligence_matrix"]["integrity_priority"]
        == integrity["priority"]
    )
    assert (
        plan["managerial_intelligence_matrix"]["integrity_score"]
        == integrity["integrity_score"]
    )
    assert (
        plan["managerial_intelligence_matrix"]["integrity_actions"]
        == tuple(integrity["restoration_actions"])
    )
    assert (
        plan["managerial_intelligence_matrix"]["integrity_phase_delta"]
        == integrity["phase_delta"]
    )

