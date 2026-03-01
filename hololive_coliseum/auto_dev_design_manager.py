"""Blend functionality and mechanics signals into actionable design blueprints."""

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


def _priority(score: float) -> str:
    if score >= 78.0:
        return "amplify"
    if score >= 64.0:
        return "accelerate"
    if score >= 50.0:
        return "stabilise"
    if score >= 36.0:
        return "refine"
    return "observe"


def _normalise_strings(values: Sequence[Any] | None) -> tuple[str, ...]:
    normalised: list[str] = []
    for value in values or ():
        text = str(value).strip()
        if text and text not in normalised:
            normalised.append(text)
    return tuple(normalised)


def _merge_requirements(*requirements: Mapping[str, Any] | None) -> dict[str, Any]:
    security_scores: list[float] = []
    bandwidth_samples: list[float] = []
    upgrade_actions: list[str] = []
    latency_targets: list[float] = []
    for requirement in requirements:
        if not isinstance(requirement, Mapping):
            continue
        security = _as_float(requirement.get("security_score"))
        bandwidth = _as_float(requirement.get("bandwidth_mbps"))
        latency = _as_float(requirement.get("latency_target_ms"))
        if security:
            security_scores.append(security)
        if bandwidth:
            bandwidth_samples.append(bandwidth)
        if latency:
            latency_targets.append(latency)
        upgrade_actions.extend(_normalise_strings(requirement.get("upgrade_actions")))
    security_score = sum(security_scores) / len(security_scores) if security_scores else 0.0
    bandwidth = max(bandwidth_samples) if bandwidth_samples else 0.0
    latency_target = sum(latency_targets) / len(latency_targets) if latency_targets else 0.0
    return {
        "security_score": round(security_score, 2),
        "bandwidth_mbps": round(bandwidth, 2),
        "latency_target_ms": round(latency_target, 2) if latency_target else 0.0,
        "upgrade_actions": tuple(dict.fromkeys(upgrade_actions)),
    }


def _merge_holographic_requirements(
    transmission: Mapping[str, Any] | None,
    *requirements: Mapping[str, Any] | None,
) -> dict[str, Any]:
    actions: list[str] = []
    phase_targets: list[float] = []
    efficiency_scores: list[float] = []
    for requirement in requirements:
        if not isinstance(requirement, Mapping):
            continue
        actions.extend(_normalise_strings(requirement.get("recommended_actions")))
        phase_targets.append(_as_float(requirement.get("phase_target")))
        efficiency_scores.append(_as_float(requirement.get("efficiency_score")))
    transmission = transmission or {}
    phase_alignment: Mapping[str, Any] = transmission.get("phase_alignment", {})  # type: ignore[assignment]
    lithographic: Mapping[str, Any] = transmission.get("lithographic_integrity", {})  # type: ignore[assignment]
    actions.extend(
        _normalise_strings(phase_alignment.get("recommended_actions"))
    )
    efficiency_scores.append(_as_float(lithographic.get("score")))
    phase_targets.append(_as_float(phase_alignment.get("target")))
    return {
        "recommended_actions": tuple(dict.fromkeys(actions)),
        "phase_target": round(
            sum(phase_targets) / len(phase_targets), 2
        )
        if phase_targets
        else 0.0,
        "efficiency_score": round(
            sum(efficiency_scores) / len(efficiency_scores), 2
        )
        if efficiency_scores
        else 0.0,
    }


