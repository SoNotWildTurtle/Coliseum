"""Security orchestration manager for the auto-dev pipeline."""

from __future__ import annotations

from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_tuple(values: Sequence[Any] | None) -> tuple[Any, ...]:
    if not values:
        return ()
    return tuple(values)


class AutoDevSecurityManager:
    """Derive actionable hardening steps from pipeline telemetry."""

    def security_brief(
        self,
        *,
        network: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        guidance: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Summarise network security posture and downstream tasks."""

        network = network or {}
        codebase = codebase or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        research = research or {}
        guidance = guidance or {}

        security_score = _as_float(network.get("network_security_score"))
        guardrail_status = str(
            (network.get("transmission_guardrails") or {}).get("status", "nominal")
        )
        anomaly_signals = tuple(network.get("anomaly_signals", ()))
        mitigation_priority = str(mitigation.get("priority", "monitor"))
        projected_security = _as_float(
            (remediation.get("stability_projection") or {}).get(
                "projected_security_score", security_score
            )
        )

        threat_level = self._threat_level(
            security_score,
            guardrail_status,
            mitigation_priority,
            len(anomaly_signals),
        )
        automation = self._automation_directives(network, mitigation)
        hardening = self._hardening_tasks(codebase, remediation)
        lattice = self._holographic_lattice(network, remediation, mitigation_priority)
        intel = self._intel_brief(
            research,
            codebase,
            threat_level,
            mitigation_priority,
        )
        network_actions = self._network_security_actions(network, automation, hardening)
        governance = self._governance_alignment(guidance, mitigation, threat_level)

        return {
            "threat_level": threat_level,
            "security_score": round(security_score, 2),
            "projected_security_score": round(projected_security, 2),
            "guardrail_status": guardrail_status,
            "anomaly_signals": anomaly_signals,
            "automation_directives": automation,
            "hardening_tasks": hardening,
            "holographic_lattice": lattice,
            "intel_brief": intel,
            "network_security_actions": network_actions,
            "governance_alignment": governance,
        }

    def _threat_level(
        self,
        security_score: float,
        guardrail_status: str,
        mitigation_priority: str,
        anomaly_count: int,
    ) -> str:
        guardrail_status = guardrail_status.lower()
        priority = mitigation_priority.lower()
        if security_score >= 80.0 and guardrail_status in {"nominal", "stable"}:
            return "fortified"
        if security_score < 50.0 or guardrail_status in {"reinforce", "critical"}:
            return "at-risk"
        if anomaly_count >= 2 or priority in {"high", "critical"}:
            return "elevated"
        return "guarded"

    def _automation_directives(
        self,
        network: Mapping[str, Any],
        mitigation: Mapping[str, Any],
    ) -> dict[str, Any]:
        security_auto_dev = dict(network.get("security_auto_dev", {}))
        zero_trust = dict(network.get("zero_trust_blueprint", {}))
        backlog = dict(network.get("upgrade_backlog", {}))
        playbooks = list(security_auto_dev.get("playbooks", ()))
        upgrades = list(mitigation.get("network_tasks", ()))
        if backlog.get("tasks"):
            for task in backlog["tasks"]:  # type: ignore[index]
                playbooks.append(str(task))
        directive = str(security_auto_dev.get("directive", "stabilise"))
        return {
            "directive": directive,
            "automation_score": _as_float(security_auto_dev.get("automation_score")),
            "playbooks": tuple(dict.fromkeys(playbooks))
            or ("Maintain baseline scanning",),
            "zero_trust": {
                "status": zero_trust.get("status", "pilot"),
                "focus": zero_trust.get("focus", ()),
            },
            "backlog_priority": backlog.get("priority", "low"),
            "mitigation_priority": mitigation.get("priority", "monitor"),
        }

    def _hardening_tasks(
        self,
        codebase: Mapping[str, Any],
        remediation: Mapping[str, Any],
    ) -> tuple[dict[str, Any], ...]:
        scorecards: Sequence[Mapping[str, Any]] = codebase.get(
            "module_scorecards", ()
        )  # type: ignore[assignment]
        progress: Sequence[Mapping[str, Any]] = remediation.get(
            "codebase_progress", ()
        )  # type: ignore[assignment]
        addressed = {str(entry.get("name")) for entry in progress if entry.get("addressed")}
        tasks: list[dict[str, Any]] = []
        for card in scorecards:
            risk = str(card.get("risk_level", "low"))
            if risk in {"low"}:
                continue
            name = str(card.get("name", "module"))
            tasks.append(
                {
                    "module": name,
                    "risk_level": risk,
                    "recommended_actions": tuple(card.get("recommended_actions", ())),
                    "addressed": name in addressed,
                    "stability_modifier": card.get("stability_modifier", 0.0),
                }
            )
        return tuple(tasks)

    def _holographic_lattice(
        self,
        network: Mapping[str, Any],
        remediation: Mapping[str, Any],
        mitigation_priority: str,
    ) -> dict[str, Any]:
        diagnostics = dict(network.get("holographic_diagnostics", {}))
        enhancements = dict(network.get("holographic_enhancements", {}))
        adjustments = _as_tuple(remediation.get("holographic_adjustments"))
        efficiency = _as_float(diagnostics.get("efficiency_score")) / 100.0
        phase = _as_float(diagnostics.get("phase_coherence_index")) / 100.0
        density = max(0.2, min(1.0, (efficiency + phase) / 2.0))
        coherence = max(0.0, min(1.0, phase + 0.1))
        stability = "stable"
        if coherence < 0.55:
            stability = "drifting"
        if coherence < 0.4 or mitigation_priority.lower() in {"high", "critical"}:
            stability = "reinforce"
        actions: list[str] = []
        phase_directive = enhancements.get("phase_lock_directives")
        if phase_directive:
            actions.append(str(phase_directive))
        layer_upgrades: Sequence[str] = enhancements.get("layer_upgrades", ())  # type: ignore[assignment]
        for upgrade in layer_upgrades[:2]:
            actions.append(f"Integrate holographic layer: {upgrade}")
        for adjustment in adjustments[:3]:
            actions.append(str(adjustment))
        if not actions:
            actions.append("Maintain holographic lattice monitors")
        return {
            "density": round(density, 3),
            "coherence": round(coherence, 3),
            "stability": stability,
            "actions": tuple(dict.fromkeys(actions)),
            "spectral_priority": mitigation_priority,
        }

    def _intel_brief(
        self,
        research: Mapping[str, Any],
        codebase: Mapping[str, Any],
        threat_level: str,
        mitigation_priority: str,
    ) -> dict[str, Any]:
        latest = research.get("latest_sample_percent")
        if latest is None:
            latest = research.get("raw_utilization_percent")
        coverage = _as_float(codebase.get("coverage_ratio"))
        instability = _as_float(codebase.get("instability_index"))
        trend = str(research.get("trend_direction", "stable"))
        pressure = _as_float(research.get("research_pressure_index"))
        return {
            "threat_level": threat_level,
            "research_utilization_percent": round(_as_float(latest), 2),
            "trend_direction": trend,
            "coverage_ratio": round(coverage, 2),
            "instability_index": round(instability, 2),
            "pressure_index": round(pressure, 2),
            "mitigation_priority": mitigation_priority,
        }

    def _network_security_actions(
        self,
        network: Mapping[str, Any],
        automation: Mapping[str, Any],
        hardening: Sequence[Mapping[str, Any]],
    ) -> tuple[str, ...]:
        upgrades = list(network.get("network_security_upgrades", ()))
        backlog = list((network.get("upgrade_backlog") or {}).get("tasks", ()))
        playbooks = list(automation.get("playbooks", ()))
        if hardening:
            upgrades.append("Coordinate with codebase hardening tasks")
        combined = [str(item) for item in (*playbooks, *backlog, *upgrades) if item]
        if not combined:
            combined.append("Maintain baseline network monitoring")
        return tuple(dict.fromkeys(combined))

    def _governance_alignment(
        self,
        guidance: Mapping[str, Any],
        mitigation: Mapping[str, Any],
        threat_level: str,
    ) -> dict[str, Any]:
        outlook = str(guidance.get("governance_outlook", "guidance-monitor"))
        alignment = float(guidance.get("backend_alignment_score", 0.0))
        priority = str(mitigation.get("priority", "monitor"))
        status = "aligned"
        if alignment < 45.0 or outlook.endswith("oversight"):
            status = "oversight"
        elif threat_level == "at-risk" and priority not in {"high", "critical"}:
            status = "escalate"
        return {
            "status": status,
            "outlook": outlook,
            "alignment_score": round(alignment, 2),
            "mitigation_priority": priority,
        }
