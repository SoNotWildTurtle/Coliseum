"""Tests for auto dev synthesis manager."""

from hololive_coliseum.auto_dev_synthesis_manager import AutoDevSynthesisManager


def test_synthesis_manager_builds_brief() -> None:
    manager = AutoDevSynthesisManager()
    brief = manager.synthesis_brief(
        functionality={
            "functionality_score": 72.0,
            "functionality_tracks": ("core-loop", "support-loop"),
            "functionality_threads": ("burst", "sustain"),
            "managerial_directives": ("reinforce-network",),
            "risk_index": 24.0,
            "network_requirements": {"security_score": 62.0, "bandwidth_mbps": 28.0},
            "holographic_requirements": {"recommended_actions": ("phase-trim",)},
        },
        mechanics={
            "novelty_score": 68.0,
            "risk_score": 26.0,
            "functionality_tracks": ("core-loop", "combo-thread"),
            "network_considerations": {"security_score": 60.0, "bandwidth_mbps": 30.0},
        },
        creation={
            "creation_score": 70.0,
            "creation_tracks": ("core-loop",),
            "creation_threads": ("loop-alpha",),
            "creation_actions": ("prototype-upgrade",),
            "creation_gap_summary": {
                "gap_index": 34.0,
                "focus_modules": ("auto_dev_gameplay_manager",),
                "recommendations": ("auto_dev_gameplay_manager: add unit tests",),
            },
            "risk_profile": {"risk_index": 22.0, "gap_index": 34.0},
            "codebase_alignment": {
                "creation_alignment_score": 62.0,
                "creation_focus_modules": ("auto_dev_gameplay_manager",),
            },
            "network_requirements": {"security_score": 61.0, "bandwidth_mbps": 32.0},
            "holographic_requirements": {"recommended_actions": ("phase-align",)},
            "supporting_signals": {"modernization_priority": "accelerate"},
            "mechanics_synergy_index": 58.0,
            "functionality_extension_index": 64.0,
            "expansion_tracks": ("core-loop", "combo-thread"),
            "mechanics_expansion_tracks": ("combo-thread",),
            "functionality_extension_tracks": ("core-loop",),
        },
        blueprint={
            "blueprint_score": 71.0,
            "gap_index": 32.0,
            "cohesion_index": 68.0,
            "alignment_index": 64.0,
            "tracks": ("core-loop", "combo-thread"),
            "threads": ("loop-alpha", "combo-thread"),
            "actions": ("reinforce-blueprint",),
            "network_requirements": {"security_score": 64.0},
            "holographic_requirements": {"recommended_actions": ("phase-balance",)},
            "supporting_signals": {"modernization_priority": "accelerate"},
            "focus_modules": ("auto_dev_gameplay_manager",),
            "recommendations": ("auto_dev_gameplay_manager: add tests",),
        },
        design={
            "design_score": 71.0,
            "creation_tracks": ("core-loop",),
            "prototype_threads": ("loop-alpha",),
            "design_actions": ("prototype-upgrade",),
            "network_requirements": {"security_score": 60.0},
            "holographic_requirements": {"recommended_actions": ("phase-balance",)},
        },
        systems={
            "systems_score": 69.0,
            "systems_tracks": ("sync-loop",),
            "systems_threads": ("sync-thread",),
            "systems_actions": ("balance-cycle",),
            "network_requirements": {"security_score": 59.0},
            "holographic_requirements": {"recommended_actions": ("phase-lock",)},
        },
        dynamics={
            "synergy_score": 63.0,
            "backend_actions": ("sync-network",),
            "managerial_directives": ("reinforce-combos",),
            "systems_tracks": ("sync-loop",),
            "systems_threads": ("sync-thread",),
        },
        innovation={"innovation_score": 66.0},
        experience={"experience_score": 65.0},
        gameplay={
            "loops": ({"name": "loop-alpha"},),
            "managerial_actions": ("calibrate-loop",),
            "network_requirements": {"security_score": 58.0},
            "holographic_requirements": {"recommended_actions": ("phase-sync",)},
        },
        playstyle={
            "tracks": ("aggressive",),
            "managerial_directives": ("boost-combos",),
            "archetypes": ("burst",),
            "network_requirements": {"security_score": 57.0},
            "holographic_requirements": {"recommended_actions": ("phase-trim",)},
        },
        interaction={
            "interaction_threads": ("combo-thread",),
            "network_requirements": {"security_score": 56.0},
            "holographic_requirements": {"recommended_actions": ("phase-guard",)},
        },
        network={"network_security_score": 63.0},
        network_auto_dev={"network_requirements": {"security_score": 62.0}},
        transmission={
            "phase_alignment": {"target": 0.82, "recommended_actions": ("trim-noise",)},
            "lithographic_integrity": {"score": 75.0},
        },
        security={"security_score": 64.0, "threat_level": "guarded"},
        modernization={"priority": "accelerate", "modernization_actions": ("refactor-loop",)},
        optimization={"priority": "stabilise", "optimization_actions": ("tighten-cycle",)},
        integrity={"priority": "stabilise", "restoration_actions": ("audit-creation",)},
        governance={"oversight_actions": ("audit-creation",)},
        codebase={"creation_alignment_score": 64.0},
        research={"raw_utilization_percent": 44.0, "research_pressure_index": 16.0},
    )

    assert brief["synthesis_score"] >= 0.0
    assert brief["expansion_tracks"]
    assert brief["mechanics_expansion_tracks"]
    assert brief["functionality_extension_tracks"]
    assert brief["expansion_actions"]
    assert brief["network_requirements"]["security_score"] >= 0.0
    assert brief["holographic_requirements"]["recommended_actions"]
    assert brief["alignment_summary"]["mechanics_synergy_index"] >= 0.0
    assert brief["codebase_alignment"]["gap_index"] >= 0.0
    assert brief["blueprint_priority"] in {"accelerate", "stabilise", "refine", "survey"}
    assert brief["blueprint_tracks"]
