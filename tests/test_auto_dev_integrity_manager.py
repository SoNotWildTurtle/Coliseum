"""Unit tests for the auto-dev integrity manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_integrity_manager import AutoDevIntegrityManager


def test_integrity_report_combines_integrity_signals() -> None:
    manager = AutoDevIntegrityManager()
    report = manager.integrity_report(
        codebase={
            "coverage_ratio": 0.58,
            "debt_risk_score": 0.8,
            "weakness_signals": ["Low coverage", "Legacy module"],
        },
        network={
            "network_security_score": 61.0,
            "anomaly_signals": ("relay drift",),
            "holographic_diagnostics": {"efficiency_score": 62.0},
        },
        security={
            "security_score": 59.0,
            "projected_security_score": 72.0,
            "network_security_actions": ["Rotate keys"],
            "automation_directives": {"playbooks": ["Deploy sensors"]},
        },
        transmission={
            "lithographic_integrity": {"score": 55.0},
            "spectral_waveform": {
                "bandwidth_density": 0.6,
                "recommended_actions": ["Apply smoothing"],
            },
            "guardrails": {"follow_up": ["Anchor review"]},
            "phase_alignment": {
                "current": 0.5,
                "target": 0.8,
                "actions": ["Lock anchors"],
            },
            "notes": ("Calibrate lattice",),
        },
        modernization={
            "priority": "accelerate",
            "modernization_actions": ["Refactor relay driver"],
            "weakness_resolutions": ["Add tests"],
            "targets": [{"name": "relay_driver"}],
        },
        optimization={
            "priority": "stabilise",
            "optimization_actions": ["Tune holographic budget"],
        },
        resilience={
            "resilience_index": 0.64,
            "grade": "adaptive",
            "resilience_actions": ["Stage failover"],
        },
    )

    assert report["priority"] == "accelerate"
    assert report["integrity_score"] > 0.0
    assert report["coverage_gap"] > 0.0
    assert report["security_gap"] > 0.0
    assert report["holographic_gap"] >= 0.0
    assert report["weakness_focus"]["codebase"]
    assert "relay_driver" in report["weakness_focus"]["modernization_targets"]
    assert report["restoration_actions"]
    assert report["holographic_actions"]
    assert report["network_hardening"]
    assert report["stability_projection"]["projected_security"] == 72.0
    assert report["stability_projection"]["coverage_projection"] >= 0.58
    assert report["integrity_trends"]["modernization_priority"] == "accelerate"
