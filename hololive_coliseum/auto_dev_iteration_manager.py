"""Manager for blending functionality and mechanics into iteration cycles."""

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


def _dedupe(values: Sequence[Any] | None) -> tuple[Any, ...]:
    items: list[Any] = []
    for value in values or ():
        if value in items:
            continue
        items.append(value)
    return tuple(items)


def _priority(score: float, gap_index: float, risk_index: float) -> str:
    if score >= 78.0 and gap_index <= 28.0 and risk_index <= 30.0:
        return "accelerate"
    if score >= 70.0 and gap_index <= 40.0:
        return "amplify"
    if score >= 60.0:
        return "stabilise"
    if score >= 48.0:
        return "refine"
    return "observe"


def _merge_network_requirements(*requirements: Mapping[str, Any] | None) -> dict[str, Any]:
    security_scores: list[float] = []
    bandwidth_samples: list[float] = []
    latency_targets: list[float] = []
    upgrade_actions: list[str] = []
    for requirement in requirements:
        if not isinstance(requirement, Mapping):
            continue
        security_scores.append(
            _as_float(
                requirement.get("security_score"),
                _as_float(requirement.get("projected_security_score")),
            )
        )
        bandwidth = requirement.get("bandwidth_mbps")
        if bandwidth is None:
            bandwidth = requirement.get("bandwidth_budget_mbps")
        if bandwidth is None:
            bandwidth = requirement.get("average_bandwidth_mbps")
        bandwidth_samples.append(_as_float(bandwidth))
        latency = requirement.get("latency_target_ms")
        if latency is None:
            latency = requirement.get("latency_ms")
        latency_targets.append(_as_float(latency))
        upgrade_actions.extend(
            str(action).strip()
            for action in requirement.get("upgrade_actions", ())
            if str(action).strip()
        )
        upgrade_actions.extend(
            str(track).strip()
            for track in requirement.get("upgrade_tracks", ())
            if str(track).strip()
        )
    security = (
        sum(security_scores) / len(security_scores) if security_scores else 0.0
    )
    bandwidth = max(bandwidth_samples) if bandwidth_samples else 0.0
    latency = (
        sum(latency_targets) / len(latency_targets) if latency_targets else 0.0
    )
    return {
        "security_score": round(_clamp(security, 0.0, 100.0), 2),
        "bandwidth_mbps": round(max(0.0, bandwidth), 2),
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
            str(action).strip()
            for action in requirement.get("recommended_actions", ())
            if str(action).strip()
        )
        efficiency_scores.append(_as_float(requirement.get("efficiency_score")))
        phase_targets.append(_as_float(requirement.get("phase_target")))
    transmission = transmission or {}
    spectral: Mapping[str, Any] = transmission.get(
        "spectral_waveform", {},
    )  # type: ignore[assignment]
    lattice: Mapping[str, Any] = transmission.get(
        "lattice_overlay", {},
    )  # type: ignore[assignment]
    guardrails: Mapping[str, Any] = transmission.get(
        "guardrails", {},
    )  # type: ignore[assignment]
    actions.extend(
        str(action).strip()
        for action in spectral.get("recommended_actions", ())
        if str(action).strip()
    )
    actions.extend(
        str(action).strip()
        for action in lattice.get("actions", ())
        if str(action).strip()
    )
    actions.extend(
        str(action).strip()
        for action in guardrails.get("follow_up", ())
        if str(action).strip()
    )
    efficiency_scores.append(_as_float(spectral.get("efficiency")))
    phase_targets.append(_as_float(lattice.get("phase_target")))
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
        "efficiency_score": round(_clamp(efficiency, 0.0, 100.0), 2),
        "phase_target": round(phase_target, 2),
    }


def _iteration_cycles(
    functionality: Mapping[str, Any],
    mechanics: Mapping[str, Any],
    creation: Mapping[str, Any],
    blueprint: Mapping[str, Any],
) -> tuple[str, ...]:
    cycles: list[str] = []
    for track in functionality.get("functionality_tracks", ()):  # type: ignore[assignment]
        text = str(track).strip()
        if text and text not in cycles:
            cycles.append(text)
    for thread in mechanics.get("gameplay_threads", ()):  # type: ignore[assignment]
        text = str(thread).strip()
        if text and text not in cycles:
            cycles.append(text)
    for thread in creation.get("creation_threads", ()):  # type: ignore[assignment]
        text = str(thread).strip()
        if text and text not in cycles:
            cycles.append(text)
    for track in blueprint.get("tracks", ()):  # type: ignore[assignment]
        text = str(track).strip()
        if text and text not in cycles:
            cycles.append(text)
    return tuple(cycles)


