"""Tests for the auto-dev transmission calibration manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_transmission_manager import (
    AutoDevTransmissionManager,
)


def test_transmission_manager_calibrates_holographic_channels() -> None:
    manager = AutoDevTransmissionManager()
    network = {
        "holographic_channels": {
            "encrypted_channels": 4,
            "layer_count": 3,
        },
        "holographic_diagnostics": {
            "efficiency_score": 0.78,
            "phase_coherence_index": 0.74,
        },
        "verification_layers": {
            "layers": 3,
            "integrity": "harden",
            "severity_focus": ("high", "medium"),
        },
        "network_processing_detail": {
            "encrypted_channels": 3,
        },
        "security_auto_dev": {
            "directive": "fortify",
            "verification_layers": 2,
        },
        "resilience_matrix": {"score": 68.0},
        "holographic_enhancements": {
            "layer_upgrades": ("Spectral lattice",),
            "phase_lock_directives": "Stabilise phase drift",
        },
        "bandwidth": {"average_mbps": 18.5},
        "processing_utilization_percent": 32.0,
        "transmission_guardrails": {
            "status": "reinforce",
            "severity": "elevated",
            "actions": ("Lock spectral anchors",),
        },
        "lithographic_integrity": {
            "score": 68.0,
            "severity": "monitor",
            "headline_action": "Maintain guardrails",
        },
    }
    mitigation = {
        "priority": "high",
        "holographic_upgrades": ("Quantum mesh",),
    }
    remediation = {
        "applied_fixes": ("network", "codebase"),
        "holographic_adjustments": ("Rebalanced channels",),
    }
    research = {"latest_sample_percent": 42.0}

    calibration = manager.calibrate(
        network=network,
        research=research,
        mitigation=mitigation,
        remediation=remediation,
    )

    compression = calibration["compression_profile"]
    assert compression["algorithm"] in {"lzma", "auto", "zlib"}
    assert compression["level"] >= 4
    phase_alignment = calibration["phase_alignment"]
    assert phase_alignment["target"] >= phase_alignment["current"]
    layers = calibration["security_layers"]
    assert layers["recommended_layers"] >= layers["active_layers"]
    assert calibration["bandwidth_budget_mbps"] > 0.0
    assert calibration["utilization_projection_percent"] >= research["latest_sample_percent"]
    assert calibration["notes"]
    assert calibration["guardrails"]["status"]
    assert calibration["lithographic_integrity"]["score"] >= 0.0
    waveform = calibration["spectral_waveform"]
    assert waveform["stability"] in {"steady", "drifting", "turbulent"}
    assert waveform["recommended_actions"]
