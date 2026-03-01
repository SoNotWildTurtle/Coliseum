"""Blend managerial telemetry into a self-evolution blueprint."""

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
class AutoDevSelfEvolutionManager:
    """Fuse pipeline outputs into actionable self-evolution directives."""

    horizon: int = 4

    def blueprint(
        self,
        *,
        guidance: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        continuity: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a consolidated managerial blueprint for auto-dev evolution."""

        guidance = guidance or {}
        network = network or {}
        codebase = codebase or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        transmission = transmission or {}
        security = security or {}
        governance = governance or {}
        research = research or {}
        continuity = continuity or {}
        resilience = resilience or {}

        intelligence_score = _as_float(guidance.get("general_intelligence_score"))
        security_score = _as_float(
            security.get("security_score", network.get("network_security_score", 0.0))
        )
        coverage = _as_float(codebase.get("coverage_ratio"))
        stability_score = _as_float(mitigation.get("stability_score"))
        readiness_index = self._readiness_index(
            intelligence_score,
            security_score,
            coverage,
            stability_score,
        )
        readiness_state = self._readiness_state(
            readiness_index,
            governance.get("state"),
        )

        upgrade_directives = self._upgrade_directives(network)
        security_enhancements = self._security_enhancements(security)
        holographic_directives = self._holographic_directives(transmission)
        codebase_focus = self._codebase_focus(codebase, mitigation, remediation)
        research_focus = self._research_focus(research, mitigation)
        oversight = self._oversight(governance)
        progress_overview = self._progress_overview(remediation)
        managerial_threads = self._managerial_threads(guidance)
        composite_score = self._composite_score(
            intelligence_score,
            security_score,
            stability_score,
            readiness_index,
        )
        next_actions = self._next_actions(
            upgrade_directives,
            security_enhancements,
            holographic_directives,
            codebase_focus["mitigation_plan"],
            research_focus["tasks"],
        )
        learning_loops = self._learning_loops(
            continuity,
            resilience,
            readiness_state,
        )
        telemetry_focus = self._telemetry_focus(
            continuity,
            resilience,
            readiness_state,
        )
        adaptive_tuning = self._adaptive_tuning(
            readiness_state,
            continuity,
            resilience,
            governance,
        )

        managerial_overwatch = {
            "intelligence_score": round(intelligence_score, 2),
            "composite_score": composite_score,
            "threads": managerial_threads,
            "governance_state": oversight["state"],
        }

        return {
            "horizon": self.horizon,
            "readiness_index": readiness_index,
            "readiness_state": readiness_state,
            "managerial_overwatch": managerial_overwatch,
            "upgrade_directives": upgrade_directives,
            "security_enhancements": security_enhancements,
            "holographic_directives": holographic_directives,
            "codebase_focus": codebase_focus,
            "research_focus": research_focus,
            "governance_alignment": oversight,
            "progress_overview": progress_overview,
            "learning_loops": learning_loops,
            "telemetry_focus": telemetry_focus,
            "adaptive_tuning": adaptive_tuning,
            "next_actions": next_actions,
        }

    def _readiness_index(
        self,
        intelligence_score: float,
        security_score: float,
        coverage: float,
        stability_score: float,
    ) -> float:
        composite = (
            intelligence_score / 100.0
            + security_score / 100.0
            + max(0.0, min(1.0, coverage))
            + stability_score / 100.0
        ) / 4.0
        return round(max(0.0, min(1.0, composite)), 3)

    def _readiness_state(self, readiness: float, governance_state: Any) -> str:
        state = "triage"
        if readiness >= 0.78:
            state = "accelerate"
        elif readiness >= 0.58:
            state = "expand"
        elif readiness >= 0.38:
            state = "stabilise"
        gov_state = str(governance_state or "").lower()
        if gov_state in {"intervene", "triage"}:
            return "triage"
        if gov_state in {"guided", "directive"} and readiness >= 0.58:
            return "expand"
        if gov_state in {"monitor", "observational"} and readiness < 0.38:
            return "stabilise"
        return state

    def _upgrade_directives(self, network: Mapping[str, Any]) -> tuple[str, ...]:
        paths: list[str] = []
        paths.extend(str(path) for path in network.get("upgrade_paths", ()))
        paths.extend(str(path) for path in network.get("network_security_upgrades", ()))
        security_auto_dev = network.get("security_auto_dev", {})
        directive = security_auto_dev.get("directive")
        if directive:
            paths.append(f"Security focus: {directive}")
        if not paths:
            paths.append("Maintain upgrade cadence")
        return _dedupe(paths)

    def _security_enhancements(self, security: Mapping[str, Any]) -> tuple[str, ...]:
        actions = [str(action) for action in security.get("network_security_actions", ())]
        hardening = security.get("hardening_tasks") or ()
        for task in hardening:
            if isinstance(task, Mapping):
                actions.append(
                    f"Hardening: {task.get('module', 'module')} ({task.get('risk_level', 'low')})"
                )
        if not actions:
            actions.append("Review security automation posture")
        return _dedupe(actions)

    def _holographic_directives(self, transmission: Mapping[str, Any]) -> tuple[str, ...]:
        actions: list[str] = []
        waveform = transmission.get("spectral_waveform", {})
        overlay = transmission.get("lattice_overlay", {})
        guardrails = transmission.get("guardrails", {})
        notes = transmission.get("notes", ())
        actions.extend(str(step) for step in waveform.get("recommended_actions", ()))
        actions.extend(str(step) for step in overlay.get("actions", ()))
        actions.extend(str(step) for step in guardrails.get("follow_up", ()))
        actions.extend(str(step) for step in notes or ())
        if not actions:
            actions.append("Maintain spectral balance")
        return _dedupe(actions)

    def _codebase_focus(
        self,
        codebase: Mapping[str, Any],
        mitigation: Mapping[str, Any],
        remediation: Mapping[str, Any],
    ) -> dict[str, Any]:
        mitigation_plan = tuple(str(item) for item in codebase.get("mitigation_plan", ()))
        modernization = tuple(
            str(item) for item in codebase.get("modernization_targets", ())
        )
        progress: Sequence[Mapping[str, Any]] = remediation.get(
            "codebase_progress", ()
        )  # type: ignore[assignment]
        addressed = sum(1 for entry in progress if entry.get("addressed"))
        total = len(progress)
        coverage = _as_float(codebase.get("coverage_ratio"))
        return {
            "stability_outlook": codebase.get("stability_outlook", "stable"),
            "mitigation_plan": mitigation_plan,
            "modernization_targets": modernization,
            "progress": tuple(progress),
            "addressed_modules": addressed,
            "total_modules": total,
            "coverage_ratio": round(coverage, 2),
            "mitigation_priority": mitigation.get("priority", "monitor"),
        }

    def _research_focus(
        self,
        research: Mapping[str, Any],
        mitigation: Mapping[str, Any],
    ) -> dict[str, Any]:
        utilization = 0.0
        for key in (
            "raw_utilization_percent",
            "latest_sample_percent",
            "utilization_percent",
        ):
            value = research.get(key)
            if value is not None:
                utilization = _as_float(value)
                break
        pressure = _as_float(research.get("research_pressure_index"))
        tasks = tuple(str(task) for task in mitigation.get("research_tasks", ()))
        return {
            "utilization_percent": round(utilization, 2),
            "pressure_index": round(pressure, 2),
            "tasks": tasks,
            "competitive_utilization_percent": _as_float(
                research.get("competitive_utilization_percent", 0.0)
            ),
        }

    def _oversight(self, governance: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "state": governance.get("state", "guided"),
            "score": _as_float(governance.get("oversight_score", 0.0)),
            "actions": _dedupe(governance.get("oversight_actions")),
        }

    def _progress_overview(self, remediation: Mapping[str, Any]) -> dict[str, Any]:
        applied_counts = self._domain_counts(remediation.get("applied_fixes"))
        scheduled_counts = self._domain_counts(remediation.get("scheduled_fixes"))
        return {
            "applied": applied_counts,
            "scheduled": scheduled_counts,
        }

    def _domain_counts(self, entries: Sequence[Mapping[str, Any]] | None) -> dict[str, int]:
        counts: dict[str, int] = {}
        for entry in entries or ():
            domain = str(entry.get("domain", "general"))
            counts[domain] = counts.get(domain, 0) + 1
        return counts

    def _managerial_threads(self, guidance: Mapping[str, Any]) -> tuple[str, ...]:
        threads: list[str] = []
        threads.extend(str(value) for value in guidance.get("managerial_threads", ()))
        threads.extend(str(value) for value in guidance.get("guidance_backbone", ()))
        return _dedupe(threads)

    def _composite_score(
        self,
        intelligence_score: float,
        security_score: float,
        stability_score: float,
        readiness_index: float,
    ) -> float:
        composite = (
            intelligence_score * 0.45
            + security_score * 0.25
            + stability_score * 0.2
            + readiness_index * 100.0 * 0.1
        )
        return round(max(0.0, min(100.0, composite)), 2)

    def _next_actions(
        self,
        upgrades: Sequence[str],
        security: Sequence[str],
        holographic: Sequence[str],
        codebase_tasks: Sequence[str],
        research_tasks: Sequence[str],
    ) -> tuple[str, ...]:
        actions: list[str] = []
        for bucket in (upgrades, security, holographic, codebase_tasks, research_tasks):
            if bucket:
                actions.append(str(bucket[0]))
        if not actions:
            actions.append("Collect managerial telemetry")
        return _dedupe(actions)

    def _learning_loops(
        self,
        continuity: Mapping[str, Any],
        resilience: Mapping[str, Any],
        readiness_state: str,
    ) -> tuple[str, ...]:
        loops: list[str] = []
        timeline = continuity.get("timeline", ())
        for entry in timeline:
            if isinstance(entry, Mapping):
                focus = entry.get("focus")
                if focus:
                    loops.append(str(focus))
        resilience_actions = resilience.get("resilience_actions", ())
        loops.extend(str(action) for action in resilience_actions)
        if readiness_state in {"triage", "stabilise"}:
            loops.append("Run stability retrospectives every sprint")
        if not loops:
            loops.append("Maintain evolution feedback cadence")
        return _dedupe(loops)[:6]

    def _telemetry_focus(
        self,
        continuity: Mapping[str, Any],
        resilience: Mapping[str, Any],
        readiness_state: str,
    ) -> dict[str, Any]:
        continuity_risks = continuity.get("continuity_risks", {})
        resilience_grade = resilience.get("grade", "steady")
        watchlist = []
        for key, value in continuity_risks.items() if isinstance(continuity_risks, Mapping) else []:
            watchlist.append(f"{key}:{value}")
        if readiness_state in {"triage", "stabilise"}:
            watchlist.append("recovery:focus")
        return {
            "readiness_state": readiness_state,
            "resilience_grade": resilience_grade,
            "watchlist": tuple(dict.fromkeys(watchlist)),
        }

    def _adaptive_tuning(
        self,
        readiness_state: str,
        continuity: Mapping[str, Any],
        resilience: Mapping[str, Any],
        governance: Mapping[str, Any],
    ) -> dict[str, Any]:
        continuity_risks = continuity.get("continuity_risks", {})
        grade = str(resilience.get("grade", "steady"))
        governance_state = str(governance.get("state", "guided"))
        focus = "stability"
        if readiness_state in {"expand", "accelerate"}:
            focus = "innovation"
        if isinstance(continuity_risks, Mapping):
            network_risk = str(continuity_risks.get("network", "managed"))
            if network_risk in {"critical", "elevated"}:
                focus = "security"
        cadence = "weekly"
        if readiness_state in {"triage", "stabilise"}:
            cadence = "daily"
        elif readiness_state in {"accelerate"}:
            cadence = "twice-weekly"
        risk_budget = "balanced"
        if grade in {"fortified", "resilient"} and readiness_state in {
            "expand",
            "accelerate",
        }:
            risk_budget = "aggressive"
        elif readiness_state in {"triage"}:
            risk_budget = "conservative"
        feedback_window = 3 if cadence == "daily" else 7
        return {
            "focus": focus,
            "cadence": cadence,
            "risk_budget": risk_budget,
            "feedback_window_days": feedback_window,
            "governance_state": governance_state,
        }
