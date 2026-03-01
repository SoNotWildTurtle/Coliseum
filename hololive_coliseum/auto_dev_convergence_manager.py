"""Convergence manager that aligns creation, functionality, and mechanics planning."""

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
        security_scores.append(_as_float(requirement.get("security_score")))
        bandwidth_samples.append(_as_float(requirement.get("bandwidth_mbps")))
        latency_targets.append(_as_float(requirement.get("latency_target_ms")))
        upgrade_actions.extend(_normalise_strings(requirement.get("upgrade_actions")))
    security_score = (
        sum(security_scores) / len(security_scores) if security_scores else 0.0
    )
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
    efficiency_scores: list[float] = []
    phase_targets: list[float] = []
    for requirement in requirements:
        if not isinstance(requirement, Mapping):
            continue
        actions.extend(_normalise_strings(requirement.get("recommended_actions")))
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
    phase_target = sum(phase_targets) / len(phase_targets) if phase_targets else 0.0
    return {
        "recommended_actions": tuple(dict.fromkeys(actions)),
        "efficiency_score": round(efficiency, 2),
        "phase_target": round(phase_target, 2),
    }


def _priority(score: float, risk_index: float, gap_index: float) -> str:
    if score >= 82.0 and risk_index <= 24.0 and gap_index <= 26.0:
        return "amplify"
    if score >= 74.0 and risk_index <= 32.0:
        return "accelerate"
    if score >= 60.0:
        return "stabilise"
    if score >= 48.0:
        return "refine"
    return "observe"


def _merge_threads(*collections: Sequence[Any] | None) -> tuple[str, ...]:
    threads: list[str] = []
    for collection in collections:
        for value in collection or ():
            text = str(value).strip()
            if text and text not in threads:
                threads.append(text)
    return tuple(threads)


def _merge_actions(*collections: Sequence[Any] | None) -> tuple[str, ...]:
    actions: list[str] = []
    for collection in collections:
        for value in collection or ():
            if isinstance(value, Mapping):
                text = str(value.get("name", "")).strip()
            else:
                text = str(value).strip()
            if text and text not in actions:
                actions.append(text)
    return tuple(actions)


def _cohesion_index(*values: float) -> float:
    valid = [value for value in values if value > 0.0]
    if not valid:
        return 0.0
    spread = max(valid) - min(valid)
    return round(max(0.0, 100.0 - spread), 2)


