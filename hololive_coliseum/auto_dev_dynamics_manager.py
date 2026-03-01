"""Assess cross-domain system dynamics for the auto-dev workflow."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import chain
from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _normalise_strings(values: Sequence[Any] | None) -> tuple[str, ...]:
    seen: list[str] = []
    for value in values or ():
        text = str(value).strip()
        if text and text not in seen:
            seen.append(text)
    return tuple(seen)


def _unique_from_sources(*sources: Sequence[Any] | None) -> tuple[str, ...]:
    sequences: list[Sequence[Any]] = [seq for seq in sources if seq]
    if not sequences:
        return ()
    flattened = chain.from_iterable(sequences)
    return _normalise_strings(flattened)  # type: ignore[arg-type]


def _clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def _priority(score: float, risk: float) -> str:
    if score >= 80.0 and risk <= 35.0:
        return "amplify"
    if score >= 65.0 and risk <= 45.0:
        return "accelerate"
    if score >= 50.0:
        return "stabilise"
    if score >= 35.0:
        return "refine"
    return "observe"


def _threat_modifier(level: str) -> float:
    severity = {
        "fortified": 0.85,
        "guarded": 0.95,
        "elevated": 1.1,
        "at-risk": 1.35,
    }
    return severity.get(level.lower(), 1.0)


@dataclass
class AutoDevDynamicsManager:
    """Blend functionality, mechanics, and network data into systems dynamics."""

    functionality_weight: float = 0.4
    mechanics_weight: float = 0.3
    innovation_weight: float = 0.2
    experience_weight: float = 0.1
    resilience_weight: float = 0.25
    integrity_weight: float = 0.2
    security_weight: float = 0.2
    network_weight: float = 0.15
    risk_penalty_factor: float = 0.45

    def dynamics_brief(
        self,
        *,
        guidance: Mapping[str, Any] | None = None,
        functionality: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        innovation: Mapping[str, Any] | None = None,
        experience: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        integrity: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        network_auto_dev: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
        continuity: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        self_evolution: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return deterministic dynamics telemetry for downstream planning."""

        guidance = guidance or {}
        functionality = functionality or {}
        mechanics = mechanics or {}
        innovation = innovation or {}
        experience = experience or {}
        modernization = modernization or {}
        optimization = optimization or {}
        integrity = integrity or {}
        resilience = resilience or {}
        security = security or {}
        network = network or {}
        network_auto_dev = network_auto_dev or {}
        transmission = transmission or {}
        research = research or {}
        governance = governance or {}
        continuity = continuity or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        codebase = codebase or {}
        self_evolution = self_evolution or {}

        functionality_score = _as_float(functionality.get("functionality_score"))
        mechanics_novelty = _as_float(mechanics.get("novelty_score"))
        innovation_score = _as_float(innovation.get("innovation_score"))
        experience_score = _as_float(experience.get("experience_score"))
        resilience_score = _as_float(resilience.get("resilience_score"))
        integrity_score = _as_float(integrity.get("integrity_score"))
        security_score = _as_float(security.get("security_score"))
        network_security = _as_float(network.get("network_security_score"))
        threat_level = str(security.get("threat_level", "guarded"))

        weight_total = (
            self.functionality_weight
            + self.mechanics_weight
            + self.innovation_weight
            + self.experience_weight
        )
        weighted_signal = 0.0
        if weight_total:
            weighted_signal = (
                functionality_score * self.functionality_weight
                + mechanics_novelty * self.mechanics_weight
                + innovation_score * self.innovation_weight
                + experience_score * self.experience_weight
            ) / weight_total

        stabiliser_total = (
            self.resilience_weight
            + self.integrity_weight
            + self.network_weight
            + self.security_weight
        ) or 1e-6
        stability_bonus = (
            resilience_score * self.resilience_weight
            + integrity_score * self.integrity_weight
            + network_security * self.network_weight
            + security_score * self.security_weight
        ) / stabiliser_total
        stability_bonus = min(18.0, stability_bonus * 0.35)

        risk_index = _as_float(functionality.get("risk_index"))
        mechanics_risk = _as_float(mechanics.get("risk_score"))
        research_pressure = _as_float(research.get("research_pressure_index"))
        risk_penalty = min(
            32.0,
            (risk_index + mechanics_risk) * self.risk_penalty_factor
            + research_pressure * 0.25,
        )
        threat_penalty = (_threat_modifier(threat_level) - 1.0) * 18.0

        synergy_score = _clamp(weighted_signal + stability_bonus - risk_penalty - threat_penalty)
        combined_risk = _clamp(
            (risk_index * 0.55)
            + (mechanics_risk * 0.35)
            + (research_pressure * 0.25)
            + (100.0 - network_security) * 0.15,
        )
        priority = _priority(synergy_score, combined_risk)

        functionality_tracks = _normalise_strings(functionality.get("functionality_tracks", ()))
        mechanics_tracks = _normalise_strings(mechanics.get("functionality_tracks", ()))
        innovation_tracks = _normalise_strings(innovation.get("functionality_tracks", ()))
        experience_threads = _normalise_strings(experience.get("experience_threads", ()))
        gameplay_threads = _normalise_strings(mechanics.get("gameplay_threads", ()))
        functionality_threads = _normalise_strings(functionality.get("functionality_threads", ()))

        systems_tracks = _unique_from_sources(
            functionality_tracks,
            mechanics_tracks,
            innovation_tracks,
        )
        systems_threads = _unique_from_sources(
            gameplay_threads,
            experience_threads,
            functionality_threads,
        )

        functionality_requirements = _as_mapping(functionality.get("network_requirements"))
        innovation_requirements = _as_mapping(innovation.get("network_requirements"))
        experience_requirements = _as_mapping(experience.get("network_blueprint"))
        network_upgrade = _as_mapping(network_auto_dev)
        transmission_guardrails = _as_mapping(transmission.get("guardrails"))

        network_requirements = {
            "security_score": round(
                max(
                    _as_float(functionality_requirements.get("security_score")),
                    _as_float(innovation_requirements.get("security_score")),
                    _as_float(experience_requirements.get("security_score")),
                    _as_float(network_upgrade.get("readiness_score")),
                    network_security,
                ),
                2,
            ),
            "bandwidth_mbps": round(
                max(
                    _as_float(functionality_requirements.get("bandwidth_mbps")),
                    _as_float(innovation_requirements.get("bandwidth_mbps")),
                    _as_float(experience_requirements.get("bandwidth_mbps")),
                    _as_float(transmission.get("bandwidth_budget_mbps")),
                    _as_float(network_upgrade.get("bandwidth_budget_mbps")),
                ),
                2,
            ),
            "upgrade_tracks": _unique_from_sources(
                functionality_requirements.get("upgrade_tracks", ()),
                innovation_requirements.get("upgrade_tracks", ()),
                network_upgrade.get("upgrade_tracks", ()),
                modernization.get("modernization_actions", ()),
            ),
            "guardrail_severity": transmission_guardrails.get(
                "severity",
                network.get("transmission_guardrails", {}).get("severity", "monitor"),
            ),
        }

        mechanics_hooks = _as_mapping(mechanics.get("holographic_hooks"))
        functionality_holo = _as_mapping(functionality.get("holographic_requirements"))
        innovation_holo = _as_mapping(innovation.get("holographic_requirements"))
        experience_holo = _as_mapping(experience.get("holographic_choreography"))
        integrity_actions = _normalise_strings(integrity.get("holographic_actions", ()))
        remediation_adjustments = _normalise_strings(
            remediation.get("holographic_adjustments", ())
        )

        holographic_requirements = {
            "recommended_actions": _unique_from_sources(
                mechanics_hooks.get("recommended_actions", ()),
                functionality_holo.get("recommended_actions", ()),
                innovation_holo.get("recommended_actions", ()),
                experience_holo.get("actions", ()),
                remediation_adjustments,
                integrity_actions,
            ),
            "phase_target": transmission.get("phase_alignment", {}).get("target"),
            "efficiency_score": round(
                max(
                    _as_float(mechanics_hooks.get("efficiency_score")),
                    _as_float(functionality_holo.get("efficiency_score")),
                    _as_float(innovation_holo.get("efficiency_score")),
                    _as_float(experience_holo.get("efficiency_score")),
                    _as_float(
                        transmission.get("spectral_waveform", {}).get("efficiency_score")
                    ),
                ),
                2,
            ),
            "stability": mechanics_hooks.get(
                "stability",
                functionality_holo.get(
                    "stability", experience_holo.get("stability", "steady")
                ),
            ),
        }

        modernization_targets = _normalise_strings(
            (
                target.get("name")
                for target in modernization.get("modernization_targets", ())
                if isinstance(target, Mapping)
            )
        )
        mitigation_tasks = _normalise_strings(mitigation.get("codebase_tasks", ()))
        remediation_progress = _normalise_strings(
            entry.get("name")
            for entry in remediation.get("codebase_progress", ())
            if isinstance(entry, Mapping) and entry.get("addressed")
        )
        continuity_windows = _normalise_strings(
            entry.get("window")
            for entry in continuity.get("timeline", ())
            if isinstance(entry, Mapping)
        )

        backend_actions = _unique_from_sources(
            functionality.get("managerial_directives", ()),
            innovation.get("backend_actions", ()),
            experience.get("backend_directives", ()),
            mitigation_tasks,
            modernization.get("modernization_actions", ()),
            optimization.get("optimization_actions", ()),
        )

        managerial_directives = _unique_from_sources(
            backend_actions,
            guidance.get("managerial_threads", ()),
            governance.get("oversight_actions", ()),
            self_evolution.get("next_actions", ()),
        )

        return {
            "priority": priority,
            "synergy_score": round(synergy_score, 2),
            "systems_tracks": systems_tracks,
            "systems_threads": systems_threads,
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "backend_actions": backend_actions,
            "managerial_directives": managerial_directives,
            "risk_profile": {
                "combined_risk": round(combined_risk, 2),
                "functionality_risk": round(risk_index, 2),
                "mechanics_risk": round(mechanics_risk, 2),
                "research_pressure": round(research_pressure, 2),
                "security_threat_level": threat_level,
            },
            "stability_alignment": {
                "resilience_score": round(resilience_score, 2),
                "integrity_score": round(integrity_score, 2),
                "security_score": round(security_score, 2),
                "network_security_score": round(network_security, 2),
            },
            "codebase_alignment": {
                "modernization_targets": modernization_targets,
                "mitigation_tasks": mitigation_tasks,
                "addressed_modules": remediation_progress,
                "debt_outlook": codebase.get("stability_outlook", "steady"),
            },
            "continuity_windows": continuity_windows,
            "upgrade_actions": _unique_from_sources(
                network_auto_dev.get("next_steps", ()),
                modernization.get("modernization_actions", ()),
                optimization.get("optimization_actions", ()),
            ),
        }
