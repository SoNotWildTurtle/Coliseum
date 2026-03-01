"""Assess resilience of the auto-dev loop using multi-domain telemetry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalise_sequence(values: Sequence[Any] | None) -> tuple[Mapping[str, Any], ...]:
    normalised: list[Mapping[str, Any]] = []
    for value in values or ():
        if isinstance(value, Mapping):
            normalised.append(value)
    return tuple(normalised)


def _count_domains(fixes: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    counts = {"codebase": 0, "network": 0, "research": 0, "guidance": 0}
    for fix in fixes:
        domain = str(fix.get("domain", "")).lower()
        if domain in counts:
            counts[domain] += 1
    return counts


@dataclass
class AutoDevResilienceManager:
    """Combine telemetry to score resilience and surface stabilisation advice."""

    codebase_weight: float = 0.4
    network_weight: float = 0.35
    remediation_weight: float = 0.15
    research_penalty_weight: float = 0.1

    def assess_resilience(
        self,
        *,
        codebase: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        guidance: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a resilience brief that links applied fixes to stability posture."""

        codebase = codebase or {}
        network = network or {}
        research = research or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        guidance = guidance or {}

        coverage = _as_float(codebase.get("coverage_ratio"))
        instability = _as_float(codebase.get("instability_index"))
        debt_risk = _as_float(codebase.get("debt_risk_score"))

        security_score = _as_float(network.get("network_security_score"))
        reliability = network.get("reliability", {})  # type: ignore[assignment]
        uptime = _as_float(reliability.get("average_uptime"))
        network_health = network.get("network_health", {})  # type: ignore[assignment]
        network_status = str(network_health.get("status", "stable"))
        guardrails = network.get("transmission_guardrails", {})  # type: ignore[assignment]
        guardrail_severity = str(guardrails.get("severity", "monitor"))
        holographic = network.get("holographic_diagnostics", {})  # type: ignore[assignment]
        phase = _as_float(holographic.get("phase_coherence_index"))
        efficiency = _as_float(holographic.get("efficiency_score"))

        research_pressure = _as_float(research.get("research_pressure_index"))
        utilisation = _as_float(
            research.get("latest_sample_percent")
            or research.get("raw_utilization_percent"),
        )
        trend = str(research.get("trend_direction", "stable"))

        mitigation_priority = str(mitigation.get("priority", "monitor"))
        mitigation_score = _as_float(mitigation.get("stability_score"))
        network_tasks = len(mitigation.get("network_tasks", ()))  # type: ignore[arg-type]
        codebase_tasks = len(mitigation.get("codebase_tasks", ()))  # type: ignore[arg-type]

        applied_fixes = _normalise_sequence(remediation.get("applied_fixes"))
        scheduled_fixes = _normalise_sequence(remediation.get("scheduled_fixes"))
        applied_counts = _count_domains(applied_fixes)
        scheduled_counts = _count_domains(scheduled_fixes)

        index = self._resilience_index(
            coverage,
            security_score,
            uptime,
            guardrail_severity,
            mitigation_score,
            instability,
            research_pressure,
            utilisation,
            mitigation_priority,
            network_status,
            applied_counts,
        )
        grade = self._grade(index)

        stability_projection = remediation.get("stability_projection", {})
        resilience_actions = self._resilience_actions(
            coverage,
            security_score,
            guardrail_severity,
            research_pressure,
            utilisation,
            mitigation_priority,
            applied_counts,
        )
        stability_risks = self._stability_risks(
            coverage,
            security_score,
            network_status,
            research_pressure,
            utilisation,
            trend,
            debt_risk,
            instability,
        )
        holographic_readiness = self._holographic_readiness(
            phase,
            efficiency,
            guardrail_severity,
            resilience_actions,
        )
        network_security_focus = self._network_security_focus(
            security_score,
            network,
            guardrail_severity,
            network_tasks,
        )
        managerial_overwatch = self._managerial_overwatch(
            guidance,
            grade,
            scheduled_counts,
            mitigation_priority,
        )

        return {
            "resilience_index": index,
            "resilience_score": round(index * 100.0, 1),
            "grade": grade,
            "stability_risks": stability_risks,
            "resilience_actions": resilience_actions,
            "applied_fix_counts": applied_counts,
            "scheduled_fix_counts": scheduled_counts,
            "stability_projection": {
                "baseline_security": _as_float(
                    stability_projection.get("security_score")
                ),
                "projected_security": _as_float(
                    stability_projection.get("projected_security_score")
                ),
                "projected_coverage": _as_float(
                    stability_projection.get("projected_coverage")
                ),
            },
            "holographic_readiness": holographic_readiness,
            "network_security_focus": network_security_focus,
            "managerial_overwatch": managerial_overwatch,
            "research_penalty": round(
                self._research_penalty(research_pressure, utilisation),
                3,
            ),
            "mitigation_overview": {
                "priority": mitigation_priority,
                "stability_score": round(mitigation_score, 2),
                "codebase_tasks": codebase_tasks,
                "network_tasks": network_tasks,
            },
        }

    def _resilience_index(
        self,
        coverage: float,
        security_score: float,
        uptime: float,
        guardrail_severity: str,
        mitigation_score: float,
        instability: float,
        research_pressure: float,
        utilisation: float,
        mitigation_priority: str,
        network_status: str,
        applied_counts: Mapping[str, int],
    ) -> float:
        security_component = (security_score / 100.0) * self.network_weight
        coverage_component = coverage * self.codebase_weight
        uptime_component = min(0.25, max(0.0, uptime) * 0.25)
        remediation_component = min(
            self.remediation_weight,
            applied_counts.get("codebase", 0) * 0.05
            + applied_counts.get("network", 0) * 0.04
            + applied_counts.get("research", 0) * 0.03,
        )
        guardrail_bonus = 0.0
        severity = guardrail_severity.lower()
        if severity in {"reinforce", "harden"}:
            guardrail_bonus = 0.05
        elif severity in {"monitor", "balanced"}:
            guardrail_bonus = 0.03
        mitigation_bonus = min(0.05, mitigation_score / 200.0)
        penalty = self._penalty(
            instability,
            research_pressure,
            utilisation,
            mitigation_priority,
            network_status,
            security_score,
        )
        index = (
            coverage_component
            + security_component
            + uptime_component
            + remediation_component
            + guardrail_bonus
            + mitigation_bonus
            - penalty
        )
        return max(0.0, min(1.0, round(index, 3)))

    def _penalty(
        self,
        instability: float,
        research_pressure: float,
        utilisation: float,
        mitigation_priority: str,
        network_status: str,
        security_score: float,
    ) -> float:
        penalty = min(0.2, max(0.0, instability) * 0.06)
        penalty += self._research_penalty(research_pressure, utilisation)
        if security_score < 60.0:
            penalty += 0.08
        elif security_score < 70.0:
            penalty += 0.04
        priority = mitigation_priority.lower()
        if priority in {"high", "critical"}:
            penalty += 0.06
        status = network_status.lower()
        if status in {"degraded", "critical"}:
            penalty += 0.08
        return penalty

    def _research_penalty(self, pressure: float, utilisation: float) -> float:
        penalty = 0.0
        if pressure > 45.0:
            penalty += min(
                self.research_penalty_weight,
                (pressure - 45.0) / 55.0 * self.research_penalty_weight,
            )
        if utilisation > 65.0:
            penalty += min(0.06, (utilisation - 65.0) / 35.0 * 0.06)
        return penalty

    def _grade(self, index: float) -> str:
        if index >= 0.82:
            return "fortified"
        if index >= 0.68:
            return "resilient"
        if index >= 0.5:
            return "steady"
        if index >= 0.35:
            return "vigilant"
        return "at-risk"

    def _resilience_actions(
        self,
        coverage: float,
        security_score: float,
        guardrail_severity: str,
        research_pressure: float,
        utilisation: float,
        mitigation_priority: str,
        applied_counts: Mapping[str, int],
    ) -> tuple[str, ...]:
        actions: list[str] = []
        if coverage < 0.75:
            actions.append("Boost regression coverage for brittle modules")
        if security_score < 72.0:
            actions.append("Accelerate network security automation rollout")
        if guardrail_severity.lower() not in {"monitor", "balanced"}:
            actions.append("Review lithographic guardrail adherence with ops")
        if research_pressure > 55.0:
            actions.append("Throttle rival-game studies until pressure normalises")
        if utilisation > 70.0:
            actions.append("Rebalance processing toward encounter preparation")
        if mitigation_priority.lower() in {"high", "critical"}:
            actions.append("Keep mitigation crew on accelerated cadence")
        if applied_counts.get("network", 0) == 0 and security_score < 80.0:
            actions.append("Schedule immediate network hardening task")
        if not actions:
            actions.append("Maintain current resilience posture")
        return tuple(dict.fromkeys(actions))

    def _stability_risks(
        self,
        coverage: float,
        security_score: float,
        network_status: str,
        research_pressure: float,
        utilisation: float,
        trend: str,
        debt_risk: float,
        instability: float,
    ) -> tuple[str, ...]:
        risks: list[str] = []
        if coverage < 0.7:
            risks.append("Coverage below resilience threshold")
        if security_score < 65.0:
            risks.append("Network security posture vulnerable")
        if network_status.lower() in {"degraded", "critical"}:
            risks.append(f"Network health reports {network_status}")
        if research_pressure > 60.0:
            risks.append("Research pressure exceeding comfort band")
        if utilisation > 75.0:
            risks.append("Processing utilisation dominated by research")
        if trend.lower() in {"rising", "spiking"}:
            risks.append("Research trend escalating")
        if debt_risk >= 4.0:
            risks.append("Technical debt risk critical")
        elif debt_risk >= 2.5:
            risks.append("Technical debt risk elevated")
        if instability >= 1.5:
            risks.append("Instability index signalling volatility")
        if not risks:
            risks.append("No acute stability risks detected")
        return tuple(dict.fromkeys(risks))

    def _holographic_readiness(
        self,
        phase: float,
        efficiency: float,
        guardrail_severity: str,
        actions: Sequence[str],
    ) -> dict[str, Any]:
        severity = guardrail_severity.lower()
        if phase < 0.6 or severity in {"reinforce", "harden"}:
            status = "intervene"
        elif phase < 0.72 or efficiency < 0.6:
            status = "tune"
        else:
            status = "stable"
        recommended = [action for action in actions if "lithographic" in action.lower()]
        if not recommended and status != "stable":
            recommended.append("Add holographic tuning to mitigation follow-ups")
        return {
            "phase_coherence": round(phase, 2),
            "efficiency": round(efficiency, 2),
            "guardrail_severity": guardrail_severity,
            "status": status,
            "recommended_actions": tuple(dict.fromkeys(recommended)),
        }

    def _network_security_focus(
        self,
        security_score: float,
        network: Mapping[str, Any],
        guardrail_severity: str,
        network_tasks: int,
    ) -> dict[str, Any]:
        automation = network.get("security_auto_dev", {})  # type: ignore[assignment]
        zero_trust = network.get("zero_trust_blueprint", {})  # type: ignore[assignment]
        upgrade_paths = network.get("upgrade_paths", ())
        return {
            "security_score": round(security_score, 2),
            "automation_directive": automation.get("directive", "monitor"),
            "zero_trust_tier": zero_trust.get("tier", "baseline"),
            "guardrail_severity": guardrail_severity,
            "queued_network_tasks": network_tasks,
            "recommended_upgrades": tuple(upgrade_paths)[:3],
        }

    def _managerial_overwatch(
        self,
        guidance: Mapping[str, Any],
        grade: str,
        scheduled_counts: Mapping[str, int],
        mitigation_priority: str,
    ) -> dict[str, Any]:
        threads = guidance.get("managerial_threads", ())
        return {
            "governance_outlook": guidance.get("governance_outlook", "guidance-monitor"),
            "priority": guidance.get("priority", "low"),
            "resilience_grade": grade,
            "backend_alignment": guidance.get("backend_alignment_score", 0.0),
            "managerial_threads": tuple(threads)[:4],
            "scheduled_followups": {
                "codebase": scheduled_counts.get("codebase", 0),
                "network": scheduled_counts.get("network", 0),
                "research": scheduled_counts.get("research", 0),
                "guidance": scheduled_counts.get("guidance", 0),
            },
            "mitigation_priority": mitigation_priority,
        }
