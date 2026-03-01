"""Blend functionality and mechanics telemetry into creation blueprints."""

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


def _priority(score: float, gap_index: float, risk_index: float) -> str:
    if score >= 80.0 and gap_index <= 30.0 and risk_index <= 35.0:
        return "accelerate"
    if score >= 70.0 and gap_index <= 42.0:
        return "amplify"
    if score >= 58.0:
        return "stabilise"
    if score >= 46.0:
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
    phase_target = (
        sum(phase_targets) / len(phase_targets) if phase_targets else 0.0
    )
    return {
        "recommended_actions": tuple(dict.fromkeys(actions)),
        "efficiency_score": round(efficiency, 2),
        "phase_target": round(phase_target, 2),
    }


def _concept_portfolio(
    functionality: Mapping[str, Any],
    innovation: Mapping[str, Any],
    gameplay: Mapping[str, Any],
) -> tuple[dict[str, Any], ...]:
    portfolio: list[dict[str, Any]] = []
    for concept in functionality.get("concept_briefs", ()):  # type: ignore[assignment]
        if not isinstance(concept, Mapping):
            continue
        portfolio.append(
            {
                "name": str(concept.get("name", "")).strip() or "core-track",
                "track": str(concept.get("track", "")).strip() or "core",
                "readiness": str(concept.get("readiness", "monitor")),
                "target_module": str(concept.get("target_module", "gameplay")),
            }
        )
    for concept in innovation.get("feature_concepts", ()):  # type: ignore[assignment]
        if isinstance(concept, Mapping):
            name = str(concept.get("name", "")).strip()
        else:
            name = str(concept).strip()
        if not name:
            continue
        portfolio.append(
            {
                "name": name,
                "track": str(concept.get("track", "innovation"))
                if isinstance(concept, Mapping)
                else "innovation",
                "readiness": str(concept.get("readiness", "refine"))
                if isinstance(concept, Mapping)
                else "refine",
                "target_module": str(concept.get("target_module", "systems"))
                if isinstance(concept, Mapping)
                else "systems",
            }
        )
    if not portfolio:
        loops: Sequence[Any] = gameplay.get("loops", ())  # type: ignore[assignment]
        for loop in loops[:2]:
            if isinstance(loop, Mapping):
                loop_name = str(loop.get("name", "")).strip()
            else:
                loop_name = str(loop).strip()
            if loop_name:
                portfolio.append(
                    {
                        "name": loop_name,
                        "track": "gameplay",
                        "readiness": "refine",
                        "target_module": "gameplay",
                    }
                )
    return tuple(portfolio[:6])


def _prototype_requirements(
    design: Mapping[str, Any],
    functionality: Mapping[str, Any],
    modernization: Mapping[str, Any],
    optimization: Mapping[str, Any],
) -> tuple[dict[str, Any], ...]:
    requirements: list[dict[str, Any]] = []
    for window in design.get("creation_windows", ()):  # type: ignore[assignment]
        requirements.append({"window": str(window), "focus": "design"})
    for window in functionality.get("continuity_windows", ()):  # type: ignore[assignment]
        requirements.append({"window": str(window), "focus": "functionality"})
    for entry in modernization.get("timeline", ()):  # type: ignore[assignment]
        if isinstance(entry, Mapping):
            requirements.append(
                {
                    "window": str(entry.get("window", "")),
                    "focus": str(entry.get("focus", "modernization")),
                }
            )
    for window in optimization.get("fix_windows", ()):  # type: ignore[assignment]
        requirements.append({"window": str(window), "focus": "optimization"})
    filtered = [
        {"window": item.get("window", ""), "focus": item.get("focus", "creation")}
        for item in requirements
        if item.get("window")
    ]
    return tuple(filtered[:6])


