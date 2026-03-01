"""Tests for auto dev interaction manager."""

from hololive_coliseum.auto_dev_interaction_manager import AutoDevInteractionManager


def test_interaction_manager_compiles_brief() -> None:
    manager = AutoDevInteractionManager()
    brief = manager.interaction_brief(
        functionality={
            "functionality_score": 72.0,
            "risk_index": 26.0,
            "functionality_tracks": ("core-loop", "support-loop"),
            "managerial_directives": ("sync-network",),
            "network_requirements": {
                "security_score": 57.0,
                "bandwidth_mbps": 24.0,
                "upgrade_actions": ("edge-cache",),
            },
            "holographic_requirements": {"recommended_actions": ("phase-tune",)},
        },
        mechanics={
            "novelty_score": 66.0,
            "functionality_tracks": ("combo-chain",),
            "gameplay_threads": ("momentum", "support"),
        },
        gameplay={
            "gameplay_score": 68.0,
            "loops": (
                {
                    "name": "loop-alpha",
                    "experience_thread": "arc-alpha",
                    "focus_track": "core-loop",
                },
            ),
            "managerial_actions": ("reinforce-threads",),
            "network_requirements": {
                "security_score": 58.0,
                "bandwidth_mbps": 26.0,
            },
            "holographic_requirements": {
                "recommended_actions": ("stabilise-phase",),
            },
            "risk_profile": {
                "functionality": 24.0,
                "dynamics": 18.0,
                "playstyle": 16.0,
            },
        },
        dynamics={
            "synergy_score": 64.0,
            "systems_tracks": ("combo-net",),
            "managerial_directives": ("rebalance-ai",),
            "network_requirements": {
                "security_score": 59.0,
                "bandwidth_mbps": 25.0,
                "upgrade_actions": ("optimise-routing",),
            },
            "holographic_requirements": {
                "recommended_actions": ("pulse-align",),
            },
            "risk_profile": {"combined_risk": 21.0},
        },
        innovation={"innovation_score": 63.0},
        experience={
            "experience_score": 65.0,
            "experience_threads": ("arc-alpha",),
            "network_blueprint": {"bandwidth_mbps": 23.0},
        },
        playstyle={
            "playstyle_score": 62.0,
            "tracks": ("aggressive", "support"),
            "managerial_directives": ("monitor-aggro",),
            "network_requirements": {
                "security_score": 56.0,
                "bandwidth_mbps": 24.0,
            },
            "holographic_requirements": {
                "recommended_actions": ("stabilise-holo",),
            },
            "risk_index": 20.0,
        },
        modernization={"modernization_actions": ("refactor-loop",)},
        optimization={"optimization_actions": ("optimise-thread",)},
        resilience={"resilience_score": 70.0},
        integrity={"integrity_score": 66.0},
        security={"security_score": 61.0},
        network={"network_security_score": 60.0},
        network_auto_dev={
            "priority": "accelerate",
            "next_steps": ("deploy-cache",),
            "security_focus": {"harden": ("edge",)},
        },
        transmission={
            "spectral_waveform": {"recommended_actions": ("trim-noise",)},
            "phase_alignment": {"target": 0.82},
        },
        research={
            "research_pressure_index": 14.0,
            "raw_utilization_percent": 48.0,
            "trend_direction": "rising",
        },
        mitigation={"codebase_tasks": ("improve-tests",)},
        remediation={"restoration_actions": ("deploy-hotfix",)},
        codebase={
            "functionality_gap_index": 32.0,
            "functionality_gaps": ("auto_dev_network_manager lacks tests coverage",),
            "mechanics_alignment_score": 74.0,
            "mitigation_plan": ("add regression tests",),
            "modernization_targets": ("auto_dev_network_manager",),
        },
        self_evolution={"readiness_state": "accelerate"},
    )

    assert brief["interaction_score"] >= 0.0
    assert brief["interaction_tracks"]
    assert brief["interaction_threads"]
    assert brief["interaction_actions"]
    assert brief["network_requirements"]["security_score"] >= 0.0
    assert brief["holographic_requirements"]["recommended_actions"]
    assert brief["gap_summary"]["functionality_gap_index"] >= 0.0
    assert brief["research_implications"]["utilization_percent"] >= 0.0
    assert brief["network_synergy"]["next_steps"]
    assert brief["backend_alignment"]["mitigation_focus"]
    assert brief["risk_profile"]["gap_penalty"] >= 0.0