@dataclass
class AutoDevDesignManager:
    """Fuse functionality, mechanics, and networking signals into design briefs."""

    functionality_weight: float = 0.34
    mechanics_weight: float = 0.26
    innovation_weight: float = 0.22
    dynamics_weight: float = 0.2
    experience_weight: float = 0.18
    interaction_weight: float = 0.16
    gameplay_weight: float = 0.18
    risk_penalty_factor: float = 0.42
    fragility_penalty_factor: float = 0.55
    network_bonus_factor: float = 0.18

    def design_blueprint(
        self,
        *,
        functionality: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        innovation: Mapping[str, Any] | None = None,
        dynamics: Mapping[str, Any] | None = None,
        experience: Mapping[str, Any] | None = None,
        interaction: Mapping[str, Any] | None = None,
        gameplay: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        network_auto_dev: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        integrity: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        self_evolution: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic design blueprint for MMO feature creation."""

        functionality = functionality or {}
        mechanics = mechanics or {}
        innovation = innovation or {}
        dynamics = dynamics or {}
        experience = experience or {}
        interaction = interaction or {}
        gameplay = gameplay or {}
        research = research or {}
        network = network or {}
        network_auto_dev = network_auto_dev or {}
        security = security or {}
        transmission = transmission or {}
        modernization = modernization or {}
        optimization = optimization or {}
        integrity = integrity or {}
        governance = governance or {}
        codebase = codebase or {}
        self_evolution = self_evolution or {}

        functionality_score = _as_float(functionality.get("functionality_score"))
        mechanics_novelty = _as_float(mechanics.get("novelty_score"))
        innovation_score = _as_float(innovation.get("innovation_score"))
        dynamics_synergy = _as_float(dynamics.get("synergy_score"))
        experience_score = _as_float(experience.get("experience_score"))
        interaction_score = _as_float(interaction.get("interaction_score"))
        gameplay_score = _as_float(gameplay.get("gameplay_score"))

        weight_total = (
            self.functionality_weight
            + self.mechanics_weight
            + self.innovation_weight
            + self.dynamics_weight
            + self.experience_weight
            + self.interaction_weight
            + self.gameplay_weight
        ) or 1e-6
        weighted_signal = (
            functionality_score * self.functionality_weight
            + mechanics_novelty * self.mechanics_weight
            + innovation_score * self.innovation_weight
            + dynamics_synergy * self.dynamics_weight
            + experience_score * self.experience_weight
            + interaction_score * self.interaction_weight
            + gameplay_score * self.gameplay_weight
        ) / weight_total

        integrity_bonus = min(12.0, _as_float(integrity.get("integrity_score")) * 0.12)
        resilience_bonus = min(
            8.0,
            _as_float(network_auto_dev.get("readiness_score")) * 0.6
            + _as_float(network.get("network_security_score")) * self.network_bonus_factor,
        )
        security_score = max(
            _as_float(security.get("security_score")),
            _as_float(network.get("network_security_score")),
        )
        holographic_bonus = min(
            6.0,
            _as_float(
                transmission.get("lithographic_integrity", {}).get("score")
            )
            * 0.12,
        )

        functionality_risk = _as_float(functionality.get("risk_index"))
        dynamics_risk = _as_float((dynamics.get("risk_profile") or {}).get("combined_risk"))
        interaction_gap = _as_float(
            (interaction.get("gap_summary") or {}).get("functionality_gap_index")
        )
        research_pressure = _as_float(research.get("research_pressure_index"))
        fragility_index = _as_float(codebase.get("design_fragility_index"))

        risk_penalty = min(
            35.0,
            max(functionality_risk, dynamics_risk, interaction_gap)
            * self.risk_penalty_factor
            + research_pressure * 0.25,
        )
        fragility_penalty = min(
            40.0,
            fragility_index * self.fragility_penalty_factor,
        )
        security_gap = max(0.0, 75.0 - security_score)

        design_score = _clamp(
            weighted_signal
                + integrity_bonus
                + resilience_bonus
                + holographic_bonus
                - risk_penalty
                - fragility_penalty
        )
        priority = _priority(design_score)

        creation_tracks = _normalise_strings(
            (
                *functionality.get("functionality_tracks", ()),
                *mechanics.get("functionality_tracks", ()),
                *dynamics.get("systems_tracks", ()),
                *gameplay.get("functionality_tracks", ()),
            )
        )
        prototype_threads = _normalise_strings(
            (
                *mechanics.get("gameplay_threads", ()),
                *experience.get("experience_threads", ()),
                *gameplay.get("loops", ()),
            )
        )
        design_actions = _normalise_strings(
            (
                *modernization.get("modernization_actions", ()),
                *optimization.get("optimization_actions", ()),
                *network_auto_dev.get("next_steps", ()),
                *governance.get("oversight_actions", ()),
                *self_evolution.get("next_actions", ()),
            )
        )
        design_directives = _normalise_strings(
            (
                *functionality.get("managerial_directives", ()),
                *interaction.get("interaction_actions", ()),
                *gameplay.get("managerial_actions", ()),
            )
        )

        functionality_requirements = functionality.get("network_requirements", {})
        dynamics_requirements = dynamics.get("network_requirements", {})
        interaction_requirements = interaction.get("network_requirements", {})
        gameplay_requirements = gameplay.get("network_requirements", {})
        network_requirements = _merge_requirements(
            functionality_requirements,
            dynamics_requirements,
            interaction_requirements,
            gameplay_requirements,
            network_auto_dev.get("security_focus", {}),
        )
        holographic_requirements = _merge_holographic_requirements(
            transmission,
            functionality.get("holographic_requirements", {}),
            dynamics.get("holographic_requirements", {}),
            interaction.get("holographic_requirements", {}),
            gameplay.get("holographic_requirements", {}),
        )

        modernization_targets: Sequence[Mapping[str, Any]] = modernization.get(
            "modernization_targets",
            (),
        )  # type: ignore[assignment]
        design_focus_modules = tuple(
            dict.fromkeys(
                (
                    *codebase.get("design_focus_modules", ()),
                    *(
                        target.get("name", "module")
                        for target in modernization_targets
                        if isinstance(target, Mapping)
                    ),
                )
            )
        )
        design_recommendations = tuple(
            dict.fromkeys(
                (
                    *codebase.get("design_recommendations", ()),
                    *(
                        ", ".join(target.get("modernization_steps", ()))
                        for target in modernization_targets
                        if isinstance(target, Mapping)
                    ),
                )
            )
        )
        creation_windows = _normalise_strings(
            (
                *modernization.get("timeline", ()),
                *optimization.get("fix_windows", ()),
            )
        )

        codebase_alignment = {
            "functionality_gaps": tuple(codebase.get("functionality_gaps", ())),
            "design_focus_modules": design_focus_modules,
            "modernization_targets": tuple(
                target.get("name", "module")
                for target in modernization_targets
            ),
        }
        research_implications = {
            "utilization_percent": _as_float(research.get("raw_utilization_percent")),
            "pressure_index": research_pressure,
            "trend": str(research.get("trend_direction", "steady")),
        }
        design_gap_summary = {
            "focus_index": round(fragility_index, 2),
            "focus_modules": design_focus_modules,
            "recommendations": design_recommendations,
        }
        risk_profile = {
            "risk_penalty": round(risk_penalty, 2),
            "fragility_penalty": round(fragility_penalty, 2),
            "security_gap": round(security_gap, 2),
        }
        innovation_dependencies = _normalise_strings(
            (
                *innovation.get("feature_concepts", ()),
                *interaction.get("interaction_threads", ()),
            )
        )

        return {
            "priority": priority,
            "design_score": round(design_score, 2),
            "creation_tracks": creation_tracks,
            "prototype_threads": prototype_threads,
            "design_actions": design_actions,
            "design_directives": design_directives,
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "codebase_alignment": codebase_alignment,
            "research_implications": research_implications,
            "risk_profile": risk_profile,
            "design_gap_summary": design_gap_summary,
            "creation_windows": creation_windows,
            "innovation_dependencies": innovation_dependencies,
        }