def _iteration_actions(
    functionality: Mapping[str, Any],
    mechanics: Mapping[str, Any],
    creation: Mapping[str, Any],
    blueprint: Mapping[str, Any],
    network_auto_dev: Mapping[str, Any],
    security: Mapping[str, Any],
) -> tuple[str, ...]:
    actions: list[str] = []
    actions.extend(
        str(action).strip()
        for action in functionality.get("managerial_directives", ())
        if str(action).strip()
    )
    actions.extend(
        str(action).strip()
        for action in mechanics.get("backend_actions", ())
        if str(action).strip()
    )
    actions.extend(
        str(action).strip()
        for action in creation.get("creation_actions", ())
        if str(action).strip()
    )
    actions.extend(
        str(action).strip()
        for action in blueprint.get("actions", ())
        if str(action).strip()
    )
    actions.extend(
        str(action).strip()
        for action in network_auto_dev.get("next_steps", ())
        if str(action).strip()
    )
    actions.extend(
        str(action).strip()
        for action in security.get("network_security_actions", ())
        if str(action).strip()
    )
    if not actions:
        actions.append("Schedule iterative review")
    return tuple(dict.fromkeys(actions))


def _iteration_threads(
    functionality: Mapping[str, Any],
    creation: Mapping[str, Any],
    blueprint: Mapping[str, Any],
    execution: Mapping[str, Any],
) -> tuple[str, ...]:
    threads: list[str] = []
    threads.extend(
        str(thread).strip()
        for thread in functionality.get("functionality_threads", ())
        if str(thread).strip()
    )
    threads.extend(
        str(thread).strip()
        for thread in creation.get("creation_threads", ())
        if str(thread).strip()
    )
    threads.extend(
        str(thread).strip()
        for thread in blueprint.get("threads", ())
        if str(thread).strip()
    )
    threads.extend(
        str(thread).strip()
        for thread in execution.get("execution_threads", ())
        if str(thread).strip()
    )
    return tuple(dict.fromkeys(threads))


def _iteration_windows(
    creation: Mapping[str, Any],
    blueprint: Mapping[str, Any],
    implementation: Mapping[str, Any],
) -> tuple[str, ...]:
    windows: list[str] = []
    windows.extend(
        str(window).strip()
        for window in creation.get("prototype_windows", ())
        if str(window).strip()
    )
    windows.extend(
        str(window).strip()
        for window in blueprint.get("windows", ())
        if str(window).strip()
    )
    windows.extend(
        str(window).strip()
        for window in implementation.get("delivery_windows", ())
        if str(window).strip()
    )
    return tuple(dict.fromkeys(windows))


def _iteration_focus(
    codebase: Mapping[str, Any],
    functionality: Mapping[str, Any],
    creation: Mapping[str, Any],
    blueprint: Mapping[str, Any],
) -> dict[str, Any]:
    gap_index = _as_float(codebase.get("iteration_gap_index"))
    alignment_score = _as_float(codebase.get("iteration_alignment_score"))
    focus_modules = _dedupe(codebase.get("iteration_focus_modules"))
    recommendations = _dedupe(codebase.get("iteration_recommendations"))
    if not focus_modules:
        focus_modules = _dedupe(
            (
                *functionality.get("functionality_tracks", ()),
                *creation.get("creation_tracks", ()),
            )
        )
    if not recommendations:
        recommendations = _dedupe(
            (
                *blueprint.get("actions", ()),
                *creation.get("creation_actions", ()),
            )
        )
    return {
        "gap_index": round(_clamp(gap_index, 0.0, 100.0), 2),
        "alignment_score": round(_clamp(alignment_score, 0.0, 100.0), 2),
        "focus_modules": focus_modules,
        "recommendations": recommendations,
    }


