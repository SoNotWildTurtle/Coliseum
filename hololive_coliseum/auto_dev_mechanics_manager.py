"""Synthesize mechanics expansion briefs for the auto-dev workflow."""

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


def _collect_from_mappings(
    values: Sequence[Mapping[str, Any]] | None,
    *keys: str,
) -> tuple[str, ...]:
    collected: list[str] = []
    for value in values or ():
        if not isinstance(value, Mapping):
            continue
        for key in keys:
            entry = str(value.get(key, "")).strip()
            if entry and entry not in collected:
                collected.append(entry)
    return tuple(collected)


def _threat_value(level: str) -> float:
    level = level.lower()
    mapping = {
        "critical": 95.0,
        "high": 80.0,
        "elevated": 65.0,
        "guarded": 45.0,
        "low": 30.0,
        "monitor": 20.0,
    }
    return mapping.get(level, 40.0)


def _priority_from_score(score: float) -> str:
    if score >= 75.0:
        return "critical"
    if score >= 55.0:
        return "high"
    if score >= 40.0:
        return "elevated"
    if score >= 25.0:
        return "medium"
    return "monitor"


@dataclass
class AutoDevMechanicsManager:
    """Blend encounter, research, and governance data into mechanics plans."""

    novelty_weight: float = 0.45
    cohesion_weight: float = 0.35
    risk_weight: float = 0.2

    def mechanics_blueprint(
        self,
        *,
        monsters: Sequence[Mapping[str, Any]] | None = None,
        quests: Sequence[Mapping[str, Any]] | None = None,
        mob_ai: Mapping[str, Any] | None = None,
        guidance: Mapping[str, Any] | None = None,
        research: Mapping[str, Any] | None = None,
        network: Mapping[str, Any] | None = None,
        security: Mapping[str, Any] | None = None,
        codebase: Mapping[str, Any] | None = None,
        modernization: Mapping[str, Any] | None = None,
        optimization: Mapping[str, Any] | None = None,
        transmission: Mapping[str, Any] | None = None,
        resilience: Mapping[str, Any] | None = None,
        mitigation: Mapping[str, Any] | None = None,
        remediation: Mapping[str, Any] | None = None,
        self_evolution: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a deterministic mechanics brief for new functionality."""

        monsters = monsters or ()
        quests = quests or ()
        mob_ai = mob_ai or {}
        guidance = guidance or {}
        research = research or {}
        network = network or {}
        security = security or {}
        codebase = codebase or {}
        modernization = modernization or {}
        optimization = optimization or {}
        transmission = transmission or {}
        resilience = resilience or {}
        mitigation = mitigation or {}
        remediation = remediation or {}
        self_evolution = self_evolution or {}

        hazards = _collect_from_mappings(monsters, "hazard")
        ai_escalation = str(
            (mob_ai.get("coordination_matrix", {}) or {}).get("escalation", "adaptive")
        )
        mechanic_archetypes = tuple(
            f"{hazard}:{ai_escalation}" for hazard in hazards if hazard
        ) or (f"general:{ai_escalation}",)

        quest_tags = set()
        quest_synergies: list[str] = []
        support_threads: list[str] = []
        for quest in quests:
            tags = quest.get("tags", ())  # type: ignore[arg-type]
            quest_tags.update(str(tag) for tag in tags if tag)
            trade_synergy = quest.get("trade_synergy", {})  # type: ignore[assignment]
            hazard = str(trade_synergy.get("hazard", ""))
            tempo = str(trade_synergy.get("tempo", ""))
            if hazard:
                quest_synergies.append(f"{hazard}:{tempo or 'balanced'}")
            support_threads.extend(
                str(thread)
                for thread in quest.get("support_threads", ())  # type: ignore[arg-type]
                if thread
            )

        ai_threads = tuple(mob_ai.get("evolution_threads", ()))
        gameplay_threads = _normalise_strings((*support_threads, *ai_threads))

        modernization_targets = modernization.get("targets", ())  # type: ignore[assignment]
        modernization_names = _collect_from_mappings(modernization_targets, "name")
        modernization_actions = _normalise_strings(
            modernization.get("modernization_actions", ())  # type: ignore[arg-type]
        )
        optimization_actions = _normalise_strings(
            optimization.get("optimization_actions", ())  # type: ignore[arg-type]
        )
        mitigation_tasks = _normalise_strings(
            mitigation.get("codebase_tasks", ())  # type: ignore[arg-type]
        )
        remediation_applied = remediation.get("applied_fixes", ())  # type: ignore[assignment]
        remediation_steps = _collect_from_mappings(remediation_applied, "task")
        self_evolution_actions = _normalise_strings(
            self_evolution.get("next_actions", ())  # type: ignore[arg-type]
        )

        functionality_tracks = _normalise_strings(
            (
                *modernization_names,
                *modernization_actions,
                *optimization_actions,
                *mitigation_tasks,
                *remediation_steps,
                *self_evolution_actions,
            )
        )

        holographic = transmission.get("spectral_waveform", {})  # type: ignore[assignment]
        holographic_hooks = {
            "recommended_actions": _normalise_strings(
                holographic.get("recommended_actions", ())  # type: ignore[arg-type]
            ),
            "density": _as_float(holographic.get("bandwidth_density")),
            "stability": str(holographic.get("stability", "stable")),
            "guardrail_status": str(
                network.get("transmission_guardrails", {}).get("status", "stable")
            ),
        }

        network_considerations = {
            "security_score": _as_float(security.get("security_score")),
            "threat_level": security.get("threat_level", "guarded"),
            "bandwidth_budget_mbps": _as_float(
                transmission.get("bandwidth_budget_mbps", 0.0)
            ),
            "efficiency_score": _as_float(
                network.get("holographic_diagnostics", {}).get("efficiency_score")
            ),
        }

        weakness_links = {
            "codebase": _normalise_strings(codebase.get("weakness_signals", ())),
            "security": _normalise_strings(
                security.get("network_security_actions", ())  # type: ignore[arg-type]
            ),
            "network": _normalise_strings(
                network.get("upgrade_backlog", {}).get("tasks", ())  # type: ignore[arg-type]
            ),
        }

        managerial_directives = _normalise_strings(
            (
                *guidance.get("managerial_threads", ()),  # type: ignore[arg-type]
                *resilience.get("resilience_actions", ()),  # type: ignore[arg-type]
                *self_evolution_actions,
            )
        )

        novelty_score = self._novelty_score(
            hazards,
            quest_tags,
            functionality_tracks,
            research,
            modernization,
        )
        cohesion_score = self._cohesion_score(
            guidance,
            resilience,
            optimization,
            network_considerations["efficiency_score"],
        )
        risk_score = self._risk_score(
            codebase,
            security,
            resilience,
        )
        priority = _priority_from_score(risk_score)

        return {
            "priority": priority,
            "novelty_score": round(novelty_score, 2),
            "cohesion_score": round(cohesion_score, 2),
            "risk_score": round(risk_score, 2),
            "mechanic_archetypes": mechanic_archetypes,
            "quest_synergies": _normalise_strings(quest_synergies),
            "skill_tags": tuple(sorted(quest_tags)),
            "gameplay_threads": gameplay_threads,
            "functionality_tracks": functionality_tracks,
            "network_considerations": network_considerations,
            "holographic_hooks": holographic_hooks,
            "managerial_directives": managerial_directives,
            "weakness_links": weakness_links,
        }

    def _novelty_score(
        self,
        hazards: Sequence[str],
        quest_tags: Sequence[str],
        functionality_tracks: Sequence[str],
        research: Mapping[str, Any],
        modernization: Mapping[str, Any],
    ) -> float:
        hazard_signal = min(1.0, len(hazards) / 6.0)
        tag_signal = min(1.0, len(quest_tags) / 8.0)
        track_signal = min(1.0, len(functionality_tracks) / 10.0)
        volatility = min(100.0, _as_float(research.get("volatility_percent")))
        trend = str(research.get("trend_direction", "stable")).lower()
        trend_bonus = 10.0 if trend == "increasing" else 0.0
        modernization_priority = str(modernization.get("priority", "monitor"))
        modernization_bonus = {
            "critical": 12.0,
            "high": 8.0,
            "medium": 5.0,
        }.get(modernization_priority, 2.0)
        return (
            hazard_signal * 35.0
            + tag_signal * 20.0
            + track_signal * 15.0
            + volatility * 0.2
            + trend_bonus
            + modernization_bonus
        )

    def _cohesion_score(
        self,
        guidance: Mapping[str, Any],
        resilience: Mapping[str, Any],
        optimization: Mapping[str, Any],
        efficiency_score: float,
    ) -> float:
        intelligence_score = _as_float(guidance.get("general_intelligence_score"))
        resilience_index = _as_float(resilience.get("resilience_index"))
        optimization_priority = str(optimization.get("priority", "monitor"))
        optimization_bonus = {
            "critical": 18.0,
            "high": 12.0,
            "medium": 8.0,
            "monitor": 4.0,
        }.get(optimization_priority, 6.0)
        base = intelligence_score * 0.4
        resilience_component = resilience_index * 100.0 * 0.3
        efficiency_component = min(100.0, max(0.0, efficiency_score * 100.0)) * 0.2
        return base + resilience_component + efficiency_component + optimization_bonus

    def _risk_score(
        self,
        codebase: Mapping[str, Any],
        security: Mapping[str, Any],
        resilience: Mapping[str, Any],
    ) -> float:
        debt_risk = _as_float(codebase.get("debt_risk_score")) * 22.0
        threat_level = _threat_value(str(security.get("threat_level", "guarded")))
        resilience_gap = max(0.0, 1.0 - _as_float(resilience.get("resilience_index")))
        resilience_component = resilience_gap * 100.0 * 0.6
        security_score = _as_float(security.get("security_score"))
        security_component = max(0.0, 70.0 - security_score) * 0.5
        return min(
            100.0,
            debt_risk * 0.4 + threat_level * 0.35 + resilience_component + security_component,
        )
