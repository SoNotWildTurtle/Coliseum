"""Tests for auto dev gameplay manager."""

from hololive_coliseum.auto_dev_gameplay_manager import AutoDevGameplayManager


def test_gameplay_manager_builds_loops() -> None:
    manager = AutoDevGameplayManager()
    blueprint = manager.gameplay_blueprint(
        functionality={
            "functionality_score": 72.0,
            "risk_index": 24.0,
            "functionality_tracks": ("raid-loop", "support-loop"),
            "managerial_directives": ("sustain-network",),
            "holographic_requirements": {"recommended_actions": ("phase-align",)},
        },
        mechanics={
            "novelty_score": 68.0,
            "gameplay_threads": ("momentum", "support"),
        },
        innovation={"innovation_score": 64.0},
        experience={
            "experience_score": 66.0,
            "experience_threads": ("momentum-arc",),
            "network_blueprint": {"bandwidth_mbps": 28.0},
        },
        dynamics={
            "synergy_score": 62.0,
            "systems_tracks": ("synergy-net",),
            "managerial_directives": ("rebalance-ai",),
            "network_requirements": {
                "security_score": 58.0,
                "bandwidth_mbps": 26.0,
            },
            "holographic_requirements": {"recommended_actions": ("pulse-tune",)},
            "risk_profile": {"combined_risk": 18.0},
            "upgrade_actions": ("optimise-routing",),
        },
        playstyle={
            "playstyle_score": 64.0,
            "tracks": ("aggressive", "support"),
            "managerial_directives": ("monitor-aggro",),
            "network_requirements": {
                "security_score": 59.0,
                "bandwidth_mbps": 25.0,
            },
            "holographic_requirements": {"recommended_actions": ("stabilise-phase",)},
            "risk_index": 22.0,
            "archetypes": ({"name": "Sky Dancer"},),
        },
        resilience={"resilience_score": 72.0},
        integrity={"integrity_score": 68.0},
        security={"security_score": 60.0},
        network={"network_security_score": 57.0},
        network_auto_dev={"upgrade_tracks": ("edge-cache",)},
        transmission={
            "spectral_waveform": {"recommended_actions": ("phase-trim",)},
            "phase_alignment": {"target": 0.82},
        },
        research={
            "research_pressure_index": 15.0,
            "raw_utilization_percent": 48.0,
            "trend_direction": "rising",
        },
        modernization={"modernization_actions": ("refactor-loop",)},
        optimization={"optimization_actions": ("optimise-path",)},
        codebase={
            "modernization_targets": ("combat-loop", "ai-loop"),
            "mitigation_plan": ("reduce-latency",),
            "weakness_signals": ("low-test",),
        },
        governance={"oversight_actions": ("document-loops",)},
    )

    assert blueprint["loops"]
    assert blueprint["network_requirements"]["security_score"] >= 0.0
    assert blueprint["holographic_requirements"]["recommended_actions"]
    assert blueprint["managerial_actions"]
    assert blueprint["codebase_alignment"]["modernization_targets"]
    assert blueprint["research_implications"]["pressure_index"] >= 0.0
