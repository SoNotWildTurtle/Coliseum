"""Tests for the auto-dev mitigation manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_mitigation_manager import AutoDevMitigationManager


def test_mitigation_manager_generates_prioritised_tasks() -> None:
    manager = AutoDevMitigationManager()
    plan = manager.derive_actions(
        codebase={
            "coverage_ratio": 0.6,
            "mitigation_plan": ("Refactor high complexity hotspots before next release",),
            "weakness_signals": (
                "Module 2 complexity exceeds warning threshold",
                "Tests missing for modules: 2, 3",
            ),
            "module_scorecards": (
                {
                    "name": "auto_dev_network_manager",
                    "risk_level": "high",
                    "recommended_actions": ("Refactor network guardrails",),
                    "stability_modifier": 0.7,
                },
            ),
        },
        network={
            "network_security_score": 50.0,
            "upgrade_backlog": {"tasks": ("Install adaptive firewalls",)},
            "security_auto_dev": {"directive": "fortify"},
            "upgrade_paths": ("Deploy quantum uplink",),
            "holographic_diagnostics": {"signal_health": "unstable"},
            "holographic_enhancements": {
                "layer_upgrades": ("Spectral lattice",),
                "phase_lock_directives": "Stabilise phase drift",
            },
        },
        research={
            "research_pressure_index": 72.0,
            "weakness_signals": ("Research coverage is below sustainability thresholds",),
            "competitive_research": {"primary_game": "RealmQuest"},
        },
        guidance={
            "risk_index": 1.6,
            "priority": "high",
            "directives": ("Prioritise counters for lava threats",),
            "general_intelligence_score": 45.0,
        },
    )

    assert plan["stability_score"] < 80.0
    assert plan["priority"] in {"high", "critical"}
    assert plan["codebase_tasks"]
    assert any("auto_dev_network_manager" in task["task"] for task in plan["codebase_tasks"])
    assert plan["network_tasks"]
    assert any("Research" in task for task in plan["research_tasks"])
    assert plan["intelligence_tasks"]
    assert plan["holographic_upgrades"]
    assert any(window["focus"] == "network" for window in plan["execution_windows"])