def _iteration_research(
    research: Mapping[str, Any],
    innovation: Mapping[str, Any],
    network_auto_dev: Mapping[str, Any],
) -> dict[str, Any]:
    utilization = _as_float(
        research.get("raw_utilization_percent"),
        _as_float(research.get("latest_sample_percent")),
    )
    pressure = _as_float(research.get("research_pressure_index"))
    novelty = _as_float(innovation.get("innovation_score"))
    budget_health = str(
        network_auto_dev.get("processing_focus", {}).get("budget_health", "stable")
    )
    recommendation = "Maintain observational cadence"
    if pressure >= 60.0 or budget_health in {"strained", "watch"}:
        recommendation = "Throttle iteration bandwidth"
    elif novelty >= 70.0:
        recommendation = "Accelerate iteration prototyping"
    return {
        "utilization_percent": round(_clamp(utilization, 0.0, 100.0), 2),
        "pressure_index": round(_clamp(pressure, 0.0, 100.0), 2),
        "novelty_score": round(_clamp(novelty, 0.0, 100.0), 2),
        "recommendation": recommendation,
    }


@dataclass
class AutoDevIterationManager:
    """Blend functionality, mechanics, and creation signals into iteration guidance."""

    def iteration_brief(
        self,
        *,
        functionality: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        creation: Mapping[str, Any] | None = None,
        blueprint: Mapping[str, Any] | None = None,
        innovation: Mapping[str, Any] | None = None,
        execution: Mapping[str, Any] | None = None,
        implementation: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        network_auto_dev: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic iteration blueprint."""

        functionality = functionality or {}
        mechanics = mechanics or {}
        creation = creation or {}
        blueprint = blueprint or {}
        innovation = innovation or {}
        execution = execution or {}
        implementation = implementation or {}
        network = network or {}
        network_auto_dev = network_auto_dev or {}
        security = security or {}
        transmission = transmission or {}
        research = research or {}
        codebase = codebase or {}

        functionality_score = _as_float(functionality.get("functionality_score"))
        mechanics_novelty = _as_float(mechanics.get("novelty_score"))
        creation_score = _as_float(creation.get("creation_score"))
        blueprint_score = _as_float(blueprint.get("blueprint_score"))
        cohesion_index = _as_float(blueprint.get("cohesion_index"))
        iteration_score = _clamp(
            functionality_score * 0.3
            + mechanics_novelty * 0.22
            + creation_score * 0.2
            + blueprint_score * 0.18
            + cohesion_index * 0.1,
            0.0,
            100.0,
        )
        functionality_risk = _as_float(functionality.get("risk_index"))
        mechanics_risk = _as_float(mechanics.get("risk_score"))
        creation_risk = _as_float(creation.get("risk_profile", {}).get("risk_index"))
        risk_index = _clamp(
            functionality_risk * 0.4
            + mechanics_risk * 0.3
            + creation_risk * 0.3,
            0.0,
            100.0,
        )
        gap_summary = _iteration_focus(codebase, functionality, creation, blueprint)
        priority = _priority(iteration_score, gap_summary["gap_index"], risk_index)

        network_requirements = _merge_network_requirements(
            functionality.get("network_requirements"),
            creation.get("network_requirements"),
            blueprint.get("network_requirements"),
            network.get("network_security"),
            network_auto_dev.get("processing_focus"),
            security,
        )
        holographic_requirements = _merge_holographic_requirements(
            transmission,
            functionality.get("holographic_requirements", {}),
            creation.get("holographic_requirements", {}),
            blueprint.get("holographic_requirements", {}),
            network_auto_dev.get("holographic_integration", {}),
        )
        cycles = _iteration_cycles(functionality, mechanics, creation, blueprint)
        actions = _iteration_actions(
            functionality,
            mechanics,
            creation,
            blueprint,
            network_auto_dev,
            security,
        )
        threads = _iteration_threads(functionality, creation, blueprint, execution)
        windows = _iteration_windows(creation, blueprint, implementation)
        research_implications = _iteration_research(
            research,
            innovation,
            network_auto_dev,
        )

        iteration_security = {
            "threat_level": str(security.get("threat_level", "guarded")),
            "hardening": _dedupe(security.get("network_security_actions", ())),
            "guardrail": _dedupe(
                security.get("holographic_lattice", {}).get("actions", ())
                if isinstance(security.get("holographic_lattice"), Mapping)
                else (),
            ),
        }

        return {
            "priority": priority,
            "iteration_score": round(iteration_score, 2),
            "risk_index": round(risk_index, 2),
            "gap_summary": gap_summary,
            "cycles": cycles,
            "actions": actions,
            "threads": threads,
            "windows": windows,
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "research_implications": research_implications,
            "security_profile": iteration_security,
        }