@dataclass
class AutoDevCreationManager:
    """Combine auto-dev signals into actionable creation briefs."""

    functionality_weight: float = 0.3
    mechanics_weight: float = 0.22
    design_weight: float = 0.2
    systems_weight: float = 0.18
    innovation_weight: float = 0.16
    experience_weight: float = 0.14
    alignment_weight: float = 0.2
    risk_penalty_factor: float = 0.18
    gap_penalty_factor: float = 0.22

    def creation_blueprint(
        self,
        *,
        functionality: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        design: Mapping[str, Any] | None = None,
        systems: Mapping[str, Any] | None = None,
        innovation: Mapping[str, Any] | None = None,
        experience: Mapping[str, Any] | None = None,
        interaction: Mapping[str, Any] | None = None,
        gameplay: Mapping[str, Any] | None = None,
        playstyle: Mapping[str, Any] | None = None,
        dynamics: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        integrity: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic creation plan for downstream orchestration."""

        functionality = functionality or {}
        mechanics = mechanics or {}
        design = design or {}
        systems = systems or {}
        innovation = innovation or {}
        experience = experience or {}
        interaction = interaction or {}
        gameplay = gameplay or {}
        playstyle = playstyle or {}
        dynamics = dynamics or {}
        modernization = modernization or {}
        optimization = optimization or {}
        integrity = integrity or {}
        codebase = codebase or {}
        research = research or {}
        network = network or {}
        transmission = transmission or {}
        governance = governance or {}

        functionality_score = _as_float(functionality.get("functionality_score"))
        mechanics_novelty = _as_float(mechanics.get("novelty_score"))
        design_score = _as_float(design.get("design_score"))
        systems_score = _as_float(systems.get("systems_score"))
        innovation_score = _as_float(innovation.get("innovation_score"))
        dynamics_synergy = _as_float(dynamics.get("synergy_score"))
        experience_score = _as_float(experience.get("experience_score"))
        alignment_score = _as_float(codebase.get("creation_alignment_score"))
        gap_index = _as_float(codebase.get("creation_gap_index"))

        risk_components = [
            functionality.get("risk_index"),
            mechanics.get("risk_score"),
            (dynamics.get("risk_profile", {}) or {}).get("combined_risk"),
            (interaction.get("risk_profile", {}) or {}).get("interaction_risk"),
            (design.get("risk_profile", {}) or {}).get("security_gap"),
            (systems.get("risk_profile", {}) or {}).get("security_gap"),
            (integrity.get("risk_profile", {}) or {}).get("security_gap"),
        ]
        risk_index = max((_as_float(value) for value in risk_components if value), default=0.0)

        weighted_score = (
            functionality_score * self.functionality_weight
            + mechanics_novelty * self.mechanics_weight
            + design_score * self.design_weight
            + systems_score * self.systems_weight
            + innovation_score * self.innovation_weight
            + experience_score * self.experience_weight
            + alignment_score * self.alignment_weight
        )
        penalty = risk_index * self.risk_penalty_factor + gap_index * self.gap_penalty_factor
        creation_score = _clamp(weighted_score - penalty)
        priority = _priority(creation_score, gap_index, risk_index)

        creation_tracks = _normalise_strings(
            (
                *functionality.get("functionality_tracks", ()),
                *design.get("creation_tracks", ()),
                *systems.get("systems_tracks", ()),
                *innovation.get("functionality_tracks", ()),
                *playstyle.get("tracks", ()),
            )
        )
        creation_threads = _normalise_strings(
            (
                *functionality.get("functionality_threads", ()),
                *design.get("prototype_threads", ()),
                *systems.get("systems_threads", ()),
                *experience.get("experience_threads", ()),
                *interaction.get("interaction_threads", ()),
            )
        )
        creation_actions = _normalise_strings(
            (
                *functionality.get("managerial_directives", ()),
                *design.get("design_actions", ()),
                *modernization.get("modernization_actions", ()),
                *optimization.get("optimization_actions", ()),
                *governance.get("oversight_actions", ()),
                *integrity.get("restoration_actions", ()),
            )
        )

        network_requirements = _merge_network_requirements(
            functionality.get("network_requirements"),
            design.get("network_requirements"),
            systems.get("network_requirements"),
            gameplay.get("network_requirements"),
            playstyle.get("network_requirements"),
        )
        holographic_requirements = _merge_holographic_requirements(
            transmission,
            functionality.get("holographic_requirements"),
            design.get("holographic_requirements"),
            systems.get("holographic_requirements"),
            gameplay.get("holographic_requirements"),
            playstyle.get("holographic_requirements"),
        )

        concept_portfolio = _concept_portfolio(functionality, innovation, gameplay)
        prototype_requirements = _prototype_requirements(
            design,
            functionality,
            modernization,
            optimization,
        )

        research_implications = {
            "utilization_percent": _as_float(
                research.get("raw_utilization_percent")
                or research.get("latest_sample_percent")
            ),
            "pressure_index": _as_float(research.get("research_pressure_index")),
            "trend": str(research.get("trend_direction", research.get("trend", "steady"))),
        }

        governance_alignment = {
            "state": str(governance.get("state", "guided")),
            "actions": tuple(governance.get("oversight_actions", ())),
            "modernization_alignment": (
                governance.get("modernization_alignment", {})  # type: ignore[arg-type]
            ),
        }

        playstyle_alignment = {
            "archetypes": tuple(playstyle.get("archetypes", ())),
            "tuning_actions": tuple(playstyle.get("tuning_actions", ())),
        }

        creation_gap_summary = {
            "gap_index": gap_index,
            "focus_modules": tuple(codebase.get("creation_focus_modules", ())),
            "recommendations": tuple(codebase.get("creation_recommendations", ())),
        }

        risk_profile = {
            "risk_index": round(risk_index, 2),
            "gap_index": round(gap_index, 2),
            "alignment_score": round(alignment_score, 2),
            "network_security_score": _as_float(network.get("network_security_score")),
        }

        mechanics_synergy_index = _clamp(
            (
                mechanics_novelty
                + dynamics_synergy
                + systems_score
            )
            / 3.0
            if any((mechanics_novelty, dynamics_synergy, systems_score))
            else 0.0
        )
        functionality_extension_index = _clamp(
            (
                functionality_score
                + design_score
                + innovation_score
            )
            / 3.0
            if any((functionality_score, design_score, innovation_score))
            else 0.0
        )
        mechanics_expansion_tracks = _normalise_strings(
            (
                *mechanics.get("gameplay_threads", ()),
                *dynamics.get("systems_tracks", ()),
                *systems.get("systems_threads", ()),
            )
        )
        functionality_extension_tracks = _normalise_strings(
            (
                *functionality.get("functionality_tracks", ()),
                *design.get("creation_tracks", ()),
                *innovation.get("functionality_tracks", ()),
            )
        )
        expansion_tracks = _normalise_strings(
            (
                *creation_tracks,
                *mechanics_expansion_tracks,
                *functionality_extension_tracks,
            )
        )

        codebase_alignment = {
            "creation_alignment_score": round(alignment_score, 2),
            "creation_gap_index": round(gap_index, 2),
            "creation_focus_modules": tuple(codebase.get("creation_focus_modules", ())),
            "creation_recommendations": tuple(
                codebase.get("creation_recommendations", ())
            ),
            "stability_outlook": codebase.get("stability_outlook", "steady"),
        }

        supporting_signals = {
            "modernization_priority": modernization.get("priority", "monitor"),
            "optimization_priority": optimization.get("priority", "monitor"),
            "integrity_priority": integrity.get("priority", "monitor"),
        }

        return {
            "priority": priority,
            "creation_score": round(creation_score, 2),
            "creation_tracks": creation_tracks,
            "creation_threads": creation_threads,
            "creation_actions": creation_actions,
            "concept_portfolio": concept_portfolio,
            "prototype_requirements": prototype_requirements,
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "research_implications": research_implications,
            "governance_alignment": governance_alignment,
            "playstyle_alignment": playstyle_alignment,
            "creation_gap_summary": creation_gap_summary,
            "risk_profile": risk_profile,
            "codebase_alignment": codebase_alignment,
            "supporting_signals": supporting_signals,
            "mechanics_synergy_index": round(mechanics_synergy_index, 2),
            "functionality_extension_index": round(functionality_extension_index, 2),
            "mechanics_expansion_tracks": mechanics_expansion_tracks,
            "functionality_extension_tracks": functionality_extension_tracks,
            "expansion_tracks": expansion_tracks,
        }

