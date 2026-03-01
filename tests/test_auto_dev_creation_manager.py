"""Tests for auto dev creation manager."""

from hololive_coliseum.auto_dev_creation_manager import AutoDevCreationManager


def test_creation_manager_produces_blueprint() -> None:
    manager = AutoDevCreationManager()
    blueprint = manager.creation_blueprint(
        functionality={
            "functionality_score": 72.0,
            "functionality_tracks": ("combat-loop", "support-loop"),
            "functionality_threads": ("burst", "sustain"),
            "managerial_directives": ("reinforce-network",),
            "concept_briefs": (
                {
                    "name": "adaptive-surge",
                    "track": "combat",
                    "readiness": "accelerate",
                    "target_module": "gameplay",
                },
            ),
            "network_requirements": {
                "security_score": 62.0,
                "bandwidth_mbps": 28.0,
                "latency_target_ms": 42.0,
                "upgrade_actions": ("deploy-cache",),
            },
            "holographic_requirements": {
                "recommended_actions": ("phase-trim",),
                "efficiency_score": 76.0,
            },
            "continuity_windows": ("sprint-12",),
            "risk_index": 24.0,
        },
        mechanics={"novelty_score": 68.0, "risk_score": 26.0},
        design={
            "design_score": 70.0,
            "creation_tracks": ("core-loop",),
            "prototype_threads": ("loop-alpha",),
            "design_actions": ("prototype-upgrade",),
            "design_gap_summary": {
                "focus_index": 32.0,
                "focus_modules": ("auto_dev_gameplay_manager",),
                "recommendations": ("auto_dev_gameplay_manager: add unit tests",),
            },
            "network_requirements": {"security_score": 60.0},
            "holographic_requirements": {"recommended_actions": ("phase-align",)},
            "risk_profile": {"security_gap": 18.0},
            "creation_windows": ("sprint-13",),
        },
        systems={
            "systems_score": 67.0,
            "systems_tracks": ("sync-loop",),
            "systems_threads": ("sync-thread",),
            "systems_actions": ("balance-cycle",),
            "systems_gap_summary": {
                "alignment_index": 58.0,
                "focus_modules": ("auto_dev_network_manager",),
                "recommendations": ("auto_dev_network_manager: expand tests",),
            },
            "risk_profile": {"security_gap": 22.0},
            "network_requirements": {"security_score": 61.0, "bandwidth_mbps": 30.0},
            "holographic_requirements": {"recommended_actions": ("phase-lock",)},
        },
        innovation={
            "innovation_score": 66.0,
            "functionality_tracks": ("innovation-loop",),
            "feature_concepts": (
                {"name": "holographic-bridge", "track": "support", "readiness": "refine"},
            ),
        },
        experience={
            "experience_score": 65.0,
            "experience_threads": ("experience-arc",),
        },
        interaction={
            "interaction_threads": ("combo-thread",),
            "interaction_actions": ("reinforce-combos",),
            "risk_profile": {"interaction_risk": 21.0},
        },
        gameplay={
            "loops": ({"name": "loop-alpha"},),
            "network_requirements": {"security_score": 59.0},
            "holographic_requirements": {"recommended_actions": ("phase-sync",)},
        },
        playstyle={
            "tracks": ("aggressive",),
            "archetypes": ("burst",),
            "tuning_actions": ("boost-combos",),
            "network_requirements": {"security_score": 58.0},
        },
        dynamics={"risk_profile": {"combined_risk": 20.0}},
        modernization={
            "priority": "accelerate",
            "modernization_actions": ("refactor-loop",),
            "timeline": ({"window": "sprint-11", "focus": "creation"},),
        },
        optimization={
            "priority": "amplify",
            "optimization_actions": ("tighten-cycle",),
            "fix_windows": ("sprint-10",),
        },
        integrity={"priority": "stabilise", "restoration_actions": ("audit-creation",)},
        codebase={
            "creation_alignment_score": 64.0,
            "creation_gap_index": 38.0,
            "creation_focus_modules": (
                "auto_dev_gameplay_manager",
                "auto_dev_network_manager",
            ),
            "creation_recommendations": (
                "auto_dev_network_manager: expand tests",
                "auto_dev_gameplay_manager: add unit tests",
            ),
            "stability_outlook": "improve",
        },
        research={
            "raw_utilization_percent": 44.0,
            "research_pressure_index": 16.0,
            "trend_direction": "rising",
        },
        network={"network_security_score": 63.0},
        transmission={
            "phase_alignment": {"target": 0.82, "recommended_actions": ("trim-noise",)},
            "lithographic_integrity": {"score": 75.0},
        },
        governance={"state": "guided", "oversight_actions": ("audit-creation",)},
    )

    assert blueprint["creation_score"] >= 0.0
    assert blueprint["creation_tracks"]
    assert blueprint["creation_threads"]
    assert blueprint["creation_actions"]
    assert blueprint["network_requirements"]["security_score"] >= 0.0
    assert blueprint["holographic_requirements"]["recommended_actions"]
    assert blueprint["concept_portfolio"]
    assert blueprint["prototype_requirements"]
    assert blueprint["creation_gap_summary"]["gap_index"] >= 0.0
    assert blueprint["codebase_alignment"]["creation_alignment_score"] >= 0.0
    assert blueprint["supporting_signals"]["modernization_priority"] == "accelerate"
    assert blueprint["mechanics_synergy_index"] >= 0.0
    assert blueprint["functionality_extension_index"] >= 0.0
    assert blueprint["mechanics_expansion_tracks"]
    assert blueprint["functionality_extension_tracks"]
    assert blueprint["expansion_tracks"]
