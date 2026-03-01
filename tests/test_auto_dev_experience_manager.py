"""Unit tests for the auto-dev experience manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_experience_manager import AutoDevExperienceManager


def test_experience_brief_extends_functionality_creation() -> None:
    manager = AutoDevExperienceManager()
    brief = manager.experience_brief(
        mechanics={
            "novelty_score": 72.0,
            "cohesion_score": 64.0,
            "risk_score": 28.0,
            "gameplay_threads": ("forge-loop", "relay-surge"),
            "functionality_tracks": ("hazard-labs", "network-forges"),
            "holographic_hooks": {
                "recommended_actions": ("Stabilise anchors",),
                "stability": "steady",
            },
            "mechanic_archetypes": ("lava:adaptive",),
            "managerial_directives": ("link-upgrades",),
        },
        innovation={
            "innovation_score": 66.0,
            "feature_concepts": (
                {
                    "track": "hazard-labs",
                    "readiness": "accelerate",
                    "target_module": "auto_dev_pipeline",
                },
            ),
            "backend_actions": ("Deploy hazard prototype",),
            "network_requirements": {
                "security_score": 70.0,
                "threat_level": "guarded",
                "bandwidth_budget_mbps": 42.0,
            },
            "holographic_requirements": {"recommended_actions": ("Phase sync",)},
            "risk_summary": {
                "mechanics_risk": 28.0,
                "codebase_instability": 0.4,
                "debt_risk_score": 0.6,
                "network_threat_level": "guarded",
            },
            "research_synergy": {"trend": "increasing"},
        },
        guidance={"managerial_threads": ("backend-lab",)},
        research={
            "research_pressure_index": 24.0,
            "raw_utilization_percent": 48.0,
            "competitive_utilization_percent": 12.0,
        },
        network={
            "holographic_diagnostics": {"efficiency_score": 68.0},
            "upgrade_paths": ("lattice-upgrade",),
        },
        transmission={
            "bandwidth_budget_mbps": 36.0,
            "spectral_waveform": {
                "recommended_actions": ("Recalibrate lattice",),
                "stability": "stable",
                "bandwidth_density": 0.48,
            },
            "phase_alignment": {"actions": ("Align relays",)},
        },
        security={"security_score": 72.0, "threat_level": "guarded"},
        resilience={"resilience_index": 0.62, "grade": "steady"},
        modernization={
            "priority": "stabilise",
            "modernization_actions": ("Refactor hazard planner",),
        },
        optimization={
            "priority": "accelerate",
            "optimization_actions": ("Tune waveform cache",),
        },
        mitigation={"codebase_tasks": ("Add tests",)},
        remediation={"restoration_actions": ("Tighten guardrails",)},
        continuity={
            "timeline": (
                {"window": "cycle-1", "focus": "stabilise"},
                {"window": "cycle-2"},
            ),
            "holographic_transmission_actions": {"actions": ("Sustain anchors",)},
            "continuity_index": 0.54,
            "continuity_focus": "stabilise",
        },
        governance={"state": "guided", "oversight_actions": ("Approve hazard refactor",)},
        network_auto_dev={
            "next_steps": ("Deploy mesh update",),
            "upgrade_tracks": ("mesh-upgrade",),
        },
        self_evolution={"next_actions": ("Activate hazard uplift",)},
    )

    assert brief["priority"] in {"amplify", "sustain", "refine", "observe"}
    assert brief["experience_score"] >= 0.0
    assert brief["experience_arcs"]
    assert brief["functionality_enhancements"]
    assert brief["network_blueprint"]["security_score"] >= 0.0
    assert brief["holographic_choreography"]["actions"]
    assert brief["backend_directives"]
    assert brief["risk_profile"]["mechanics_risk"] >= 0.0
    assert brief["research_implications"]["trend"] == "increasing"
    assert "cycle-1" in brief["experience_focus_windows"]
