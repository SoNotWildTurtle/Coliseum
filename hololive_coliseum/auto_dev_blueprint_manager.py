"""Blueprint orchestration for functionality and mechanics planning."""

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


def _unique_strings(*sources: Sequence[Any] | None) -> tuple[str, ...]:
    values: list[str] = []
    for source in sources:
        for item in source or ():
            text = ""
            if isinstance(item, Mapping):
                text = str(item.get("name", "")).strip()
            else:
                text = str(item).strip()
            if text and text not in values:
                values.append(text)
    return tuple(values)


def _priority(score: float, gap_index: float) -> str:
    if score >= 78.0 and gap_index <= 28.0:
        return "accelerate"
    if score >= 68.0 and gap_index <= 40.0:
        return "stabilise"
    if score >= 52.0:
        return "refine"
    return "survey"


def _merge_network_requirements(
    functionality: Mapping[str, Any],
    creation: Mapping[str, Any],
    systems: Mapping[str, Any],
    design: Mapping[str, Any],
    network: Mapping[str, Any],
    security: Mapping[str, Any],
    modernization: Mapping[str, Any],
) -> dict[str, Any]:
    requirements: list[Mapping[str, Any]] = []
    for candidate in (
        functionality.get("network_requirements"),
        creation.get("network_requirements"),
        systems.get("network_requirements"),
        design.get("network_requirements"),
        network.get("network_requirements"),
    ):
        if isinstance(candidate, Mapping):
            requirements.append(candidate)
    security_scores = [
        _as_float(req.get("security_score"))
        for req in requirements
        if isinstance(req, Mapping)
    ]
    security_scores.append(_as_float(network.get("network_security_score")))
    security_scores.append(_as_float(security.get("security_score")))
    upgrade_actions = _unique_strings(
        *(req.get("upgrade_tracks") for req in requirements if isinstance(req, Mapping)),
        modernization.get("modernization_actions"),
    )
    bandwidth_samples = [
        _as_float(req.get("bandwidth_budget_mbps") or req.get("bandwidth_mbps"))
        for req in requirements
        if isinstance(req, Mapping)
    ]
    latency_targets = [
        _as_float(req.get("latency_target_ms"))
        for req in requirements
        if isinstance(req, Mapping)
    ]
    return {
        "security_score": round(max(security_scores) if security_scores else 0.0, 2),
        "bandwidth_budget_mbps": round(max(bandwidth_samples) if bandwidth_samples else 0.0, 2),
        "latency_target_ms": round(
            sum(latency_targets) / len(latency_targets) if latency_targets else 0.0,
            2,
        ),
        "upgrade_actions": upgrade_actions,
        "threat_level": str(security.get("threat_level", "guarded")),
    }


def _merge_holographic_requirements(
    functionality: Mapping[str, Any],
    creation: Mapping[str, Any],
    systems: Mapping[str, Any],
    design: Mapping[str, Any],
    transmission: Mapping[str, Any],
) -> dict[str, Any]:
    requirements: list[Mapping[str, Any]] = []
    for candidate in (
        functionality.get("holographic_requirements"),
        creation.get("holographic_requirements"),
        systems.get("holographic_requirements"),
        design.get("holographic_requirements"),
    ):
        if isinstance(candidate, Mapping):
            requirements.append(candidate)
    actions = _unique_strings(*(req.get("recommended_actions") for req in requirements))
    efficiency_scores = [
        _as_float(req.get("efficiency_score"))
        for req in requirements
        if isinstance(req, Mapping)
    ]
    transmission = transmission or {}
    spectral: Mapping[str, Any] = transmission.get("spectral_waveform", {})  # type: ignore[assignment]
    phase_alignment: Mapping[str, Any] = transmission.get("phase_alignment", {})  # type: ignore[assignment]
    actions = _unique_strings(actions, spectral.get("recommended_actions"), phase_alignment.get("actions"))
    efficiency_scores.append(_as_float(spectral.get("bandwidth_density")))
    efficiency_scores.append(_as_float(transmission.get("efficiency_score")))
    phase_target = _as_float(phase_alignment.get("target"))
    return {
        "recommended_actions": actions,
        "efficiency_score": round(
            sum(efficiency_scores) / len(efficiency_scores) if efficiency_scores else 0.0,
            2,
        ),
        "phase_target": round(phase_target, 2),
        "stability": str(spectral.get("stability", "steady")),
    }


