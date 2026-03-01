"""Tests for auto dev execution manager."""

from hololive_coliseum.auto_dev_execution_manager import AutoDevExecutionManager


def test_execution_manager_builds_brief() -> None:
    manager = AutoDevExecutionManager()
    brief = manager.execution_brief(
        functionality={
            "functionality_score": 74.0,
            "functionality_tracks": ("core-loop", "support-loop"),
            "managerial_directives": ("align-core",),
            "network_requirements": {
                "security_score": 64.0,
                "bandwidth_mbps": 28.0,
                "latency_target_ms": 42.0,
                "upgrade_actions": ("deploy-cache",),
            },
            "holographic_requirements": {
                "recommended_actions": ("phase-trim",),
                "efficiency_score": 72.0,
                "phase_target": 0.8,
            },
        },
        mechanics={
            "novelty_score": 68.0,
            "gameplay_threads": ("burst-thread",),
            "holographic_requirements": {"recommended_actions": ("phase-balance",)},
            "network_considerations": {"security_score": 62.0},
        },
        gameplay={
            "gameplay_score": 70.0,
            "loops": ("combo-loop",),
            "managerial_actions": ("reinforce-loop",),
            "network_requirements": {"security_score": 63.0},
            "holographic_requirements": {"recommended_actions": ("sync-wave",)},
        },
        design={
            "prototype_threads": ("prototype-thread",),
        },
        systems={
            "systems_threads": ("systems-thread",),
        },
        creation={
            "creation_alignment_score": 66.0,
            "creation_tracks": ("prototype-loop",),
            "creation_actions": ("draft-upgrade",),
            "holographic_requirements": {"recommended_actions": ("phase-align",)},
            "network_requirements": {"security_score": 61.0},
        },
        synthesis={
            "holographic_requirements": {"recommended_actions": ("phase-merge",)},
        },
        convergence={
            "integration_index": 64.0,
            "convergence_tracks": ("fusion-loop",),
            "convergence_actions": ("merge-paths",),
            "gap_index": 36.0,
            "codebase_alignment": {
                "convergence_alignment_score": 58.0,
                "convergence_gap_index": 44.0,
                "convergence_focus_modules": ("auto_dev_network_manager",),
            },
            "network_requirements": {"security_score": 65.0},
        },
        implementation={
            "implementation_score": 71.0,
            "implementation_gap_index": 38.0,
            "implementation_tracks": ("delivery-loop",),
            "implementation_actions": ("ship-upgrade",),
            "implementation_threads": ("delivery-thread",),
            "delivery_windows": ("sprint-14",),
            "network_requirements": {"security_score": 66.0},
            "holographic_requirements": {"recommended_actions": ("phase-sync",)},
            "implementation_backlog": (
                {"module": "auto_dev_pipeline", "status": "scheduled", "focus": "codebase"},
            ),
        },
        network={
            "network_security_upgrades": {"security_score": 67.0},
        },
        transmission={
            "phase_alignment": {"target": 0.82, "recommended_actions": ("phase-lock",)},
            "lithographic_integrity": {"score": 74.0},
        },
        security={
            "security_score": 68.0,
            "threat_level": "guarded",
            "automation_directives": {"playbooks": ("auto-hardening",)},
        },
        modernization={
            "priority": "accelerate",
            "modernization_actions": ("modernize-network",),
        },
        optimization={
            "priority": "amplify",
            "optimization_actions": ("balance-load",),
        },
        resilience={
            "resilience_score": 72.0,
        },
        continuity={
            "continuity_index": 0.71,
            "timeline": (
                {"window": "Day 0-7", "focus": "stabilise"},
                {"window": "Day 8-14", "focus": "execute"},
            ),
            "codebase_continuity_actions": {
                "planned_tasks": ("verify-mitigations",),
                "outstanding_modules": ("auto_dev_mechanics_manager",),
            },
        },
        governance={
            "state": "guided",
            "oversight_actions": ("audit-execution",),
        },
        mitigation={
            "codebase_tasks": ("Refactor network adapters",),
        },
        remediation={
            "applied_fixes": (
                {"name": "auto_dev_network_manager", "addressed": True},
            ),
            "scheduled_fixes": (
                {"name": "auto_dev_gameplay_manager", "addressed": False},
            ),
        },
        research={
            "raw_utilization_percent": 44.0,
            "research_pressure_index": 22.0,
            "trend_direction": "rising",
        },
        codebase={
            "execution_gap_index": 42.0,
            "execution_alignment_score": 58.0,
            "execution_focus_modules": ("auto_dev_transmission_manager",),
            "execution_recommendations": ("Add regression tests",),
            "implementation_gap_index": 40.0,
            "creation_gap_index": 38.0,
            "convergence_gap_index": 36.0,
            "debt_risk_score": 0.3,
        },
    )

    assert brief["priority"] in {"deploy", "accelerate", "stabilise", "align", "monitor"}
    assert brief["execution_tracks"]
    assert brief["network_requirements"]["security_score"] >= 0.0
    assert brief["holographic_requirements"]["recommended_actions"]
    assert brief["execution_backlog"]
    assert brief["stability_state"] in {"steady", "guarded", "vigilant", "balancing"}
