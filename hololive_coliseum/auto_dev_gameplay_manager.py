"""Synthesize functionality, dynamics, and playstyle data into gameplay loops."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalise_strings(values: Sequence[Any] | None) -> tuple[str, ...]:
    items: list[str] = []
    for value in values or ():
        text = str(value).strip()
        if text and text not in items:
            items.append(text)
    return tuple(items)


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


def _archetype_label(data: Any, index: int) -> str:
    if isinstance(data, Mapping):
        label = str(
            data.get("name")
            or data.get("focus")
            or data.get("experience")
            or "playstyle"
        )
    else:
        label = str(data)
    label = label.strip() or "playstyle"
    return f"{label.lower().replace(' ', '-')}-{index + 1}"[:48]


@dataclass
class AutoDevGameplayManager:
    """Blend functionality, dynamics, and playstyle data into gameplay loops."""

    functionality_weight: float = 0.34
    dynamics_weight: float = 0.28
    playstyle_weight: float = 0.22
    mechanics_weight: float = 0.16
    innovation_weight: float = 0.12
    experience_weight: float = 0.18
    resilience_bonus_factor: float = 0.18
    risk_penalty_factor: float = 0.36

    def gameplay_blueprint(
        self,
        *,
        functionality: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        innovation: Mapping[str, Any] | None = None,
        experience: Mapping[str, Any] | None = None,
        dynamics: Mapping[str, Any] | None = None,
        playstyle: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
        integrity: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        network_auto_dev: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic gameplay loop blueprint for downstream orchestration."""

        functionality = functionality or {}
        mechanics = mechanics or {}
        innovation = innovation or {}
        experience = experience or {}
        dynamics = dynamics or {}
        playstyle = playstyle or {}
        resilience = resilience or {}
        integrity = integrity or {}
        security = security or {}
        network = network or {}
        network_auto_dev = network_auto_dev or {}
        transmission = transmission or {}
        research = research or {}
        modernization = modernization or {}
        optimization = optimization or {}
        codebase = codebase or {}
        governance = governance or {}

        functionality_score = _as_float(functionality.get("functionality_score"))
        dynamics_synergy = _as_float(dynamics.get("synergy_score"))
        playstyle_score = _as_float(playstyle.get("playstyle_score"))
        mechanics_novelty = _as_float(mechanics.get("novelty_score"))
        innovation_score = _as_float(innovation.get("innovation_score"))
        experience_score = _as_float(experience.get("experience_score"))
        resilience_score = _as_float(resilience.get("resilience_score"))
        integrity_score = _as_float(integrity.get("integrity_score"))
        security_score = _as_float(security.get("security_score"))
        network_security = _as_float(network.get("network_security_score"))

        weight_total = (
            self.functionality_weight
            + self.dynamics_weight
            + self.playstyle_weight
            + self.mechanics_weight
            + self.innovation_weight
            + self.experience_weight
        ) or 1e-6
        weighted_signal = (
            functionality_score * self.functionality_weight
            + dynamics_synergy * self.dynamics_weight
            + playstyle_score * self.playstyle_weight
            + mechanics_novelty * self.mechanics_weight
            + innovation_score * self.innovation_weight
            + experience_score * self.experience_weight
        ) / weight_total

        stability_bonus = (
            resilience_score * self.resilience_bonus_factor
            + integrity_score * 0.16
            + max(security_score, network_security) * 0.12
        )
        stability_bonus = min(20.0, stability_bonus)

        functionality_risk = _as_float(functionality.get("risk_index"))
        dynamics_risk = _as_float((dynamics.get("risk_profile") or {}).get("combined_risk"))
        playstyle_risk = _as_float(playstyle.get("risk_index"))
        research_pressure = _as_float(research.get("research_pressure_index"))

        risk_penalty = min(
            30.0,
            (
                functionality_risk * 0.45
                + dynamics_risk * 0.3
                + playstyle_risk * 0.25
            )
            * self.risk_penalty_factor
            + research_pressure * 0.2,
        )

        gameplay_score = max(
            0.0,
            min(100.0, weighted_signal + stability_bonus - risk_penalty),
        )
        priority = _priority(gameplay_score)

        functionality_tracks = _normalise_strings(
            functionality.get("functionality_tracks", ())
        )
        dynamics_tracks = _normalise_strings(dynamics.get("systems_tracks", ()))
        playstyle_tracks = _normalise_strings(playstyle.get("tracks", ()))
        mechanics_threads = _normalise_strings(mechanics.get("gameplay_threads", ()))
        experience_threads = _normalise_strings(experience.get("experience_threads", ()))

        archetypes = playstyle.get("archetypes", ())
        loops: list[dict[str, Any]] = []
        span = max(
            len(functionality_tracks),
            len(dynamics_tracks),
            len(playstyle_tracks),
            len(mechanics_threads),
            len(experience_threads),
            len(archetypes),
        )
        span = max(1, min(3, span))
        for index in range(span):
            track = (
                functionality_tracks[index % len(functionality_tracks)]
                if functionality_tracks
                else f"loop-track-{index + 1}"
            )
            dynamic = (
                dynamics_tracks[index % len(dynamics_tracks)]
                if dynamics_tracks
                else "core-dynamic"
            )
            mechanic_thread = (
                mechanics_threads[index % len(mechanics_threads)]
                if mechanics_threads
                else "core-thread"
            )
            experience_thread = (
                experience_threads[index % len(experience_threads)]
                if experience_threads
                else "core-experience"
            )
            playstyle_label = (
                playstyle_tracks[index % len(playstyle_tracks)]
                if playstyle_tracks
                else _archetype_label(archetypes[index % len(archetypes)] if archetypes else "playstyle", index)
            )
            loops.append(
                {
                    "name": _archetype_label(archetypes[index % len(archetypes)] if archetypes else playstyle_label, index),
                    "focus_track": track,
                    "systems_dynamic": dynamic,
                    "playstyle": playstyle_label,
                    "mechanic_thread": mechanic_thread,
                    "experience_thread": experience_thread,
                }
            )

        managerial_actions = _normalise_strings(
            (
                *functionality.get("managerial_directives", ()),
                *dynamics.get("managerial_directives", ()),
                *playstyle.get("managerial_directives", ()),
                *modernization.get("modernization_actions", ()),
                *optimization.get("optimization_actions", ()),
                *governance.get("oversight_actions", ()),
            )
        )

        network_requirements = {
            "security_score": round(
                max(
                    _as_float(
                        (dynamics.get("network_requirements") or {}).get("security_score")
                    ),
                    _as_float(
                        (playstyle.get("network_requirements") or {}).get("security_score")
                    ),
                    security_score,
                    network_security,
                ),
                2,
            ),
            "bandwidth_mbps": round(
                max(
                    _as_float(
                        (experience.get("network_blueprint") or {}).get("bandwidth_mbps")
                    ),
                    _as_float(
                        (dynamics.get("network_requirements") or {}).get("bandwidth_mbps")
                    ),
                    _as_float(
                        (playstyle.get("network_requirements") or {}).get("bandwidth_mbps")
                    ),
                ),
                2,
            ),
            "upgrade_tracks": _normalise_strings(
                (
                    *(dynamics.get("upgrade_actions") or ()),
                    *(playstyle.get("tuning_actions") or ()),
                    *network_auto_dev.get("upgrade_tracks", ()),
                )
            ),
        }

        holographic_requirements = {
            "recommended_actions": _normalise_strings(
                (
                    *(dynamics.get("holographic_requirements") or {}).get(
                        "recommended_actions", ()
                    ),
                    *(playstyle.get("holographic_requirements") or {}).get(
                        "recommended_actions", ()
                    ),
                    *(functionality.get("holographic_requirements") or {}).get(
                        "recommended_actions", ()
                    ),
                    *(transmission.get("spectral_waveform") or {}).get(
                        "recommended_actions", ()
                    ),
                )
            ),
            "phase_target": _as_float(
                (transmission.get("phase_alignment") or {}).get("target"),
                default=0.0,
            ),
        }

        research_implications = {
            "pressure_index": round(research_pressure, 2),
            "utilization_percent": _as_float(
                research.get("raw_utilization_percent"),
                default=0.0,
            ),
            "trend": str(research.get("trend_direction", "stable")),
        }

        codebase_alignment = {
            "modernization_targets": tuple(
                codebase.get("modernization_targets", ())
            ),
            "weakness_signals": tuple(codebase.get("weakness_signals", ()))[:3],
            "recommended_fixes": tuple(codebase.get("mitigation_plan", ()))[:3],
        }

        risk_profile = {
            "functionality": round(functionality_risk, 2),
            "dynamics": round(dynamics_risk, 2),
            "playstyle": round(playstyle_risk, 2),
            "research_pressure": round(research_pressure, 2),
        }

        return {
            "priority": priority,
            "gameplay_score": round(gameplay_score, 2),
            "loops": tuple(loops),
            "managerial_actions": managerial_actions,
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "research_implications": research_implications,
            "codebase_alignment": codebase_alignment,
            "risk_profile": risk_profile,
            "functionality_tracks": functionality_tracks,
            "dynamics_tracks": dynamics_tracks,
            "playstyle_tracks": playstyle_tracks,
            "mechanic_threads": mechanics_threads,
            "experience_threads": experience_threads,
        }

