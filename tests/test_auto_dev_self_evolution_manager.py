"""Tests for auto dev self evolution manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_self_evolution_manager import (
    AutoDevSelfEvolutionManager,
)


def test_self_evolution_blueprint_compiles_directives() -> None:
    manager = AutoDevSelfEvolutionManager(horizon=5)
    blueprint = manager.blueprint(
        guidance={
            "general_intelligence_score": 72.0,
            "managerial_threads": ("Stabilise network mesh",),
            "guidance_backbone": ("Propagate quest reinforcements",),
        },
        network={
            "upgrade_paths": ("Expand holographic lattice throughput",),
            "network_security_upgrades": ("Accelerate zero-trust hardening",),
            "security_auto_dev": {"directive": "triage"},
            "network_security_score": 58.0,
        },
        codebase={
            "coverage_ratio": 0.71,
            "mitigation_plan": ("Schedule regression tests",),
            "modernization_targets": ("Refactor holographic relay module",),
            "stability_outlook": "watch",
        },
        mitigation={
            "stability_score": 62.0,
            "priority": "high",
            "research_tasks": ("Throttle rival research sampling",),
        },
        remediation={
            "applied_fixes": (
                {"domain": "codebase", "task": "relay :: add integration tests"},
                {"domain": "network", "task": "deploy guardrails"},
            ),
            "scheduled_fixes": (
                {"domain": "research", "task": "add sampling budget"},
            ),
            "codebase_progress": (
                {"name": "relay", "addressed": True, "risk_level": "high"},
                {"name": "ai", "addressed": False, "risk_level": "elevated"},
            ),
        },
        transmission={
            "spectral_waveform": {
                "recommended_actions": ("Apply lattice smoothing", "Maintain spectral balance"),
            },
            "lattice_overlay": {
                "actions": ("Synchronise lattice with guardrail review",),
            },
            "guardrails": {
                "follow_up": ("Re-check holographic dampening",),
            },
            "notes": ("Compression algorithm set to lzma",),
        },
        security={
            "network_security_actions": ("Deploy sensors",),
            "hardening_tasks": (
                {"module": "relay", "risk_level": "high"},
            ),
            "security_score": 61.0,
        },
        governance={
            "state": "guided",
            "oversight_score": 74.0,
            "oversight_actions": ("Schedule oversight sync",),
        },
        research={
            "raw_utilization_percent": 48.0,
            "research_pressure_index": 42.0,
            "competitive_utilization_percent": 18.0,
        },
        continuity={
            "timeline": ({"focus": "Stabilise critical systems"},),
            "continuity_risks": {"network": "elevated"},
        },
        resilience={
            "grade": "steady",
            "resilience_actions": ("Maintain current resilience posture",),
        },
    )

    assert blueprint["horizon"] == 5
    assert blueprint["readiness_state"] in {"stabilise", "expand", "accelerate", "triage"}
    assert blueprint["upgrade_directives"]
    assert blueprint["security_enhancements"]
    assert blueprint["holographic_directives"]
    assert blueprint["codebase_focus"]["mitigation_plan"]
    assert blueprint["research_focus"]["utilization_percent"] == 48.0
    assert blueprint["managerial_overwatch"]["threads"]
    assert blueprint["learning_loops"]
    assert blueprint["telemetry_focus"]["watchlist"]
    assert blueprint["adaptive_tuning"]["focus"] in {"stability", "security", "innovation"}
    assert blueprint["next_actions"]


def test_self_evolution_blueprint_handles_sparse_inputs() -> None:
    manager = AutoDevSelfEvolutionManager()
    blueprint = manager.blueprint(
        guidance={},
        network={},
        codebase={},
        mitigation={},
        remediation={},
        transmission={},
        security={},
        governance={},
        research={},
    )

    assert blueprint["readiness_index"] == 0.0
    assert blueprint["upgrade_directives"] == ("Maintain upgrade cadence",)
    assert blueprint["holographic_directives"] == ("Maintain spectral balance",)
    assert "Run stability retrospectives every sprint" in blueprint["learning_loops"]
    assert blueprint["telemetry_focus"]["readiness_state"] == blueprint["readiness_state"]
    assert blueprint["adaptive_tuning"]["risk_budget"] in {
        "balanced",
        "aggressive",
        "conservative",
    }
    assert blueprint["next_actions"][0] == "Maintain upgrade cadence"
    assert "Maintain spectral balance" in blueprint["next_actions"]