@dataclass
class AutoDevBlueprintManager:
    """Synthesise creation, functionality, and mechanics insights into blueprints."""

    functionality_weight: float = 0.34
    mechanics_weight: float = 0.24
    creation_weight: float = 0.24
    synthesis_weight: float = 0.18
    risk_penalty_factor: float = 0.32
    gap_penalty_factor: float = 0.28

    def blueprint_brief(
        self,
        *,
        functionality: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        creation: Mapping[str, Any] | None = None,
        design: Mapping[str, Any] | None = None,
        systems: Mapping[str, Any] | None = None,
        innovation: Mapping[str, Any] | None = None,
        experience: Mapping[str, Any] | None = None,
        dynamics: Mapping[str, Any] | None = None,
        gameplay: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic functionality blueprint for downstream managers."""

        functionality = functionality or {}
        mechanics = mechanics or {}
        creation = creation or {}
        design = design or {}
        systems = systems or {}
        innovation = innovation or {}
        experience = experience or {}
        dynamics = dynamics or {}
        gameplay = gameplay or {}
        research = research or {}
        network = network or {}
        transmission = transmission or {}
        security = security or {}
        modernization = modernization or {}
        optimization = optimization or {}
        governance = governance or {}
        codebase = codebase or {}

        functionality_score = _as_float(functionality.get("functionality_score"))
        mechanics_novelty = _as_float(mechanics.get("novelty_score"))
        creation_score = _as_float(creation.get("creation_score"))
        dynamics_synergy = _as_float(dynamics.get("synergy_score"))
        innovation_score = _as_float(innovation.get("innovation_score"))
        experience_score = _as_float(experience.get("experience_score"))

        weight_total = (
            self.functionality_weight
            + self.mechanics_weight
            + self.creation_weight
            + self.synthesis_weight
        ) or 1e-6
        weighted_signal = (
            functionality_score * self.functionality_weight
            + mechanics_novelty * self.mechanics_weight
            + creation_score * self.creation_weight
            + max(dynamics_synergy, innovation_score, experience_score) * self.synthesis_weight
        ) / weight_total

        cohesion_bonus = min(18.0, (dynamics_synergy + experience_score) * 0.25)
        innovation_bonus = min(14.0, innovation_score * 0.22)
        research_pressure = _as_float(research.get("research_pressure_index"))
        research_bonus = min(10.0, research_pressure * 0.18)

        functionality_risk = _as_float(functionality.get("risk_index"))
        mechanics_risk = _as_float(mechanics.get("risk_score"))
        creation_risk = _as_float((creation.get("risk_profile") or {}).get("risk_index"))
        combined_risk = max(functionality_risk, mechanics_risk, creation_risk)
        risk_penalty = min(36.0, combined_risk * self.risk_penalty_factor)

        codebase_gap = _as_float(codebase.get("blueprint_gap_index"))
        gap_penalty = min(28.0, codebase_gap * self.gap_penalty_factor)
        alignment_score = _as_float(codebase.get("blueprint_alignment_score"))
        alignment_bonus = min(16.0, alignment_score * 0.18)

        blueprint_score = _clamp(
            weighted_signal + cohesion_bonus + innovation_bonus + research_bonus + alignment_bonus - risk_penalty - gap_penalty
        )
        priority = _priority(blueprint_score, codebase_gap)

        cohesion_index = _clamp(
            (
                alignment_score * 0.4
                + (100.0 - codebase_gap) * 0.3
                + functionality_score * 0.15
                + creation_score * 0.15
            )
        )

        tracks = _unique_strings(
            functionality.get("functionality_tracks"),
            creation.get("creation_tracks"),
            design.get("creation_tracks"),
            systems.get("systems_tracks"),
            gameplay.get("functionality_tracks"),
        )
        threads = _unique_strings(
            functionality.get("functionality_threads"),
            mechanics.get("gameplay_threads"),
            creation.get("creation_threads"),
            systems.get("systems_threads"),
            design.get("prototype_threads"),
        )
        actions = _unique_strings(
            functionality.get("managerial_directives"),
            creation.get("creation_actions"),
            design.get("design_actions"),
            systems.get("systems_actions"),
            dynamics.get("backend_actions"),
            optimization.get("optimization_actions"),
            modernization.get("modernization_actions"),
        )

        network_requirements = _merge_network_requirements(
            functionality,
            creation,
            systems,
            design,
            network,
            security,
            modernization,
        )
        holographic_requirements = _merge_holographic_requirements(
            functionality,
            creation,
            systems,
            design,
            transmission,
        )

        codebase_alignment = {
            "blueprint_gap_index": round(codebase_gap, 2),
            "blueprint_alignment_score": round(alignment_score, 2),
            "focus_modules": tuple(codebase.get("blueprint_focus_modules", ())),
            "recommendations": tuple(codebase.get("blueprint_recommendations", ())),
        }

        supporting_signals = {
            "modernization_priority": modernization.get("priority", "monitor"),
            "optimization_priority": optimization.get("priority", "monitor"),
            "governance_state": governance.get("state", "guided"),
        }

        mechanics_extensions = _unique_strings(
            creation.get("mechanics_expansion_tracks"),
            dynamics.get("systems_tracks"),
            mechanics.get("functionality_tracks"),
        )
        functionality_extensions = _unique_strings(
            creation.get("functionality_extension_tracks"),
            design.get("creation_tracks"),
            functionality.get("functionality_tracks"),
        )

        return {
            "priority": priority,
            "blueprint_score": round(blueprint_score, 2),
            "cohesion_index": round(cohesion_index, 2),
            "alignment_index": round(alignment_score, 2),
            "gap_index": round(codebase_gap, 2),
            "tracks": tracks,
            "threads": threads,
            "actions": actions,
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "codebase_alignment": codebase_alignment,
            "supporting_signals": supporting_signals,
            "mechanics_extension_tracks": mechanics_extensions,
            "functionality_extension_tracks": functionality_extensions,
            "focus_modules": tuple(codebase.get("blueprint_focus_modules", ())),
            "recommendations": tuple(codebase.get("blueprint_recommendations", ())),
            "research_outlook": {
                "pressure_index": round(research_pressure, 2),
                "utilization_percent": _as_float(
                    research.get("raw_utilization_percent")
                    or research.get("latest_sample_percent")
                ),
                "trend": str(research.get("trend_direction", research.get("trend", "steady"))),
            },
        }
