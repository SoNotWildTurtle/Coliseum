"""Unit tests for the auto-dev functionality manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_functionality_manager import (
    AutoDevFunctionalityManager,
)


def test_functionality_brief_blends_gameplay_and_backend_signals() -> None:
    manager = AutoDevFunctionalityManager()
    brief = manager.functionality_brief(
        guidance={"managerial_threads": ("backend-lab", "innovation-track")},
        mechanics={
            "novelty_score": 72.0,
            "risk_score": 36.0,
            "functionality_tracks": ("hazard-labs", "network-forges"),
            "gameplay_threads": ("forge-loop", "relay-surge"),
            "mechanic_archetypes": ("lava:adaptive",),
            "holographic_hooks": {
                "recommended_actions": ("Stabilise anchors",),
                "stability": "steady",
            },
        },
        innovation={
            "innovation_score": 64.0,
            "functionality_tracks": ("hazard-labs",),
            "backend_actions": ("Deploy hazard prototype",),
            "feature_concepts": (
                {
                    "track": "hazard-labs",
                    "readiness": "accelerate",
                    "target_module": "auto_dev_pipeline",
                },
            ),
            "holographic_requirements": {
                "recommended_actions": ("Phase sync",),
            },
        },
        experience={
            "experience_score": 62.0,
            "functionality_enhancements": ("Hazard mastery loop",),
            "experience_threads": ("forge-loop",),
            "holographic_choreography": {
                "actions": ("Sustain anchors",),
                "stability": "stable",
            },
            "backend_directives": ("Wire hazard tutorial",),
        },
        modernization={
            "modernization_actions": ("Refactor hazard planner",),
        },
        optimization={
            "optimization_actions": ("Tune waveform cache",),
        },
        integrity={"integrity_score": 82.0},
        resilience={"resilience_score": 68.0},
        research={
            "research_pressure_index": 24.0,
            "trend_direction": "rising",
            "raw_utilization_percent": 48.0,
        },
        network={
            "network_security_score": 72.0,
            "upgrade_paths": ("lattice-upgrade",),
            "transmission_guardrails": {"severity": "monitor"},
            "holographic_diagnostics": {"efficiency_score": 68.0},
        },
        network_auto_dev={
            "upgrade_tracks": ("lattice-upgrade",),
            "next_steps": ("Deploy mesh update",),
            "bandwidth_budget_mbps": 36.0,
        },
        transmission={
            "bandwidth_budget_mbps": 34.0,
            "phase_alignment": {"actions": ("Align relays",)},
            "spectral_waveform": {"stability": "stable"},
        },
        security={"security_score": 74.0, "threat_level": "guarded"},
        governance={"oversight_actions": ("Approve hazard refactor",)},
        continuity={
            "timeline": (
                {"window": "cycle-1", "focus": "stabilise"},
                {"window": "cycle-2"},
            ),
        },
        mitigation={"codebase_tasks": ("Add unit tests",)},
        remediation={
            "restoration_actions": ("Tighten guardrails",),
            "applied_fixes": ("Patched hazard module",),
        },
        codebase={
            "stability_outlook": "steady",
            "modernization_targets": (
                {"name": "auto_dev_network_manager"},
            ),
        },
        self_evolution={"next_actions": ("Activate hazard uplift",)},
    )

    assert brief["priority"] in {"amplify", "accelerate", "stabilise", "refine", "observe"}
    assert brief["functionality_score"] >= 0.0
    assert brief["concept_briefs"]
    assert brief["network_requirements"]["security_score"] >= 0.0
    assert brief["holographic_requirements"]["recommended_actions"]
    assert brief["managerial_directives"]
    assert "cycle-1" in brief["continuity_windows"]
    assert brief["codebase_alignment"]["modernization_targets"]