@dataclass
class AutoDevConvergenceManager:
    """Blend functionality, mechanics, and creation telemetry into convergence briefs."""

    functionality_weight: float = 0.26
    mechanics_weight: float = 0.22
    creation_weight: float = 0.2
    dynamics_weight: float = 0.16
    synthesis_weight: float = 0.16
    design_weight: float = 0.12
    systems_weight: float = 0.12
    innovation_weight: float = 0.1
    experience_weight: float = 0.1
    risk_penalty_factor: float = 0.22
    gap_penalty_factor: float = 0.2
    network_bonus_factor: float = 0.08
    holographic_bonus_factor: float = 0.07
    research_bonus_factor: float = 0.06

    def convergence_brief(
        self,
        *,
        functionality: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        creation: Mapping[str, Any] | None = None,
        dynamics: Mapping[str, Any] | None = None,
        synthesis: Mapping[str, Any] | None = None,
        design: Mapping[str, Any] | None = None,
        systems: Mapping[str, Any] | None = None,
        innovation: Mapping[str, Any] | None = None,
        experience: Mapping[str, Any] | None = None,
        gameplay: Mapping[str, Any] | None = None,
        interaction: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        network_auto_dev: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        integrity: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic convergence brief for downstream orchestration."""

        functionality = functionality or {}
        mechanics = mechanics or {}
        creation = creation or {}
        dynamics = dynamics or {}
        synthesis = synthesis or {}
        design = design or {}
        systems = systems or {}
        innovation = innovation or {}
        experience = experience or {}
        gameplay = gameplay or {}
        interaction = interaction or {}
        network = network or {}
        network_auto_dev = network_auto_dev or {}
        transmission = transmission or {}
        security = security or {}
        modernization = modernization or {}
        optimization = optimization or {}
        integrity = integrity or {}
        governance = governance or {}
        research = research or {}
        codebase = codebase or {}

        functionality_score = _as_float(functionality.get("functionality_score"))
        mechanics_novelty = _as_float(mechanics.get("novelty_score"))
        creation_score = _as_float(creation.get("creation_score"))
        dynamics_synergy = _as_float(dynamics.get("synergy_score"))
        synthesis_score = _as_float(synthesis.get("synthesis_score"))
        design_score = _as_float(design.get("design_score"))
        systems_score = _as_float(systems.get("systems_score"))
        innovation_score = _as_float(innovation.get("innovation_score"))
        experience_score = _as_float(experience.get("experience_score"))

        weight_total = (
            self.functionality_weight
            + self.mechanics_weight
            + self.creation_weight
            + self.dynamics_weight
            + self.synthesis_weight
            + self.design_weight
            + self.systems_weight
            + self.innovation_weight
            + self.experience_weight
        )
        weighted_signal = 0.0
        if weight_total:
            weighted_signal = (
                functionality_score * self.functionality_weight
                + mechanics_novelty * self.mechanics_weight
                + creation_score * self.creation_weight
                + dynamics_synergy * self.dynamics_weight
                + synthesis_score * self.synthesis_weight
                + design_score * self.design_weight
                + systems_score * self.systems_weight
                + innovation_score * self.innovation_weight
                + experience_score * self.experience_weight
            ) / weight_total

        risk_index = (
            _as_float(functionality.get("risk_index"))
            + _as_float(mechanics.get("risk_score"))
            + _as_float(creation.get("risk_profile", {}).get("risk_index"))
            + _as_float(synthesis.get("risk_index"))
        ) / 4.0
        gap_index = (
            _as_float(functionality.get("gap_index"))
            + _as_float(creation.get("creation_gap_summary", {}).get("gap_index"))
            + _as_float(synthesis.get("gap_index"))
            + _as_float(codebase.get("convergence_gap_index"))
        ) / 4.0

        network_security = _as_float(network.get("network_security_score"))
        security_score = _as_float(security.get("security_score"))
        holographic_efficiency = _as_float(
            transmission.get("lithographic_integrity", {}).get("score")
        )
        research_utilisation = _as_float(research.get("raw_utilization_percent"))

        bonus = (
            network_security * self.network_bonus_factor
            + security_score * (self.network_bonus_factor / 2.0)
            + holographic_efficiency * self.holographic_bonus_factor
            + research_utilisation * self.research_bonus_factor
        ) / max(1.0, self.network_bonus_factor + self.holographic_bonus_factor)

        penalty = risk_index * self.risk_penalty_factor + gap_index * self.gap_penalty_factor
        convergence_score = _clamp(weighted_signal + bonus - penalty)

        integration_index = round(
            min(
                100.0,
                (functionality_score + mechanics_novelty + creation_score + synthesis_score)
                / 4.0,
            ),
            2,
        )
        cohesion_index = _cohesion_index(
            functionality_score,
            mechanics_novelty,
            creation_score,
            dynamics_synergy,
            synthesis_score,
        )

        network_requirements = _merge_network_requirements(
            functionality.get("network_requirements"),
            mechanics.get("network_considerations"),
            creation.get("network_requirements"),
            synthesis.get("network_requirements"),
            gameplay.get("network_requirements"),
            interaction.get("network_requirements"),
            network_auto_dev.get("network_requirements"),
        )
        holographic_requirements = _merge_holographic_requirements(
            transmission,
            functionality.get("holographic_requirements"),
            mechanics.get("holographic_requirements"),
            creation.get("holographic_requirements"),
            synthesis.get("holographic_requirements"),
            gameplay.get("holographic_requirements"),
            interaction.get("holographic_requirements"),
        )

        functionality_tracks = functionality.get("functionality_tracks", ())
        mechanics_threads = mechanics.get("gameplay_threads", ())
        creation_threads = creation.get("creation_threads", ())
        synthesis_threads = synthesis.get("concept_threads", ())
        dynamics_threads = dynamics.get("systems_threads", ())
        gameplay_loops = gameplay.get("loops", ())
        interaction_threads = interaction.get("interaction_threads", ())

        convergence_tracks = _merge_threads(
            functionality_tracks,
            creation.get("creation_tracks"),
            synthesis.get("expansion_tracks"),
            gameplay.get("loops"),
        )
        convergence_threads = _merge_threads(
            mechanics_threads,
            creation_threads,
            synthesis_threads,
            dynamics_threads,
            gameplay_loops,
            interaction_threads,
        )
        convergence_actions = _merge_actions(
            creation.get("creation_actions"),
            synthesis.get("expansion_actions"),
            gameplay.get("managerial_actions"),
            interaction.get("interaction_actions"),
            modernization.get("modernization_actions"),
            optimization.get("optimization_actions"),
            integrity.get("restoration_actions"),
        )

        governance_state = str(governance.get("state", "guided"))
        modernization_priority = str(modernization.get("priority", "monitor"))
        optimization_priority = str(optimization.get("priority", "monitor"))

        priority = _priority(convergence_score, risk_index, gap_index)
        research_implications = {
            "utilization_percent": round(research_utilisation, 2),
            "pressure_index": round(_as_float(research.get("research_pressure_index")), 2),
            "trend": str(research.get("trend_direction", "stable")),
        }

        codebase_alignment = {
            "convergence_alignment_score": round(
                _as_float(codebase.get("convergence_alignment_score")), 2
            ),
            "convergence_gap_index": round(_as_float(codebase.get("convergence_gap_index")), 2),
            "convergence_focus_modules": tuple(
                dict.fromkeys(codebase.get("convergence_focus_modules", ()))
            ),
        }

        supporting_signals = {
            "governance_state": governance_state,
            "modernization_priority": modernization_priority,
            "optimization_priority": optimization_priority,
            "network_security_score": round(network_security, 2),
            "security_threat_level": str(security.get("threat_level", "guarded")),
        }

        alignment_summary = {
            "functionality_score": round(functionality_score, 2),
            "mechanics_novelty_score": round(mechanics_novelty, 2),
            "creation_score": round(creation_score, 2),
            "dynamics_synergy_score": round(dynamics_synergy, 2),
            "synthesis_score": round(synthesis_score, 2),
            "design_focus_index": round(
                _as_float(design.get("design_gap_summary", {}).get("focus_index")), 2
            ),
            "systems_alignment_index": round(
                _as_float(systems.get("systems_gap_summary", {}).get("alignment_index")), 2
            ),
            "innovation_score": round(innovation_score, 2),
            "experience_score": round(experience_score, 2),
        }

        return {
            "priority": priority,
            "convergence_score": round(convergence_score, 2),
            "integration_index": integration_index,
            "cohesion_index": cohesion_index,
            "risk_index": round(risk_index, 2),
            "gap_index": round(gap_index, 2),
            "convergence_tracks": convergence_tracks,
            "convergence_threads": convergence_threads,
            "convergence_actions": convergence_actions,
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "research_implications": research_implications,
            "codebase_alignment": codebase_alignment,
            "alignment_summary": alignment_summary,
            "supporting_signals": supporting_signals,
        }
