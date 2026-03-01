"""Tests for auto dev convergence manager."""

from hololive_coliseum.auto_dev_convergence_manager import AutoDevConvergenceManager


def test_convergence_manager_builds_brief() -> None:
    manager = AutoDevConvergenceManager()
    brief = manager.convergence_brief(
        functionality={
            "functionality_score": 72.0,
            "functionality_tracks": ("core-loop", "support"),
            "functionality_threads": ("burst", "sustain"),
            "risk_index": 28.0,
            "network_requirements": {"security_score": 60.0, "bandwidth_mbps": 24.0},
            "holographic_requirements": {"recommended_actions": ("phase-trim",)},
        },
        mechanics={
            "novelty_score": 68.0,
            "risk_score": 24.0,
            "gameplay_threads": ("burst", "combo"),
            "network_considerations": {"security_score": 62.0, "bandwidth_mbps": 26.0},
            "holographic_requirements": {"recommended_actions": ("phase-align",)},
        },
        creation={
            "creation_score": 70.0,
            "creation_tracks": ("core-loop",),
            "creation_threads": ("loop-alpha",),
            "creation_actions": ("prototype",),
            "creation_gap_summary": {"gap_index": 32.0},
            "risk_profile": {"risk_index": 26.0},
            "network_requirements": {"security_score": 63.0, "bandwidth_mbps": 28.0},
            "holographic_requirements": {"recommended_actions": ("phase-balance",)},
        },
        dynamics={"synergy_score": 64.0, "systems_threads": ("sync",)},
        synthesis={
            "synthesis_score": 66.0,
            "gap_index": 34.0,
            "expansion_tracks": ("core-loop", "combo"),
            "expansion_actions": ("extend-loop",),
            "concept_threads": ("fusion",),
            "network_requirements": {"security_score": 61.0, "bandwidth_mbps": 27.0},
            "holographic_requirements": {"recommended_actions": ("phase-sync",)},
            "alignment_summary": {"functionality_extension_index": 62.0},
        },
        design={"design_score": 69.0, "design_gap_summary": {"focus_index": 38.0}},
        systems={
            "systems_score": 67.0,
            "systems_gap_summary": {"alignment_index": 58.0},
            "systems_threads": ("sync",),
        },
        innovation={"innovation_score": 65.0},
        experience={"experience_score": 64.0},
        gameplay={
            "loops": ({"name": "loop-alpha"},),
            "managerial_actions": ("calibrate",),
            "network_requirements": {"security_score": 59.0},
            "holographic_requirements": {"recommended_actions": ("phase-lock",)},
        },
        interaction={
            "interaction_threads": ("combo",),
            "interaction_actions": ("tighten",),
            "network_requirements": {"security_score": 58.0},
            "holographic_requirements": {"recommended_actions": ("phase-guard",)},
        },
        network={"network_security_score": 64.0},
        network_auto_dev={"network_requirements": {"security_score": 63.0}},
        transmission={
            "phase_alignment": {"target": 0.82, "recommended_actions": ("trim-noise",)},
            "lithographic_integrity": {"score": 74.0},
        },
        security={"security_score": 66.0, "threat_level": "guarded"},
        modernization={"priority": "accelerate", "modernization_actions": ("refactor",)},
        optimization={"priority": "stabilise", "optimization_actions": ("tighten",)},
        integrity={"restoration_actions": ("audit",)},
        governance={"state": "guided"},
        research={"raw_utilization_percent": 42.0, "research_pressure_index": 18.0},
        codebase={
            "convergence_alignment_score": 62.0,
            "convergence_gap_index": 36.0,
            "convergence_focus_modules": ("auto_dev_creation_manager",),
        },
    )

    assert brief["convergence_score"] >= 0.0
    assert brief["priority"] in {"observe", "refine", "stabilise", "accelerate", "amplify"}
    assert brief["convergence_tracks"]
    assert brief["convergence_threads"]
    assert brief["convergence_actions"]
    assert brief["network_requirements"]["security_score"] >= 0.0
    assert brief["holographic_requirements"]["recommended_actions"]
    assert brief["research_implications"]["utilization_percent"] >= 0.0
    assert brief["codebase_alignment"]["convergence_gap_index"] >= 0.0
