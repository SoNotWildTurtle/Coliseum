"""Synthesis manager that aligns creation and mechanics planning outputs."""

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


def _priority(score: float, risk_index: float, gap_index: float) -> str:
    if score >= 82.0 and risk_index <= 26.0 and gap_index <= 24.0:
        return "amplify"
    if score >= 72.0 and risk_index <= 32.0:
        return "accelerate"
    if score >= 60.0:
        return "stabilise"
    if score >= 48.0:
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
    phase_alignment: Mapping[str, Any] = transmission.get("phase_alignment", {})  # type: ignore[assignment]
    lithographic: Mapping[str, Any] = transmission.get("lithographic_integrity", {})  # type: ignore[assignment]
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


@dataclass
class AutoDevSynthesisManager:
    """Blend creation and mechanics telemetry into actionable synthesis briefs."""

    functionality_weight: float = 0.26
    mechanics_weight: float = 0.24
    creation_weight: float = 0.24
    design_weight: float = 0.18
    systems_weight: float = 0.18
    dynamics_weight: float = 0.18
    innovation_weight: float = 0.15
    experience_weight: float = 0.12
    risk_penalty_factor: float = 0.24
    gap_penalty_factor: float = 0.22
    security_bonus_factor: float = 0.12
    novelty_bonus_factor: float = 0.18

    def synthesis_brief(
        self,
        *,
        functionality: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        creation: Mapping[str, Any] | None = None,
        blueprint: Mapping[str, Any] | None = None,
        design: Mapping[str, Any] | None = None,
        systems: Mapping[str, Any] | None = None,
        dynamics: Mapping[str, Any] | None = None,
        innovation: Mapping[str, Any] | None = None,
        experience: Mapping[str, Any] | None = None,
        gameplay: Mapping[str, Any] | None = None,
        playstyle: Mapping[str, Any] | None = None,
        interaction: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        network_auto_dev: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        integrity: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic synthesis brief for downstream orchestration."""

        functionality = functionality or {}
        mechanics = mechanics or {}
        creation = creation or {}
        blueprint = blueprint or {}
        design = design or {}
        systems = systems or {}
        dynamics = dynamics or {}
        innovation = innovation or {}
        experience = experience or {}
        gameplay = gameplay or {}
        playstyle = playstyle or {}
        interaction = interaction or {}
        network = network or {}
        network_auto_dev = network_auto_dev or {}
        transmission = transmission or {}
        security = security or {}
        modernization = modernization or {}
        optimization = optimization or {}
        integrity = integrity or {}
        governance = governance or {}
        codebase = codebase or {}
        research = research or {}

        functionality_score = _as_float(functionality.get("functionality_score"))
        mechanics_novelty = _as_float(mechanics.get("novelty_score"))
        creation_score = _as_float(creation.get("creation_score"))
        design_score = _as_float(design.get("design_score"))
        systems_score = _as_float(systems.get("systems_score"))
        dynamics_synergy = _as_float(dynamics.get("synergy_score"))
        innovation_score = _as_float(innovation.get("innovation_score"))
        experience_score = _as_float(experience.get("experience_score"))
        blueprint_score = _as_float(blueprint.get("blueprint_score"))
        blueprint_cohesion = _as_float(blueprint.get("cohesion_index"))
        blueprint_alignment_score = _as_float(blueprint.get("alignment_index"))

        mechanics_synergy_index = _as_float(
            creation.get("mechanics_synergy_index", mechanics.get("cohesion_score"))
        )
        functionality_extension_index = _as_float(
            creation.get(
                "functionality_extension_index",
                functionality.get("functionality_score"),
            )
        )
        creation_gap_summary: Mapping[str, Any] = creation.get("creation_gap_summary", {})
        risk_profile: Mapping[str, Any] = creation.get("risk_profile", {})
        codebase_alignment: Mapping[str, Any] = creation.get("codebase_alignment", {})

        gap_index = max(
            _as_float(creation_gap_summary.get("gap_index")),
            _as_float(risk_profile.get("gap_index")),
            _as_float(codebase_alignment.get("creation_gap_index")),
            _as_float(blueprint.get("gap_index")),
        )
        risk_index = max(
            _as_float(risk_profile.get("risk_index")),
            _as_float(functionality.get("risk_index")),
            _as_float(mechanics.get("risk_score")),
            _as_float((dynamics.get("risk_profile", {}) or {}).get("combined_risk")),
            _as_float((interaction.get("risk_profile", {}) or {}).get("interaction_risk")),
        )

        weight_total = (
            self.functionality_weight
            + self.mechanics_weight
            + self.creation_weight
            + self.design_weight
            + self.systems_weight
            + self.dynamics_weight
            + self.innovation_weight
            + self.experience_weight
        ) or 1e-6
        weighted_signal = (
            functionality_score * self.functionality_weight
            + mechanics_novelty * self.mechanics_weight
            + creation_score * self.creation_weight
            + design_score * self.design_weight
            + systems_score * self.systems_weight
            + dynamics_synergy * self.dynamics_weight
            + innovation_score * self.innovation_weight
            + experience_score * self.experience_weight
        ) / weight_total

        security_bonus = min(
            10.0,
            _as_float(security.get("security_score", network.get("network_security_score")))
            * self.security_bonus_factor,
        )
        novelty_signal = (
            mechanics_synergy_index
            + functionality_extension_index
            + innovation_score * 0.5
            + blueprint_cohesion * 0.6
            + blueprint_alignment_score * 0.4
        )
        novelty_bonus = min(14.0, novelty_signal * self.novelty_bonus_factor)
        novelty_bonus += min(5.0, blueprint_score * 0.06)
        penalty = risk_index * self.risk_penalty_factor + gap_index * self.gap_penalty_factor
        synthesis_score = _clamp(weighted_signal + security_bonus + novelty_bonus - penalty)
        priority = _priority(synthesis_score, risk_index, gap_index)

        mechanics_tracks = creation.get("mechanics_expansion_tracks") or blueprint.get(
            "mechanics_extension_tracks"
        ) or mechanics.get("functionality_tracks", ())
        functionality_tracks = creation.get("functionality_extension_tracks") or blueprint.get(
            "functionality_extension_tracks"
        ) or functionality.get("functionality_tracks", ())
        expansion_tracks = creation.get("expansion_tracks") or (
            *mechanics_tracks,
            *functionality_tracks,
        )
        expansion_tracks = _normalise_strings(expansion_tracks)

        mechanics_expansion_tracks = _normalise_strings(mechanics_tracks)
        functionality_extension_tracks = _normalise_strings(functionality_tracks)

        concept_threads = _normalise_strings(
            (
                *creation.get("creation_threads", ()),
                *functionality.get("functionality_threads", ()),
                *interaction.get("interaction_threads", ()),
                *gameplay.get("loops", ()),
                *blueprint.get("threads", ()),
            )
        )

        expansion_actions = _normalise_strings(
            (
                *creation.get("creation_actions", ()),
                *functionality.get("managerial_directives", ()),
                *design.get("design_actions", ()),
                *systems.get("systems_actions", ()),
                *modernization.get("modernization_actions", ()),
                *optimization.get("optimization_actions", ()),
                *governance.get("oversight_actions", ()),
                *integrity.get("restoration_actions", ()),
                *blueprint.get("actions", ()),
            )
        )

        network_requirements = _merge_network_requirements(
            functionality.get("network_requirements"),
            mechanics.get("network_considerations"),
            creation.get("network_requirements"),
            design.get("network_requirements"),
            systems.get("network_requirements"),
            gameplay.get("network_requirements"),
            playstyle.get("network_requirements"),
            interaction.get("network_requirements"),
            network_auto_dev.get("network_requirements"),
            blueprint.get("network_requirements"),
        )

        holographic_requirements = _merge_holographic_requirements(
            transmission,
            functionality.get("holographic_requirements"),
            creation.get("holographic_requirements"),
            design.get("holographic_requirements"),
            systems.get("holographic_requirements"),
            gameplay.get("holographic_requirements"),
            playstyle.get("holographic_requirements"),
            interaction.get("holographic_requirements"),
            blueprint.get("holographic_requirements"),
        )

        research_implications = {
            "trend": str(research.get("trend_direction", research.get("trend", "steady"))),
            "pressure_index": _as_float(research.get("research_pressure_index")),
            "utilization_percent": _as_float(
                research.get("raw_utilization_percent")
                or research.get("latest_sample_percent")
            ),
        }

        supporting_signals = {
            "modernization_priority": modernization.get("priority", "monitor"),
            "optimization_priority": optimization.get("priority", "monitor"),
            "integrity_priority": integrity.get("priority", "monitor"),
            "security_threat_level": security.get("threat_level", "guarded"),
            "blueprint_priority": blueprint.get("priority", "survey"),
        }

        alignment_summary = {
            "mechanics_synergy_index": round(mechanics_synergy_index, 2),
            "functionality_extension_index": round(functionality_extension_index, 2),
            "design_alignment": round(design_score, 2),
            "systems_alignment": round(systems_score, 2),
            "experience_alignment": round(experience_score, 2),
            "blueprint_cohesion_index": round(blueprint_cohesion, 2),
            "blueprint_alignment_score": round(blueprint_alignment_score, 2),
            "codebase_alignment": _as_float(
                codebase_alignment.get("creation_alignment_score")
                or codebase.get("creation_alignment_score")
            ),
        }

        codebase_summary = {
            "creation_alignment_score": alignment_summary["codebase_alignment"],
            "risk_index": risk_index,
            "gap_index": gap_index,
            "focus_modules": tuple(codebase_alignment.get("creation_focus_modules", ())),
            "blueprint_focus_modules": tuple(blueprint.get("focus_modules", ())),
        }

        return {
            "priority": priority,
            "synthesis_score": round(synthesis_score, 2),
            "risk_index": round(risk_index, 2),
            "gap_index": round(gap_index, 2),
            "expansion_tracks": expansion_tracks,
            "mechanics_expansion_tracks": mechanics_expansion_tracks,
            "functionality_extension_tracks": functionality_extension_tracks,
            "expansion_actions": expansion_actions,
            "concept_threads": concept_threads,
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "research_implications": research_implications,
            "supporting_signals": supporting_signals,
            "blueprint_priority": blueprint.get("priority", "survey"),
            "blueprint_score": round(blueprint_score, 2),
            "blueprint_gap_index": round(_as_float(blueprint.get("gap_index")), 2),
            "blueprint_cohesion_index": round(blueprint_cohesion, 2),
            "blueprint_tracks": _normalise_strings(blueprint.get("tracks", ())),
            "blueprint_threads": _normalise_strings(blueprint.get("threads", ())),
            "blueprint_actions": _normalise_strings(blueprint.get("actions", ())),
            "blueprint_network_requirements": blueprint.get("network_requirements", {}),
            "blueprint_holographic_requirements": blueprint.get(
                "holographic_requirements",
                {},
            ),
            "blueprint_supporting_signals": blueprint.get("supporting_signals", {}),
            "alignment_summary": alignment_summary,
            "codebase_alignment": codebase_summary,
        }

