"""Long-range continuity planning for the auto-dev orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalise_strings(values: Sequence[Any] | None) -> list[str]:
    result: list[str] = []
    for value in values or ():
        text = str(value).strip()
        if text:
            result.append(text)
    return result


@dataclass
class AutoDevContinuityManager:
    """Synthesize continuity, security, and holographic guidance."""

    short_window_days: int = 3
    mid_window_days: int = 7
    horizon_days: int = 14

    def continuity_plan(
        self,
        *,
        guidance: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic continuity outlook for the auto-dev loop."""

        guidance = guidance or {}
        network = network or {}
        codebase = codebase or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        resilience = resilience or {}

        priority = str(guidance.get("priority", "low"))
        grade = str(resilience.get("grade", "vigilant"))
        mitigation_priority = str(mitigation.get("priority", "monitor"))
        network_security_score = _as_float(network.get("network_security_score"))
        guardrails = network.get("transmission_guardrails", {})  # type: ignore[assignment]
        guardrail_severity = str(guardrails.get("severity", "monitor"))
        holographic_enhancements = network.get("holographic_enhancements", {})
        holographic_diagnostics = network.get("holographic_diagnostics", {})
        lithographic = network.get("lithographic_integrity", {})
        backlog = network.get("upgrade_backlog", {})
        security_auto_dev = network.get("security_auto_dev", {})
        resilience_score = _as_float(resilience.get("resilience_score"))
        resilience_index = _as_float(resilience.get("resilience_index"), resilience_score / 100.0)
        debt_risk = _as_float(codebase.get("debt_risk_score"))
        codebase_outlook = str(codebase.get("stability_outlook", "steady"))
        mitigation_score = _as_float(mitigation.get("stability_score"))
        research_penalty = _as_float(resilience.get("research_penalty"))
        module_progress = remediation.get("codebase_progress", {})  # type: ignore[assignment]
        resilience_overwatch = resilience.get("managerial_overwatch", {})  # type: ignore[assignment]

        timeline = self._timeline(
            priority,
            mitigation_priority,
            network_security_score,
            debt_risk,
            guardrail_severity,
            grade,
            module_progress,
        )
        continuity_index = self._continuity_index(
            network_security_score,
            resilience_index,
            debt_risk,
            mitigation_score,
        )
        continuity_risks = self._continuity_risks(
            network_security_score,
            debt_risk,
            guardrail_severity,
            research_penalty,
            codebase_outlook,
        )
        holographic_actions = self._holographic_actions(
            guardrails,
            holographic_enhancements,
            holographic_diagnostics,
            lithographic,
        )
        playbooks = self._network_security_playbooks(
            security_auto_dev,
            network.get("network_security_upgrades", ()),
            backlog,
        )
        codebase_actions = self._codebase_continuity_actions(
            codebase,
            module_progress,
            mitigation.get("codebase_tasks"),
        )
        managerial_overwatch = self._managerial_overwatch(
            guidance,
            resilience_overwatch,
            continuity_index,
        )

        return {
            "timeline": tuple(timeline),
            "continuity_index": continuity_index,
            "continuity_risks": continuity_risks,
            "holographic_transmission_actions": holographic_actions,
            "network_security_playbooks": tuple(playbooks),
            "codebase_continuity_actions": codebase_actions,
            "managerial_overwatch": managerial_overwatch,
        }

    def _timeline(
        self,
        priority: str,
        mitigation_priority: str,
        network_security_score: float,
        debt_risk: float,
        guardrail_severity: str,
        grade: str,
        module_progress: Mapping[str, Any] | Sequence[Mapping[str, Any]],
    ) -> list[dict[str, Any]]:
        addressed_total = 0
        if isinstance(module_progress, Mapping):
            addressed_flags = module_progress.get("addressed", ())
            addressed_total = len([flag for flag in addressed_flags if flag])
        else:
            addressed_total = sum(
                1
                for entry in module_progress
                if isinstance(entry, Mapping) and entry.get("addressed")
            )
        windows: list[dict[str, Any]] = []

        immediate_focus = "Stabilise critical systems" if priority in {"high", "critical"} or network_security_score < 60.0 else "Monitor baseline operations"
        windows.append(
            {
                "window": f"Day 0-{self.short_window_days}",
                "focus": immediate_focus,
                "drivers": (
                    f"priority:{priority}",
                    f"guardrail:{guardrail_severity}",
                    f"grade:{grade}",
                ),
                "addressed_modules": addressed_total,
            }
        )

        network_focus = "Accelerate security automation" if network_security_score < 70.0 else "Maintain network cadence"
        windows.append(
            {
                "window": f"Day {self.short_window_days + 1}-{self.mid_window_days}",
                "focus": network_focus,
                "drivers": (
                    f"mitigation:{mitigation_priority}",
                    f"security:{round(network_security_score, 2)}",
                ),
                "guardrail_severity": guardrail_severity,
            }
        )

        codebase_focus = "Retire technical debt" if debt_risk >= 3.0 else "Expand quest automation"
        windows.append(
            {
                "window": f"Day {self.mid_window_days + 1}-{self.horizon_days}",
                "focus": codebase_focus,
                "drivers": (
                    f"debt_risk:{round(debt_risk, 1)}",
                    f"resilience_grade:{grade}",
                ),
                "forecast": "holographic-upgrade" if guardrail_severity in {"elevated", "critical"} else "steady-state",
            }
        )

        return windows

    def _continuity_index(
        self,
        network_security_score: float,
        resilience_index: float,
        debt_risk: float,
        mitigation_score: float,
    ) -> float:
        network_component = max(0.0, min(1.0, network_security_score / 100.0))
        resilience_component = max(0.0, min(1.0, resilience_index))
        debt_component = 1.0 - max(0.0, min(1.0, debt_risk / 5.0))
        mitigation_component = max(0.0, min(1.0, mitigation_score / 100.0))
        continuity = (
            network_component * 0.35
            + resilience_component * 0.25
            + debt_component * 0.2
            + mitigation_component * 0.2
        )
        return round(min(1.0, continuity), 3)

    def _continuity_risks(
        self,
        network_security_score: float,
        debt_risk: float,
        guardrail_severity: str,
        research_penalty: float,
        codebase_outlook: str,
    ) -> dict[str, Any]:
        network_risk = "critical" if network_security_score < 50.0 else "elevated" if network_security_score < 65.0 else "managed"
        codebase_risk = "high" if debt_risk >= 3.5 else "moderate" if debt_risk >= 2.0 else "low"
        research_risk = "pressure" if research_penalty >= 0.25 else "balanced"
        return {
            "network": network_risk,
            "codebase": codebase_risk,
            "holographic": guardrail_severity,
            "research": research_risk,
            "outlook": codebase_outlook,
        }

    def _holographic_actions(
        self,
        guardrails: Mapping[str, Any],
        enhancements: Mapping[str, Any],
        diagnostics: Mapping[str, Any],
        lithographic: Mapping[str, Any],
    ) -> dict[str, Any]:
        actions = _normalise_strings(guardrails.get("actions"))
        actions.extend(_normalise_strings(enhancements.get("actions")))
        if not actions:
            actions.append("Maintain spectral lattice")
        return {
            "actions": tuple(dict.fromkeys(actions)),
            "guardrail_status": guardrails.get("status", "nominal"),
            "phase_coherence": _as_float(diagnostics.get("phase_coherence_index")),
            "efficiency": _as_float(diagnostics.get("efficiency_score")),
            "lithographic_score": _as_float(lithographic.get("score")),
        }

    def _network_security_playbooks(
        self,
        security_auto_dev: Mapping[str, Any],
        upgrades: Sequence[Any],
        backlog: Mapping[str, Any],
    ) -> list[dict[str, Any]]:
        directive = str(security_auto_dev.get("directive", "stabilise"))
        automation_score = _as_float(security_auto_dev.get("automation_score"))
        playbooks: list[dict[str, Any]] = []
        for index, upgrade in enumerate(upgrades, start=1):
            playbooks.append(
                {
                    "name": str(upgrade),
                    "directive": directive,
                    "window": "short-term" if index == 1 else "mid-term",
                }
            )
        priority = str(backlog.get("priority", "low"))
        if priority in {"medium", "high"}:
            playbooks.append(
                {
                    "name": "Rebalance upgrade backlog",
                    "directive": directive,
                    "window": "mid-term",
                }
            )
        if automation_score < 55.0:
            playbooks.append(
                {
                    "name": "Raise automation scoring",  # emphasise security auto-dev improvements
                    "directive": "bootstrap",
                    "window": "short-term",
                }
            )
        if not playbooks:
            playbooks.append(
                {
                    "name": "Maintain current security automation cadence",
                    "directive": directive,
                    "window": "monitor",
                }
            )
        return playbooks

    def _codebase_continuity_actions(
        self,
        codebase: Mapping[str, Any],
        progress: Mapping[str, Any] | Sequence[Mapping[str, Any]],
        mitigation_tasks: Any,
    ) -> dict[str, Any]:
        scorecards: Sequence[Mapping[str, Any]] = codebase.get("module_scorecards", ())  # type: ignore[assignment]
        addressed: list[str] = []
        outstanding: list[str] = []
        if isinstance(progress, Mapping):
            addressed = _normalise_strings(progress.get("addressed_modules"))
            outstanding = _normalise_strings(progress.get("outstanding_modules"))
        else:
            for entry in progress:
                if not isinstance(entry, Mapping):
                    continue
                name = str(entry.get("name", ""))
                if not name:
                    continue
                if entry.get("addressed"):
                    addressed.append(name)
                else:
                    outstanding.append(name)
        priority_modules = [card.get("name") for card in scorecards if card.get("risk") in {"high", "critical"}]
        tasks = []
        for task in mitigation_tasks or ():
            if isinstance(task, Mapping):
                tasks.append(str(task.get("task", "")))
            else:
                tasks.append(str(task))
        return {
            "stability_outlook": codebase.get("stability_outlook", "steady"),
            "priority_modules": tuple(name for name in priority_modules if name),
            "addressed_modules": tuple(addressed),
            "outstanding_modules": tuple(outstanding),
            "planned_tasks": tuple(task for task in tasks if task),
        }

    def _managerial_overwatch(
        self,
        guidance: Mapping[str, Any],
        resilience_overwatch: Mapping[str, Any],
        continuity_index: float,
    ) -> dict[str, Any]:
        threads = list(resilience_overwatch.get("managerial_threads", ()))  # type: ignore[assignment]
        threads.extend(guidance.get("managerial_threads", ()))
        if not threads:
            threads.append("stability-watch")
        return {
            "priority": guidance.get("priority", resilience_overwatch.get("priority", "low")),
            "governance_outlook": guidance.get(
                "governance_outlook",
                resilience_overwatch.get("governance_outlook", "guidance-monitor"),
            ),
            "alignment": guidance.get("backend_alignment_score", resilience_overwatch.get("backend_alignment", 0.0)),
            "continuity_index": continuity_index,
            "managerial_threads": tuple(dict.fromkeys(threads))[:5],
        }
