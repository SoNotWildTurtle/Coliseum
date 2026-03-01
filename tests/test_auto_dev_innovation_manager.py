"""Unit tests for the auto-dev innovation manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_innovation_manager import AutoDevInnovationManager


def test_innovation_brief_fuses_functionality_and_mechanics() -> None:
    manager = AutoDevInnovationManager()
    brief = manager.innovation_brief(
        guidance={"managerial_threads": ("encounter-lab",)},
        mechanics={
            "novelty_score": 68.0,
            "risk_score": 22.0,
            "functionality_tracks": ("hazard-forges", "network-labs"),
            "gameplay_threads": ("forge-loop",),
            "mechanic_archetypes": ("lava:relentless",),
        },
        codebase={"instability_index": 0.45, "debt_risk_score": 0.61},
        modernization={
            "network_alignment": {"alignment": "upgrade-ready"},
            "modernization_actions": ("Refactor hazard planner",),
            "targets": ({"name": "auto_dev_pipeline"},),
        },
        optimization={"optimization_actions": ("Tune waveforms",)},
        network={
            "network_security_score": 72.0,
            "upgrade_paths": ("mesh-upgrade",),
        },
        transmission={
            "bandwidth_budget_mbps": 34.0,
            "phase_alignment": {"actions": ("Sync anchors",)},
            "spectral_waveform": {
                "recommended_actions": ("Rebalance harmonics",),
                "stability": "steady",
                "bandwidth_density": 0.52,
            },
        },
        security={"security_score": 74.0, "threat_level": "guarded"},
        research={
            "research_pressure_index": 22.0,
            "trend_direction": "increasing",
            "raw_utilization_percent": 48.0,
            "competitive_utilization_percent": 12.0,
        },
        resilience={"grade": "hardened"},
        mitigation={"codebase_tasks": ("Add tests",)},
        remediation={
            "codebase_progress": (
                {"name": "auto_dev_pipeline", "addressed": True},
            ),
        },
    )

    assert brief["priority"] in {"accelerate", "stabilise", "explore", "monitor"}
    assert brief["innovation_score"] >= 0.0
    assert brief["feature_concepts"]
    assert brief["network_requirements"]["security_score"] >= 0.0
    assert "Rebalance harmonics" in brief["holographic_requirements"]["recommended_actions"]
    assert brief["backend_actions"]
    assert brief["research_synergy"]["trend"] == "increasing"
    assert "auto_dev_pipeline" in brief["addressed_modules"]
