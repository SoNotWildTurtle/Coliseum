"""Unit tests for the auto-dev iteration manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_iteration_manager import AutoDevIterationManager


def test_iteration_brief_merges_functionality_and_network_tracks() -> None:
    manager = AutoDevIterationManager()
    brief = manager.iteration_brief(
        functionality={
            "functionality_score": 74.0,
            "functionality_tracks": ("core-loop", "support-loop"),
            "functionality_threads": ("alpha",),
            "managerial_directives": ("stabilise-loop",),
            "risk_index": 28.0,
            "network_requirements": {
                "security_score": 62.0,
                "bandwidth_mbps": 28.0,
                "latency_target_ms": 45.0,
            },
            "holographic_requirements": {
                "recommended_actions": ("phase-trim",),
                "efficiency_score": 72.0,
                "phase_target": 0.82,
            },
        },
        mechanics={
            "novelty_score": 68.0,
            "risk_score": 26.0,
            "gameplay_threads": ("combo-thread",),
            "backend_actions": ("sync-ai",),
        },
        creation={
            "creation_score": 70.0,
            "creation_tracks": ("core-loop",),
            "creation_threads": ("proto-alpha",),
            "creation_actions": ("prototype-upgrade",),
            "risk_profile": {"risk_index": 24.0},
            "network_requirements": {
                "security_score": 63.0,
                "bandwidth_mbps": 30.0,
            },
            "holographic_requirements": {
                "recommended_actions": ("phase-align",),
                "efficiency_score": 71.0,
            },
        },
        blueprint={
            "blueprint_score": 69.0,
            "cohesion_index": 64.0,
            "tracks": ("core-loop",),
            "threads": ("combo-thread",),
            "actions": ("document-blueprint",),
            "network_requirements": {"security_score": 64.0},
            "holographic_requirements": {
                "recommended_actions": ("phase-balance",),
                "efficiency_score": 70.0,
            },
        },
        innovation={"innovation_score": 66.0},
        execution={"execution_threads": ("stabilise",)},
        implementation={"delivery_windows": ("Sprint-3",)},
        network={"network_security": {"security_score": 61.0}},
        network_auto_dev={
            "next_steps": ("Upgrade routers",),
            "processing_focus": {
                "budget_health": "watch",
                "average_bandwidth_mbps": 42.0,
            },
            "holographic_integration": {
                "actions": ("rephase",),
                "efficiency": 0.74,
            },
        },
        security={
            "security_score": 65.0,
            "threat_level": "guarded",
            "network_security_actions": ("audit-firewalls",),
            "holographic_lattice": {"actions": ("lattice-trim",)},
        },
        transmission={
            "spectral_waveform": {"recommended_actions": ("phase-tune",), "efficiency": 73.0},
            "lattice_overlay": {"actions": ("re-align",), "phase_target": 0.8},
            "guardrails": {"follow_up": ("monitor-phase",)},
        },
        research={
            "raw_utilization_percent": 48.0,
            "research_pressure_index": 46.0,
        },
        codebase={
            "iteration_gap_index": 32.0,
            "iteration_alignment_score": 61.0,
            "iteration_focus_modules": ("auto_dev_functionality_manager",),
            "iteration_recommendations": ("auto_dev_functionality_manager: add coverage",),
        },
    )

    assert brief["priority"] in {"accelerate", "amplify", "stabilise", "refine", "observe"}
    assert brief["iteration_score"] >= 0.0
    assert brief["network_requirements"]["security_score"] >= 0.0
    assert brief["holographic_requirements"]["recommended_actions"]
    assert brief["research_implications"]["recommendation"]
    assert brief["security_profile"]["threat_level"]
    assert brief["cycles"]
    assert brief["actions"]
