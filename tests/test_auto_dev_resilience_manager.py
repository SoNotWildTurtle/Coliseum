"""Tests for auto dev resilience manager."""

from hololive_coliseum.auto_dev_resilience_manager import AutoDevResilienceManager


def test_resilience_manager_summarises_cross_domain_signals() -> None:
    manager = AutoDevResilienceManager()
    brief = manager.assess_resilience(
        codebase={
            "coverage_ratio": 0.68,
            "instability_index": 1.4,
            "debt_risk_score": 3.1,
        },
        network={
            "network_security_score": 62.0,
            "reliability": {"average_uptime": 0.94},
            "network_health": {"status": "degraded"},
            "transmission_guardrails": {"severity": "reinforce"},
            "holographic_diagnostics": {
                "phase_coherence_index": 0.58,
                "efficiency_score": 0.66,
            },
            "security_auto_dev": {"directive": "fortify"},
            "zero_trust_blueprint": {"tier": "hardened"},
            "upgrade_paths": ("edge-hardening", "litho-handoff", "relay-cache"),
        },
        research={
            "research_pressure_index": 58.0,
            "latest_sample_percent": 72.0,
            "trend_direction": "rising",
        },
        mitigation={
            "priority": "high",
            "stability_score": 64.0,
            "network_tasks": ("patch relays",),
            "codebase_tasks": ({"task": "increase coverage", "severity": "high"},),
        },
        remediation={
            "applied_fixes": (
                {"domain": "codebase"},
                {"domain": "network"},
            ),
            "scheduled_fixes": ({"domain": "research"},),
            "stability_projection": {
                "security_score": 55.0,
                "projected_security_score": 70.0,
                "projected_coverage": 0.74,
            },
        },
        guidance={
            "priority": "critical",
            "governance_outlook": "guidance-oversight",
            "backend_alignment_score": 0.62,
            "managerial_threads": ("network-hardening", "coverage-drive"),
        },
    )

    assert 0.0 <= brief["resilience_index"] <= 1.0
    assert brief["grade"] in {"fortified", "resilient", "steady", "vigilant", "at-risk"}
    assert brief["stability_risks"]
    assert (
        "Accelerate network security automation rollout" in brief["resilience_actions"]
    )
    readiness = brief["holographic_readiness"]
    assert readiness["guardrail_severity"] == "reinforce"
    assert readiness["status"] in {"intervene", "tune", "stable"}
    focus = brief["network_security_focus"]
    assert focus["security_score"] == round(focus["security_score"], 2)
    assert focus["automation_directive"] == "fortify"
    overwatch = brief["managerial_overwatch"]
    assert overwatch["resilience_grade"] == brief["grade"]
    assert overwatch["mitigation_priority"] == "high"
    assert brief["research_penalty"] > 0.0
