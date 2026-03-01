"""Unit tests for the auto-dev blueprint manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_blueprint_manager import AutoDevBlueprintManager


def test_blueprint_brief_blends_creation_and_functionality() -> None:
    manager = AutoDevBlueprintManager()
    brief = manager.blueprint_brief(
        functionality={
            "functionality_score": 72.0,
            "functionality_tracks": ("core-loop", "support-loop"),
            "functionality_threads": ("alpha",),
            "managerial_directives": ("stabilise-loop",),
            "network_requirements": {"security_score": 64.0, "bandwidth_budget_mbps": 28.0},
            "holographic_requirements": {"recommended_actions": ("phase-trim",)},
            "risk_index": 22.0,
        },
        mechanics={
            "novelty_score": 68.0,
            "risk_score": 24.0,
            "functionality_tracks": ("core-loop", "combo-thread"),
            "gameplay_threads": ("combo-thread",),
        },
        creation={
            "creation_score": 70.0,
            "creation_tracks": ("core-loop",),
            "creation_threads": ("proto-alpha",),
            "creation_actions": ("prototype-upgrade",),
            "risk_profile": {"risk_index": 18.0},
            "network_requirements": {"security_score": 63.0, "bandwidth_mbps": 30.0},
            "holographic_requirements": {"recommended_actions": ("phase-align",)},
            "mechanics_expansion_tracks": ("combo-thread",),
            "functionality_extension_tracks": ("core-loop",),
            "supporting_signals": {"modernization_priority": "accelerate"},
        },
        design={
            "creation_tracks": ("core-loop",),
            "prototype_threads": ("proto-alpha",),
            "design_actions": ("document-loop",),
            "network_requirements": {"security_score": 62.0},
            "holographic_requirements": {"recommended_actions": ("phase-balance",)},
        },
        systems={
            "systems_tracks": ("sync-loop",),
            "systems_threads": ("sync-thread",),
            "systems_actions": ("balance-cycle",),
            "network_requirements": {"security_score": 61.0},
            "holographic_requirements": {"recommended_actions": ("phase-lock",)},
        },
        innovation={"innovation_score": 66.0},
        experience={"experience_score": 65.0},
        dynamics={"synergy_score": 63.0, "backend_actions": ("sync-network",)},
        gameplay={
            "functionality_tracks": ("core-loop",),
            "loops": ({"name": "proto-alpha"},),
            "managerial_actions": ("calibrate-loop",),
        },
        research={
            "research_pressure_index": 18.0,
            "trend_direction": "increasing",
            "raw_utilization_percent": 44.0,
        },
        network={"network_security_score": 65.0},
        transmission={
            "spectral_waveform": {"stability": "steady", "recommended_actions": ("rephase",)},
            "phase_alignment": {"target": 0.82, "actions": ("trim-noise",)},
        },
        security={"security_score": 68.0, "threat_level": "guarded"},
        modernization={"priority": "accelerate", "modernization_actions": ("refactor-loop",)},
        optimization={"priority": "stabilise", "optimization_actions": ("tighten-cycle",)},
        governance={"state": "guided", "oversight_actions": ("audit-blueprint",)},
        codebase={
            "blueprint_gap_index": 28.0,
            "blueprint_alignment_score": 62.0,
            "blueprint_focus_modules": ("auto_dev_gameplay_manager",),
            "blueprint_recommendations": ("auto_dev_gameplay_manager: add tests",),
        },
    )

    assert brief["priority"] in {"accelerate", "stabilise", "refine", "survey"}
    assert brief["blueprint_score"] >= 0.0
    assert brief["cohesion_index"] >= 0.0
    assert brief["network_requirements"]["security_score"] >= 60.0
    assert "trim-noise" in brief["holographic_requirements"]["recommended_actions"]
    assert brief["codebase_alignment"]["blueprint_gap_index"] == 28.0
    assert "auto_dev_gameplay_manager" in brief["focus_modules"]
