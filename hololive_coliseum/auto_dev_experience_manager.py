"""Experience design synthesis for the Coliseum auto-dev pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalise_strings(values: Sequence[Any] | None) -> tuple[str, ...]:
    result: list[str] = []
    for value in values or ():
        text = str(value).strip()
        if text and text not in result:
            result.append(text)
    return tuple(result)


def _priority_value(priority: str) -> float:
    mapping = {
        "critical": 92.0,
        "high": 82.0,
        "accelerate": 85.0,
        "stabilise": 72.0,
        "medium": 68.0,
        "sustain": 68.0,
        "explore": 62.0,
        "refine": 60.0,
        "monitor": 52.0,
        "observe": 48.0,
    }
    return mapping.get(priority.strip().lower(), 55.0)


def _threat_penalty(threat: str) -> float:
    mapping = {
        "critical": 18.0,
        "high": 14.0,
        "elevated": 10.0,
        "guarded": 6.0,
        "low": 4.0,
        "monitor": 2.0,
    }
    return mapping.get(threat.strip().lower(), 6.0)


def _experience_priority(score: float) -> str:
    if score >= 78.0:
        return "amplify"
    if score >= 58.0:
        return "sustain"
    if score >= 38.0:
        return "refine"
    return "observe"


def _window_strings(timeline: Sequence[Mapping[str, Any]] | None) -> tuple[str, ...]:
    windows: list[str] = []
    for entry in timeline or ():
        window = str(entry.get("window", "")).strip()
        if window:
            windows.append(window)
    return tuple(windows)


def _concepts(concepts: Sequence[Mapping[str, Any]] | None) -> tuple[Mapping[str, Any], ...]:
    collected: list[Mapping[str, Any]] = []
    for concept in concepts or ():
        if isinstance(concept, Mapping):
            collected.append(concept)
    return tuple(collected)


@dataclass
class AutoDevExperienceManager:
    """Blend mechanics, innovation, and governance data into experience arcs."""

    novelty_weight: float = 0.4
    cohesion_weight: float = 0.35
    systems_weight: float = 0.25
    risk_weight: float = 0.3

    def experience_brief(
        self,
        *,
        mechanics: Mapping[str, Any] | None = None,
        innovation: Mapping[str, Any] | None = None,
        guidance: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        continuity: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
        network_auto_dev: Mapping[str, Any] | None = None,
        self_evolution: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return an experience plan that extends functionality creation."""

        mechanics = mechanics or {}
        innovation = innovation or {}
        guidance = guidance or {}
        research = research or {}
        network = network or {}
        transmission = transmission or {}
        security = security or {}
        resilience = resilience or {}
        modernization = modernization or {}
        optimization = optimization or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        continuity = continuity or {}
        governance = governance or {}
        network_auto_dev = network_auto_dev or {}
        self_evolution = self_evolution or {}

        novelty_score = _as_float(mechanics.get("novelty_score"))
        innovation_score = _as_float(innovation.get("innovation_score"))
        cohesion_score = _as_float(mechanics.get("cohesion_score"))
        risk_score = _as_float(mechanics.get("risk_score"))
        modernization_priority = _priority_value(str(modernization.get("priority", "monitor")))
        optimization_priority = _priority_value(str(optimization.get("priority", "monitor")))
        resilience_index = _as_float(resilience.get("resilience_index")) * 100.0
        security_score = _as_float(security.get("security_score"))
        efficiency_score = _as_float(
            (network.get("holographic_diagnostics", {}) or {}).get("efficiency_score"),
        )
        continuity_index = _as_float(continuity.get("continuity_index")) * 100.0

        novelty_component = min(100.0, (novelty_score + innovation_score) / 2.0)
        novelty_component *= self.novelty_weight
        cohesion_component = min(100.0, cohesion_score) * self.cohesion_weight
        systems_signal = (
            modernization_priority
            + optimization_priority
            + resilience_index
            + security_score
            + efficiency_score
            + continuity_index
        ) / 6.0
        systems_component = systems_signal * self.systems_weight
        threat_penalty = _threat_penalty(str(security.get("threat_level", "guarded")))
        risk_penalty = min(35.0, risk_score * self.risk_weight + threat_penalty)
        experience_score = max(
            0.0,
            min(
                100.0,
                round(
                    novelty_component
                    + cohesion_component
                    + systems_component
                    - risk_penalty,
                    2,
                ),
            ),
        )
        priority = _experience_priority(experience_score)

        gameplay_threads = _normalise_strings(mechanics.get("gameplay_threads"))
        functionality_tracks = _normalise_strings(mechanics.get("functionality_tracks"))
        feature_concepts = _concepts(innovation.get("feature_concepts"))
        experience_arcs: list[dict[str, Any]] = []
        if not gameplay_threads:
            gameplay_threads = ("core-loop",)
        if not functionality_tracks:
            functionality_tracks = ("core-systems",)
        for index, thread in enumerate(gameplay_threads):
            concept = (
                feature_concepts[index % len(feature_concepts)]
                if feature_concepts
                else {}
            )
            experience_arcs.append(
                {
                    "thread": thread,
                    "track": functionality_tracks[index % len(functionality_tracks)],
                    "readiness": concept.get("readiness", priority),
                    "target_module": concept.get("target_module", "core-platform"),
                }
            )

        continuity_windows = _window_strings(continuity.get("timeline"))
        functionality_enhancements = _normalise_strings(
            (
                *innovation.get("backend_actions", ()),
                *mechanics.get("managerial_directives", ()),
                *modernization.get("modernization_actions", ()),
                *optimization.get("optimization_actions", ()),
                *mitigation.get("codebase_tasks", ()),
            )
        )

        network_requirements = innovation.get("network_requirements", {})
        transmission_waveform = transmission.get("spectral_waveform", {})
        holographic_hooks = mechanics.get("holographic_hooks", {})
        phase_alignment = (transmission.get("phase_alignment", {}) or {}).get("actions", ())
        continuity_actions = (
            (continuity.get("holographic_transmission_actions", {}) or {}).get("actions", ())
        )
        holographic_actions = _normalise_strings(
            (
                *holographic_hooks.get("recommended_actions", ()),
                *transmission_waveform.get("recommended_actions", ()),
                *phase_alignment,
                *continuity_actions,
            )
        )

        backend_directives = _normalise_strings(
            (
                *guidance.get("managerial_threads", ()),
                *governance.get("oversight_actions", ()),
                *self_evolution.get("next_actions", ()),
                *remediation.get("restoration_actions", ()),
                *network_auto_dev.get("next_steps", ()),
            )
        )

        risk_summary = innovation.get("risk_summary", {})
        research_synergy = innovation.get("research_synergy", {})
        research_implications = {
            "trend": research_synergy.get("trend") or research.get("trend_direction", "stable"),
            "pressure_index": _as_float(research.get("research_pressure_index")),
            "utilization_percent": _as_float(research.get("raw_utilization_percent")),
            "competitive_utilization": _as_float(research.get("competitive_utilization_percent")),
        }

        network_security = network_requirements.get("security_score", security_score)
        network_threat = network_requirements.get(
            "threat_level", security.get("threat_level", "guarded")
        )
        network_blueprint = {
            "security_score": round(_as_float(network_security), 2),
            "threat_level": str(network_threat),
            "bandwidth_budget_mbps": _as_float(
                network_requirements.get("bandwidth_budget_mbps")
                or transmission.get("bandwidth_budget_mbps"),
            ),
            "upgrade_tracks": _normalise_strings(
                (
                    *network.get("upgrade_paths", ()),
                    *network_auto_dev.get("upgrade_tracks", ()),
                )
            ),
            "resilience_grade": resilience.get("grade", "vigilant"),
        }

        holographic_choreography = {
            "actions": holographic_actions,
            "stability": str(
                transmission_waveform.get(
                    "stability", holographic_hooks.get("stability", "stable")
                )
            ),
            "density": _as_float(transmission_waveform.get("bandwidth_density")),
            "continuity_windows": continuity_windows,
        }

        continuity_support = {
            "focus": continuity.get("continuity_focus", "monitor"),
            "windows": continuity_windows,
            "timeline_length": len(continuity_windows),
        }

        governance_alignment = {
            "state": governance.get("state", "guided"),
            "oversight_actions": governance.get("oversight_actions", ()),
        }

        risk_profile = {
            "mechanics_risk": round(_as_float(risk_summary.get("mechanics_risk", risk_score)), 2),
            "codebase_instability": _as_float(risk_summary.get("codebase_instability")),
            "debt_risk_score": _as_float(risk_summary.get("debt_risk_score")),
            "network_threat_level": risk_summary.get("network_threat_level")
            or security.get("threat_level", "guarded"),
        }

        experience_threads = _normalise_strings(
            (
                *gameplay_threads,
                *mechanics.get("mechanic_archetypes", ()),
            )
        )

        return {
            "priority": priority,
            "experience_score": experience_score,
            "experience_arcs": tuple(experience_arcs),
            "functionality_enhancements": functionality_enhancements,
            "network_blueprint": network_blueprint,
            "holographic_choreography": holographic_choreography,
            "backend_directives": backend_directives,
            "risk_profile": risk_profile,
            "research_implications": research_implications,
            "experience_focus_windows": continuity_windows,
            "governance_alignment": governance_alignment,
            "continuity_support": continuity_support,
            "experience_threads": experience_threads,
        }
