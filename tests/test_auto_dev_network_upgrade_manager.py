"""Tests for auto dev network upgrade manager."""

from __future__ import annotations

from hololive_coliseum.auto_dev_network_upgrade_manager import (
    AutoDevNetworkUpgradeManager,
)


def test_network_upgrade_manager_compiles_directives() -> None:
    manager = AutoDevNetworkUpgradeManager()
    plan = manager.plan_auto_dev(
        network={
            "upgrade_paths": ("Expand edge relays",),
            "network_security_upgrades": ("Deploy zero-trust mesh",),
            "security_auto_dev": {"directive": "triage"},
            "upgrade_roadmap": {"milestones": ("Q2 lattice uplift",)},
            "processing_utilization_percent": 68.0,
            "bandwidth": {"average_mbps": 18.4},
        },
        security={
            "threat_level": "high",
            "security_score": 54.0,
            "network_security_actions": ("Harden ingress",),
            "hardening_tasks": ({"module": "relay", "risk_level": "high"},),
        },
        transmission={
            "spectral_waveform": {"recommended_actions": ("Tune phase",)},
            "lattice_overlay": {"actions": ("Rebalance lattice",), "stability": "guarded"},
            "guardrails": {"follow_up": ("Re-run guardrail diagnostics",), "status": "watch"},
        },
        research={"raw_utilization_percent": 72.0},
        codebase={
            "modernization_targets": (
                {
                    "name": "network_relay",
                    "risk_level": "high",
                    "modernization_steps": ("Refactor relay handlers",),
                },
            )
        },
        mitigation={"network_tasks": ("Propagate hardening playbook",)},
    )

    assert plan["priority"] in {"critical", "accelerate", "stabilise", "monitor"}
    assert plan["readiness_score"] <= 1.0
    assert plan["upgrade_tracks"]
    assert plan["security_automation"]
    assert plan["holographic_integration"]["actions"]
    assert plan["processing_focus"]["budget_health"] in {"strained", "watch", "stable"}
    assert plan["codebase_links"]
    assert plan["next_steps"]


def test_network_upgrade_manager_handles_sparse_inputs() -> None:
    manager = AutoDevNetworkUpgradeManager()
    plan = manager.plan_auto_dev(
        network={},
        security={},
        transmission={},
        research={},
        codebase={},
        mitigation={},
    )

    assert plan["priority"] == "monitor"
    assert plan["upgrade_tracks"] == ("Maintain upgrade cadence",)
    assert plan["holographic_integration"]["actions"] == ("Maintain spectral balance",)
    assert plan["codebase_links"] == (
        "No network-focused modernization targets identified",
    )
