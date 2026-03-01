"""Derive network upgrade and security automation tasks for the auto-dev loop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _dedupe(values: Sequence[Any] | None) -> tuple[Any, ...]:
    result: list[Any] = []
    for value in values or ():
        if value not in result:
            result.append(value)
    return tuple(result)


@dataclass
class AutoDevNetworkUpgradeManager:
    """Synthesize networking, security, and holographic directives."""

    utilization_threshold: float = 62.0
    security_threshold: float = 55.0

    def plan_auto_dev(
        self,
        *,
        network: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic blueprint for network auto-development."""

        network = network or {}
        security = security or {}
        transmission = transmission or {}
        research = research or {}
        codebase = codebase or {}
        mitigation = mitigation or {}

        upgrade_tracks = self._upgrade_tracks(network)
        security_automation = self._security_automation(security, mitigation)
        holographic = self._holographic_integration(transmission)
        processing_focus = self._processing_focus(network, research)
        readiness_score = self._readiness_score(network, security, processing_focus)
        priority = self._priority(security, processing_focus)
        codebase_links = self._codebase_links(codebase)
        next_steps = self._next_steps(
            upgrade_tracks,
            security_automation,
            holographic["actions"],
            codebase_links,
        )

        return {
            "priority": priority,
            "readiness_score": readiness_score,
            "upgrade_tracks": upgrade_tracks,
            "security_automation": security_automation,
            "holographic_integration": holographic,
            "processing_focus": processing_focus,
            "codebase_links": codebase_links,
            "next_steps": next_steps,
        }

    def _upgrade_tracks(self, network: Mapping[str, Any]) -> tuple[str, ...]:
        tracks: list[str] = []
        tracks.extend(str(path) for path in network.get("upgrade_paths", ()))
        tracks.extend(str(path) for path in network.get("network_security_upgrades", ()))
        security_auto_dev = network.get("security_auto_dev") or {}
        directive = security_auto_dev.get("directive")
        if directive:
            tracks.append(f"Security directive: {directive}")
        roadmap = network.get("upgrade_roadmap") or {}
        for milestone in roadmap.get("milestones", ()):  # type: ignore[assignment]
            tracks.append(str(milestone))
        if not tracks:
            tracks.append("Maintain upgrade cadence")
        return _dedupe(tracks)

    def _security_automation(
        self,
        security: Mapping[str, Any],
        mitigation: Mapping[str, Any],
    ) -> tuple[str, ...]:
        actions: list[str] = []
        actions.extend(str(item) for item in security.get("network_security_actions", ()))
        hardening = security.get("hardening_tasks", ())
        for task in hardening:  # type: ignore[assignment]
            if isinstance(task, Mapping):
                label = task.get("module", "module")
                risk = task.get("risk_level", "medium")
                actions.append(f"Hardening {label} ({risk})")
            else:
                actions.append(str(task))
        actions.extend(str(task) for task in mitigation.get("network_tasks", ()))
        if not actions:
            actions.append("Review security automation posture")
        return _dedupe(actions)

    def _holographic_integration(
        self,
        transmission: Mapping[str, Any],
    ) -> dict[str, Any]:
        waveform = transmission.get("spectral_waveform", {})
        lattice = transmission.get("lattice_overlay", {})
        guardrails = transmission.get("guardrails", {})
        actions = []
        actions.extend(str(step) for step in waveform.get("recommended_actions", ()))
        actions.extend(str(step) for step in lattice.get("actions", ()))
        actions.extend(str(step) for step in guardrails.get("follow_up", ()))
        if not actions:
            actions.append("Maintain spectral balance")
        return {
            "efficiency": _as_float(waveform.get("efficiency", waveform.get("bandwidth_gain"))),
            "stability": lattice.get("stability", guardrails.get("status", "stable")),
            "actions": _dedupe(actions),
        }

    def _processing_focus(
        self,
        network: Mapping[str, Any],
        research: Mapping[str, Any],
    ) -> dict[str, Any]:
        research_percent = _as_float(
            research.get("raw_utilization_percent"),
            _as_float(research.get("latest_sample_percent")),
        )
        processing_budget = _as_float(
            network.get("processing_utilization_percent"),
            research_percent,
        )
        bandwidth = network.get("bandwidth", {})
        average_bandwidth = _as_float(bandwidth.get("average_mbps"))
        budget_health = "stable"
        if research_percent >= self.utilization_threshold or processing_budget >= self.utilization_threshold:
            budget_health = "strained"
        elif research_percent >= (self.utilization_threshold - 10.0):
            budget_health = "watch"
        return {
            "research_utilization_percent": round(research_percent, 2),
            "processing_utilization_percent": round(processing_budget, 2),
            "average_bandwidth_mbps": round(average_bandwidth, 2),
            "budget_health": budget_health,
        }

    def _readiness_score(
        self,
        network: Mapping[str, Any],
        security: Mapping[str, Any],
        processing_focus: Mapping[str, Any],
    ) -> float:
        security_score = _as_float(
            security.get("security_score"),
            _as_float(network.get("network_security_score")),
        )
        stability = 1.0 - min(1.0, processing_focus.get("processing_utilization_percent", 0.0) / 100.0)
        readiness = (security_score / 100.0 + stability) / 2.0
        return round(max(0.0, min(1.0, readiness)), 3)

    def _priority(
        self,
        security: Mapping[str, Any],
        processing_focus: Mapping[str, Any],
    ) -> str:
        threat = str(security.get("threat_level", "guarded")).lower() or "guarded"
        security_score = _as_float(security.get("security_score"))
        budget_health = str(processing_focus.get("budget_health", "stable"))
        if security_score <= 0.0 and threat in {"guarded", "monitor"}:
            if budget_health == "strained":
                return "accelerate"
            if budget_health == "watch":
                return "stabilise"
            return "monitor"
        if threat in {"critical", "severe"} or security_score < self.security_threshold:
            return "critical"
        if threat in {"elevated", "high"} or budget_health == "strained":
            return "accelerate"
        if budget_health == "watch" or threat in {"guarded", "monitor"}:
            return "stabilise"
        return "monitor"

    def _codebase_links(self, codebase: Mapping[str, Any]) -> tuple[str, ...]:
        targets: Sequence[Mapping[str, Any]] = codebase.get("modernization_targets", ())  # type: ignore[assignment]
        links: list[str] = []
        for target in targets:
            name = str(target.get("name", "module"))
            risk = str(target.get("risk_level", "moderate"))
            if any(keyword in name.lower() for keyword in ("network", "holo", "transmission")):
                steps: Sequence[str] = target.get("modernization_steps", ())  # type: ignore[assignment]
                first_step = steps[0] if steps else "Schedule review"
                links.append(f"{name} ({risk}): {first_step}")
        if not links and targets:
            fallback = targets[0]
            links.append(
                f"{fallback.get('name', 'module')} ({fallback.get('risk_level', 'moderate')}): "
                f"{next(iter(fallback.get('modernization_steps', ('Schedule review',))), 'Schedule review')}"
            )
        if not links:
            links.append("No network-focused modernization targets identified")
        return _dedupe(links)

    def _next_steps(
        self,
        upgrade_tracks: Sequence[str],
        security_automation: Sequence[str],
        holographic_actions: Sequence[str],
        codebase_links: Sequence[str],
    ) -> tuple[str, ...]:
        steps: list[str] = []
        steps.extend(upgrade_tracks[:3])
        steps.extend(security_automation[:3])
        steps.extend(holographic_actions[:2])
        steps.extend(codebase_links[:2])
        return _dedupe(steps)

