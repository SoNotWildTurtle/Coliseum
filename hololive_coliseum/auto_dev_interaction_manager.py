"""Fuse functionality, mechanics, and gameplay signals into interaction briefs."""

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
    unique: list[str] = []
    for value in values or ():
        text = str(value).strip()
        if text and text not in unique:
            unique.append(text)
    return tuple(unique)


def _priority(score: float) -> str:
    if score >= 80.0:
        return "amplify"
    if score >= 66.0:
        return "accelerate"
    if score >= 52.0:
        return "stabilise"
    if score >= 38.0:
        return "refine"
    return "observe"


def _loop_names(loops: Sequence[Mapping[str, Any]] | None) -> tuple[str, ...]:
    names: list[str] = []
    for loop in loops or ():
        if not isinstance(loop, Mapping):
            continue
        name = str(loop.get("name") or loop.get("focus_track") or "loop").strip()
        if name and name not in names:
            names.append(name)
    return tuple(names)


@dataclass
class AutoDevInteractionManager:
    """Blend gameplay, functionality, and network signals into interaction briefs."""

    functionality_weight: float = 0.32
    mechanics_weight: float = 0.24
    gameplay_weight: float = 0.22
    dynamics_weight: float = 0.2
    innovation_weight: float = 0.16
    experience_weight: float = 0.16
    playstyle_weight: float = 0.14
    resilience_weight: float = 0.18
    security_weight: float = 0.16
    network_weight: float = 0.14
    gap_penalty_factor: float = 0.42
    research_penalty_factor: float = 0.28

    def interaction_brief(
        self,
        *,
        functionality: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        gameplay: Mapping[str, Any] | None = None,
        dynamics: Mapping[str, Any] | None = None,
        innovation: Mapping[str, Any] | None = None,
        experience: Mapping[str, Any] | None = None,
        playstyle: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
        integrity: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        network_auto_dev: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        self_evolution: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return deterministic interaction telemetry for downstream planning."""

        functionality = functionality or {}
        mechanics = mechanics or {}
        gameplay = gameplay or {}
        dynamics = dynamics or {}
        innovation = innovation or {}
        experience = experience or {}
        playstyle = playstyle or {}
        modernization = modernization or {}
        optimization = optimization or {}
        resilience = resilience or {}
        integrity = integrity or {}
        security = security or {}
        network = network or {}
        network_auto_dev = network_auto_dev or {}
        transmission = transmission or {}
        research = research or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        codebase = codebase or {}
        self_evolution = self_evolution or {}

        functionality_score = _as_float(functionality.get("functionality_score"))
        mechanics_novelty = _as_float(mechanics.get("novelty_score"))
        gameplay_score = _as_float(gameplay.get("gameplay_score"))
        dynamics_synergy = _as_float(dynamics.get("synergy_score"))
        innovation_score = _as_float(innovation.get("innovation_score"))
        experience_score = _as_float(experience.get("experience_score"))
        playstyle_score = _as_float(playstyle.get("playstyle_score"))
        resilience_score = _as_float(resilience.get("resilience_score"))
        integrity_score = _as_float(integrity.get("integrity_score"))
        security_score = _as_float(security.get("security_score"))
        network_security = _as_float(network.get("network_security_score"))
        functionality_gap_index = _as_float(codebase.get("functionality_gap_index"))
        mechanics_alignment_score = _as_float(
            codebase.get("mechanics_alignment_score"),
            default=max(0.0, 100.0 - functionality_gap_index * 0.6),
        )
        research_pressure = _as_float(research.get("research_pressure_index"))
        research_utilisation = _as_float(
            research.get("raw_utilization_percent"),
            default=research.get("latest_sample_percent", 0.0),
        )

        functionality_risk = _as_float(functionality.get("risk_index"))
        dynamics_risk = _as_float((dynamics.get("risk_profile") or {}).get("combined_risk"))
        playstyle_risk = _as_float(playstyle.get("risk_index"))
        gameplay_profile = gameplay.get("risk_profile") or {}
        gameplay_risk = max(
            _as_float(gameplay_profile.get("functionality")),
            _as_float(gameplay_profile.get("dynamics")),
            _as_float(gameplay_profile.get("playstyle")),
        )

        weight_total = (
            self.functionality_weight
            + self.mechanics_weight
            + self.gameplay_weight
            + self.dynamics_weight
            + self.innovation_weight
            + self.experience_weight
            + self.playstyle_weight
        ) or 1e-6
        weighted_signal = (
            functionality_score * self.functionality_weight
            + mechanics_novelty * self.mechanics_weight
            + gameplay_score * self.gameplay_weight
            + dynamics_synergy * self.dynamics_weight
            + innovation_score * self.innovation_weight
            + experience_score * self.experience_weight
            + playstyle_score * self.playstyle_weight
        ) / weight_total

        stability_bonus = (
            resilience_score * self.resilience_weight
            + integrity_score * 0.14
            + max(security_score, network_security) * self.security_weight
            + mechanics_alignment_score * 0.15
        )
        stability_bonus = min(24.0, stability_bonus)

        risk_penalty = min(
            32.0,
            (
                functionality_risk * 0.32
                + dynamics_risk * 0.24
                + playstyle_risk * 0.18
                + gameplay_risk * 0.16
            )
            * self.research_penalty_factor
            + research_pressure * 0.3,
        )
        gap_penalty = min(28.0, functionality_gap_index * self.gap_penalty_factor)

        interaction_score = _clamp(
            weighted_signal + stability_bonus - risk_penalty - gap_penalty
        )
        priority = _priority(interaction_score)

        functionality_tracks = _normalise_strings(
            functionality.get("functionality_tracks", ())
        )
        dynamics_tracks = _normalise_strings(dynamics.get("systems_tracks", ()))
        mechanics_tracks = _normalise_strings(
            mechanics.get("functionality_tracks", ())
        )
        gameplay_loops = _loop_names(gameplay.get("loops"))
        interaction_tracks = _normalise_strings(
            (
                *functionality_tracks,
                *dynamics_tracks,
                *mechanics_tracks,
                *gameplay_loops,
            )
        )

        gameplay_threads = tuple(
            str(loop.get("experience_thread"))
            for loop in gameplay.get("loops", ())
            if isinstance(loop, Mapping) and loop.get("experience_thread")
        )
        interaction_threads = _normalise_strings(
            (
                *mechanics.get("gameplay_threads", ()),
                *experience.get("experience_threads", ()),
                *playstyle.get("tracks", ()),
                *gameplay_threads,
            )
        )

        managerial_directives = _normalise_strings(
            (
                *functionality.get("managerial_directives", ()),
                *dynamics.get("managerial_directives", ()),
                *playstyle.get("managerial_directives", ()),
                *gameplay.get("managerial_actions", ()),
                *modernization.get("modernization_actions", ()),
                *optimization.get("optimization_actions", ()),
                *mitigation.get("codebase_tasks", ()),
                *remediation.get("restoration_actions", ()),
            )
        )

        functionality_network = functionality.get("network_requirements") or {}
        dynamics_network = dynamics.get("network_requirements") or {}
        playstyle_network = playstyle.get("network_requirements") or {}
        gameplay_network = gameplay.get("network_requirements") or {}
        experience_network = experience.get("network_blueprint") or {}

        network_requirements = {
            "security_score": round(
                max(
                    _as_float(functionality_network.get("security_score")),
                    _as_float(dynamics_network.get("security_score")),
                    _as_float(playstyle_network.get("security_score")),
                    _as_float(gameplay_network.get("security_score")),
                    security_score,
                    network_security,
                ),
                2,
            ),
            "bandwidth_mbps": round(
                max(
                    _as_float(functionality_network.get("bandwidth_mbps")),
                    _as_float(dynamics_network.get("bandwidth_mbps")),
                    _as_float(playstyle_network.get("bandwidth_mbps")),
                    _as_float(gameplay_network.get("bandwidth_mbps")),
                    _as_float(experience_network.get("bandwidth_mbps")),
                ),
                2,
            ),
            "upgrade_actions": _normalise_strings(
                (
                    *(functionality_network.get("upgrade_actions") or ()),
                    *(dynamics_network.get("upgrade_actions") or ()),
                    *network_auto_dev.get("upgrade_tracks", ()),
                )
            ),
        }

        functionality_holographic = functionality.get("holographic_requirements") or {}
        dynamics_holographic = dynamics.get("holographic_requirements") or {}
        playstyle_holographic = playstyle.get("holographic_requirements") or {}
        gameplay_holographic = gameplay.get("holographic_requirements") or {}
        transmission_waveform = transmission.get("spectral_waveform") or {}
        transmission_phase = transmission.get("phase_alignment") or {}

        holographic_requirements = {
            "recommended_actions": _normalise_strings(
                (
                    *(functionality_holographic.get("recommended_actions") or ()),
                    *(dynamics_holographic.get("recommended_actions") or ()),
                    *(playstyle_holographic.get("recommended_actions") or ()),
                    *(gameplay_holographic.get("recommended_actions") or ()),
                    *(transmission_waveform.get("recommended_actions") or ()),
                )
            ),
            "phase_target": _as_float(
                transmission_phase.get("target"),
                default=0.0,
            ),
        }

        codebase_alignment = {
            "functionality_gaps": tuple(codebase.get("functionality_gaps", ()))[:4],
            "modernization_targets": tuple(codebase.get("modernization_targets", ()))[:4],
            "mitigation_plan": tuple(codebase.get("mitigation_plan", ()))[:3],
        }

        gap_summary = {
            "functionality_gap_index": round(functionality_gap_index, 2),
            "highlighted_gaps": codebase_alignment["functionality_gaps"],
            "mechanics_alignment_score": round(mechanics_alignment_score, 2),
        }

        research_implications = {
            "pressure_index": round(research_pressure, 2),
            "utilization_percent": round(research_utilisation, 2),
            "trend": str(research.get("trend_direction", "stable")),
        }

        network_synergy = {
            "upgrade_priority": network_auto_dev.get("priority", "monitor"),
            "next_steps": tuple(network_auto_dev.get("next_steps", ())),
            "security_focus": network_auto_dev.get("security_focus", {}),
        }

        backend_alignment = {
            "mitigation_focus": tuple(mitigation.get("codebase_tasks", ()))[:3],
            "remediation_actions": tuple(remediation.get("restoration_actions", ()))[:3],
            "self_evolution_state": self_evolution.get("readiness_state", "stabilise"),
        }

        risk_profile = {
            "functionality": round(functionality_risk, 2),
            "dynamics": round(dynamics_risk, 2),
            "playstyle": round(playstyle_risk, 2),
            "gameplay": round(gameplay_risk, 2),
            "research_pressure": round(research_pressure, 2),
            "gap_penalty": round(gap_penalty, 2),
        }

        return {
            "priority": priority,
            "interaction_score": round(interaction_score, 2),
            "interaction_tracks": interaction_tracks,
            "interaction_threads": interaction_threads,
            "interaction_actions": managerial_directives,
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "codebase_alignment": codebase_alignment,
            "gap_summary": gap_summary,
            "research_implications": research_implications,
            "network_synergy": network_synergy,
            "backend_alignment": backend_alignment,
            "risk_profile": risk_profile,
        }
