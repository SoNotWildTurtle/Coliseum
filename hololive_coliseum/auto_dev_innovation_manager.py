"""Innovation planning for the Coliseum auto-dev pipeline."""

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


def _alignment_score(alignment: str) -> float:
    alignment = alignment.lower().strip()
    if alignment in {"upgrade-ready", "accelerated"}:
        return 24.0
    if alignment in {"balanced", "steady"}:
        return 16.0
    if alignment in {"requires-hardening", "lagging"}:
        return 11.0
    return 13.0


def _priority_from_score(score: float) -> str:
    if score >= 72.0:
        return "accelerate"
    if score >= 48.0:
        return "stabilise"
    if score >= 32.0:
        return "explore"
    return "monitor"


@dataclass
class AutoDevInnovationManager:
    """Synthesize functionality blueprints from mechanics and modernization data."""

    novelty_weight: float = 0.55
    modernization_weight: float = 0.25
    risk_weight: float = 0.2

    def innovation_brief(
        self,
        *,
        guidance: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Blend mechanics output with modernization goals for new functionality."""

        guidance = guidance or {}
        mechanics = mechanics or {}
        codebase = codebase or {}
        modernization = modernization or {}
        optimization = optimization or {}
        network = network or {}
        transmission = transmission or {}
        security = security or {}
        research = research or {}
        resilience = resilience or {}
        mitigation = mitigation or {}
        remediation = remediation or {}

        novelty = _as_float(mechanics.get("novelty_score"))
        modernization_alignment = modernization.get("network_alignment", {})
        alignment = _alignment_score(str(modernization_alignment.get("alignment", "balanced")))
        risk = _as_float(mechanics.get("risk_score"))
        security_score = _as_float(
            security.get("security_score"),
            _as_float(network.get("network_security_score")),
        )
        risk_penalty = min(22.0, risk * self.risk_weight)
        research_pressure = _as_float(research.get("research_pressure_index"))
        research_bonus = min(15.0, research_pressure * 0.35)
        novelty_component = novelty * self.novelty_weight
        modernization_component = alignment * self.modernization_weight
        security_bonus = 6.0 if security_score >= 68.0 else -4.0
        score = novelty_component + modernization_component + research_bonus + security_bonus
        score -= risk_penalty
        score = max(0.0, min(100.0, round(score, 2)))
        priority = _priority_from_score(score)

        functionality_tracks = _normalise_strings(
            mechanics.get("functionality_tracks")
        )
        gameplay_threads = _normalise_strings(mechanics.get("gameplay_threads"))
        mechanic_archetypes = _normalise_strings(mechanics.get("mechanic_archetypes"))
        modernization_targets: Sequence[Mapping[str, Any]] = modernization.get(
            "targets",
            (),
        )  # type: ignore[assignment]
        target_names = _normalise_strings(
            tuple(entry.get("name") for entry in modernization_targets)
        )
        optimization_actions = _normalise_strings(
            optimization.get("optimization_actions", ())
        )
        modernization_actions = _normalise_strings(
            modernization.get("modernization_actions", ())
        )
        guidance_threads = _normalise_strings(guidance.get("managerial_threads", ()))
        remediation_progress: Sequence[Mapping[str, Any]] = remediation.get(
            "codebase_progress",
            (),
        )  # type: ignore[assignment]
        addressed = _normalise_strings(
            entry.get("name")
            for entry in remediation_progress
            if entry.get("addressed")
        )

        feature_concepts: list[dict[str, Any]] = []
        if not functionality_tracks:
            functionality_tracks = ("core-systems",)
        for index, track in enumerate(functionality_tracks):
            concept = {
                "track": track,
                "target_module": target_names[index % len(target_names)]
                if target_names
                else "core-platform",
                "innovation_thread": gameplay_threads[index % len(gameplay_threads)]
                if gameplay_threads
                else "adaptive-loop",
                "readiness": priority,
            }
            feature_concepts.append(concept)

        network_requirements = {
            "security_score": round(security_score, 2),
            "threat_level": str(security.get("threat_level", "guarded")),
            "bandwidth_budget_mbps": _as_float(
                transmission.get("bandwidth_budget_mbps"),
            ),
            "upgrade_tracks": _normalise_strings(network.get("upgrade_paths", ())),
            "resilience_grade": resilience.get("grade", "vigilant"),
        }

        spectral_waveform = transmission.get("spectral_waveform", {})
        holographic_requirements = {
            "recommended_actions": _normalise_strings(
                spectral_waveform.get("recommended_actions", ())
            ),
            "stability": str(spectral_waveform.get("stability", "stable")),
            "density": _as_float(spectral_waveform.get("bandwidth_density")),
            "phase_actions": _normalise_strings(
                transmission.get("phase_alignment", {}).get("actions", ())
            ),
        }

        risk_summary = {
            "mechanics_risk": round(risk, 2),
            "codebase_instability": _as_float(codebase.get("instability_index")),
            "debt_risk_score": _as_float(codebase.get("debt_risk_score")),
            "network_threat_level": security.get("threat_level", "guarded"),
        }

        backend_source = (
            *guidance_threads,
            *modernization_actions,
            *optimization_actions,
            *mitigation.get("codebase_tasks", ()),
        )
        backend_actions = _normalise_strings(backend_source)

        research_synergy = {
            "trend": research.get("trend_direction", "stable"),
            "pressure_index": round(research_pressure, 2),
            "utilization_percent": _as_float(
                research.get("raw_utilization_percent"),
                _as_float(research.get("latest_sample_percent")),
            ),
            "competitive_utilization": _as_float(
                research.get("competitive_utilization_percent"),
            ),
        }

        return {
            "priority": priority,
            "innovation_score": score,
            "feature_concepts": tuple(feature_concepts),
            "gameplay_inspirations": mechanic_archetypes or gameplay_threads,
            "functionality_tracks": functionality_tracks,
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "risk_summary": risk_summary,
            "backend_actions": backend_actions,
            "research_synergy": research_synergy,
            "addressed_modules": addressed,
        }
