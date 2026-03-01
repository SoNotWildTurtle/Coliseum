"""Blend implementation readiness into execution orchestration telemetry."""

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


def _normalise_strings(values: Sequence[Any] | None) -> list[str]:
    results: list[str] = []
    for value in values or ():
        if isinstance(value, Mapping):
            text = str(value.get("name", "")).strip()
        else:
            text = str(value).strip()
        if text and text not in results:
            results.append(text)
    return results


def _merge_network_requirements(
    *requirements: Mapping[str, Any] | None,
) -> dict[str, Any]:
    security_scores: list[float] = []
    bandwidth_samples: list[float] = []
    latency_targets: list[float] = []
    upgrade_actions: list[str] = []
    for requirement in requirements:
        if not isinstance(requirement, Mapping):
            continue
        security_scores.append(_as_float(requirement.get("security_score")))
        bandwidth_samples.append(_as_float(requirement.get("bandwidth_mbps")))
        latency_targets.append(_as_float(requirement.get("latency_target_ms")))
        upgrade_actions.extend(_normalise_strings(requirement.get("upgrade_actions")))
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
    transmission = transmission or {}
    phase_alignment: Mapping[str, Any] = transmission.get("phase_alignment", {})
    lithographic: Mapping[str, Any] = transmission.get("lithographic_integrity", {})
    actions = _normalise_strings(phase_alignment.get("recommended_actions"))
    efficiency_scores = [_as_float(lithographic.get("score"))]
    phase_targets = [_as_float(phase_alignment.get("target"))]
    for requirement in requirements:
        if not isinstance(requirement, Mapping):
            continue
        actions.extend(_normalise_strings(requirement.get("recommended_actions")))
        efficiency_scores.append(_as_float(requirement.get("efficiency_score")))
        phase_targets.append(_as_float(requirement.get("phase_target")))
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


def _threat_penalty(level: str) -> float:
    level = level.lower()
    if level in {"at-risk", "critical"}:
        return 78.0
    if level in {"elevated", "high"}:
        return 52.0
    if level in {"guarded", "steady"}:
        return 34.0
    return 28.0


def _priority(score: float, gap_index: float, risk_index: float) -> str:
    if score >= 84.0 and gap_index <= 24.0 and risk_index <= 28.0:
        return "deploy"
    if score >= 76.0 and gap_index <= 36.0:
        return "accelerate"
    if score >= 66.0:
        return "stabilise"
    if score >= 54.0:
        return "align"
    return "monitor"


def _stability_state(
    score: float,
    risk_index: float,
    resilience_score: float,
    continuity_percent: float,
) -> str:
    if score >= 82.0 and risk_index <= 28.0 and continuity_percent >= 72.0:
        return "steady"
    if resilience_score >= 70.0 and risk_index <= 40.0:
        return "guarded"
    if risk_index >= 62.0 or continuity_percent <= 48.0:
        return "vigilant"
    return "balancing"


def _velocity_index(
    implementation_velocity: float,
    applied_fixes: Sequence[Any] | None,
    scheduled_fixes: Sequence[Any] | None,
    continuity_windows: Sequence[Any] | None,
) -> float:
    applied_count = len(applied_fixes or ())
    scheduled_count = len(scheduled_fixes or ())
    window_count = len(continuity_windows or ())
    velocity = (
        implementation_velocity * 0.6
        + applied_count * 6.0
        + window_count * 3.0
        - scheduled_count * 2.5
    )
    return _clamp(velocity)


def _execution_tracks(
    implementation_tracks: Sequence[Any] | None,
    convergence_tracks: Sequence[Any] | None,
    creation_tracks: Sequence[Any] | None,
    gameplay_loops: Sequence[Mapping[str, Any]] | None,
    systems_threads: Sequence[Any] | None,
) -> tuple[str, ...]:
    tracks: list[str] = []
    for source in (
        implementation_tracks,
        convergence_tracks,
        creation_tracks,
        systems_threads,
    ):
        for value in source or ():
            text = str(value).strip()
            if text and text not in tracks:
                tracks.append(text)
    for loop in gameplay_loops or ():
        if isinstance(loop, Mapping):
            name = str(loop.get("name", "")).strip()
        else:
            name = str(loop).strip()
        if name and name not in tracks:
            tracks.append(name)
    return tuple(tracks)


def _execution_actions(
    implementation_actions: Sequence[Any] | None,
    convergence_actions: Sequence[Any] | None,
    creation_actions: Sequence[Any] | None,
    gameplay_actions: Sequence[Any] | None,
    mitigation_tasks: Sequence[Any] | None,
    continuity_actions: Mapping[str, Any] | None,
) -> tuple[str, ...]:
    actions: list[str] = []
    for source in (
        implementation_actions,
        convergence_actions,
        creation_actions,
        gameplay_actions,
    ):
        for value in source or ():
            text = str(value).strip()
            if text and text not in actions:
                actions.append(text)
    for task in mitigation_tasks or ():
        if isinstance(task, Mapping):
            text = str(task.get("task", "")).strip()
        else:
            text = str(task).strip()
        if text and text not in actions:
            actions.append(text)
    continuity_actions = continuity_actions or {}
    for entry in continuity_actions.get("planned_tasks", ()):  # type: ignore[assignment]
        text = str(entry).strip()
        if text and text not in actions:
            actions.append(text)
    return tuple(actions)


