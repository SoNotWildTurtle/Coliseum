"""Tests for auto dev optimization manager."""

from hololive_coliseum.auto_dev_optimization_manager import (
    AutoDevOptimizationManager,
)


def test_optimization_manager_builds_brief() -> None:
    manager = AutoDevOptimizationManager()
    brief = manager.optimization_brief(
        codebase={
            "stability_outlook": "watch",
            "debt_risk_score": 0.6,
            "coverage_ratio": 0.72,
            "weakness_signals": (
                "Integration tests missing for critical modules",
                "Docstrings absent",
            ),
            "modernization_targets": (
                {"name": "auto_dev_network_manager", "next_step": "Refactor I/O"},
                {"name": "auto_dev_transmission_manager", "next_step": "Expand tests"},
            ),
        },
        mitigation={
            "priority": "high",
            "codebase_tasks": (
                {"task": "auto_dev_network_manager :: Add coverage", "severity": "high"},
            ),
        },
        remediation={
            "applied_fixes": (
                {"domain": "codebase", "task": "auto_dev_network_manager :: Add coverage"},
            ),
            "scheduled_fixes": (
                {"domain": "network", "task": "Tune guardrails"},
            ),
            "stability_projection": {
                "projected_security_score": 54.0,
                "projected_coverage": 0.8,
            },
            "codebase_progress": (
                {"name": "auto_dev_network_manager", "addressed": True},
                {"name": "auto_dev_transmission_manager", "addressed": False},
            ),
            "holographic_adjustments": (
                "Increase lattice sampling",
            ),
        },
        modernization={
            "priority": "stabilise",
            "targets": (
                {
                    "name": "auto_dev_network_manager",
                    "next_step": "Refactor I/O",
                },
            ),
            "timeline": (
                {"window": "Sprint 1", "target": "auto_dev_network_manager"},
            ),
        },
        network={"network_security_score": 48.0},
        network_auto_dev={
            "security_automation": ("Patch edge firewall",),
            "upgrade_tracks": ("Security directive: Harden edge",),
            "next_steps": ("Roll out guardrail patch",),
        },
        transmission={
            "guardrails": {"status": "review", "follow_up": ("Audit guardrails",)},
            "spectral_waveform": {
                "efficiency": 0.21,
                "recommended_actions": ("Increase spectral sampling",),
            },
            "phase_alignment": {"current": 0.62, "target": 0.8},
        },
        security={
            "security_score": 52.0,
            "threat_level": "elevated",
            "network_security_actions": ("Deploy IDS update",),
        },
        research={
            "raw_utilization_percent": 58.0,
            "research_pressure_index": 68.0,
            "trend_direction": "increasing",
            "recommendation": "Throttle research",
            "weakness_signals": ("Research pressure high",),
        },
        guidance={"priority": "medium"},
        resilience={
            "grade": "guarded",
            "holographic_readiness": {
                "status": "review",
                "recommended_actions": ("Rebalance lattice",),
            },
        },
    )

    assert brief["priority"] in {"accelerate", "stabilise"}
    assert brief["codebase_focus"]["weaknesses"]
    assert "auto_dev_network_manager" in brief["codebase_focus"]["target_modules"]
    assert brief["network_security_focus"]["actions"]
    assert brief["holographic_plan"]["actions"]
    assert brief["remediation_support"]["applied_count"] >= 1
    assert brief["research_signal"]["pressure"] == 68.0
    assert brief["modernization_dependencies"]
    assert brief["fix_windows"]
    assert brief["optimization_actions"]
    assert brief["managerial_focus"] in {
        "stabilise-backend",
        "balance-research",
        "accelerate-upgrades",
        "monitor",
    }
