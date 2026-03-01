"""Blend modernization, security, and remediation into optimisation briefs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _collect_strings(values: Sequence[Any] | None, *keys: str) -> tuple[str, ...]:
    collected: list[str] = []
    for value in values or ():
        text: str = ""
        if isinstance(value, Mapping):
            for key in keys or ("task", "name", "action"):
                if key in value and value[key]:
                    text = str(value[key])
                    break
        else:
            text = str(value)
        text = text.strip()
        if text and text not in collected:
            collected.append(text)
    return tuple(collected)


def _dedupe_strings(values: Sequence[str] | None) -> tuple[str, ...]:
    seen: list[str] = []
    for value in values or ():
        text = str(value).strip()
        if text and text not in seen:
            seen.append(text)
    return tuple(seen)


@dataclass
class AutoDevOptimizationManager:
    """Blend telemetry into optimisation tasks for managerial planning."""

    security_floor: float = 60.0
    debt_threshold: float = 0.55

    def optimization_brief(
        self,
        *,
        codebase: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        network_auto_dev: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        guidance: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return an optimisation snapshot for the auto-dev orchestration."""

        codebase = codebase or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        modernization = modernization or {}
        network = network or {}
        network_auto_dev = network_auto_dev or {}
        transmission = transmission or {}
        security = security or {}
        research = research or {}
        guidance = guidance or {}
        resilience = resilience or {}

        codebase_focus = self._codebase_focus(codebase, mitigation, remediation)
        network_focus = self._network_security_focus(
            network,
            security,
            network_auto_dev,
        )
        holographic_plan = self._holographic_plan(
            transmission,
            resilience,
            remediation,
        )
        remediation_support = self._remediation_support(remediation)
        research_signal = self._research_signal(research)
        modernization_dependencies = self._modernization_dependencies(
            modernization,
            codebase,
        )
        fix_windows = self._fix_windows(remediation, modernization)
        managerial_focus = self._managerial_focus(
            guidance,
            resilience,
            research_signal,
        )
        optimization_actions = self._optimization_actions(
            codebase_focus,
            network_focus,
            holographic_plan,
            modernization_dependencies,
            remediation_support,
        )
        priority = self._priority(
            codebase,
            modernization,
            mitigation,
            security,
            network_focus,
        )

        return {
            "priority": priority,
            "codebase_focus": codebase_focus,
            "network_security_focus": network_focus,
            "holographic_plan": holographic_plan,
            "remediation_support": remediation_support,
            "research_signal": research_signal,
            "modernization_dependencies": modernization_dependencies,
            "fix_windows": fix_windows,
            "optimization_actions": optimization_actions,
            "managerial_focus": managerial_focus,
            "network_upgrade_tracks": network_focus.get("upgrade_tracks", ()),
        }

    def _codebase_focus(
        self,
        codebase: Mapping[str, Any],
        mitigation: Mapping[str, Any],
        remediation: Mapping[str, Any],
    ) -> dict[str, Any]:
        weaknesses = _dedupe_strings(codebase.get("weakness_signals"))
        targets: Sequence[Mapping[str, Any]] = codebase.get(
            "modernization_targets",
            (),
        )  # type: ignore[assignment]
        target_modules = _collect_strings(targets, "name")
        mitigation_tasks = _collect_strings(mitigation.get("codebase_tasks"))  # type: ignore[arg-type]
        progress: Sequence[Mapping[str, Any]] = remediation.get(
            "codebase_progress",
            (),
        )  # type: ignore[assignment]
        addressed = tuple(
            str(entry.get("name", "module"))
            for entry in progress
            if entry.get("addressed")
        )
        pending = tuple(
            str(entry.get("name", "module"))
            for entry in progress
            if not entry.get("addressed")
        )
        return {
            "stability_outlook": codebase.get("stability_outlook", "steady"),
            "debt_risk_score": round(_as_float(codebase.get("debt_risk_score")), 2),
            "coverage_ratio": round(_as_float(codebase.get("coverage_ratio")), 3),
            "weaknesses": weaknesses,
            "target_modules": target_modules,
            "mitigation_tasks": mitigation_tasks,
            "addressed_modules": addressed,
            "outstanding_modules": pending,
        }

    def _network_security_focus(
        self,
        network: Mapping[str, Any],
        security: Mapping[str, Any],
        network_auto_dev: Mapping[str, Any],
    ) -> dict[str, Any]:
        security_score = _as_float(
            security.get("security_score"),
            _as_float(network.get("network_security_score")),
        )
        threat_level = str(security.get("threat_level", "guarded"))
        actions = list(
            _collect_strings(security.get("network_security_actions"))  # type: ignore[arg-type]
        )
        actions.extend(_collect_strings(network.get("network_tasks")))  # type: ignore[arg-type]
        automation = network_auto_dev.get("security_automation", ())
        actions.extend(_collect_strings(automation))
        upgrade_tracks = _collect_strings(network_auto_dev.get("upgrade_tracks"))
        next_steps = _collect_strings(network_auto_dev.get("next_steps"))
        if not actions:
            actions.append("Audit network guardrails")
        return {
            "security_score": round(security_score, 2),
            "threat_level": threat_level,
            "actions": _dedupe_strings(actions),
            "upgrade_tracks": upgrade_tracks,
            "next_steps": next_steps,
        }

    def _holographic_plan(
        self,
        transmission: Mapping[str, Any],
        resilience: Mapping[str, Any],
        remediation: Mapping[str, Any],
    ) -> dict[str, Any]:
        guardrails = transmission.get("guardrails", {})
        status = str(guardrails.get("status", "stable"))
        lattice = resilience.get("holographic_readiness", {})
        readiness_status = str(lattice.get("status", status))
        spectral = transmission.get("spectral_waveform", {})
        efficiency = _as_float(
            spectral.get("efficiency"),
            _as_float(spectral.get("bandwidth_gain")),
        )
        phase = transmission.get("phase_alignment", {})
        phase_delta = round(
            max(0.0, _as_float(phase.get("target")) - _as_float(phase.get("current"))),
            3,
        )
        actions: list[str] = []
        actions.extend(_collect_strings(guardrails.get("follow_up")))
        actions.extend(_collect_strings(lattice.get("recommended_actions")))
        actions.extend(_collect_strings(spectral.get("recommended_actions")))
        actions.extend(_collect_strings(remediation.get("holographic_adjustments")))
        if not actions:
            actions.append("Maintain holographic diagnostics cadence")
        return {
            "status": readiness_status,
            "phase_delta": phase_delta,
            "efficiency": round(efficiency, 3),
            "actions": _dedupe_strings(actions),
        }

    def _remediation_support(self, remediation: Mapping[str, Any]) -> dict[str, Any]:
        applied: Sequence[Mapping[str, Any]] = remediation.get(
            "applied_fixes",
            (),
        )  # type: ignore[assignment]
        scheduled: Sequence[Mapping[str, Any]] = remediation.get(
            "scheduled_fixes",
            (),
        )  # type: ignore[assignment]
        projection: Mapping[str, Any] = remediation.get(
            "stability_projection",
            {},
        )  # type: ignore[assignment]
        return {
            "applied_count": len(tuple(applied)),
            "scheduled_count": len(tuple(scheduled)),
            "projected_security_score": projection.get("projected_security_score", 0.0),
            "projected_coverage": projection.get("projected_coverage", 0.0),
        }

    def _research_signal(self, research: Mapping[str, Any]) -> dict[str, Any]:
        raw_percent = _as_float(
            research.get("raw_utilization_percent"),
            _as_float(research.get("latest_sample_percent")),
        )
        pressure = _as_float(research.get("research_pressure_index"))
        trend = str(research.get("trend_direction", "stable"))
        recommendation = str(
            research.get("recommendation", "Maintain balanced auto-dev research")
        )
        weaknesses = _dedupe_strings(research.get("weakness_signals"))
        return {
            "raw_percent": round(raw_percent, 2),
            "pressure": round(pressure, 2),
            "trend": trend,
            "recommendation": recommendation,
            "weaknesses": weaknesses,
        }

    def _modernization_dependencies(
        self,
        modernization: Mapping[str, Any],
        codebase: Mapping[str, Any],
    ) -> tuple[dict[str, Any], ...]:
        targets: Sequence[Mapping[str, Any]] = modernization.get(
            "targets",
            (),
        )  # type: ignore[assignment]
        if not targets:
            targets = codebase.get("modernization_targets", ())  # type: ignore[assignment]
        dependencies: list[dict[str, Any]] = []
        for target in targets:
            name = str(target.get("name", "module"))
            next_step = str(target.get("next_step", "Schedule review"))
            dependencies.append({"module": name, "next_step": next_step})
        if not dependencies:
            dependencies.append({"module": "codebase", "next_step": "Review backlog"})
        return tuple(dependencies)

    def _fix_windows(
        self,
        remediation: Mapping[str, Any],
        modernization: Mapping[str, Any],
    ) -> tuple[str, ...]:
        modernization_timeline: Sequence[Mapping[str, Any]] = modernization.get(
            "timeline",
            (),
        )  # type: ignore[assignment]
        windows = [
            str(entry.get("window", ""))
            for entry in modernization_timeline
            if isinstance(entry, Mapping)
        ]
        if not windows:
            windows.append("Sprint 1")
        scheduled: Sequence[Mapping[str, Any]] = remediation.get(
            "scheduled_fixes",
            (),
        )  # type: ignore[assignment]
        for entry in scheduled:
            if isinstance(entry, Mapping):
                window = entry.get("window")
                if window:
                    windows.append(str(window))
        return _dedupe_strings(windows)

    def _managerial_focus(
        self,
        guidance: Mapping[str, Any],
        resilience: Mapping[str, Any],
        research_signal: Mapping[str, Any],
    ) -> str:
        priority = str(guidance.get("priority", "low"))
        resilience_grade = str(resilience.get("grade", "vigilant"))
        pressure = _as_float(research_signal.get("pressure"))
        if priority in {"high", "critical"} or resilience_grade in {"guarded", "strained"}:
            return "stabilise-backend"
        if pressure >= 65.0:
            return "balance-research"
        if resilience_grade in {"resilient", "robust"} and pressure <= 40.0:
            return "accelerate-upgrades"
        return "monitor"

    def _optimization_actions(
        self,
        codebase_focus: Mapping[str, Any],
        network_focus: Mapping[str, Any],
        holographic_plan: Mapping[str, Any],
        dependencies: Sequence[Mapping[str, Any]],
        remediation_support: Mapping[str, Any],
    ) -> tuple[str, ...]:
        actions: list[str] = []
        for module in codebase_focus.get("target_modules", ()):  # type: ignore[assignment]
            actions.append(f"Refine {module} with targeted tests")
        weaknesses = codebase_focus.get("weaknesses", ())
        if weaknesses:
            actions.append("Address highlighted codebase weaknesses")
        security_actions = network_focus.get("actions", ())
        actions.extend(str(action) for action in security_actions)
        holographic_actions = holographic_plan.get("actions", ())
        actions.extend(str(action) for action in holographic_actions)
        for dependency in dependencies:
            module = dependency.get("module", "module")
            next_step = dependency.get("next_step", "review")
            actions.append(f"Schedule {module} :: {next_step}")
        projected_security = _as_float(
            remediation_support.get("projected_security_score"),
            0.0,
        )
        if projected_security < self.security_floor:
            actions.append("Increase remediation throughput to raise security score")
        if not actions:
            actions.append("Maintain optimisation cadence")
        return _dedupe_strings(actions)

    def _priority(
        self,
        codebase: Mapping[str, Any],
        modernization: Mapping[str, Any],
        mitigation: Mapping[str, Any],
        security: Mapping[str, Any],
        network_focus: Mapping[str, Any],
    ) -> str:
        debt = _as_float(codebase.get("debt_risk_score"))
        modernization_priority = str(modernization.get("priority", "monitor"))
        mitigation_priority = str(mitigation.get("priority", "monitor"))
        security_score = _as_float(network_focus.get("security_score"))
        threat = str(security.get("threat_level", "guarded"))
        if threat in {"critical", "severe"} or security_score < self.security_floor:
            return "accelerate"
        if modernization_priority in {"accelerate", "stabilise"}:
            return "stabilise"
        if mitigation_priority in {"high", "critical"} or debt >= self.debt_threshold:
            return "stabilise"
        return "monitor"
