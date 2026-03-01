"""Synthesize design, functionality, and networking data into systems briefs."""

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


def _priority(score: float, fragility: float) -> str:
    if score >= 78.0 and fragility <= 30.0:
        return "amplify"
    if score >= 66.0 and fragility <= 45.0:
        return "accelerate"
    if score >= 52.0:
        return "stabilise"
    if score >= 38.0:
        return "refine"
    return "observe"


def _normalise_strings(values: Sequence[Any] | None) -> tuple[str, ...]:
    normalised: list[str] = []
    for value in values or ():
        if isinstance(value, Mapping):
            text = str(value.get("name", "")).strip()
        else:
            text = str(value).strip()
        if text and text not in normalised:
            normalised.append(text)
    return tuple(normalised)


def _merge_network_requirements(*requirements: Mapping[str, Any] | None) -> dict[str, Any]:
    security_scores: list[float] = []
    bandwidth_samples: list[float] = []
    latency_targets: list[float] = []
    upgrade_actions: list[str] = []
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
    latency_target = (
        sum(latency_targets) / len(latency_targets) if latency_targets else 0.0
    )
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
    actions.extend(_normalise_strings(phase_alignment.get("recommended_actions")))
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


def _architecture_overview(
    network: Mapping[str, Any],
    transmission: Mapping[str, Any],
    security: Mapping[str, Any],
    governance: Mapping[str, Any],
    self_evolution: Mapping[str, Any],
) -> dict[str, Any]:
    network_health: Mapping[str, Any] = network.get("network_health", {})  # type: ignore[assignment]
    network_status = str(network_health.get("status", network.get("status", "stable")))
    upgrade_paths = tuple(
        str(step).strip()
        for step in network.get("upgrade_paths", ())
        if str(step).strip()
    )
    phase_alignment: Mapping[str, Any] = transmission.get("phase_alignment", {})  # type: ignore[assignment]
    lithographic: Mapping[str, Any] = transmission.get("lithographic_integrity", {})  # type: ignore[assignment]
    governance_state = str(
        governance.get("state", governance.get("oversight_state", "guided"))
    )
    return {
        "network_status": network_status,
        "upgrade_paths": upgrade_paths,
        "phase_target": _as_float(phase_alignment.get("target")),
        "phase_actions": tuple(
            dict.fromkeys(
                _normalise_strings(phase_alignment.get("recommended_actions"))
            )
        ),
        "lithographic_score": _as_float(lithographic.get("score")),
        "security_threat_level": str(security.get("threat_level", "guarded")),
        "governance_focus": governance_state,
        "self_evolution_state": str(
            self_evolution.get("readiness_state", "stabilise")
        ),
    }


