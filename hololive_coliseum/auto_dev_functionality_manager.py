"""Assemble functionality expansion briefs for the auto-dev workflow."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalise_strings(values: Sequence[Any] | None) -> tuple[str, ...]:
    normalised: list[str] = []
    for value in values or ():
        text = str(value).strip()
        if text and text not in normalised:
            normalised.append(text)
    return tuple(normalised)


def _timeline_windows(timeline: Sequence[Mapping[str, Any]] | None) -> tuple[str, ...]:
    windows: list[str] = []
    for entry in timeline or ():
        if not isinstance(entry, Mapping):
            continue
        window = str(entry.get("window", "")).strip()
        if window and window not in windows:
            windows.append(window)
    return tuple(windows)


def _priority_from_score(score: float) -> str:
    if score >= 75.0:
        return "amplify"
    if score >= 60.0:
        return "accelerate"
    if score >= 45.0:
        return "stabilise"
    if score >= 30.0:
        return "refine"
    return "observe"


@dataclass
class AutoDevFunctionalityManager:
    """Blend mechanics, innovation, and experience data into functionality briefs."""

    novelty_weight: float = 0.4
    experience_weight: float = 0.35
    innovation_weight: float = 0.25
    resilience_weight: float = 0.2
    risk_penalty_factor: float = 0.35

    def functionality_brief(
        self,
        *,
        guidance: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        innovation: Mapping[str, Any] | None = None,
        experience: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        integrity: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        network_auto_dev: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
        continuity: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        self_evolution: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic functionality brief for MMO feature planning."""

        guidance = guidance or {}
        mechanics = mechanics or {}
        innovation = innovation or {}
        experience = experience or {}
        modernization = modernization or {}
        optimization = optimization or {}
        integrity = integrity or {}
        resilience = resilience or {}
        research = research or {}
        network = network or {}
        network_auto_dev = network_auto_dev or {}
        transmission = transmission or {}
        security = security or {}
        governance = governance or {}
        continuity = continuity or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        codebase = codebase or {}
        self_evolution = self_evolution or {}

        novelty_score = _as_float(mechanics.get("novelty_score"))
        experience_score = _as_float(experience.get("experience_score"))
        innovation_score = _as_float(innovation.get("innovation_score"))
        risk_score = _as_float(mechanics.get("risk_score"))
        resilience_score = _as_float(
            resilience.get("resilience_score", resilience.get("resilience_index", 0.0) * 100.0)
        )
        integrity_score = _as_float(integrity.get("integrity_score"))
        research_pressure = _as_float(research.get("research_pressure_index"))

        weight_total = self.novelty_weight + self.experience_weight + self.innovation_weight
        weighted_signal = 0.0
        if weight_total:
            weighted_signal = (
                novelty_score * self.novelty_weight
                + experience_score * self.experience_weight
                + innovation_score * self.innovation_weight
            ) / weight_total
        stability_bonus = min(12.0, (resilience_score * self.resilience_weight) / 1.5)
        integrity_bonus = min(10.0, integrity_score * 0.15)
        risk_penalty = min(30.0, risk_score * self.risk_penalty_factor)
        functionality_score = max(
            0.0,
            min(
                100.0,
                weighted_signal + stability_bonus + integrity_bonus - risk_penalty,
            ),
        )
        priority = _priority_from_score(functionality_score)

        risk_index = max(
            0.0,
            min(
                100.0,
                risk_score * 0.8
                + research_pressure * 0.35
                - resilience_score * 0.3
                - integrity_score * 0.2,
            ),
        )

        modernization_actions = _normalise_strings(
            modernization.get("modernization_actions", ())  # type: ignore[arg-type]
        )
        optimization_actions = _normalise_strings(
            optimization.get("optimization_actions", ())  # type: ignore[arg-type]
        )
        mitigation_tasks = _normalise_strings(mitigation.get("codebase_tasks", ()))
        remediation_actions = _normalise_strings(
            remediation.get("restoration_actions", ())  # type: ignore[arg-type]
        )
        functionality_tracks = _normalise_strings(
            (
                *mechanics.get("functionality_tracks", ()),
                *innovation.get("functionality_tracks", ()),
                *experience.get("functionality_enhancements", ()),
                *modernization_actions,
                *optimization_actions,
            )
        )

        experience_threads = _normalise_strings(experience.get("experience_threads", ()))
        mechanics_threads = _normalise_strings(mechanics.get("gameplay_threads", ()))
        functionality_threads = _normalise_strings(
            (
                *experience_threads,
                *mechanics_threads,
                *innovation.get("feature_threads", ()),
                *self_evolution.get("next_actions", ()),
            )
        )

        concept_briefs: list[dict[str, Any]] = []
        for concept in innovation.get("feature_concepts", ()):  # type: ignore[assignment]
            if not isinstance(concept, Mapping):
                continue
            track = str(concept.get("track") or concept.get("name") or "core-track")
            readiness = str(concept.get("readiness", priority))
            target = str(concept.get("target_module", "gameplay"))
            concept_briefs.append(
                {
                    "track": track,
                    "readiness": readiness,
                    "target_module": target,
                    "risk": round(risk_index, 2),
                }
            )

        if not concept_briefs:
            for track in functionality_tracks[:3]:
                concept_briefs.append(
                    {
                        "track": track,
                        "readiness": priority,
                        "target_module": "gameplay",
                        "risk": round(risk_index, 2),
                    }
                )

        mechanic_alignment = {
            "novelty_score": round(novelty_score, 2),
            "risk_score": round(risk_score, 2),
            "mechanic_archetypes": mechanics.get("mechanic_archetypes", ()),
        }
        experience_alignment = {
            "experience_score": round(experience_score, 2),
            "experience_arcs": experience.get("experience_arcs", ()),
        }
        innovation_alignment = {
            "innovation_score": round(innovation_score, 2),
            "backend_actions": innovation.get("backend_actions", ()),
        }

        holographic_hooks = mechanics.get("holographic_hooks", {})
        holographic_requirements = {
            "recommended_actions": _normalise_strings(
                (
                    *holographic_hooks.get("recommended_actions", ()),
                    *experience.get("holographic_choreography", {}).get("actions", ()),
                    *innovation.get("holographic_requirements", {}).get("recommended_actions", ()),
                    *transmission.get("phase_alignment", {}).get("actions", ()),
                )
            ),
            "stability": str(
                experience.get("holographic_choreography", {}).get("stability")
                or transmission.get("spectral_waveform", {}).get("stability")
                or holographic_hooks.get("stability", "steady")
            ),
            "efficiency_score": _as_float(
                network.get("holographic_diagnostics", {}).get("efficiency_score")
            ),
        }

        network_requirements = {
            "security_score": _as_float(
                security.get("security_score", network.get("network_security_score", 0.0))
            ),
            "threat_level": str(security.get("threat_level", "guarded")),
            "bandwidth_budget_mbps": _as_float(
                transmission.get("bandwidth_budget_mbps")
                or network.get("bandwidth_budget_mbps")
                or network_auto_dev.get("bandwidth_budget_mbps", 0.0)
            ),
            "upgrade_tracks": _normalise_strings(
                (
                    *network.get("upgrade_paths", ()),
                    *network_auto_dev.get("upgrade_tracks", ()),
                )
            ),
            "guardrail_severity": str(
                network.get("transmission_guardrails", {}).get("severity", "monitor")
            ),
        }

        research_implications = {
            "pressure_index": round(research_pressure, 2),
            "trend": str(research.get("trend_direction", research.get("trend", "steady"))),
            "utilization_percent": _as_float(
                research.get("raw_utilization_percent", research.get("latest_sample_percent", 0.0))
            ),
        }

        codebase_targets = _normalise_strings(
            entry.get("name")
            for entry in codebase.get("modernization_targets", ())  # type: ignore[arg-type]
            if isinstance(entry, Mapping)
        )
        codebase_focus = {
            "stability_outlook": codebase.get("stability_outlook", "steady"),
            "mitigation_plan": mitigation.get("codebase_tasks", ()),
            "remediation_progress": remediation.get("applied_fixes", ()),
            "modernization_targets": codebase_targets,
        }

        managerial_directives = _normalise_strings(
            (
                *guidance.get("managerial_threads", ()),
                *governance.get("oversight_actions", ()),
                *experience.get("backend_directives", ()),
                *innovation.get("backend_actions", ()),
                *mitigation_tasks,
                *remediation_actions,
                *self_evolution.get("next_actions", ()),
                *network_auto_dev.get("next_steps", ()),
            )
        )

        continuity_windows = _timeline_windows(continuity.get("timeline"))

        return {
            "priority": priority,
            "functionality_score": round(functionality_score, 2),
            "risk_index": round(risk_index, 2),
            "functionality_tracks": functionality_tracks,
            "functionality_threads": functionality_threads,
            "concept_briefs": tuple(concept_briefs),
            "mechanic_alignment": mechanic_alignment,
            "experience_alignment": experience_alignment,
            "innovation_alignment": innovation_alignment,
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "research_implications": research_implications,
            "codebase_alignment": codebase_focus,
            "managerial_directives": managerial_directives,
            "continuity_windows": continuity_windows,
        }

