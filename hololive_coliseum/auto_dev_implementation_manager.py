"""Translate functionality and creation telemetry into implementation briefs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def _normalise_strings(values: Sequence[Any] | None) -> tuple[str, ...]:
    results: list[str] = []
    for value in values or ():
        if isinstance(value, Mapping):
            text = str(value.get("name", "")).strip()
        else:
            text = str(value).strip()
        if text and text not in results:
            results.append(text)
    return tuple(results)


def _merge_network_requirements(
    primary: Mapping[str, Any] | None,
    *supplemental: Mapping[str, Any] | None,
) -> dict[str, Any]:
    security_scores: list[float] = []
    bandwidth_samples: list[float] = []
    latency_targets: list[float] = []
    upgrade_actions: list[str] = []
    for requirement in (primary, *supplemental):
        if not isinstance(requirement, Mapping):
            continue
        security_scores.append(_as_float(requirement.get("security_score")))
        bandwidth_samples.append(_as_float(requirement.get("bandwidth_mbps")))
        latency_targets.append(_as_float(requirement.get("latency_target_ms")))
        upgrade_actions.extend(
            _normalise_strings(requirement.get("upgrade_actions"))
        )
    security_score = (
        sum(security_scores) / len(security_scores) if security_scores else 0.0
    )
    bandwidth = max(bandwidth_samples) if bandwidth_samples else 0.0
    latency = (
        sum(latency_targets) / len(latency_targets) if latency_targets else 0.0
    )
    return {
        "security_score": round(security_score, 2),
        "bandwidth_mbps": round(bandwidth, 2),
        "latency_target_ms": round(latency, 2) if latency else 0.0,
        "upgrade_actions": tuple(dict.fromkeys(upgrade_actions)),
    }


def _merge_holographic_requirements(
    transmission: Mapping[str, Any] | None,
    *requirements: Mapping[str, Any] | None,
) -> dict[str, Any]:
    actions: list[str] = []
    efficiency_scores: list[float] = []
    phase_targets: list[float] = []
    for requirement in requirements:
        if not isinstance(requirement, Mapping):
            continue
        actions.extend(
            _normalise_strings(requirement.get("recommended_actions"))
        )
        efficiency_scores.append(_as_float(requirement.get("efficiency_score")))
        phase_targets.append(_as_float(requirement.get("phase_target")))
    transmission = transmission or {}
    phase_alignment: Mapping[str, Any] = transmission.get(
        "phase_alignment", {}
    )  # type: ignore[assignment]
    lithographic: Mapping[str, Any] = transmission.get(
        "lithographic_integrity", {}
    )  # type: ignore[assignment]
    actions.extend(_normalise_strings(phase_alignment.get("recommended_actions")))
    efficiency_scores.append(_as_float(lithographic.get("score")))
    phase_targets.append(_as_float(phase_alignment.get("target")))
    efficiency = (
        sum(efficiency_scores) / len(efficiency_scores)
        if efficiency_scores
        else 0.0
    )
    phase_target = (
        sum(phase_targets) / len(phase_targets) if phase_targets else 0.0
    )
    return {
        "recommended_actions": tuple(dict.fromkeys(actions)),
        "efficiency_score": round(efficiency, 2),
        "phase_target": round(phase_target, 2),
    }


def _priority(score: float, gap_index: float, risk_index: float) -> str:
    if score >= 82.0 and gap_index <= 28.0 and risk_index <= 32.0:
        return "deploy"
    if score >= 74.0 and gap_index <= 36.0:
        return "accelerate"
    if score >= 64.0:
        return "stabilise"
    if score >= 52.0:
        return "refine"
    return "observe"


def _readiness(score: float, gap_index: float, risk_index: float) -> str:
    if score >= 80.0 and gap_index <= 30.0 and risk_index <= 28.0:
        return "ready"
    if score >= 70.0 and risk_index <= 40.0:
        return "align"
    if gap_index >= 55.0 or risk_index >= 60.0:
        return "stabilise"
    return "refine"


def _delivery_windows(
    prototype_requirements: Sequence[Mapping[str, Any]] | None,
    mitigation_windows: Sequence[Any] | None,
    remediation_schedule: Sequence[Mapping[str, Any]] | None,
    modernization_timeline: Sequence[Mapping[str, Any]] | None,
) -> tuple[str, ...]:
    windows: list[str] = []
    for requirement in prototype_requirements or ():
        window = str(requirement.get("window", "")).strip()
        focus = str(requirement.get("focus", "creation")).strip() or "creation"
        if window:
            entry = f"{window}::{focus}"
            if entry not in windows:
                windows.append(entry)
    for entry in mitigation_windows or ():
        if isinstance(entry, Mapping):
            window = str(entry.get("window", "")).strip()
            focus = str(entry.get("focus", "mitigation")).strip() or "mitigation"
        else:
            window = str(entry).strip()
            focus = "mitigation"
        if window:
            label = f"{window}::{focus}"
            if label not in windows:
                windows.append(label)
    for task in remediation_schedule or ():
        if not isinstance(task, Mapping):
            continue
        domain = str(task.get("domain", "remediation")).strip() or "remediation"
        descriptor = str(task.get("task", "")).strip()
        if descriptor:
            label = f"{domain}::{descriptor[:42]}"
            if label not in windows:
                windows.append(label)
    for milestone in modernization_timeline or ():
        if not isinstance(milestone, Mapping):
            continue
        window = str(milestone.get("window", "")).strip()
        focus = str(milestone.get("focus", "modernization")).strip() or "modernization"
        if window:
            label = f"{window}::{focus}"
            if label not in windows:
                windows.append(label)
    return tuple(windows[:8])


def _backlog(
    scheduled: Sequence[Mapping[str, Any]] | None,
    modernization_targets: Sequence[Mapping[str, Any]] | None,
) -> tuple[dict[str, Any], ...]:
    backlog: list[dict[str, Any]] = []
    for task in scheduled or ():
        if not isinstance(task, Mapping):
            continue
        backlog.append(
            {
                "domain": str(task.get("domain", "remediation")),
                "task": str(task.get("task", ""))[:72],
                "severity": str(task.get("severity", "medium")),
            }
        )
    for target in modernization_targets or ():
        if not isinstance(target, Mapping):
            continue
        backlog.append(
            {
                "domain": "modernization",
                "task": str(target.get("name", "upgrade")),
                "severity": "high",
            }
        )
    unique: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in backlog:
        key = (item.get("domain", ""), item.get("task", ""))
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return tuple(unique[:10])


def _codebase_alignment(codebase: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "implementation_alignment_score": _as_float(
            codebase.get("implementation_alignment_score")
        ),
        "implementation_gap_index": _as_float(
            codebase.get("implementation_gap_index")
        ),
        "implementation_focus_modules": tuple(
            codebase.get("implementation_focus_modules", ())
        ),
        "implementation_recommendations": tuple(
            codebase.get("implementation_recommendations", ())
        ),
    }


def _security_alignment(security: Mapping[str, Any]) -> dict[str, Any]:
    lattice: Mapping[str, Any] = security.get(
        "holographic_lattice", {}
    )  # type: ignore[assignment]
    return {
        "threat_level": str(security.get("threat_level", "guarded")),
        "security_score": _as_float(security.get("security_score")),
        "recommended_actions": tuple(
            dict.fromkeys(security.get("network_security_actions", ()))
        ),
        "lattice_density": _as_float(lattice.get("density", 0.0)),
        "lattice_actions": tuple(dict.fromkeys(lattice.get("actions", ()))),
    }


def _research_implications(research: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "utilization_percent": _as_float(
            research.get("raw_utilization_percent")
            or research.get("latest_sample_percent")
        ),
        "pressure_index": _as_float(research.get("research_pressure_index")),
        "trend": str(research.get("trend_direction", research.get("trend", "steady"))),
    }


@dataclass
class AutoDevImplementationManager:
    """Fuse functionality, creation, and convergence data into implementation plans."""

    functionality_weight: float = 0.26
    creation_weight: float = 0.24
    convergence_weight: float = 0.2
    design_weight: float = 0.16
    systems_weight: float = 0.14

    def implementation_brief(
        self,
        *,
        functionality: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        gameplay: Mapping[str, Any] | None = None,
        design: Mapping[str, Any] | None = None,
        systems: Mapping[str, Any] | None = None,
        creation: Mapping[str, Any] | None = None,
        synthesis: Mapping[str, Any] | None = None,
        convergence: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        integrity: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        network_auto_dev: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
        guidance: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return an implementation brief that links mechanics to execution windows."""

        functionality = functionality or {}
        mechanics = mechanics or {}
        gameplay = gameplay or {}
        design = design or {}
        systems = systems or {}
        creation = creation or {}
        synthesis = synthesis or {}
        convergence = convergence or {}
        codebase = codebase or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        modernization = modernization or {}
        optimization = optimization or {}
        integrity = integrity or {}
        resilience = resilience or {}
        security = security or {}
        network_auto_dev = network_auto_dev or {}
        transmission = transmission or {}
        research = research or {}
        governance = governance or {}
        guidance = guidance or {}

        functionality_score = _as_float(functionality.get("functionality_score"))
        creation_score = _as_float(creation.get("creation_score"))
        convergence_score = _as_float(convergence.get("convergence_score"))
        design_score = _as_float(design.get("design_score"))
        systems_score = _as_float(systems.get("systems_score"))

        modernization_priority = str(modernization.get("priority", "monitor"))
        optimization_priority = str(optimization.get("priority", "monitor"))
        integrity_priority = str(integrity.get("priority", "monitor"))

        base_score = (
            functionality_score * self.functionality_weight
            + creation_score * self.creation_weight
            + convergence_score * self.convergence_weight
            + design_score * self.design_weight
            + systems_score * self.systems_weight
        )
        if modernization_priority in {"accelerate", "amplify"}:
            base_score += 4.0
        if optimization_priority in {"accelerate", "amplify"}:
            base_score += 3.0
        if integrity_priority in {"stabilise", "accelerate"}:
            base_score -= 3.5
        implementation_score = _clamp(base_score)

        functionality_gap = _as_float(codebase.get("functionality_gap_index"))
        creation_gap = _as_float(codebase.get("creation_gap_index"))
        convergence_gap = _as_float(codebase.get("convergence_gap_index"))
        implementation_gap = _as_float(
            codebase.get("implementation_gap_index")
            or (functionality_gap * 0.3 + creation_gap * 0.35 + convergence_gap * 0.25)
        )
        gap_index = _clamp(implementation_gap)

        functionality_risk = _as_float(functionality.get("risk_index"))
        creation_risk = _as_float(
            (creation.get("risk_profile") or {}).get("risk_index", 0.0)
        )
        security_gap = _as_float(integrity.get("security_gap"))
        coverage_gap = _as_float(integrity.get("coverage_gap"))
        resilience_index = _as_float(resilience.get("resilience_index"))
        risk_index = _clamp(
            functionality_risk * 0.35
            + creation_risk * 0.3
            + security_gap * 0.18
            + (coverage_gap * 100.0) * 0.12
            + (1.0 - min(resilience_index, 1.0)) * 35.0
        )

        priority = _priority(implementation_score, gap_index, risk_index)
        readiness_state = _readiness(implementation_score, gap_index, risk_index)

        functionality_tracks = _normalise_strings(
            functionality.get("functionality_tracks")
        )
        mechanics_threads = _normalise_strings(
            mechanics.get("gameplay_threads")
        )
        creation_tracks = _normalise_strings(creation.get("creation_tracks"))
        convergence_tracks = _normalise_strings(
            convergence.get("convergence_tracks")
        )
        synthesis_tracks = _normalise_strings(synthesis.get("expansion_tracks"))
        gameplay_loops = _normalise_strings(gameplay.get("loops"))

        implementation_tracks = tuple(
            dict.fromkeys(
                (
                    *functionality_tracks,
                    *creation_tracks,
                    *convergence_tracks,
                    *synthesis_tracks,
                )
            )
        )
        implementation_threads = tuple(
            dict.fromkeys(
                (
                    *mechanics_threads,
                    *creation.get("creation_threads", ()),
                    *convergence.get("convergence_threads", ()),
                )
            )
        )
        action_sources: list[str] = []
        for value in creation.get("creation_actions", ()):
            action_sources.append(str(value).strip())
        for value in convergence.get("convergence_actions", ()):
            action_sources.append(str(value).strip())
        for value in synthesis.get("expansion_actions", ()):
            action_sources.append(str(value).strip())
        for task in mitigation.get("codebase_tasks", ()):  # type: ignore[arg-type]
            if isinstance(task, Mapping):
                action_sources.append(str(task.get("task", "")).strip())
            else:
                action_sources.append(str(task).strip())
        implementation_actions = tuple(
            item
            for item in dict.fromkeys(action_sources)
            if item
        )

        delivery_windows = _delivery_windows(
            creation.get("prototype_requirements"),
            mitigation.get("execution_windows"),
            remediation.get("scheduled_fixes"),
            modernization.get("timeline"),
        )
        readiness_window = delivery_windows[0] if delivery_windows else "unscheduled"

        applied_fixes: Sequence[Mapping[str, Any]] = remediation.get(
            "applied_fixes", ()
        )  # type: ignore[assignment]
        scheduled_fixes: Sequence[Mapping[str, Any]] = remediation.get(
            "scheduled_fixes", ()
        )  # type: ignore[assignment]
        velocity_index = _clamp(
            (len(applied_fixes) * 18.0)
            + (len(delivery_windows) * 3.5)
            + (2.5 if priority in {"deploy", "accelerate"} else 0.0)
            - (len(scheduled_fixes) * 2.0)
        )

        network_requirements = _merge_network_requirements(
            creation.get("network_requirements"),
            convergence.get("network_requirements"),
            functionality.get("network_requirements"),
            network_auto_dev.get("network_requirements"),
        )
        holographic_requirements = _merge_holographic_requirements(
            transmission,
            creation.get("holographic_requirements"),
            convergence.get("holographic_requirements"),
            functionality.get("holographic_hooks"),
        )

        supporting_signals: Mapping[str, Any] = creation.get(
            "supporting_signals", {}
        )  # type: ignore[assignment]
        signal_values = tuple(
            str(value)
            for value in (
                supporting_signals.get("modernization_priority"),
                supporting_signals.get("optimization_priority"),
                supporting_signals.get("integrity_priority"),
            )
            if value
        )
        managerial_directives = tuple(
            dict.fromkeys(
                (
                    *functionality.get("managerial_directives", ()),
                    *signal_values,
                    *governance.get("oversight_actions", ()),
                    *guidance.get("backend_guidance_vector", ()),
                )
            )
        )

        functionality_targets = tuple(
            dict.fromkeys(
                (
                    *functionality_tracks,
                    *gameplay_loops,
                    *mechanics.get("mechanic_archetypes", ()),
                )
            )
        )
        integration_actions = tuple(
            dict.fromkeys(
                (
                    *synthesis.get("expansion_actions", ()),
                    *convergence.get("convergence_actions", ()),
                )
            )
        )

        security_alignment = _security_alignment(security)
        modernization_alignment = modernization.get(
            "network_alignment", {}
        )  # type: ignore[assignment]
        holographic_alignment: Mapping[str, Any] = resilience.get(
            "holographic_readiness", {}
        )  # type: ignore[assignment]

        research_summary = _research_implications(research)
        codebase_alignment = _codebase_alignment(codebase)

        backlog = _backlog(
            remediation.get("scheduled_fixes"),
            modernization.get("modernization_targets"),
        )

        governance_state = str(governance.get("state", "guided"))
        governance_actions = tuple(governance.get("oversight_actions", ()))

        return {
            "priority": priority,
            "implementation_score": round(implementation_score, 2),
            "implementation_gap_index": round(gap_index, 2),
            "implementation_risk_index": round(risk_index, 2),
            "implementation_tracks": implementation_tracks,
            "implementation_threads": implementation_threads,
            "implementation_actions": implementation_actions,
            "delivery_windows": delivery_windows,
            "readiness_state": readiness_state,
            "readiness_window": readiness_window,
            "implementation_velocity_index": round(velocity_index, 2),
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "security_alignment": security_alignment,
            "modernization_alignment": modernization_alignment,
            "holographic_alignment": holographic_alignment,
            "codebase_alignment": codebase_alignment,
            "research_implications": research_summary,
            "managerial_directives": managerial_directives,
            "functionality_targets": functionality_targets,
            "integration_actions": integration_actions,
            "prototype_requirements": tuple(
                creation.get("prototype_requirements", ())
            ),
            "implementation_backlog": backlog,
            "governance_state": governance_state,
            "governance_actions": governance_actions,
            "applied_fixes": tuple(applied_fixes),
        }
