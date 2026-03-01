"""Unit tests for the auto-dev dynamics manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_dynamics_manager import AutoDevDynamicsManager


def test_dynamics_brief_blends_functionality_mechanics_and_network() -> None:
    manager = AutoDevDynamicsManager()
    brief = manager.dynamics_brief(
        guidance={"managerial_threads": ("forge-guidance",)},
        functionality={
            "functionality_score": 72.0,
            "functionality_tracks": ("forge-lines", "mesh-labs"),
            "functionality_threads": ("forge-loop", "mesh-sync"),
            "network_requirements": {
                "security_score": 62.0,
                "bandwidth_mbps": 18.0,
                "upgrade_tracks": ("forge-lines",),
                "guardrail_severity": "monitor",
            },
            "holographic_requirements": {
                "recommended_actions": ("Stabilise forge anchors",),
                "stability": "steady",
            },
            "managerial_directives": ("Align forge control",),
            "risk_index": 32.0,
        },
        mechanics={
            "novelty_score": 68.0,
            "risk_score": 28.0,
            "functionality_tracks": ("forge-lines", "relay-grid"),
            "gameplay_threads": ("mesh-sync", "relay-surge"),
            "holographic_hooks": {
                "recommended_actions": ("Recalibrate relays",),
                "efficiency_score": 64.0,
                "stability": "stable",
            },
        },
        innovation={
            "innovation_score": 66.0,
            "functionality_tracks": ("mesh-labs",),
            "network_requirements": {"security_score": 64.0, "bandwidth_mbps": 22.0},
            "holographic_requirements": {"recommended_actions": ("Phase-lock mesh",)},
            "backend_actions": ("Prototype mesh directive",),
        },
        experience={
            "experience_score": 61.0,
            "experience_threads": ("relay-surge",),
            "holographic_choreography": {
                "actions": ("Maintain spectral weave",),
                "efficiency_score": 60.0,
            },
            "backend_directives": ("Surface mesh tutorial",),
            "network_blueprint": {"security_score": 60.0, "bandwidth_mbps": 16.0},
        },
        modernization={
            "modernization_actions": ("Refine mesh pipeline",),
            "modernization_targets": ({"name": "auto_dev_mesh_module"},),
        },
        optimization={"optimization_actions": ("Compress mesh cache",)},
        integrity={"integrity_score": 74.0, "holographic_actions": ("Reinforce mesh lattice",)},
        resilience={"resilience_score": 69.0},
        security={"security_score": 76.0, "threat_level": "guarded"},
        network={
            "network_security_score": 70.0,
            "transmission_guardrails": {"severity": "monitor"},
        },
        network_auto_dev={
            "upgrade_tracks": ("mesh-grid",),
            "next_steps": ("Deploy mesh firmware",),
            "bandwidth_budget_mbps": 24.0,
            "readiness_score": 68.0,
        },
        transmission={
            "bandwidth_budget_mbps": 26.0,
            "guardrails": {"severity": "monitor"},
            "phase_alignment": {"target": 0.72},
            "spectral_waveform": {"efficiency_score": 65.0},
        },
        research={"research_pressure_index": 22.0},
        governance={"oversight_actions": ("Authorise mesh uplift",)},
        continuity={"timeline": ({"window": "cycle-alpha"}, {"window": "cycle-beta"})},
        mitigation={"codebase_tasks": ("Audit mesh tests",)},
        remediation={
            "holographic_adjustments": ("Retune mesh resonance",),
            "codebase_progress": ({"name": "auto_dev_mesh_module", "addressed": True},),
        },
        codebase={"stability_outlook": "steady"},
        self_evolution={"next_actions": ("Broaden mesh heuristics",)},
    )

    assert brief["priority"] in {"observe", "refine", "stabilise", "accelerate", "amplify"}
    assert brief["synergy_score"] >= 0.0
    assert brief["systems_tracks"]
    assert brief["systems_threads"]
    assert brief["network_requirements"]["security_score"] >= 0.0
    assert brief["network_requirements"]["bandwidth_mbps"] >= 0.0
    assert brief["holographic_requirements"]["recommended_actions"]
    assert brief["backend_actions"]
    assert brief["managerial_directives"]
    assert brief["risk_profile"]["combined_risk"] >= 0.0
    assert "cycle-alpha" in brief["continuity_windows"]
    assert brief["upgrade_actions"]
