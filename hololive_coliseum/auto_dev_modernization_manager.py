"""Combine codebase and network insights into modernization directives."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence, cast


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _dedupe(values: Sequence[Any] | None) -> tuple[Any, ...]:
    seen: list[Any] = []
    for value in values or ():
        if value not in seen:
            seen.append(value)
    return tuple(seen)


def _risk_weight(level: str) -> float:
    normalized = level.lower().strip()
    if normalized in {"critical", "severe"}:
        return 1.0
    if normalized in {"high", "elevated"}:
        return 0.8
    if normalized in {"moderate", "watch"}:
        return 0.55
    if normalized in {"low", "stable"}:
        return 0.35
    return 0.45


@dataclass
class AutoDevModernizationManager:
    """Derive modernization actions from codebase and networking signals."""

    modernization_threshold: float = 0.48
    security_baseline: float = 58.0

    def modernization_brief(
        self,
        *,
        codebase: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic modernization blueprint for the auto-dev loop."""

        codebase = codebase or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        network = network or {}
        transmission = transmission or {}
        research = research or {}
        security = security or {}

        targets = self._prioritised_targets(codebase.get("modernization_targets"))
        priority = self._priority(targets, codebase)
        alignment = self._network_alignment(network, security, transmission)
        holographic = self._holographic_enhancements(transmission, remediation)
        research_allocation = self._research_allocation(research, targets)
        mitigation_support = self._mitigation_support(mitigation, remediation)
        weakness_resolutions = self._weakness_resolutions(
            codebase,
            mitigation,
            remediation,
        )
        timeline = self._timeline(targets, remediation)
        modernization_actions = self._modernization_actions(
            targets,
            holographic,
            mitigation_support,
        )

        return {
            "priority": priority,
            "targets": targets,
            "network_alignment": alignment,
            "holographic_enhancements": holographic,
            "research_allocation": research_allocation,
            "mitigation_support": mitigation_support,
            "weakness_resolutions": weakness_resolutions,
            "timeline": timeline,
            "modernization_actions": modernization_actions,
        }

    def _prioritised_targets(
        self,
        targets: Sequence[Mapping[str, Any]] | None,
    ) -> tuple[dict[str, Any], ...]:
        prioritised: list[dict[str, Any]] = []
        for entry in targets or ():
            name = str(entry.get("name", "module"))
            risk_level = str(entry.get("risk_level", "moderate"))
            steps: Sequence[Any] = entry.get("modernization_steps", ())  # type: ignore[assignment]
            modifier = _as_float(entry.get("stability_modifier"))
            score = round(_risk_weight(risk_level) + modifier, 3)
            prioritised.append(
                {
                    "name": name,
                    "risk_level": risk_level,
                    "stability_modifier": round(modifier, 2),
                    "next_step": str(steps[0]) if steps else "Schedule review",
                    "steps": tuple(str(step) for step in steps) or ("Schedule review",),
                    "score": score,
                }
            )
        prioritised.sort(key=lambda item: item["score"], reverse=True)
        return tuple(prioritised)

    def _priority(
        self,
        targets: Sequence[Mapping[str, Any]],
        codebase: Mapping[str, Any],
    ) -> str:
        if not targets:
            debt_score = _as_float(codebase.get("debt_risk_score"))
            if debt_score >= self.modernization_threshold:
                return "stabilise"
            return "monitor"
        top = targets[0]
        top_risk = str(top.get("risk_level", "moderate")).lower()
        top_modifier = _as_float(top.get("stability_modifier"))
        if top_risk in {"critical", "severe"} or top_modifier >= 0.75:
            return "accelerate"
        if top_risk in {"high", "elevated"} or top_modifier >= self.modernization_threshold:
            return "stabilise"
        return "monitor"

    def _network_alignment(
        self,
        network: Mapping[str, Any],
        security: Mapping[str, Any],
        transmission: Mapping[str, Any],
    ) -> dict[str, Any]:
        security_score = _as_float(
            security.get("security_score"),
            _as_float(network.get("network_security_score")),
        )
        threat = str(security.get("threat_level", "guarded"))
        guardrails = transmission.get("guardrails", {})
        guardrail_status = str(guardrails.get("status", "stable"))
        phase_alignment = transmission.get("phase_alignment", {})
        phase_delta = round(
            max(
                0.0,
                _as_float(phase_alignment.get("target"))
                - _as_float(phase_alignment.get("current")),
            ),
            2,
        )
        waveform = transmission.get("spectral_waveform", {})
        bandwidth_gain = _as_float(
            waveform.get("bandwidth_gain"),
            _as_float(waveform.get("efficiency")),
        )
        alignment = "balanced"
        if security_score < self.security_baseline or guardrail_status not in {"stable", "steady"}:
            alignment = "requires-hardening"
        elif phase_delta <= 0.05 and bandwidth_gain >= 0.2:
            alignment = "upgrade-ready"
        return {
            "security_score": round(security_score, 2),
            "threat_level": threat,
            "guardrail_status": guardrail_status,
            "phase_delta": phase_delta,
            "bandwidth_gain": round(bandwidth_gain, 3),
            "alignment": alignment,
        }

    def _holographic_enhancements(
        self,
        transmission: Mapping[str, Any],
        remediation: Mapping[str, Any],
    ) -> tuple[str, ...]:
        phase_alignment = transmission.get("phase_alignment", {})
        phase_actions = cast(Sequence[Any], phase_alignment.get("actions", ()))
        spectral_waveform = transmission.get("spectral_waveform", {})
        waveform_actions = cast(
            Sequence[Any],
            spectral_waveform.get("recommended_actions", ()),
        )
        guardrails = transmission.get("guardrails", {})
        guardrail_actions = cast(
            Sequence[Any],
            guardrails.get("follow_up", ()),
        )
        remediation_actions = cast(
            Sequence[Any],
            remediation.get("holographic_adjustments", ()),
        )
        combined: list[str] = []
        for bucket in (
            phase_actions,
            waveform_actions,
            guardrail_actions,
            remediation_actions,
        ):
            for action in bucket:
                text = str(action)
                if text:
                    combined.append(text)
        if not combined:
            combined.append("Maintain holographic lattice calibration")
        return _dedupe(combined)

    def _research_allocation(
        self,
        research: Mapping[str, Any],
        targets: Sequence[Mapping[str, Any]],
    ) -> dict[str, Any]:
        raw_percent = _as_float(research.get("raw_utilization_percent"))
        competitive = _as_float(research.get("competitive_utilization_percent"))
        trend = str(research.get("trend_direction", "stable"))
        focus = str(research.get("intelligence_focus", "Balance research streams"))
        required = "balanced"
        if targets and raw_percent < 40.0:
            required = "increase"
        elif raw_percent > 70.0:
            required = "throttle"
        allocation = {
            "raw_percent": round(raw_percent, 2),
            "competitive_percent": round(competitive, 2),
            "trend": trend,
            "focus": focus,
            "adjustment": required,
        }
        return allocation

    def _mitigation_support(
        self,
        mitigation: Mapping[str, Any],
        remediation: Mapping[str, Any],
    ) -> tuple[str, ...]:
        codebase_tasks = cast(Sequence[Any], mitigation.get("codebase_tasks", ()))
        network_tasks = cast(Sequence[Any], mitigation.get("network_tasks", ()))
        research_tasks = cast(Sequence[Any], mitigation.get("research_tasks", ()))
        intelligence_tasks = cast(
            Sequence[Any],
            mitigation.get("intelligence_tasks", ()),
        )
        applied = cast(Sequence[Any], remediation.get("applied_fixes", ()))
        scheduled = cast(Sequence[Any], remediation.get("scheduled_fixes", ()))

        actions: list[str] = []
        for task in codebase_tasks:
            if isinstance(task, Mapping):
                actions.append(f"Codebase: {task.get('task', 'Review module')}")
            else:
                actions.append(f"Codebase: {task}")
        actions.extend(str(task) for task in network_tasks)
        actions.extend(f"Research: {task}" for task in research_tasks)
        actions.extend(f"Guidance: {task}" for task in intelligence_tasks)
        for entry in applied:
            if isinstance(entry, Mapping):
                label = entry.get("task") or entry.get("domain", "fix")
            else:
                label = str(entry)
            actions.append(f"Applied: {label}")
        for entry in scheduled:
            if isinstance(entry, Mapping):
                label = entry.get("task") or entry.get("domain") or "Scheduled fix"
            else:
                label = str(entry)
            actions.append(f"Scheduled: {label}")
        if not actions:
            actions.append("Review mitigation queue")
        return _dedupe(actions)

    def _weakness_resolutions(
        self,
        codebase: Mapping[str, Any],
        mitigation: Mapping[str, Any],
        remediation: Mapping[str, Any],
    ) -> tuple[str, ...]:
        weaknesses: Sequence[Any] = codebase.get("weakness_signals", ())  # type: ignore[assignment]
        mitigation_plan = cast(Sequence[Any], codebase.get("mitigation_plan", ()))
        mitigation_tasks = cast(Sequence[Any], mitigation.get("codebase_tasks", ()))
        progress = cast(Sequence[Any], remediation.get("codebase_progress", ()))

        resolutions: list[str] = []
        for signal in weaknesses:
            resolutions.append(f"Signal: {signal}")
        for suggestion in mitigation_plan:
            resolutions.append(f"Plan: {suggestion}")
        for task in mitigation_tasks:
            if isinstance(task, Mapping):
                resolutions.append(f"Task: {task.get('task', 'Remediate module')}")
            else:
                resolutions.append(f"Task: {task}")
        for module in progress:
            if isinstance(module, Mapping) and module.get("addressed"):
                name = module.get("name", "module")
                resolutions.append(f"Resolved: {name}")
        if not resolutions:
            resolutions.append("No weaknesses reported")
        return _dedupe(resolutions)

    def _timeline(
        self,
        targets: Sequence[Mapping[str, Any]],
        remediation: Mapping[str, Any],
    ) -> tuple[dict[str, Any], ...]:
        scheduled = cast(Sequence[Any], remediation.get("scheduled_fixes", ()))
        timeline: list[dict[str, Any]] = []
        for index, target in enumerate(targets[:3], start=1):
            action = str(target.get("next_step", "Schedule review"))
            scheduled_action = None
            if index - 1 < len(scheduled):
                entry = scheduled[index - 1]
                if isinstance(entry, Mapping):
                    scheduled_action = entry.get("task") or entry.get("domain")
                else:
                    scheduled_action = str(entry)
            timeline.append(
                {
                    "target": target.get("name", f"module_{index}"),
                    "window": f"Sprint {index}",
                    "action": scheduled_action or action,
                }
            )
        if not timeline:
            timeline.append(
                {
                    "target": "codebase",
                    "window": "Sprint 1",
                    "action": "Review modernization backlog",
                }
            )
        return tuple(timeline)

    def _modernization_actions(
        self,
        targets: Sequence[Mapping[str, Any]],
        holographic: Sequence[str],
        mitigation_support: Sequence[str],
    ) -> tuple[str, ...]:
        actions: list[str] = []
        for target in targets:
            actions.append(
                f"Modernize {target.get('name', 'module')} via {target.get('next_step', 'review')}"
            )
        actions.extend(str(action) for action in holographic)
        actions.extend(str(action) for action in mitigation_support)
        if not actions:
            actions.append("Maintain modernization cadence")
        return _dedupe(actions)
