"""Tests for the auto-dev security orchestration manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_security_manager import AutoDevSecurityManager


def test_security_manager_builds_security_brief() -> None:
    manager = AutoDevSecurityManager()
    network = {
        "network_security_score": 62.5,
        "transmission_guardrails": {"status": "reinforce", "severity": "elevated"},
        "anomaly_signals": ("suspicious-traffic",),
        "security_auto_dev": {
            "directive": "fortify",
            "automation_score": 52.0,
            "playbooks": ("Run intrusion triage",),
        },
        "zero_trust_blueprint": {"status": "pilot", "focus": ("identity",)},
        "upgrade_backlog": {"tasks": ("Deploy shield relays",), "priority": "high"},
        "network_security_upgrades": ("Rotate edge certificates",),
        "holographic_diagnostics": {
            "efficiency_score": 74.0,
            "phase_coherence_index": 68.0,
        },
        "holographic_enhancements": {
            "layer_upgrades": ("Spectral lattice", "Prism anchors"),
            "phase_lock_directives": "Stabilise phase drift",
        },
    }
    codebase = {
        "coverage_ratio": 0.72,
        "instability_index": 0.94,
        "module_scorecards": (
            {
                "name": "auto_dev_network_manager",
                "risk_level": "elevated",
                "recommended_actions": ("Add deterministic tests",),
                "stability_modifier": 0.4,
            },
            {
                "name": "auto_dev_pipeline",
                "risk_level": "moderate",
                "recommended_actions": ("Document orchestration flow",),
                "stability_modifier": 0.25,
            },
        ),
    }
    mitigation = {
        "priority": "high",
        "network_tasks": ("Audit guardrail integrity",),
    }
    remediation = {
        "stability_projection": {"projected_security_score": 70.5},
        "codebase_progress": (
            {"name": "auto_dev_network_manager", "addressed": True},
            {"name": "auto_dev_pipeline", "addressed": False},
        ),
        "holographic_adjustments": ("Applied phase corrective",),
    }
    research = {
        "latest_sample_percent": 58.0,
        "trend_direction": "rising",
        "research_pressure_index": 1.3,
    }
    guidance = {
        "governance_outlook": "guidance-oversight",
        "backend_alignment_score": 43.0,
        "priority": "high",
    }

    brief = manager.security_brief(
        network=network,
        codebase=codebase,
        mitigation=mitigation,
        remediation=remediation,
        research=research,
        guidance=guidance,
    )

    assert brief["threat_level"] in {"fortified", "guarded", "elevated", "at-risk"}
    assert brief["automation_directives"]["directive"] == "fortify"
    assert brief["hardening_tasks"]
    assert brief["hardening_tasks"][0]["module"] == "auto_dev_network_manager"
    assert brief["holographic_lattice"]["stability"] in {"stable", "reinforce", "drifting"}
    assert brief["network_security_actions"]
    assert brief["governance_alignment"]["status"] in {"oversight", "escalate", "aligned"}
