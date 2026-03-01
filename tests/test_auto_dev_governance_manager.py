"""Unit tests for the auto-dev governance manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_governance_manager import AutoDevGovernanceManager


def test_governance_manager_compiles_brief() -> None:
    manager = AutoDevGovernanceManager()
    brief = manager.governance_brief(
        guidance={
            "backend_alignment_score": 72.0,
            "risk_index": 1.4,
            "priority": "medium",
            "governance_outlook": "guidance-monitor",
        },
        network={"network_security_score": 62.0},
        security={
            "threat_level": "elevated",
            "security_score": 60.0,
            "projected_security_score": 74.0,
        },
        continuity={
            "continuity_index": 0.68,
            "codebase_continuity_actions": {"actions": ("Stabilise core",)},
        },
        mitigation={
            "priority": "high",
            "codebase_tasks": ("Refactor network module",),
            "network_tasks": ("Patch edge nodes",),
        },
        remediation={
            "stability_projection": {"projected_security_score": 78.0},
            "holographic_adjustments": ("Anchor sync",),
        },
        resilience={"resilience_score": 64.0, "grade": "steady"},
        codebase={
            "debt_risk_score": 0.55,
            "modernization_targets": (
                {
                    "name": "auto_dev_network_manager",
                    "risk_level": "high",
                    "modernization_steps": ("Refactor hotspots", "Add tests"),
                    "stability_modifier": 0.6,
                },
            ),
        },
        transmission={
            "guardrails": {"status": "reinforce", "actions": ("Lock anchors",)},
            "spectral_waveform": {"stability": "drifting", "recommended_actions": ("Apply smoothing",)},
            "lithographic_integrity": {"score": 58.0},
        },
    )

    assert 0.0 <= brief["oversight_score"] <= 100.0
    assert brief["state"] in {"autonomous", "directed", "guided", "needs-oversight"}
    assert brief["oversight_actions"]
    assert "codebase" in brief["risk_flags"] or "network" in brief["risk_flags"]
    support = brief["backend_support_map"]
    assert support["network_security_score"] == 62.0
    assert brief["codebase_directives"][0]["modernization_steps"]
    assert brief["holographic_directives"]
    focus = brief["managerial_focus"]
    assert focus["threat_level"] == "elevated"
    assert brief["managerial_backlog"]