def _execution_windows(
    implementation_windows: Sequence[Any] | None,
    continuity_timeline: Sequence[Mapping[str, Any]] | None,
) -> tuple[str, ...]:
    windows: list[str] = []
    for window in implementation_windows or ():
        text = str(window).strip()
        if text and text not in windows:
            windows.append(text)
    for entry in continuity_timeline or ():
        if not isinstance(entry, Mapping):
            continue
        label = str(entry.get("window", "")).strip()
        focus = str(entry.get("focus", "")).strip()
        if label:
            composite = f"{label}::{focus}" if focus else label
            if composite not in windows:
                windows.append(composite)
    return tuple(windows)


def _execution_backlog(
    implementation_backlog: Sequence[Mapping[str, Any]] | None,
    continuity_actions: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], ...]:
    backlog: list[dict[str, Any]] = []
    for item in implementation_backlog or ():
        if not isinstance(item, Mapping):
            continue
        backlog.append(
            {
                "module": item.get("module", item.get("name", "module")),
                "status": item.get("status", "scheduled"),
                "focus": item.get("focus", "implementation"),
            }
        )
    continuity_actions = continuity_actions or {}
    outstanding: Sequence[Any] = continuity_actions.get("outstanding_modules", ())  # type: ignore[assignment]
    for module in outstanding:
        name = str(module).strip()
        if name and not any(entry["module"] == name for entry in backlog):
            backlog.append({"module": name, "status": "continuity", "focus": "stability"})
    return tuple(backlog)


def _debt_penalty(risk_score: float) -> float:
    return max(0.0, min(100.0, risk_score * 80.0))


