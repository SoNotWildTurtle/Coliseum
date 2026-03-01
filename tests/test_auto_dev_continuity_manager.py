"""Tests for the auto-dev continuity manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_continuity_manager import AutoDevContinuityManager


def test_continuity_plan_highlights_network_playbooks() -> None:
    manager = AutoDevContinuityManager()
    plan = manager.continuity_plan(
        guidance={
            "priority": "high",
            "backend_alignment_score": 0.67,
            "managerial_threads": ("stability", "network-scouts"),
            "governance_outlook": "guidance-oversight",
        },
        network={
            "network_security_score": 58.0,
            "transmission_guardrails": {
                "severity": "elevated",
                "status": "reinforce",
                "actions": ("Lock spectral anchors",),
            },
            "holographic_enhancements": {
                "actions": ("Expand holographic lattice layers",),
                "stability_phase": "adaptive",
            },
            "holographic_diagnostics": {
                "phase_coherence_index": 0.62,
                "efficiency_score": 0.71,
            },
            "lithographic_integrity": {"score": 66.0},
            "security_auto_dev": {
                "directive": "triage",
                "automation_score": 48.0,
            },
            "network_security_upgrades": ("Accelerate zero-trust hardening",),
            "upgrade_backlog": {"priority": "high"},
        },
        codebase={
            "stability_outlook": "volatile",
            "debt_risk_score": 3.4,
            "module_scorecards": (
                {"name": "auto_dev_network_manager", "risk": "high"},
                {"name": "auto_dev_mob_ai_manager", "risk": "moderate"},
            ),
        },
        mitigation={
            "priority": "high",
            "stability_score": 68.0,
            "codebase_tasks": (
                {"task": "Add regression tests", "severity": "high"},
            ),
        },
        remediation={
            "codebase_progress": {
                "addressed": (True, False),
                "addressed_modules": ("auto_dev_network_manager",),
                "outstanding_modules": ("auto_dev_mob_ai_manager",),
            }
        },
        resilience={
            "grade": "resilient",
            "resilience_score": 74.0,
            "resilience_index": 0.74,
            "research_penalty": 0.2,
            "managerial_overwatch": {
                "priority": "medium",
                "governance_outlook": "guidance-monitor",
                "backend_alignment": 0.58,
                "managerial_threads": ("resilience-review",),
            },
        },
    )

    assert len(plan["timeline"]) == 3
    assert 0.0 <= plan["continuity_index"] <= 1.0
    assert plan["continuity_risks"]["network"] in {"critical", "elevated", "managed"}
    assert plan["network_security_playbooks"]
    assert plan["network_security_playbooks"][0]["name"]
    assert plan["holographic_transmission_actions"]["actions"]
    assert plan["managerial_overwatch"]["continuity_index"] == plan["continuity_index"]
    assert plan["codebase_continuity_actions"]["priority_modules"]
