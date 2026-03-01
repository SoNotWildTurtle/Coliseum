"""Auto-dev networking analytics for MMO planning."""

from __future__ import annotations

from typing import Any, Iterable, Sequence


def _safe_average(values: Iterable[float]) -> float:
    total = 0.0
    count = 0
    for value in values:
        total += float(value)
        count += 1
    return total / count if count else 0.0


def _as_tuple(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(value for value in values if value)


class AutoDevNetworkManager:
    """Summarise latency, reliability, bandwidth, and security posture."""

    def __init__(
        self,
        *,
        latency_target: float = 80.0,
        uptime_target: float = 0.95,
        bandwidth_target: float = 14.0,
    ) -> None:
        self.latency_target = float(latency_target)
        self.uptime_target = float(uptime_target)
        self.bandwidth_target = float(bandwidth_target)

    def assess_network(
        self,
        *,
        nodes: Sequence[dict[str, Any]] | None = None,
        bandwidth_samples: Sequence[float] | None = None,
        security_events: Sequence[dict[str, Any]] | None = None,
        research: dict[str, Any] | None = None,
        auto_dev_load: float | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic networking brief for the auto-dev pipeline."""

        node_list = list(nodes or [])
        samples = [float(sample) for sample in (bandwidth_samples or ())]
        events = list(security_events or [])
        research_percent = self._extract_research_percent(research)
        auto_load = float(auto_dev_load or 0.0)

        latency = self._latency_summary(node_list)
        reliability = self._reliability_summary(node_list)
        bandwidth = self._bandwidth_summary(samples)
        security = self._security_summary(events)
        network_health = self._network_health(latency, reliability, bandwidth, security)
        relay_plan = self._relay_plan(node_list, reliability, security)
        processing = self._processing_summary(
            bandwidth,
            research_percent,
            auto_load,
            len(events),
        )
        recommendations = self._recommendations(
            network_health,
            relay_plan,
            security,
            bandwidth,
        )
        processing_detail = processing["detail"]["network_processing_detail"]
        security_automation = self._security_automation(
            security,
            node_list,
            events,
        )
        holographic = self._holographic_channels(
            bandwidth,
            processing_detail,
            research_percent,
            auto_load,
            len(events),
        )
        verification = self._verification_layers(security, holographic)
        upgrade_backlog = self._upgrade_backlog(
            node_list,
            relay_plan,
            security,
            network_health,
        )
        security_auto_dev = self._security_auto_dev_brief(
            security_automation,
            upgrade_backlog,
            verification,
        )
        network_security_score = self._network_security_score(
            security_auto_dev,
            security,
            verification,
        )
        security_auto_dev = dict(security_auto_dev)
        security_auto_dev["network_security_score"] = network_security_score
        security_upgrades = self._network_security_upgrades(
            security_auto_dev,
            upgrade_backlog,
        )
        holographic_diagnostics = self._holographic_diagnostics(
            holographic,
            verification,
        )
        resilience = self._resilience_matrix(
            network_health,
            reliability,
            security,
        )
        zero_trust = self._zero_trust_blueprint(security_auto_dev, security)
        anomaly_signals = self._anomaly_signals(events, node_list)
        holographic_matrix = self._holographic_signal_matrix(
            holographic,
            verification,
        )
        upgrade_paths = self._upgrade_paths(upgrade_backlog, security_auto_dev, holographic)
        security_auto_dev["upgrade_paths"] = upgrade_paths
        holographic_enhancements = self._holographic_enhancements(
            holographic,
            security_auto_dev,
            verification,
        )
        transmission_guardrails = self._transmission_guardrails(
            holographic_diagnostics,
            verification,
            network_health,
            security_auto_dev,
            holographic_enhancements,
        )
        lithographic_integrity = self._lithographic_integrity(
            holographic_diagnostics,
            transmission_guardrails,
        )
        brief: dict[str, Any] = {
            "latency": latency,
            "reliability": reliability,
            "bandwidth": bandwidth,
            "security": security,
            "network_health": network_health,
            "relay_plan": relay_plan,
            "processing_utilization_percent": processing["processing"],
            "raw_processing_percent": processing["raw"],
            "recommendations": tuple(recommendations),
            "security_automation": security_automation,
            "holographic_channels": holographic,
            "verification_layers": verification,
            "upgrade_backlog": upgrade_backlog,
            "security_auto_dev": security_auto_dev,
            "holographic_diagnostics": holographic_diagnostics,
            "resilience_matrix": resilience,
            "zero_trust_blueprint": zero_trust,
            "anomaly_signals": anomaly_signals,
            "holographic_signal_matrix": holographic_matrix,
            "upgrade_paths": upgrade_paths,
            "network_security_score": network_security_score,
            "network_security_upgrades": security_upgrades,
            "holographic_enhancements": holographic_enhancements,
            "transmission_guardrails": transmission_guardrails,
            "lithographic_integrity": lithographic_integrity,
        }
        brief.update(processing["detail"])
        detail = brief["network_processing_detail"]
        detail["holographic_layers"] = holographic["layer_count"]
        detail["encrypted_channels"] = holographic["encrypted_channels"]
        detail["anchor_quality"] = holographic["anchor_quality"]
        detail["channel_map"] = holographic["channel_map"]
        detail["phase_shift_map"] = holographic["phase_shift_map"]
        return brief

    def _latency_summary(self, nodes: Sequence[dict[str, Any]]) -> dict[str, Any]:
        if not nodes:
            return {"average_ms": 0.0, "best_ms": None, "worst_ms": None}
        latencies = [float(node.get("latency_ms", 0.0)) for node in nodes]
        return {
            "average_ms": round(_safe_average(latencies), 2),
            "best_ms": round(min(latencies), 2),
            "worst_ms": round(max(latencies), 2),
        }

    def _reliability_summary(self, nodes: Sequence[dict[str, Any]]) -> dict[str, Any]:
        if not nodes:
            return {
                "average_uptime": 0.0,
                "trusted_relays": 0,
                "untrusted_relays": 0,
            }
        uptimes = [float(node.get("uptime_ratio", 0.0)) for node in nodes]
        trusted = sum(1 for node in nodes if node.get("trusted", True))
        untrusted = sum(1 for node in nodes if not node.get("trusted", True))
        return {
            "average_uptime": round(_safe_average(uptimes), 3),
            "trusted_relays": trusted,
            "untrusted_relays": untrusted,
        }

    def _bandwidth_summary(self, samples: Sequence[float]) -> dict[str, Any]:
        if not samples:
            return {"average_mbps": 0.0, "peak_mbps": 0.0, "baseline_mbps": 0.0}
        baseline = min(samples)
        peak = max(samples)
        average = _safe_average(samples)
        return {
            "baseline_mbps": round(baseline, 2),
            "average_mbps": round(average, 2),
            "peak_mbps": round(peak, 2),
        }

    def _security_summary(self, events: Sequence[dict[str, Any]]) -> dict[str, Any]:
        if not events:
            return {
                "risk": "low",
                "incidents": 0,
                "focus": (),
                "incidents_by_severity": {"low": 0, "medium": 0, "high": 0, "critical": 0},
            }
        severity_order = ["low", "medium", "high", "critical"]
        counts = {level: 0 for level in severity_order}
        focus: list[str] = []
        highest = "low"
        for event in events:
            severity = str(event.get("severity", "low")).lower()
            if severity not in counts:
                severity = "low"
            counts[severity] += 1
            focus.append(str(event.get("type", "unknown")))
            if severity_order.index(severity) > severity_order.index(highest):
                highest = severity
        return {
            "risk": highest,
            "incidents": len(events),
            "focus": tuple(sorted(set(focus))),
            "incidents_by_severity": counts,
        }

    def _network_health(
        self,
        latency: dict[str, Any],
        reliability: dict[str, Any],
        bandwidth: dict[str, Any],
        security: dict[str, Any],
    ) -> dict[str, Any]:
        latency_avg = float(latency.get("average_ms") or 0.0)
        latency_factor = 1.0
        if self.latency_target > 0.0:
            overage = max(0.0, latency_avg - self.latency_target)
            latency_factor = max(0.0, 1.0 - overage / self.latency_target)
        uptime_avg = float(reliability.get("average_uptime") or 0.0)
        uptime_factor = 0.0
        if self.uptime_target > 0.0:
            uptime_factor = min(1.0, uptime_avg / self.uptime_target) if uptime_avg else 0.0
        peak_bw = float(bandwidth.get("peak_mbps") or 0.0)
        bandwidth_factor = 1.0
        if peak_bw > self.bandwidth_target:
            margin = peak_bw - self.bandwidth_target
            bandwidth_factor = max(0.0, 1.0 - margin / max(self.bandwidth_target * 1.5, 1.0))
        score = (
            latency_factor * 0.4
            + uptime_factor * 0.3
            + bandwidth_factor * 0.3
        ) * 100.0
        risk = str(security.get("risk", "low")).lower()
        if risk == "high":
            score *= 0.9
        elif risk == "critical":
            score *= 0.75
        score = max(0.0, min(100.0, score))
        if score >= 70.0:
            status = "stable"
        elif score >= 45.0:
            status = "degraded"
        else:
            status = "critical"
        return {"status": status, "score": round(score, 2)}

    def _relay_plan(
        self,
        nodes: Sequence[dict[str, Any]],
        reliability: dict[str, Any],
        security: dict[str, Any],
    ) -> dict[str, Any]:
        relays = [node for node in nodes if node.get("role") == "relay"]
        untrusted = sum(1 for node in relays if not node.get("trusted", True))
        needs_redundancy = False
        if untrusted:
            needs_redundancy = True
        if float(reliability.get("average_uptime", 0.0)) < self.uptime_target:
            needs_redundancy = True
        if str(security.get("risk", "low")).lower() in {"high", "critical"}:
            needs_redundancy = True
        return {
            "relays": len(relays),
            "needs_redundancy": needs_redundancy,
            "untrusted_relays": untrusted,
        }

    def _processing_summary(
        self,
        bandwidth: dict[str, Any],
        research_percent: float,
        auto_dev_load: float,
        incident_count: int,
    ) -> dict[str, Any]:
        peak_bandwidth = float(bandwidth.get("peak_mbps", 0.0))
        raw = (
            peak_bandwidth * 2.4
            + research_percent * 0.25
            + auto_dev_load * 0.3
            + incident_count * 3.5
        )
        raw = max(0.0, min(100.0, raw))
        processing = min(100.0, raw * 0.85)
        detail = {
            "network_processing_detail": {
                "peak_bandwidth_mbps": round(peak_bandwidth, 2),
                "incident_load": incident_count,
                "research_percent": round(research_percent, 2),
                "auto_dev_load": round(auto_dev_load, 2),
            }
        }
        return {
            "raw": round(raw, 2),
            "processing": round(processing, 2),
            "detail": detail,
        }

    def _recommendations(
        self,
        network_health: dict[str, Any],
        relay_plan: dict[str, Any],
        security: dict[str, Any],
        bandwidth: dict[str, Any],
    ) -> list[str]:
        recommendations: list[str] = []
        if network_health.get("status") in {"degraded", "critical"}:
            recommendations.append("Stabilise relay latency")
        if relay_plan.get("needs_redundancy"):
            recommendations.append("Add trusted relay coverage")
        risk = str(security.get("risk", "low")).lower()
        if risk in {"high", "critical"}:
            recommendations.append("Increase security monitoring")
        if float(bandwidth.get("peak_mbps", 0.0)) >= self.bandwidth_target * 0.95:
            recommendations.append("Provision additional bandwidth")
        if not recommendations:
            recommendations.append("Maintain current networking rollout")
        seen: set[str] = set()
        ordered: list[str] = []
        for item in recommendations:
            if item not in seen:
                ordered.append(item)
                seen.add(item)
        return ordered

    def _security_automation(
        self,
        security: dict[str, Any],
        nodes: Sequence[dict[str, Any]],
        events: Sequence[dict[str, Any]],
    ) -> dict[str, Any]:
        incidents = int(security.get("incidents", 0))
        risk = str(security.get("risk", "low")).lower()
        trusted_relays = sum(1 for node in nodes if node.get("trusted", True))
        automation_score = 45.0 + trusted_relays * 6.5 - incidents * 5.0
        if risk in {"high", "critical"}:
            automation_score -= 7.5
        automation_score = max(0.0, min(100.0, automation_score))
        playbooks: list[str] = []
        if incidents:
            playbooks.append("Rotate encryption keys")
        if any(not node.get("trusted", True) for node in nodes):
            playbooks.append("Audit untrusted relays")
        if risk in {"high", "critical"}:
            playbooks.append("Activate holographic verification layers")
        controls: list[str] = []
        if incidents >= 2:
            controls.append("Enable auto-isolation for hostile traffic")
        if risk in {"medium", "high", "critical"}:
            controls.append("Increase anomaly sampling cadence")
        if not controls:
            controls.append("Maintain automated security cadence")
        tiers: list[str] = ["monitoring"]
        if trusted_relays >= 2:
            tiers.append("response")
        if risk in {"medium", "high", "critical"} or incidents:
            tiers.append("hardening")
        focus = "stabilise"
        if risk in {"high", "critical"}:
            focus = "mitigate"
        elif incidents:
            focus = "contain"
        return {
            "automation_score": round(automation_score, 2),
            "playbooks": tuple(dict.fromkeys(playbooks)),
            "recommended_controls": tuple(dict.fromkeys(controls)),
            "automation_tiers": tuple(tiers),
            "security_focus": focus,
        }

    def _holographic_channels(
        self,
        bandwidth: dict[str, Any],
        detail: dict[str, Any],
        research_percent: float,
        auto_dev_load: float,
        incident_count: int,
    ) -> dict[str, Any]:
        baseline = float(bandwidth.get("baseline_mbps", 0.0))
        peak = float(bandwidth.get("peak_mbps", baseline))
        average = float(bandwidth.get("average_mbps", peak))
        spread = max(0.0, peak - baseline)
        if peak <= 0.0:
            anchor_quality = 1.0
        else:
            anchor_quality = max(0.0, 1.0 - spread / max(peak, 1.0))
        layer_count = 3 if peak >= baseline + 4.0 or incident_count >= 2 else 2
        encrypted_channels = incident_count > 0 or research_percent >= 25.0
        spectral_load = min(1.0, max(0.0, (research_percent + auto_dev_load) / 120.0))
        throughput_index = peak * (1.0 + spectral_load * 0.6)
        detail.setdefault("spectral_load", round(spectral_load, 3))
        detail.setdefault("bandwidth_utilization_score", round(throughput_index, 2))
        channel_map = {
            "redundancy": "elevated" if layer_count >= 3 else "baseline",
            "stability_index": round(anchor_quality * (1.0 - spectral_load), 3),
        }
        triangulation_hint = {
            "axes": {
                "x": round(max(0.1, spread or baseline or 0.1), 3),
                "y": round(max(0.1, average or 0.1), 3),
                "z": round(max(0.1, spectral_load * 10.0), 3),
            },
            "normalized_spread": round(spread / max(peak, 1.0), 3) if peak else 0.0,
        }
        channel_vectors = {
            "alpha": round(anchor_quality * 0.82, 3),
            "beta": round(spectral_load * 0.94, 3),
            "gamma": round(max(0.0, average) / max(peak, 1.0) if peak else 0.0, 3),
        }
        phase_shift_map = {
            "incident_load": incident_count,
            "spectral_shift": round(spectral_load * 180.0, 2),
            "stability_phase": "locked" if anchor_quality >= 0.75 else "adaptive",
        }
        lithographic_signature = f"{layer_count}L-{int(anchor_quality * 100)}Q"
        return {
            "layer_count": layer_count,
            "anchor_quality": round(anchor_quality, 3),
            "encrypted_channels": encrypted_channels,
            "bandwidth_hint": round(average, 2),
            "spectral_load": round(spectral_load, 3),
            "throughput_index": round(throughput_index, 2),
            "channel_map": channel_map,
            "triangulation_hint": triangulation_hint,
            "channel_vectors": channel_vectors,
            "phase_shift_map": phase_shift_map,
            "lithographic_signature": lithographic_signature,
        }

    def _verification_layers(
        self,
        security: dict[str, Any],
        holographic: dict[str, Any],
    ) -> dict[str, Any]:
        incidents_by = dict(security.get("incidents_by_severity", {}))
        total_incidents = int(security.get("incidents", 0))
        if incidents_by:
            total_incidents = max(total_incidents, sum(int(v) for v in incidents_by.values()))
        severity_focus = tuple(level for level, count in incidents_by.items() if count)
        anchor_quality = float(holographic.get("anchor_quality", 0.0))
        risk = str(security.get("risk", "low")).lower()
        if risk == "critical" or anchor_quality < 0.6:
            integrity = "reinforce"
        elif risk == "high":
            integrity = "harden"
        else:
            integrity = "stable"
        return {
            "layers": int(holographic.get("layer_count", 0)),
            "integrity": integrity,
            "severity_focus": severity_focus,
            "anchor_quality": round(anchor_quality, 3),
            "incident_total": total_incidents,
        }

    def _upgrade_backlog(
        self,
        nodes: Sequence[dict[str, Any]],
        relay_plan: dict[str, Any],
        security: dict[str, Any],
        health: dict[str, Any],
    ) -> dict[str, Any]:
        tasks: list[str] = []
        trusted_relays = sum(1 for node in nodes if node.get("trusted", True))
        if relay_plan.get("needs_redundancy"):
            tasks.append("Provision additional trusted relay coverage")
        if trusted_relays < 2:
            tasks.append("Promote core nodes to trusted relays")
        if str(security.get("risk", "low")).lower() in {"high", "critical"}:
            tasks.append("Run security incident post-mortem")
        if health.get("status") in {"stressed", "degraded"}:
            tasks.append("Rebalance latency across peer nodes")
        priority = "low"
        if tasks:
            priority = "medium"
        if str(security.get("risk", "low")).lower() == "critical":
            priority = "high"
        if relay_plan.get("needs_redundancy") and health.get("status") == "degraded":
            priority = "high"
        return {
            "tasks": tuple(tasks),
            "priority": priority,
            "target_nodes": len(nodes),
        }

    def _security_auto_dev_brief(
        self,
        automation: dict[str, Any],
        backlog: dict[str, Any],
        verification: dict[str, Any],
    ) -> dict[str, Any]:
        automation_score = float(automation.get("automation_score", 0.0))
        layers = int(verification.get("layers", 0))
        directive = "stabilise"
        if automation_score >= 70.0 and layers >= 3:
            directive = "expand"
        elif backlog.get("priority") == "high":
            directive = "triage"
        elif automation_score <= 30.0:
            directive = "bootstrap"
        return {
            "directive": directive,
            "automation_score": round(automation_score, 2),
            "playbooks": tuple(automation.get("playbooks", ())),
            "backlog_priority": backlog.get("priority", "low"),
            "verification_layers": layers,
        }

    def _holographic_diagnostics(
        self,
        holographic: dict[str, Any],
        verification: dict[str, Any],
    ) -> dict[str, Any]:
        tri_hint = holographic.get("triangulation_hint", {})
        channel_map = dict(holographic.get("channel_map", {}))
        anchor_quality = float(holographic.get("anchor_quality", 0.0))
        integrity = verification.get("integrity", "stable")
        spectral_load = float(holographic.get("spectral_load", 0.0))
        stability_index = float(channel_map.get("stability_index", 0.0))
        efficiency_score = max(
            0.0,
            min(100.0, anchor_quality * 70.0 + stability_index * 120.0 - spectral_load * 25.0),
        )
        phase_map = holographic.get("phase_shift_map", {})
        spectral_shift = float(phase_map.get("spectral_shift", 0.0))
        stability_phase = str(phase_map.get("stability_phase", "adaptive"))
        coherence = max(0.0, 100.0 - abs(90.0 - spectral_shift) * 0.2)
        if stability_phase == "locked":
            coherence = min(100.0, coherence + 5.0)
        return {
            "triangulation_hint": tri_hint,
            "anchor_quality": anchor_quality,
            "spectral_load": spectral_load,
            "verification_integrity": integrity,
            "stability_index": stability_index,
            "phase_sync": spectral_shift,
            "efficiency_score": round(efficiency_score, 2),
            "phase_coherence_index": round(coherence, 2),
            "stability_phase": stability_phase,
        }

    def _resilience_matrix(
        self,
        health: dict[str, Any],
        reliability: dict[str, Any],
        security: dict[str, Any],
    ) -> dict[str, Any]:
        score = float(health.get("score", 0.0))
        uptime = float(reliability.get("average_uptime", 0.0))
        risk = str(security.get("risk", "low")).lower()
        hardening = "baseline"
        if risk in {"high", "critical"} or score < 45.0:
            hardening = "urgent"
        elif score < 70.0:
            hardening = "recommended"
        vector = "stability"
        if uptime < self.uptime_target:
            vector = "redundancy"
        elif risk in {"high", "critical"}:
            vector = "security"
        return {
            "score": round(score, 2),
            "uptime": round(uptime, 3),
            "risk": risk,
            "hardening": hardening,
            "primary_vector": vector,
        }

    def _zero_trust_blueprint(
        self,
        security_auto_dev: dict[str, Any],
        security: dict[str, Any],
    ) -> dict[str, Any]:
        directive = security_auto_dev.get("directive", "stabilise")
        incidents = int(security.get("incidents", 0))
        layers = security_auto_dev.get("verification_layers", 0)
        blueprint = "baseline"
        if directive in {"triage", "mitigate"} or incidents >= 3:
            blueprint = "containment"
        elif directive == "expand" and layers >= 3:
            blueprint = "proactive"
        actions: list[str] = []
        if incidents:
            actions.append("Audit session tokens")
        if layers < 2:
            actions.append("Deploy additional verification layers")
        if directive in {"triage", "bootstrap"}:
            actions.append("Rotate keys across relays")
        if not actions:
            actions.append("Maintain zero-trust baseline")
        return {
            "blueprint": blueprint,
            "directive": directive,
            "actions": tuple(dict.fromkeys(actions)),
            "verification_layers": layers,
        }

    def _anomaly_signals(
        self,
        events: Sequence[dict[str, Any]],
        nodes: Sequence[dict[str, Any]],
    ) -> dict[str, Any]:
        anomaly_types = sorted({str(event.get("type", "unknown")) for event in events})
        severity_counts: dict[str, int] = {}
        for event in events:
            severity = str(event.get("severity", "low")).lower()
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        trusted = sum(1 for node in nodes if node.get("trusted", True))
        untrusted = sum(1 for node in nodes if not node.get("trusted", True))
        return {
            "anomaly_types": _as_tuple(anomaly_types),
            "severity_counts": severity_counts,
            "trusted_nodes": trusted,
            "untrusted_nodes": untrusted,
        }

    def _holographic_signal_matrix(
        self,
        holographic: dict[str, Any],
        verification: dict[str, Any],
    ) -> dict[str, Any]:
        channel_map = dict(holographic.get("channel_map", {}))
        vectors = dict(holographic.get("channel_vectors", {}))
        layer_count = int(holographic.get("layer_count", 0))
        integrity = verification.get("integrity", "stable")
        redundancy = channel_map.get("redundancy", "baseline")
        stability_index = channel_map.get("stability_index", 0.0)
        return {
            "layers": layer_count,
            "redundancy": redundancy,
            "integrity": integrity,
            "vectors": vectors,
            "stability_index": stability_index,
        }

    def _upgrade_paths(
        self,
        backlog: dict[str, Any],
        security_auto_dev: dict[str, Any],
        holographic: dict[str, Any],
    ) -> tuple[str, ...]:
        """Return recommended upgrade paths blending security and holographic data."""

        paths: list[str] = []
        priority = backlog.get("priority")
        if priority in {"high", "medium"} and backlog.get("tasks"):
            paths.append("Execute backlog tasks")
        directive = security_auto_dev.get("directive")
        if directive in {"triage", "bootstrap"}:
            paths.append("Deploy rapid hardening playbooks")
        if holographic.get("layer_count", 0) >= 3:
            paths.append("Expand holographic lattice throughput")
        if holographic.get("phase_shift_map", {}).get("stability_phase") == "adaptive":
            paths.append("Stabilise lithographic anchors")
        if not paths:
            paths.append("Maintain upgrade cadence")
        return tuple(dict.fromkeys(paths))

    def _extract_research_percent(self, research: dict[str, Any] | None) -> float:
        if not research:
            return 0.0
        for key in (
            "raw_utilization_percent",
            "latest_sample_percent",
            "utilization_percent",
        ):
            value = research.get(key)
            if value is not None:
                return float(value)
        return 0.0

    def _network_security_score(
        self,
        security_auto_dev: dict[str, Any],
        security: dict[str, Any],
        verification: dict[str, Any],
    ) -> float:
        base = float(security_auto_dev.get("automation_score", 0.0))
        incidents = int(security.get("incidents", 0))
        layers = int(verification.get("layers", 0))
        modifier = layers * 4.5 - incidents * 3.5
        risk = str(security.get("risk", "low")).lower()
        if risk == "high":
            modifier -= 6.0
        elif risk == "critical":
            modifier -= 12.0
        score = max(0.0, min(100.0, base + modifier))
        return round(score, 2)

    def _network_security_upgrades(
        self,
        security_auto_dev: dict[str, Any],
        backlog: dict[str, Any],
    ) -> tuple[str, ...]:
        upgrades: list[str] = []
        directive = security_auto_dev.get("directive", "stabilise")
        if directive in {"triage", "bootstrap"}:
            upgrades.append("Accelerate zero-trust hardening")
        if backlog.get("priority") in {"medium", "high"}:
            upgrades.append("Clear security upgrade backlog")
        if security_auto_dev.get("verification_layers", 0) < 3:
            upgrades.append("Deploy additional verification layers")
        if float(security_auto_dev.get("network_security_score", 0.0)) < 55.0:
            upgrades.append("Raise automated security scoring")
        if not upgrades:
            upgrades.append("Maintain security automation cadence")
        return tuple(dict.fromkeys(upgrades))

    def _holographic_enhancements(
        self,
        holographic: dict[str, Any],
        security_auto_dev: dict[str, Any],
        verification: dict[str, Any],
    ) -> dict[str, Any]:
        phase_shift = holographic.get("phase_shift_map", {})
        stability_phase = phase_shift.get("stability_phase", "adaptive")
        directive = security_auto_dev.get("directive", "stabilise")
        layers = int(holographic.get("layer_count", 0))
        integrity = verification.get("integrity", "stable")
        enhancements: list[str] = []
        if stability_phase == "adaptive":
            enhancements.append("Calibrate spectral anchors")
        if layers < 3:
            enhancements.append("Expand holographic lattice layers")
        if directive in {"triage", "mitigate"}:
            enhancements.append("Increase encrypted holographic redundancy")
        if integrity == "reinforce":
            enhancements.append("Reinforce verification integrity")
        if not enhancements:
            enhancements.append("Maintain holographic throughput balance")
        return {
            "actions": tuple(dict.fromkeys(enhancements)),
            "stability_phase": stability_phase,
            "verification_integrity": integrity,
            "layer_count": layers,
        }

    def _transmission_guardrails(
        self,
        diagnostics: dict[str, Any],
        verification: dict[str, Any],
        health: dict[str, Any],
        security_auto_dev: dict[str, Any],
        enhancements: dict[str, Any],
    ) -> dict[str, Any]:
        phase = float(diagnostics.get("phase_coherence_index", 0.0))
        efficiency = float(diagnostics.get("efficiency_score", 0.0))
        integrity = str(verification.get("integrity", "stable"))
        status = str(health.get("status", "stable"))
        directive = str(security_auto_dev.get("directive", "stabilise"))
        stability_phase = str(enhancements.get("stability_phase", "adaptive"))
        guardrail_state = "nominal"
        actions: list[str] = []
        if phase < 65.0 or integrity != "stable":
            guardrail_state = "reinforce"
            actions.append("Lock spectral anchors to reduce drift")
        if efficiency < 55.0:
            guardrail_state = "reinforce"
            actions.append("Throttle non-critical holographic channels")
        if stability_phase == "adaptive" and directive in {"triage", "bootstrap"}:
            actions.append("Mirror lithographic packets across redundant relays")
        if status in {"degraded", "stressed"}:
            actions.append("Route holographic traffic through resilience vector")
        if not actions:
            actions.append("Maintain holographic guardrails")
        severity = "monitor"
        if phase < 55.0 or efficiency < 45.0:
            severity = "critical"
        elif phase < 70.0 or efficiency < 60.0 or guardrail_state != "nominal":
            severity = "elevated"
        return {
            "status": guardrail_state,
            "severity": severity,
            "actions": tuple(dict.fromkeys(actions)),
            "phase_coherence": round(phase, 2),
            "efficiency": round(efficiency, 2),
        }

    def _lithographic_integrity(
        self,
        diagnostics: dict[str, Any],
        guardrails: dict[str, Any],
    ) -> dict[str, Any]:
        efficiency = float(diagnostics.get("efficiency_score", 0.0))
        phase = float(diagnostics.get("phase_coherence_index", 0.0))
        baseline = max(0.0, min(100.0, efficiency * 0.45 + phase * 0.55))
        severity = guardrails.get("severity", "monitor")
        adjustment = 0.0
        if severity == "critical":
            adjustment = -18.0
        elif severity == "elevated":
            adjustment = -9.0
        score = max(0.0, min(100.0, baseline + adjustment))
        recommendation: tuple[str, ...] = guardrails.get("actions", ())  # type: ignore[assignment]
        headline = recommendation[0] if recommendation else "Maintain guardrails"
        return {
            "score": round(score, 2),
            "severity": severity,
            "headline_action": headline,
        }