@dataclass
class AutoDevExecutionManager:
    """Fuse implementation, convergence, and guardrail telemetry into execution briefs."""

    def execution_brief(
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
        implementation: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
        continuity: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        functionality = functionality or {}
        mechanics = mechanics or {}
        gameplay = gameplay or {}
        design = design or {}
        systems = systems or {}
        creation = creation or {}
        synthesis = synthesis or {}
        convergence = convergence or {}
        implementation = implementation or {}
        network = network or {}
        transmission = transmission or {}
        security = security or {}
        modernization = modernization or {}
        optimization = optimization or {}
        resilience = resilience or {}
        continuity = continuity or {}
        governance = governance or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        research = research or {}
        codebase = codebase or {}

        implementation_score = _as_float(
            implementation.get("implementation_score")
        )
        convergence_alignment = _as_float(
            convergence.get("integration_index")
        )
        creation_alignment = _as_float(
            creation.get("creation_alignment_score")
        )
        functionality_score = _as_float(
            functionality.get("functionality_score")
        )
        gameplay_score = _as_float(gameplay.get("gameplay_score"))
        mechanics_novelty = _as_float(mechanics.get("novelty_score"))
        resilience_score = _as_float(resilience.get("resilience_score"))
        continuity_index = _as_float(continuity.get("continuity_index")) * 100.0
        security_score = _as_float(security.get("security_score"))

        modernization_priority = str(modernization.get("priority", "monitor"))
        optimization_priority = str(optimization.get("priority", "monitor"))

        execution_score = (
            implementation_score * 0.38
            + convergence_alignment * 0.18
            + creation_alignment * 0.14
            + functionality_score * 0.12
            + gameplay_score * 0.08
            + mechanics_novelty * 0.05
            + continuity_index * 0.03
            + resilience_score * 0.02
        )
        if modernization_priority in {"accelerate", "stabilise"}:
            execution_score += 3.0
        if optimization_priority in {"accelerate", "amplify"}:
            execution_score += 2.0
        execution_score = _clamp(execution_score)

        implementation_gap = _as_float(
            implementation.get("implementation_gap_index")
        )
        codebase_impl_gap = _as_float(codebase.get("implementation_gap_index"))
        codebase_creation_gap = _as_float(codebase.get("creation_gap_index"))
        convergence_gap = _as_float(codebase.get("convergence_gap_index"))
        execution_gap_index = _clamp(
            implementation_gap * 0.45
            + codebase_impl_gap * 0.3
            + codebase_creation_gap * 0.15
            + convergence_gap * 0.1
        )

        threat_penalty = _threat_penalty(str(security.get("threat_level", "guarded")))
        debt_penalty = _debt_penalty(_as_float(codebase.get("debt_risk_score")))
        continuity_penalty = max(0.0, 100.0 - continuity_index)
        resilience_penalty = max(0.0, 100.0 - resilience_score)
        security_penalty = max(0.0, 100.0 - security_score)
        research_pressure = _as_float(research.get("research_pressure_index"))
        risk_index = _clamp(
            security_penalty * 0.32
            + resilience_penalty * 0.2
            + continuity_penalty * 0.16
            + debt_penalty * 0.12
            + threat_penalty * 0.12
            + research_pressure * 0.08
        )

        priority = _priority(execution_score, execution_gap_index, risk_index)
        stability_state = _stability_state(
            execution_score,
            risk_index,
            resilience_score,
            continuity_index,
        )

        execution_tracks = _execution_tracks(
            implementation.get("implementation_tracks"),
            convergence.get("convergence_tracks"),
            creation.get("creation_tracks"),
            gameplay.get("loops"),
            systems.get("systems_threads"),
        )
        execution_threads = tuple(
            dict.fromkeys(
                (
                    *implementation.get("implementation_threads", ()),
                    *mechanics.get("gameplay_threads", ()),
                    *systems.get("systems_threads", ()),
                    *design.get("prototype_threads", ()),
                )
            )
        )
        execution_actions = _execution_actions(
            implementation.get("implementation_actions"),
            convergence.get("convergence_actions"),
            creation.get("creation_actions"),
            gameplay.get("managerial_actions"),
            mitigation.get("codebase_tasks"),
            continuity.get("codebase_continuity_actions"),
        )
        execution_windows = _execution_windows(
            implementation.get("delivery_windows"),
            continuity.get("timeline"),
        )
        velocity_index = _velocity_index(
            _as_float(implementation.get("implementation_velocity_index")),
            remediation.get("applied_fixes"),
            remediation.get("scheduled_fixes"),
            continuity.get("timeline"),
        )
        stability_index = _clamp(
            resilience_score * 0.35
            + security_score * 0.25
            + continuity_index * 0.2
            + (100.0 - risk_index) * 0.2
        )

        network_requirements = _merge_network_requirements(
            implementation.get("network_requirements"),
            functionality.get("network_requirements"),
            mechanics.get("network_considerations"),
            gameplay.get("network_requirements"),
            creation.get("network_requirements"),
            convergence.get("network_requirements"),
            network.get("network_security_upgrades"),
        )
        holographic_requirements = _merge_holographic_requirements(
            transmission,
            implementation.get("holographic_requirements"),
            functionality.get("holographic_requirements"),
            mechanics.get("holographic_requirements"),
            gameplay.get("holographic_requirements"),
            creation.get("holographic_requirements"),
            synthesis.get("holographic_requirements"),
        )

        security_alignment = {
            "security_score": round(security_score, 2),
            "threat_level": security.get("threat_level", "guarded"),
            "automation_directives": security.get("automation_directives", {}),
        }
        research_implications = {
            "utilization_percent": round(
                _as_float(research.get("raw_utilization_percent")), 2
            ),
            "pressure_index": round(research_pressure, 2),
            "trend": str(research.get("trend_direction", "stable")),
        }

        managerial_directives = tuple(
            dict.fromkeys(
                (
                    *functionality.get("managerial_directives", ()),
                    *gameplay.get("managerial_actions", ()),
                    *governance.get("oversight_actions", ()),
                    *modernization.get("modernization_actions", ()),
                    *optimization.get("optimization_actions", ()),
                )
            )
        )

        execution_backlog = _execution_backlog(
            implementation.get("implementation_backlog"),
            continuity.get("codebase_continuity_actions"),
        )

        codebase_alignment = {
            "execution_gap_index": round(
                _as_float(codebase.get("execution_gap_index")), 2
            ),
            "execution_alignment_score": round(
                _as_float(codebase.get("execution_alignment_score")), 2
            ),
            "focus_modules": tuple(
                dict.fromkeys(codebase.get("execution_focus_modules", ()))
            ),
            "recommendations": tuple(
                dict.fromkeys(codebase.get("execution_recommendations", ()))
            ),
        }

        governance_alignment = {
            "state": str(governance.get("state", "guided")),
            "actions": tuple(dict.fromkeys(governance.get("oversight_actions", ()))),
        }

        primary_focus = "stabilise"
        timeline: Sequence[Mapping[str, Any]] = continuity.get("timeline", ())  # type: ignore[assignment]
        if timeline:
            head = timeline[0]
            if isinstance(head, Mapping):
                primary_focus = str(head.get("focus", primary_focus))
        continuity_alignment = {
            "continuity_index": round(continuity_index, 2),
            "windows": execution_windows,
            "primary_focus": primary_focus,
        }

        return {
            "priority": priority,
            "execution_score": round(execution_score, 2),
            "execution_gap_index": round(execution_gap_index, 2),
            "execution_risk_index": round(risk_index, 2),
            "execution_tracks": execution_tracks,
            "execution_threads": execution_threads,
            "execution_actions": execution_actions,
            "delivery_windows": execution_windows,
            "execution_velocity_index": round(velocity_index, 2),
            "execution_stability_index": round(stability_index, 2),
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "security_alignment": security_alignment,
            "research_implications": research_implications,
            "managerial_directives": managerial_directives,
            "execution_backlog": execution_backlog,
            "stability_state": stability_state,
            "codebase_alignment": codebase_alignment,
            "governance_alignment": governance_alignment,
            "continuity_alignment": continuity_alignment,
        }

