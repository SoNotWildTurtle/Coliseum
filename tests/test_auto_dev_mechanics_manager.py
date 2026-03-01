"""Tests for auto dev mechanics manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_mechanics_manager import AutoDevMechanicsManager


def test_mechanics_blueprint_blends_encounter_signals() -> None:
    manager = AutoDevMechanicsManager()
    blueprint = manager.mechanics_blueprint(
        monsters=[{"hazard": "lava", "name": "Lava Imp"}],
        quests=[
            {
                "tags": ("alchemy", "lava"),
                "trade_synergy": {"hazard": "lava", "tempo": "rapid"},
                "support_threads": ("lane-1",),
            }
        ],
        mob_ai={
            "coordination_matrix": {"escalation": "relentless"},
            "evolution_threads": ("hazard:lava",),
        },
        guidance={
            "general_intelligence_score": 72.0,
            "managerial_threads": ("encounter-lab",),
        },
        research={"volatility_percent": 18.0, "trend_direction": "increasing"},
        network={
            "holographic_diagnostics": {"efficiency_score": 0.72},
            "transmission_guardrails": {"status": "stable"},
        },
        security={
            "security_score": 62.0,
            "threat_level": "high",
            "network_security_actions": ("Patch gateways",),
        },
        codebase={"weakness_signals": ("Missing tests",), "debt_risk_score": 2.3},
        modernization={
            "priority": "high",
            "targets": ({"name": "auto_dev_pipeline"},),
            "modernization_actions": ("Refactor hazard planner",),
        },
        optimization={
            "priority": "medium",
            "optimization_actions": ("Tune waveforms",),
        },
        transmission={
            "spectral_waveform": {
                "bandwidth_density": 0.58,
                "recommended_actions": ("Harmonic tuning",),
            }
        },
        resilience={
            "resilience_index": 0.64,
            "resilience_actions": ("Phase rehearsal",),
        },
        mitigation={"codebase_tasks": ("Add tests",)},
        remediation={"applied_fixes": ({"task": "Add tests"},)},
        self_evolution={"next_actions": ("Prototype hazard loops",)},
    )

    assert blueprint["mechanic_archetypes"][0].startswith("lava:")
    assert "lava:rapid" in blueprint["quest_synergies"]
    assert "auto_dev_pipeline" in blueprint["functionality_tracks"]
    assert blueprint["managerial_directives"]
    assert blueprint["network_considerations"]["security_score"] == 62.0
    assert blueprint["holographic_hooks"]["recommended_actions"]
    assert blueprint["priority"] in {"monitor", "medium", "elevated", "high", "critical"}
    assert blueprint["risk_score"] >= 0.0
