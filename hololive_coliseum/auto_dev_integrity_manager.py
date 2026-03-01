"""Synthesize integrity signals across codebase, network, and holography."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp_ratio(value: float) -> float:
    return max(0.0, min(1.0, value))


def _string_sequence(values: Sequence[Any] | None, limit: int | None = None) -> tuple[str, ...]:
    collected: list[str] = []
    for value in values or ():
        text = str(value).strip()
        if text and text not in collected:
            collected.append(text)
            if limit is not None and len(collected) >= limit:
                break
    return tuple(collected)


def _collect_actions(*sources: Sequence[Any] | None) -> tuple[str, ...]:
    actions: list[str] = []
    for source in sources:
        for entry in source or ():
            text = ""
            if isinstance(entry, Mapping):
                for key in ("action", "name", "task", "directive", "step"):
                    if entry.get(key):
                        text = str(entry[key])
                        break
            else:
                text = str(entry)
            text = text.strip()
            if text and text not in actions:
                actions.append(text)
    return tuple(actions)


def _target_names(targets: Sequence[Mapping[str, Any]] | None) -> tuple[str, ...]:
    names: list[str] = []
    for target in targets or ():
        if not isinstance(target, Mapping):
            continue
        name = str(target.get("name", "")).strip()
        if name and name not in names:
            names.append(name)
    return tuple(names)


@dataclass
class AutoDevIntegrityManager:
    """Blend telemetry into an integrity report for the auto-dev pipeline."""

    coverage_weight: float = 0.4
    security_weight: float = 0.35
    holographic_weight: float = 0.25

    def integrity_report(
        self,
        *,
        codebase: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic integrity snapshot for managerial planning."""

        codebase = codebase or {}
        network = network or {}
        security = security or {}
        transmission = transmission or {}
        modernization = modernization or {}
        optimization = optimization or {}
        resilience = resilience or {}

        coverage_ratio = _clamp_ratio(_as_float(codebase.get("coverage_ratio")))
        coverage_gap = round(1.0 - coverage_ratio, 2)
        debt_risk = _as_float(codebase.get("debt_risk_score"))

        security_score = _as_float(
            security.get("security_score"),
            _as_float(network.get("network_security_score")),
        )
        projected_security = _as_float(
            security.get("projected_security_score"),
            security_score,
        )
        security_gap = round(max(0.0, 100.0 - security_score), 2)

        network_diagnostics: Mapping[str, Any] = network.get("holographic_diagnostics", {})  # type: ignore[assignment]
        lithographic_integrity: Mapping[str, Any] = transmission.get("lithographic_integrity", {})  # type: ignore[assignment]
        spectral_waveform: Mapping[str, Any] = transmission.get("spectral_waveform", {})  # type: ignore[assignment]
        guardrails: Mapping[str, Any] = transmission.get("guardrails", {})  # type: ignore[assignment]
        phase_alignment: Mapping[str, Any] = transmission.get("phase_alignment", {})  # type: ignore[assignment]

        holographic_score = _as_float(
            lithographic_integrity.get("score"),
            _as_float(network_diagnostics.get("efficiency_score")),
        )
        if holographic_score <= 1.0:
            holographic_score *= 100.0
        holographic_density = _clamp_ratio(_as_float(spectral_waveform.get("bandwidth_density")))
        holographic_gap = round(1.0 - holographic_density, 2)
        phase_delta = round(
            max(
                0.0,
                _as_float(phase_alignment.get("target"))
                - _as_float(phase_alignment.get("current")),
            ),
            2,
        )

        modernization_priority = str(modernization.get("priority", "monitor"))
        optimization_priority = str(optimization.get("priority", "monitor"))
        resilience_index = _as_float(resilience.get("resilience_index"))
        resilience_grade = str(resilience.get("grade", "vigilant"))

        integrity_score = round(
            coverage_ratio * 100.0 * self.coverage_weight
            + security_score * self.security_weight
            + holographic_score * self.holographic_weight,
            2,
        )

        priority = self._priority(
            coverage_gap,
            security_gap,
            holographic_gap,
            debt_risk,
            modernization_priority,
            optimization_priority,
        )

        weakness_focus = {
            "codebase": _string_sequence(codebase.get("weakness_signals"), limit=3),
            "network": _string_sequence(network.get("anomaly_signals"), limit=3),
            "modernization_targets": _target_names(modernization.get("targets")),
            "coverage_gap": coverage_gap,
            "security_gap": security_gap,
        }

        restoration_actions = _collect_actions(
            modernization.get("modernization_actions"),
            modernization.get("weakness_resolutions"),
            optimization.get("optimization_actions"),
            resilience.get("resilience_actions"),
        )
        if not restoration_actions:
            restoration_actions = ("Maintain integrity monitors",)

        holographic_actions = _collect_actions(
            spectral_waveform.get("recommended_actions"),
            guardrails.get("follow_up"),
            phase_alignment.get("actions"),
            transmission.get("notes"),
        )
        if not holographic_actions:
            holographic_actions = ("Maintain holographic calibration",)

        network_hardening = _collect_actions(
            security.get("network_security_actions"),
            (security.get("automation_directives") or {}).get("playbooks"),
        )
        if not network_hardening:
            network_hardening = ("Maintain baseline network monitoring",)

        coverage_target = 0.78
        if modernization_priority == "stabilise":
            coverage_target = 0.82
        if modernization_priority == "accelerate":
            coverage_target = 0.88
        coverage_projection = round(max(coverage_ratio, min(1.0, coverage_target)), 2)

        stability_projection = {
            "projected_security": round(projected_security, 2),
            "coverage_projection": coverage_projection,
            "phase_delta": phase_delta,
            "resilience_index": round(resilience_index, 3),
            "resilience_grade": resilience_grade,
        }

        trends = {
            "debt_risk_score": round(debt_risk, 2),
            "modernization_priority": modernization_priority,
            "optimization_priority": optimization_priority,
            "resilience_grade": resilience_grade,
        }

        return {
            "priority": priority,
            "integrity_score": integrity_score,
            "coverage_gap": coverage_gap,
            "security_gap": security_gap,
            "holographic_gap": holographic_gap,
            "phase_delta": phase_delta,
            "weakness_focus": weakness_focus,
            "restoration_actions": restoration_actions,
            "holographic_actions": holographic_actions,
            "network_hardening": network_hardening,
            "stability_projection": stability_projection,
            "integrity_trends": trends,
        }

    def _priority(
        self,
        coverage_gap: float,
        security_gap: float,
        holographic_gap: float,
        debt_risk: float,
        modernization_priority: str,
        optimization_priority: str,
    ) -> str:
        priority = "monitor"
        if (
            coverage_gap > 0.3
            or security_gap > 32.0
            or holographic_gap > 0.25
            or modernization_priority in {"stabilise"}
            or optimization_priority in {"stabilise"}
        ):
            priority = "stabilise"
        if (
            coverage_gap > 0.5
            or security_gap > 45.0
            or holographic_gap > 0.4
            or debt_risk >= 0.75
            or modernization_priority == "accelerate"
            or optimization_priority == "accelerate"
        ):
            priority = "accelerate"
        return priority

