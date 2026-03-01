"""Tests for auto dev modernization manager."""

from hololive_coliseum.auto_dev_modernization_manager import (
    AutoDevModernizationManager,
)


def test_modernization_manager_builds_brief() -> None:
    manager = AutoDevModernizationManager()
    brief = manager.modernization_brief(
        codebase={
            "modernization_targets": (
                {
                    "name": "auto_dev_network_manager",
                    "risk_level": "critical",
                    "modernization_steps": (
                        "Refactor network interface",
                        "Add deterministic tests",
                    ),
                    "stability_modifier": 0.72,
                },
                {
                    "name": "auto_dev_spawn_manager",
                    "risk_level": "high",
                    "modernization_steps": ("Document spawn flow",),
                    "stability_modifier": 0.4,
                },
            ),
            "weakness_signals": (
                "Tests missing for modules: 2",
                "Docstrings absent for modules: 2",
            ),
            "mitigation_plan": (
                "Increase automated test creation to reach baseline coverage",
            ),
            "debt_risk_score": 0.52,
        },
        mitigation={
            "codebase_tasks": (
                {"task": "Add spawn regression tests", "severity": "high"},
            ),
            "network_tasks": ("Tune latency thresholds",),
            "research_tasks": ("Profile rival MMO patch cadence",),
            "intelligence_tasks": ("Review managerial dashboard",),
        },
        remediation={
            "applied_fixes": (
                {"task": "Add spawn regression tests", "domain": "codebase"},
            ),
            "scheduled_fixes": (
                {"task": "Tune latency thresholds", "domain": "network"},
            ),
            "holographic_adjustments": (
                "Increase phase-lock sampling",
            ),
            "codebase_progress": (
                {"name": "auto_dev_spawn_manager", "addressed": True},
            ),
        },
        network={
            "network_security_score": 48.0,
            "transmission_guardrails": {"status": "review"},
            "processing_utilization_percent": 62.0,
        },
        transmission={
            "spectral_waveform": {
                "recommended_actions": ("Increase spectral sampling",),
                "efficiency": 0.24,
            },
            "phase_alignment": {
                "current": 0.65,
                "target": 0.8,
                "actions": ("Synchronise lattice anchors",),
            },
            "guardrails": {"status": "review", "follow_up": ("Audit guardrails",)},
        },
        research={
            "raw_utilization_percent": 55.0,
            "competitive_utilization_percent": 12.0,
            "trend_direction": "increasing",
            "intelligence_focus": "Simulate emergent sandbox encounters",
        },
        security={
            "security_score": 52.0,
            "threat_level": "elevated",
            "network_security_actions": ("Patch edge firewall",),
        },
    )

    assert brief["priority"] in {"accelerate", "stabilise", "monitor"}
    assert brief["targets"]
    assert brief["targets"][0]["name"] == "auto_dev_network_manager"
    assert brief["network_alignment"]["alignment"] in {
        "requires-hardening",
        "balanced",
        "upgrade-ready",
    }
    assert brief["holographic_enhancements"]
    assert brief["research_allocation"]["raw_percent"] == 55.0
    assert brief["mitigation_support"]
    assert brief["weakness_resolutions"]
    assert brief["timeline"]
    assert brief["modernization_actions"]
