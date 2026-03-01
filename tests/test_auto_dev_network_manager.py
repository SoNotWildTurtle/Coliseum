"""Tests for auto dev network manager."""

from hololive_coliseum.auto_dev_network_manager import AutoDevNetworkManager


def test_auto_dev_network_manager_produces_brief() -> None:
    manager = AutoDevNetworkManager()
    nodes = [
        {"name": "central_relay", "role": "relay", "latency_ms": 52.0, "uptime_ratio": 0.91, "trusted": True},
        {"name": "south_relay", "role": "relay", "latency_ms": 74.0, "uptime_ratio": 0.89, "trusted": False},
        {"name": "core_hub", "role": "core", "latency_ms": 28.0, "uptime_ratio": 0.99, "trusted": True},
    ]
    summary = manager.assess_network(
        nodes=nodes,
        bandwidth_samples=[6.5, 8.2, 11.5],
        security_events=[
            {"severity": "high", "type": "void_surge"},
            {"severity": "medium", "type": "priority_throttle"},
        ],
        research={"raw_utilization_percent": 32.0},
        auto_dev_load=26.0,
    )
    latency = summary["latency"]
    assert latency["average_ms"] == 51.33
    assert latency["worst_ms"] == 74.0
    reliability = summary["reliability"]
    assert reliability["trusted_relays"] == 2
    assert reliability["untrusted_relays"] == 1
    assert summary["network_health"]["status"] == "stable"
    assert summary["security"]["risk"] == "high"
    assert summary["relay_plan"]["needs_redundancy"] is True
    assert "Add trusted relay coverage" in summary["recommendations"]
    assert "Increase security monitoring" in summary["recommendations"]
    assert summary["processing_utilization_percent"] > 0.0
    assert summary["raw_processing_percent"] >= summary["processing_utilization_percent"]
    detail = summary["network_processing_detail"]
    assert detail["research_percent"] == 32.0
    assert detail["auto_dev_load"] == 26.0
    assert detail["holographic_layers"] == summary["holographic_channels"]["layer_count"]
    assert detail["encrypted_channels"] is True
    automation = summary["security_automation"]
    assert automation["automation_score"] >= 0.0
    assert automation["playbooks"]
    assert "automation_tiers" in automation
    assert automation["security_focus"] in {"stabilise", "mitigate", "contain"}
    holographic = summary["holographic_channels"]
    assert holographic["layer_count"] >= 2
    assert holographic["anchor_quality"] >= 0.0
    assert "channel_map" in holographic
    assert holographic["channel_map"]["redundancy"] in {"baseline", "elevated"}
    assert "stability_index" in holographic["channel_map"]
    assert "triangulation_hint" in holographic
    verification = summary["verification_layers"]
    assert verification["layers"] == holographic["layer_count"]
    assert verification["integrity"] in {"stable", "harden", "reinforce"}
    detail_map = summary["network_processing_detail"]["channel_map"]
    assert detail_map["redundancy"] in {"baseline", "elevated"}
    assert "stability_index" in detail_map
    backlog = summary["upgrade_backlog"]
    assert backlog["priority"] in {"low", "medium", "high"}
    security_auto_dev = summary["security_auto_dev"]
    assert security_auto_dev["directive"] in {"stabilise", "expand", "triage", "bootstrap", "mitigate"}
    diagnostics = summary["holographic_diagnostics"]
    assert diagnostics["verification_integrity"] in {"stable", "harden", "reinforce"}
    assert "triangulation_hint" in diagnostics
    resilience = summary["resilience_matrix"]
    assert resilience["risk"] in {"low", "medium", "high", "critical"}
    zero_trust = summary["zero_trust_blueprint"]
    assert zero_trust["actions"]
    anomalies = summary["anomaly_signals"]
    assert anomalies["trusted_nodes"] == 2
    assert anomalies["untrusted_nodes"] == 1
    signal_matrix = summary["holographic_signal_matrix"]
    assert signal_matrix["layers"] == holographic["layer_count"]
