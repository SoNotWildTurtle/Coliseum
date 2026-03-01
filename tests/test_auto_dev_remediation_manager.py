"""Tests for the auto-dev remediation manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_remediation_manager import AutoDevRemediationManager


def test_remediation_manager_applies_high_priority_tasks() -> None:
    manager = AutoDevRemediationManager(codebase_throughput=1, network_throughput=1)
    mitigation = {
        "codebase_tasks": (
            {
                "task": "Expand automated test coverage for critical auto-dev modules",
                "owner": "Platform Core",
                "severity": "high",
            },
            {
                "task": "Refactor legacy holographic coordinator",
                "owner": "Platform Core",
                "severity": "medium",
            },
        ),
        "network_tasks": (
            "Enforce fortify network hardening playbook",
            "Execute upgrade path: Deploy quantum uplink",
        ),
        "research_tasks": (
            "Throttle research jobs to relieve processing pressure",
            "Maintain current research cadence with monitoring",
        ),
        "intelligence_tasks": (
            "Prioritise counters for lava threats",
            "Review backend guidance vector with design leadership",
        ),
    }
    network = {
        "network_security_score": 52.0,
        "security_auto_dev": {"directive": "fortify", "playbooks": ("fortify",)},
        "network_security_upgrades": (
            "Patch intrusion detection lattice",
            "Deploy adaptive shields",
        ),
        "zero_trust_blueprint": {"actions": ("Audit session tokens",)},
        "holographic_enhancements": {
            "layer_upgrades": ("Spectral lattice", "Quantum mesh"),
            "phase_lock_directives": "Stabilise phase drift",
        },
        "holographic_diagnostics": {
            "efficiency_score": 74.2,
            "phase_coherence_index": 88.4,
        },
    }
    research = {
        "latest_sample_percent": 32.0,
        "research_pressure_index": 72.0,
        "volatility_percent": 6.5,
    }
    guidance = {"general_intelligence_score": 48.0}
    codebase = {
        "coverage_ratio": 0.62,
        "module_scorecards": (
            {
                "name": "auto_dev_network_manager",
                "risk_level": "high",
                "stability_modifier": 0.8,
            },
        ),
    }

    actions = manager.implement_fixes(
        codebase=codebase,
        mitigation=mitigation,
        network=network,
        research=research,
        guidance=guidance,
    )

    assert any(fix["domain"] == "codebase" for fix in actions["applied_fixes"])
    assert any(fix["domain"] == "network" for fix in actions["applied_fixes"])
    assert actions["stability_projection"]["projected_security_score"] > actions["stability_projection"]["security_score"]
    assert actions["stability_projection"]["projected_coverage"] > actions["stability_projection"]["coverage"]
    assert actions["research_balancing"]["projected_pressure_index"] < actions["research_balancing"]["pressure_index"]
    assert actions["network_hardening"]["upgrade_focus"]
    assert actions["holographic_adjustments"]
    assert actions["codebase_progress"]
