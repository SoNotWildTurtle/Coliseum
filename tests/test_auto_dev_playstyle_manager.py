"""Tests for auto dev playstyle manager."""

from hololive_coliseum.auto_dev_playstyle_manager import AutoDevPlaystyleManager


def test_playstyle_manager_creates_archetypes() -> None:
    manager = AutoDevPlaystyleManager()
    brief = manager.playstyle_brief(
        functionality={
            "functionality_score": 72.0,
            "risk_index": 28.0,
            "functionality_tracks": ("raid-support", "defence-grid"),
            "managerial_directives": ("stabilise-network",),
            "holographic_requirements": {"recommended_actions": ("phase-tune",)},
        },
        mechanics={
            "novelty_score": 65.0,
            "mechanic_archetypes": ("aerial", "support"),
            "gameplay_threads": ("momentum",),
        },
        innovation={"innovation_score": 62.0},
        experience={
            "experience_score": 68.0,
            "experience_arcs": (("Momentum Surge"),),
            "backend_directives": ("log-metrics",),
            "holographic_choreography": {"actions": ("cascade",), "stability": "steady"},
        },
        dynamics={
            "synergy_score": 64.0,
            "network_requirements": {
                "security_score": 58.0,
                "bandwidth_mbps": 24.0,
                "upgrade_tracks": ("edge-cache",),
            },
            "holographic_requirements": {"recommended_actions": ("re-align",)},
        },
        research={"research_pressure_index": 22.0, "raw_utilization_percent": 45.0},
        network={"network_security_score": 61.0},
        network_auto_dev={
            "upgrade_tracks": ("backbone-harden",),
            "next_steps": ("audit-latency",),
        },
        security={"security_score": 59.0, "threat_level": "guarded"},
        transmission={
            "spectral_waveform": {"recommended_actions": ("phase-trim",)},
            "phase_alignment": {"target": 0.8},
        },
        modernization={"modernization_actions": ("refactor-playstyle",)},
        optimization={"optimization_actions": ("optimise-thread",)},
        integrity={"integrity_score": 66.0, "holographic_actions": ("stabilise-wave",)},
        resilience={"resilience_score": 72.0},
        governance={"oversight_actions": ("document-playstyles",)},
    )

    assert brief["priority"] in {"refine", "stabilise", "accelerate", "amplify"}
    assert brief["archetypes"]
    assert brief["network_requirements"]["security_score"] >= 0.0
    assert brief["holographic_requirements"]["recommended_actions"]
    assert brief["managerial_directives"]
    assert brief["research_implications"]["trend"]
