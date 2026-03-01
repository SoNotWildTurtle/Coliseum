"""Translate auto-dev telemetry into actionable mitigation tasks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence


_DEF_OWNERS = {
    "codebase": "Platform Core",
    "network": "Network Reliability",
    "research": "Intelligence Ops",
    "guidance": "Encounter Direction",
}


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalise_tasks(tasks: Iterable[str], owner: str) -> list[dict[str, Any]]:
    normalised: list[dict[str, Any]] = []
    for task in tasks:
        description = str(task)
        if not description:
            continue
        normalised.append({
            "task": description,
            "owner": _DEF_OWNERS.get(owner, owner.title()),
            "severity": "medium",
        })
    return normalised


@dataclass
class AutoDevMitigationManager:
    """Generate mitigation and upgrade plans based on manager reports."""

    coverage_target: float = 0.82
    security_target: float = 68.0
    pressure_threshold: float = 60.0

    def derive_actions(
        self,
        *,
        codebase: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        guidance: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic mitigation plan keyed by responsibility."""

        codebase = codebase or {}
        network = network or {}
        research = research or {}
        guidance = guidance or {}

        coverage = _as_float(codebase.get("coverage_ratio"))
        security_score = _as_float(network.get("network_security_score"))
        pressure_index = _as_float(research.get("research_pressure_index"))
        risk_index = _as_float(guidance.get("risk_index"))

        stability_score = self._stability_score(
            coverage,
            security_score,
            pressure_index,
            risk_index,
        )
        priority = self._priority(stability_score, guidance.get("priority"))

        codebase_tasks = self._codebase_tasks(codebase, coverage)
        network_tasks = self._network_tasks(network, security_score)
        research_tasks = self._research_tasks(research, pressure_index)
        intelligence_tasks = self._intelligence_tasks(guidance, risk_index)
        holographic_upgrades = self._holographic_upgrades(network)
        execution_windows = self._execution_windows(
            codebase_tasks,
            network_tasks,
            research_tasks,
        )

        return {
            "stability_score": round(stability_score, 2),
            "priority": priority,
            "codebase_tasks": tuple(codebase_tasks),
            "network_tasks": tuple(network_tasks),
            "research_tasks": tuple(research_tasks),
            "intelligence_tasks": tuple(intelligence_tasks),
            "holographic_upgrades": tuple(holographic_upgrades),
            "execution_windows": tuple(execution_windows),
        }

    def _stability_score(
        self,
        coverage: float,
        security_score: float,
        pressure_index: float,
        risk_index: float,
    ) -> float:
        coverage_gap = max(0.0, self.coverage_target - coverage)
        security_gap = max(0.0, self.security_target - security_score) / 100.0
        pressure_component = pressure_index / 150.0
        risk_component = risk_index / 2.5
        base = 100.0
        penalty = (coverage_gap * 45.0) + (security_gap * 35.0) + (
            pressure_component * 30.0
        ) + (risk_component * 25.0)
        return max(0.0, min(100.0, base - penalty))

    def _priority(self, stability_score: float, guidance_priority: Any) -> str:
        if stability_score <= 35.0:
            return "critical"
        if stability_score <= 55.0:
            return "high"
        if str(guidance_priority) in {"high", "critical"}:
            return "high"
        if stability_score <= 75.0:
            return "medium"
        return "monitor"

    def _codebase_tasks(
        self,
        codebase: Mapping[str, Any],
        coverage: float,
    ) -> list[dict[str, Any]]:
        tasks = _normalise_tasks(codebase.get("mitigation_plan", ()), "codebase")
        debt_profile = codebase.get("debt_profile") or {}
        self._extend_from_debt_profile(tasks, debt_profile)
        scorecards: Sequence[Mapping[str, Any]] = codebase.get("module_scorecards", ())  # type: ignore[assignment]
        for card in scorecards:
            risk_level = str(card.get("risk_level", "low"))
            if risk_level in {"elevated", "high", "critical"}:
                actions: Sequence[str] = card.get("recommended_actions", ())  # type: ignore[assignment]
                headline = actions[0] if actions else "Stabilise module"
                severity = "medium"
                if risk_level == "high":
                    severity = "high"
                elif risk_level == "critical":
                    severity = "critical"
                tasks.append(
                    {
                        "task": f"{card.get('name', 'module')} :: {headline}",
                        "owner": _DEF_OWNERS["codebase"],
                        "severity": severity,
                    }
                )
            modifier = float(card.get("stability_modifier", 0.0))
            if modifier >= 0.6:
                tasks.append(
                    {
                        "task": f"Stability watch: {card.get('name', 'module')} modifier {modifier}",
                        "owner": _DEF_OWNERS["codebase"],
                        "severity": "medium",
                    }
                )
        for task in tasks:
            if "Refactor" in task["task"]:
                task["severity"] = "high"
        if coverage < self.coverage_target:
            tasks.append(
                {
                    "task": "Expand automated test coverage for critical auto-dev modules",
                    "owner": _DEF_OWNERS["codebase"],
                    "severity": "high",
                }
            )
        weaknesses: Sequence[str] = codebase.get("weakness_signals", ())  # type: ignore[assignment]
        for weakness in weaknesses[:2]:
            tasks.append(
                {
                    "task": f"Investigate: {weakness}",
                    "owner": _DEF_OWNERS["codebase"],
                    "severity": "medium",
                }
            )
        return tasks

    def _extend_from_debt_profile(
        self,
        tasks: list[dict[str, Any]],
        debt_profile: Mapping[str, Any],
    ) -> None:
        high_complexity: Sequence[int] = debt_profile.get("high_complexity", ())  # type: ignore[assignment]
        missing_tests: Sequence[int] = debt_profile.get("missing_tests", ())  # type: ignore[assignment]
        incident_modules: Sequence[int] = debt_profile.get("incident_modules", ())  # type: ignore[assignment]
        def _already_present(fragment: str) -> bool:
            return any(fragment in task.get("task", "") for task in tasks)

        for index in high_complexity[:2]:
            description = f"Refactor module {index} to reduce complexity debt"
            if not _already_present(description):
                tasks.append(
                    {
                        "task": description,
                        "owner": _DEF_OWNERS["codebase"],
                        "severity": "high",
                    }
                )
        for index in missing_tests[:2]:
            description = f"Author regression tests for module {index}"
            if not _already_present(description):
                tasks.append(
                    {
                        "task": description,
                        "owner": _DEF_OWNERS["codebase"],
                        "severity": "high",
                    }
                )
        if incident_modules and not _already_present("incident post-mortem"):
            focus = ", ".join(str(idx) for idx in incident_modules[:3])
            tasks.append(
                {
                    "task": f"Run incident post-mortem for modules: {focus}",
                    "owner": _DEF_OWNERS["codebase"],
                    "severity": "medium",
                }
            )

    def _network_tasks(
        self,
        network: Mapping[str, Any],
        security_score: float,
    ) -> list[str]:
        tasks: list[str] = []
        upgrade_backlog = network.get("upgrade_backlog", {})
        backlog_tasks: Sequence[str] = upgrade_backlog.get("tasks", ())  # type: ignore[assignment]
        tasks.extend(str(task) for task in backlog_tasks if task)
        if security_score < self.security_target:
            security_auto_dev = network.get("security_auto_dev", {})
            directive = security_auto_dev.get("directive", "stabilise")
            tasks.append(f"Enforce {directive} network hardening playbook")
        paths: Sequence[str] = network.get("upgrade_paths", ())  # type: ignore[assignment]
        for path in paths[:2]:
            tasks.append(f"Execute upgrade path: {path}")
        return tasks

    def _research_tasks(
        self,
        research: Mapping[str, Any],
        pressure_index: float,
    ) -> list[str]:
        tasks: list[str] = []
        plan: Sequence[str] = research.get("weakness_signals", ())  # type: ignore[assignment]
        tasks.extend(str(item) for item in plan if item)
        if pressure_index >= self.pressure_threshold:
            tasks.append("Throttle research jobs to relieve processing pressure")
        else:
            tasks.append("Maintain current research cadence with monitoring")
        competitive = research.get("competitive_research", {})
        primary = competitive.get("primary_game")
        if primary:
            tasks.append(f"Deep-dive rival insights from {primary}")
        return tasks

    def _intelligence_tasks(
        self,
        guidance: Mapping[str, Any],
        risk_index: float,
    ) -> list[str]:
        directives: Sequence[str] = guidance.get("directives", ())  # type: ignore[assignment]
        tasks = [str(item) for item in directives if item]
        intelligence_score = _as_float(guidance.get("general_intelligence_score"))
        if intelligence_score < 40.0:
            tasks.append("Augment managerial intelligence dataset with fresh encounters")
        elif intelligence_score < 70.0:
            tasks.append("Review backend guidance vector with design leadership")
        if risk_index >= 1.4:
            tasks.append("Schedule cross-team review for elevated encounter risk")
        return tasks

    def _holographic_upgrades(self, network: Mapping[str, Any]) -> list[str]:
        diagnostics = network.get("holographic_diagnostics", {})
        enhancements = network.get("holographic_enhancements", {})
        upgrades: list[str] = []
        signal = diagnostics.get("signal_health")
        if signal and signal != "optimal":
            upgrades.append(f"Calibrate holographic signal: {signal}")
        layers = enhancements.get("layer_upgrades", ())
        for layer in layers:
            upgrades.append(f"Deploy holographic layer upgrade: {layer}")
        phase = enhancements.get("phase_lock_directives")
        if phase:
            upgrades.append(f"Apply phase lock directive: {phase}")
        if not upgrades:
            upgrades.append("Maintain holographic transmission health checks")
        return upgrades

    def _execution_windows(
        self,
        codebase_tasks: Sequence[Mapping[str, Any]],
        network_tasks: Sequence[str],
        research_tasks: Sequence[str],
    ) -> list[dict[str, Any]]:
        windows: list[dict[str, Any]] = []
        if network_tasks:
            windows.append({"window": "immediate", "focus": "network"})
        if any(task.get("severity") == "high" for task in codebase_tasks):
            windows.append({"window": "next_sprint", "focus": "codebase"})
        if research_tasks:
            windows.append({"window": "continuous", "focus": "research"})
        if not windows:
            windows.append({"window": "monitor", "focus": "all"})
        return windows
