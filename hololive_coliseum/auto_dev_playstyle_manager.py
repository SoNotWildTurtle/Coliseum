"""Derive playstyle archetypes from functionality and dynamics telemetry."""

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
    if score >= 82.0:
        return "amplify"
    if score >= 66.0:
        return "accelerate"
    if score >= 52.0:
        return "stabilise"
    if score >= 38.0:
        return "refine"
    return "observe"


def _archetype_name(base: str, focus: str, index: int) -> str:
    base = base.strip() or f"archetype-{index + 1}"
    focus = focus.strip() or "core"
    return f"{base}-{focus}".lower().replace(" ", "-")


@dataclass
class AutoDevPlaystyleManager:
    """Blend functionality, experience, and dynamics data into playstyle briefs."""

    synergy_weight: float = 0.4
    functionality_weight: float = 0.35
    experience_weight: float = 0.25
    innovation_weight: float = 0.2
    resilience_weight: float = 0.18
    stability_weight: float = 0.16
    risk_penalty_factor: float = 0.35

    def playstyle_brief(
        self,
        *,
        functionality: Mapping[str, Any] | None = None,
        mechanics: Mapping[str, Any] | None = None,
        innovation: Mapping[str, Any] | None = None,
        experience: Mapping[str, Any] | None = None,
        dynamics: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        network_auto_dev: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        integrity: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
        governance: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic playstyle briefing for downstream automation."""

        functionality = functionality or {}
        mechanics = mechanics or {}
        innovation = innovation or {}
        experience = experience or {}
        dynamics = dynamics or {}
        research = research or {}
        network = network or {}
        network_auto_dev = network_auto_dev or {}
        security = security or {}
        transmission = transmission or {}
        modernization = modernization or {}
        optimization = optimization or {}
        integrity = integrity or {}
        resilience = resilience or {}
        governance = governance or {}

        functionality_score = _as_float(functionality.get("functionality_score"))
        dynamics_synergy = _as_float(dynamics.get("synergy_score"))
        experience_score = _as_float(experience.get("experience_score"))
        innovation_score = _as_float(innovation.get("innovation_score"))
        resilience_score = _as_float(resilience.get("resilience_score"))
        integrity_score = _as_float(integrity.get("integrity_score"))
        security_score = _as_float(security.get("security_score"))
        network_security = _as_float(network.get("network_security_score"))

        weight_total = (
            self.synergy_weight
            + self.functionality_weight
            + self.experience_weight
            + self.innovation_weight
        ) or 1e-6
        weighted_signal = (
            dynamics_synergy * self.synergy_weight
            + functionality_score * self.functionality_weight
            + experience_score * self.experience_weight
            + innovation_score * self.innovation_weight
        ) / weight_total

        stability_bonus = (
            resilience_score * self.resilience_weight
            + integrity_score * self.stability_weight
            + security_score * 0.12
            + network_security * 0.12
        )
        stability_bonus = min(18.0, stability_bonus * 0.45)

        functionality_risk = _as_float(functionality.get("risk_index"))
        dynamics_risk = _as_float(
            (dynamics.get("risk_profile") or {}).get("combined_risk")
        )
        research_pressure = _as_float(research.get("research_pressure_index"))
        risk_penalty = min(
            28.0,
            (functionality_risk * 0.55 + dynamics_risk * 0.45)
            * self.risk_penalty_factor
            + research_pressure * 0.25,
        )

        playstyle_score = max(
            0.0,
            min(100.0, weighted_signal + stability_bonus - risk_penalty),
        )
        cohesion_score = round((playstyle_score + dynamics_synergy) / 2.0, 2)
        novelty_score = _as_float(mechanics.get("novelty_score"))
        priority = _priority(playstyle_score)

        mechanic_archetypes = _normalise_strings(
            mechanics.get("mechanic_archetypes", ())
        )
        experience_arcs = experience.get("experience_arcs", ())
        functionality_concepts = functionality.get("concept_briefs", ())
        tracks = _normalise_strings(functionality.get("functionality_tracks", ()))

        archetypes: list[dict[str, Any]] = []
        max_len = max(
            len(mechanic_archetypes),
            len(experience_arcs),
            len(functionality_concepts),
        )
        for index in range(min(3, max_len or 3)):
            mechanic = mechanic_archetypes[index % len(mechanic_archetypes)] if mechanic_archetypes else "core"
            concept = functionality_concepts[index % len(functionality_concepts)] if functionality_concepts else {}
            concept_track = (
                concept.get("track")
                if isinstance(concept, Mapping)
                else str(concept)
            ) or tracks[index % len(tracks)] if tracks else "core"
            experience_arc = experience_arcs[index % len(experience_arcs)] if experience_arcs else {}
            arc_name = (
                experience_arc.get("name")
                if isinstance(experience_arc, Mapping)
                else str(experience_arc)
            ) or "experience"
            archetypes.append(
                {
                    "name": _archetype_name(str(mechanic), str(concept_track), index),
                    "experience": arc_name,
                    "focus": str(concept_track),
                    "risk": round(functionality_risk, 2),
                }
            )

        if not archetypes:
            archetypes.append(
                {
                    "name": "core-playstyle",
                    "experience": "experience",
                    "focus": "core",
                    "risk": round(functionality_risk, 2),
                }
            )

        tuning_actions = _normalise_strings(
            (
                *functionality.get("managerial_directives", ()),
                *experience.get("backend_directives", ()),
                *dynamics.get("backend_actions", ()),
                *modernization.get("modernization_actions", ()),
                *optimization.get("optimization_actions", ()),
                *network_auto_dev.get("next_steps", ()),
            )
        )

        network_requirements = {
            "security_score": round(
                max(
                    _as_float(
                        (dynamics.get("network_requirements") or {}).get(
                            "security_score"
                        )
                    ),
                    _as_float(
                        (functionality.get("network_requirements") or {}).get(
                            "security_score"
                        )
                    ),
                    network_security,
                ),
                2,
            ),
            "bandwidth_mbps": round(
                max(
                    _as_float(
                        (dynamics.get("network_requirements") or {}).get(
                            "bandwidth_mbps"
                        )
                    ),
                    _as_float(
                        (experience.get("network_blueprint") or {}).get(
                            "bandwidth_budget_mbps"
                        )
                    ),
                    _as_float(network_auto_dev.get("bandwidth_budget_mbps")),
                ),
                2,
            ),
            "upgrade_tracks": _normalise_strings(
                (
                    *((dynamics.get("network_requirements") or {}).get(
                        "upgrade_tracks", ()
                    )),
                    *((functionality.get("network_requirements") or {}).get(
                        "upgrade_tracks", ()
                    )),
                    *network_auto_dev.get("upgrade_tracks", ()),
                )
            ),
            "threat_level": security.get("threat_level", "guarded"),
        }

        holographic_requirements = {
            "recommended_actions": _normalise_strings(
                (
                    *((dynamics.get("holographic_requirements") or {}).get(
                        "recommended_actions", ()
                    )),
                    *((functionality.get("holographic_requirements") or {}).get(
                        "recommended_actions", ()
                    )),
                    *((experience.get("holographic_choreography") or {}).get(
                        "actions", ()
                    )),
                    *((transmission.get("spectral_waveform") or {}).get(
                        "recommended_actions", ()
                    )),
                    *integrity.get("holographic_actions", ()),
                )
            ),
            "phase_target": (transmission.get("phase_alignment") or {}).get("target"),
            "stability": (experience.get("holographic_choreography") or {}).get(
                "stability",
                (dynamics.get("holographic_requirements") or {}).get(
                    "stability",
                    "steady",
                ),
            ),
        }

        managerial_directives = _normalise_strings(
            (
                *tuning_actions,
                *((dynamics.get("managerial_directives") or ())),
                *governance.get("oversight_actions", ()),
            )
        )

        research_implications = {
            "trend": research.get("trend_direction", "stable"),
            "pressure_index": round(research_pressure, 2),
            "utilization_percent": _as_float(
                research.get("raw_utilization_percent")
                or research.get("latest_sample_percent")
            ),
        }

        return {
            "priority": priority,
            "playstyle_score": round(playstyle_score, 2),
            "cohesion_score": cohesion_score,
            "novelty_score": round(novelty_score, 2),
            "risk_index": round(functionality_risk, 2),
            "combined_risk": round(dynamics_risk or functionality_risk, 2),
            "tracks": tracks,
            "archetypes": tuple(archetypes),
            "tuning_actions": tuning_actions,
            "network_requirements": network_requirements,
            "holographic_requirements": holographic_requirements,
            "managerial_directives": managerial_directives,
            "research_implications": research_implications,
        }

