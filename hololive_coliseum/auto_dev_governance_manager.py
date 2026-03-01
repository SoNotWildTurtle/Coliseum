"""Blend managerial intelligence signals into an actionable governance brief."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalise_actions(values: Sequence[Any] | None) -> tuple[str, ...]:
    normalised: list[str] = []
    for value in values or ():
        text = str(value).strip()
        if text:
            normalised.append(text)
    return tuple(dict.fromkeys(normalised))


def _threat_modifier(threat: str) -> float:
    match threat.lower():
        case "critical":
            return -12.0
        case "severe" | "high":
            return -8.0
        case "elevated":
            return -4.0
        case "guarded" | "monitored":
            return 0.0
        case _:
            return -2.0


def _governance_state(score: float) -> str:
    if score >= 82.0:
        return "autonomous"
    if score >= 70.0:
        return "directed"
    if score >= 55.0:
        return "guided"
    return "needs-oversight"


@dataclass
class AutoDevGovernanceManager:
    """Convert pipeline telemetry into backend governance directives."""

    baseline_score: float = 68.0
    debt_penalty_scale: float = 24.0
    holographic_threshold: float = 60.0

    def governance_brief(
        self,
        *,
        guidance: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        continuity: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic governance snapshot for leadership."""

        guidance = guidance or {}
        network = network or {}
        security = security or {}
        continuity = continuity or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        resilience = resilience or {}
        codebase = codebase or {}
        transmission = transmission or {}

        alignment = _as_float(guidance.get("backend_alignment_score", 0.0))
        risk_index = _as_float(guidance.get("risk_index", 0.0))
        priority = str(guidance.get("priority", "low"))
        governance_outlook = str(guidance.get("governance_outlook", "guidance-monitor"))

        network_security = max(0.0, min(100.0, _as_float(network.get("network_security_score"))))
        projected_security = _as_float(
            security.get("projected_security_score"),
            _as_float(network.get("network_security_score")),
        )
        security_score = _as_float(security.get("security_score"), network_security)
        threat_level = str(security.get("threat_level", "guarded"))

        continuity_index = _as_float(continuity.get("continuity_index", 0.0))
        continuity_percent = round(max(0.0, min(1.0, continuity_index)) * 100.0, 1)

        resilience_score = _as_float(resilience.get("resilience_score", security_score))
        resilience_grade = str(resilience.get("grade", "vigilant"))

        debt_risk = _as_float(codebase.get("debt_risk_score", 0.0))
        modernization_targets: Sequence[Mapping[str, Any]] = codebase.get(
            "modernization_targets", ()
        )  # type: ignore[assignment]

        stability_projection: Mapping[str, Any] = remediation.get(
            "stability_projection", {}
        )  # type: ignore[assignment]
        projected_security = _as_float(
            stability_projection.get("projected_security_score"), projected_security
        )
        holographic = transmission.get("lithographic_integrity", {})  # type: ignore[assignment]
        holographic_score = _as_float(holographic.get("score", 0.0))
        guardrails = transmission.get("guardrails", {})  # type: ignore[assignment]
        waveform = transmission.get("spectral_waveform", {})  # type: ignore[assignment]

        score = self._oversight_score(
            network_security,
            projected_security,
            alignment,
            continuity_percent,
            resilience_score,
            debt_risk,
            holographic_score,
            threat_level,
        )
        state = _governance_state(score)

        oversight_actions = self._oversight_actions(
            network_security,
            threat_level,
            debt_risk,
            holographic_score,
            mitigation.get("network_tasks"),
            guardrails.get("actions"),
        )
        risk_flags = self._risk_flags(
            network_security,
            threat_level,
            debt_risk,
            continuity_percent,
            governance_outlook,
        )
        codebase_directives = self._codebase_directives(modernization_targets)
        holographic_directives = self._holographic_directives(
            guardrails,
            waveform,
            remediation.get("holographic_adjustments"),
        )
        managerial_backlog = self._managerial_backlog(
            mitigation.get("codebase_tasks"),
            mitigation.get("network_tasks"),
            continuity.get("codebase_continuity_actions"),
        )

        backend_support_map = {
            "alignment_score": round(alignment, 2),
            "network_security_score": round(network_security, 2),
            "security_projection": round(projected_security, 2),
            "resilience_score": round(resilience_score, 2),
            "resilience_grade": resilience_grade,
            "continuity_percent": continuity_percent,
            "holographic_score": round(holographic_score, 2),
        }

        managerial_focus = {
            "priority": priority,
            "governance_outlook": governance_outlook,
            "risk_index": round(risk_index, 2),
            "threat_level": threat_level,
        }

        return {
            "oversight_score": score,
            "state": state,
            "oversight_actions": oversight_actions,
            "risk_flags": risk_flags,
            "backend_support_map": backend_support_map,
            "managerial_focus": managerial_focus,
            "codebase_directives": codebase_directives,
            "holographic_directives": holographic_directives,
            "managerial_backlog": managerial_backlog,
        }

    def _oversight_score(
        self,
        network_security: float,
        projected_security: float,
        alignment: float,
        continuity_percent: float,
        resilience_score: float,
        debt_risk: float,
        holographic_score: float,
        threat_level: str,
    ) -> float:
        score = self.baseline_score
        score += (network_security - 60.0) * 0.22
        score += (projected_security - network_security) * 0.08
        score += (alignment - 55.0) * 0.12
        score += (continuity_percent - 55.0) * 0.1
        score += (resilience_score - 60.0) * 0.08
        score -= min(1.0, max(0.0, debt_risk)) * self.debt_penalty_scale
        score += (holographic_score - self.holographic_threshold) * 0.05
        score += _threat_modifier(threat_level)
        return round(max(0.0, min(100.0, score)), 2)

    def _oversight_actions(
        self,
        network_security: float,
        threat_level: str,
        debt_risk: float,
        holographic_score: float,
        network_tasks: Sequence[Any] | None,
        guardrail_actions: Sequence[Any] | None,
    ) -> tuple[str, ...]:
        actions: list[str] = []
        if network_security < 65.0:
            actions.append("Accelerate network hardening playbook")
        if threat_level.lower() in {"critical", "severe", "high", "elevated"}:
            actions.append("Escalate security watch rotations")
        if debt_risk >= 0.4:
            actions.append("Approve codebase stabilisation sprint")
        if holographic_score < self.holographic_threshold:
            actions.append("Deploy holographic lattice reinforcement cycle")
        actions.extend(_normalise_actions(network_tasks))
        actions.extend(_normalise_actions(guardrail_actions))
        if not actions:
            actions.append("Maintain current oversight cadence")
        return tuple(dict.fromkeys(actions))

    def _risk_flags(
        self,
        network_security: float,
        threat_level: str,
        debt_risk: float,
        continuity_percent: float,
        governance_outlook: str,
    ) -> tuple[str, ...]:
        flags: list[str] = []
        if network_security < 60.0:
            flags.append("network")
        if threat_level.lower() in {"critical", "severe", "high"}:
            flags.append("security")
        if debt_risk >= 0.45:
            flags.append("codebase")
        if continuity_percent < 55.0:
            flags.append("continuity")
        if governance_outlook not in {"guidance-autonomous", "guidance-direct"}:
            flags.append("oversight")
        if not flags:
            flags.append("balanced")
        return tuple(dict.fromkeys(flags))

    def _codebase_directives(
        self,
        modernization_targets: Sequence[Mapping[str, Any]] | None,
    ) -> tuple[dict[str, Any], ...]:
        directives: list[dict[str, Any]] = []
        for target in modernization_targets or ():
            name = str(target.get("name", "module"))
            steps: Sequence[Any] = target.get("modernization_steps", ())  # type: ignore[assignment]
            directives.append(
                {
                    "name": name,
                    "risk_level": str(target.get("risk_level", "moderate")),
                    "modernization_steps": _normalise_actions(steps),
                    "stability_modifier": float(target.get("stability_modifier", 0.0)),
                }
            )
        if not directives:
            directives.append(
                {
                    "name": "baseline",
                    "risk_level": "low",
                    "modernization_steps": ("Maintain automated refactors",),
                    "stability_modifier": 0.0,
                }
            )
        return tuple(directives[:5])

    def _holographic_directives(
        self,
        guardrails: Mapping[str, Any],
        waveform: Mapping[str, Any],
        adjustments: Sequence[Any] | None,
    ) -> tuple[str, ...]:
        directives: list[str] = []
        directives.extend(_normalise_actions(guardrails.get("follow_up")))
        directives.extend(_normalise_actions(guardrails.get("actions")))
        directives.extend(_normalise_actions(waveform.get("recommended_actions")))
        directives.extend(_normalise_actions(adjustments))
        if not directives:
            directives.append("Maintain holographic guardrail posture")
        return tuple(dict.fromkeys(directives))

    def _managerial_backlog(
        self,
        codebase_tasks: Sequence[Any] | None,
        network_tasks: Sequence[Any] | None,
        continuity_actions: Mapping[str, Any] | None,
    ) -> tuple[str, ...]:
        backlog: list[str] = []
        backlog.extend(_normalise_actions(codebase_tasks))
        backlog.extend(_normalise_actions(network_tasks))
        if continuity_actions:
            backlog.extend(
                _normalise_actions(continuity_actions.get("actions"))
            )
        if not backlog:
            backlog.append("Monitor automation stream")
        return tuple(dict.fromkeys(backlog))