@dataclass
class AutoDevSystemsManager:
    """Fuse design, functionality, and telemetry into systems planning briefs."""

    functionality_weight: float = 0.28
    mechanics_weight: float = 0.22
    design_weight: float = 0.24
    dynamics_weight: float = 0.18
    gameplay_weight: float = 0.18
    interaction_weight: float = 0.16
    innovation_weight: float = 0.14
    experience_weight: float = 0.12
    network_bonus_factor: float = 0.18
    risk_penalty_factor: float = 0.42
    fragility_penalty_factor: float = 0.36

    def systems_blueprint(
        self,
        *,
        design: Mapping[str, Any] | None = None,
        functionality: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        dynamics: Mapping[str, Any] | None = None,
        gameplay: Mapping[str, Any] | None = None,
        playstyle: Mapping[str, Any] | None = None,
        interaction: Mapping[str, Any] | None = None,
        innovation: Mapping[str, Any] | None = None,
        experience: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        network_auto_dev: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        integrity: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        self_evolution: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic systems blueprint for downstream automation."""

        design = design or {}
        functionality = functionality or {}
        mechanics = mechanics or {}
        dynamics = dynamics or {}
        gameplay = gameplay or {}
        playstyle = playstyle or {}
        interaction = interaction or {}
        innovation = innovation or {}
        experience = experience or {}
        research = research or {}
        network = network or {}
        network_auto_dev = network_auto_dev or {}
        transmission = transmission or {}
        security = security or {}
        modernization = modernization or {}
        optimization = optimization or {}
        integrity = integrity or {}
        resilience = resilience or {}
        governance = governance or {}
        codebase = codebase or {}
        self_evolution = self_evolution or {}

        functionality_score = _as_float(functionality.get("functionality_score"))
        mechanics_novelty = _as_float(mechanics.get("novelty_score"))
        design_score = _as_float(design.get("design_score"))
        dynamics_synergy = _as_float(dynamics.get("synergy_score"))
        gameplay_score = _as_float(gameplay.get("gameplay_score"))
        interaction_score = _as_float(interaction.get("interaction_score"))
        innovation_score = _as_float(innovation.get("innovation_score"))
        experience_score = _as_float(experience.get("experience_score"))
        resilience_score = _as_float(resilience.get("resilience_score"))
        integrity_score = _as_float(integrity.get("integrity_score"))
        network_security = _as_float(network.get("network_security_score"))
        readiness_score = _as_float(network_auto_dev.get("readiness_score"))

        weight_total = (
            self.functionality_weight
            + self.mechanics_weight
            + self.design_weight
            + self.dynamics_weight
            + self.gameplay_weight
            + self.interaction_weight
            + self.innovation_weight
            + self.experience_weight
        ) or 1e-6
        weighted_signal = (
            functionality_score * self.functionality_weight
            + mechanics_novelty * self.mechanics_weight
            + design_score * self.design_weight
            + dynamics_synergy * self.dynamics_weight
            + gameplay_score * self.gameplay_weight
            + interaction_score * self.interaction_weight
            + innovation_score * self.innovation_weight
            + experience_score * self.experience_weight
        ) / weight_total

        resilience_bonus = min(
            6.5,
            resilience_score * 0.08 + integrity_score * 0.06,
        )
        holographic_bonus = min(
            5.0,
            _as_float(
                transmission.get("lithographic_integrity", {}).get("score")
            )
            * 0.08,
        )
        network_bonus = min(
            7.5,
            (readiness_score * 18.0 + network_security * 0.12)
            * self.network_bonus_factor,
        )

        functionality_risk = _as_float(functionality.get("risk_index"))
        interaction_gap = _as_float(
            (interaction.get("gap_summary") or {}).get("functionality_gap_index")
        )
        design_security_gap = _as_float(
            (design.get("risk_profile") or {}).get("security_gap")
        )
        research_pressure = _as_float(research.get("research_pressure_index"))
        fragility_index = _as_float(codebase.get("systems_fragility_index"))

        risk_penalty = min(
            36.0,
            max(functionality_risk, interaction_gap, design_security_gap)
            * self.risk_penalty_factor
            + research_pressure * 0.28,
        )
        fragility_penalty = min(
            32.0,
            fragility_index * self.fragility_penalty_factor,
        )

        systems_score = _clamp(
            weighted_signal
            + resilience_bonus
            + holographic_bonus
            + network_bonus
            - risk_penalty
            - fragility_penalty
        )
        priority = _priority(systems_score, fragility_index)

        systems_tracks = _normalise_strings(
            (
                *functionality.get("functionality_tracks", ()),
                *mechanics.get("functionality_tracks", ()),
                *dynamics.get("systems_tracks", ()),
                *gameplay.get("functionality_tracks", ()),
            )
        )
        systems_threads = _normalise_strings(
            (
                *mechanics.get("gameplay_threads", ()),
                *interaction.get("interaction_threads", ()),
                *gameplay.get("loops", ()),
                *design.get("prototype_threads", ()),
            )
        )
        systems_actions = _normalise_strings(
            (
                *design.get("design_actions", ()),
                *gameplay.get("managerial_actions", ()),
                *interaction.get("interaction_actions", ()),
                *network_auto_dev.get("next_steps", ()),
                *modernization.get("modernization_actions", ()),
                *optimization.get("optimization_actions", ()),
            )
        )
        managerial_directives = _normalise_strings(
            (
                *functionality.get("managerial_directives", ()),
                *dynamics.get("managerial_directives", ()),
                *playstyle.get("managerial_directives", ()),
                *design.get("design_directives", ()),
                *governance.get("oversight_actions", ()),
                *self_evolution.get("next_actions", ()),
            )
        )

        network_requirements = _merge_network_requirements(
            functionality.get("network_requirements"),
            design.get("network_requirements"),
            dynamics.get("network_requirements"),
            gameplay.get("network_requirements"),
            interaction.get("network_requirements"),
            playstyle.get("network_requirements"),
            network_auto_dev.get("security_focus")
            if isinstance(network_auto_dev.get("security_focus"), Mapping)
            else {},
        )
        holographic_requirements = _merge_holographic_requirements(
            transmission,
            functionality.get("holographic_requirements"),
            dynamics.get("holographic_requirements"),
            gameplay.get("holographic_requirements"),
            interaction.get("holographic_requirements"),
            design.get("holographic_requirements"),
        )

        codebase_alignment = {
            "systems_fragility_index": round(fragility_index, 2),
            "systems_alignment_index": round(
                _as_float(codebase.get("systems_alignment_index")), 2
            ),
            "systems_focus_modules": tuple(
                dict.fromkeys(codebase.get("systems_focus_modules", ()))
            ),
            "systems_recommendations": tuple(
                dict.fromkeys(codebase.get("systems_recommendations", ()))
            ),
            "functionality_gap_index": round(
                _as_float(codebase.get("functionality_gap_index")), 2
            ),
            "mechanics_alignment_score": round(
                _as_float(codebase.get("mechanics_alignment_score")), 2
            ),
        }
        systems_gap_summary = {
            "functionality_gap_index": codebase_alignment["functionality_gap_index"],
            "mechanics_alignment_score": codebase_alignment[
                "mechanics_alignment_score"
            ],
            "systems_fragility_index": codebase_alignment["systems_fragility_index"],
            "alignment_index": codebase_alignment["systems_alignment_index"],
            "focus_modules": codebase_alignment["systems_focus_modules"],
            "recommendations": codebase_alignment["systems_recommendations"],
        }

        research_implications = {
            "utilization_percent": _as_float(
                research.get("raw_utilization_percent")
            ),
            "pressure_index": _as_float(research.get("research_pressure_index")),
            "trend": str(research.get("trend_direction", "steady")),
            "required_support": _normalise_strings(
                (
                    *innovation.get("feature_concepts", ()),
                    *functionality.get("concept_briefs", ()),
                )
            ),
        }
        innovation_dependencies = _normalise_strings(
            (
                *design.get("innovation_dependencies", ()),
                *innovation.get("functionality_tracks", ()),
                *experience.get("experience_threads", ()),
            )
        )
        creation_windows = _normalise_strings(
            (
                *modernization.get("timeline", ()),
                *optimization.get("fix_windows", ()),
                *functionality.get("continuity_windows", ()),
            )
        )

        security_gap = max(0.0, 78.0 - _as_float(security.get("security_score")))
        phase_alignment: Mapping[str, Any] = transmission.get("phase_alignment", {})  # type: ignore[assignment]
        holographic_gap = max(0.0, 1.0 - _as_float(phase_alignment.get("target")))
        instability_index = _as_float(codebase.get("instability_index"))
        risk_profile = {
            "functional_risk": round(max(functionality_risk, interaction_gap), 2),
            "stability_pressure": round(instability_index * 24.0, 2),
            "security_gap": round(security_gap, 2),
            "holographic_gap": round(holographic_gap, 2),
        }

        architecture_overview = _architecture_overview(
            network,
            transmission,
            security,
            governance,
            self_evolution,
        )

        return {
            "priority": priority,
            "systems_score": round(systems_score, 2),
            "systems_tracks": systems_tracks,
            "systems_threads": systems_threads,
            "systems_actions": systems_actions,
            "systems_directives": managerial_directives,
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "risk_profile": risk_profile,
            "codebase_alignment": codebase_alignment,
            "systems_gap_summary": systems_gap_summary,
            "research_implications": research_implications,
            "innovation_dependencies": innovation_dependencies,
            "creation_windows": creation_windows,
            "architecture_overview": architecture_overview,
        }
