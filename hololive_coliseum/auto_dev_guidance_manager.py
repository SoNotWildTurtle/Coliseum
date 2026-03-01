"""Provide managerial guidance that links all auto-dev insights together."""

from __future__ import annotations

from statistics import mean
from typing import Any, Iterable, Mapping, Sequence


def _average_threat(monsters: Sequence[dict[str, Any]] | None) -> float:
    if not monsters:
        return 0.0
    values = [float(monster.get("threat", 0.0)) for monster in monsters]
    return mean(values)


def _spawn_pressure(plan: dict[str, Any] | None) -> float:
    if not plan:
        return 1.0
    return float(plan.get("danger", 1.0))


def _processing_percent(research: dict[str, Any] | None) -> float:
    if not research:
        return 0.0
    latest = research.get("latest_sample_percent")
    if latest is not None:
        return float(latest)
    return float(research.get("utilization_percent", 0.0))


class AutoDevGuidanceManager:
    """Fuse encounter, quest and research data into executive guidance."""

    def __init__(self, threat_weight: float = 0.5, processing_weight: float = 0.2) -> None:
        self.threat_weight = float(threat_weight)
        self.processing_weight = float(processing_weight)

    def compose_guidance(
        self,
        *,
        monsters: Sequence[dict[str, Any]] | None = None,
        spawn_plan: dict[str, Any] | None = None,
        mob_ai: dict[str, Any] | None = None,
        boss_plan: dict[str, Any] | None = None,
        quests: Sequence[dict[str, Any]] | None = None,
        research: dict[str, Any] | None = None,
        network: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return an aggregated guidance brief for MMO planners."""

        threat = _average_threat(monsters)
        spawn_danger = _spawn_pressure(spawn_plan)
        utilisation = _processing_percent(research)
        network_signal = self._network_signal(network)
        risk_index = self._risk(threat, spawn_danger, utilisation, network_signal)
        directives = tuple(self._directives(monsters, mob_ai, boss_plan, quests))
        priority = self._priority(risk_index)
        insight_chain = self._insight_chain(mob_ai, quests, boss_plan)
        intelligence_rating = self._intelligence_rating(
            risk_index,
            network_signal,
            quests,
        )
        managerial_threads = self._managerial_threads(
            monsters,
            spawn_plan,
            mob_ai,
            boss_plan,
            quests,
            research,
            network,
        )
        evolution_vector = self._self_evolution_vector(risk_index, research, mob_ai, network)
        intelligence_score = self._intelligence_score(
            risk_index,
            network_signal,
            quests,
            research,
            network,
        )
        backend_vector = self._backend_guidance_vector(
            research,
            network,
            directives,
            risk_index,
        )
        governance_outlook = self._governance_outlook(intelligence_score, priority)
        intelligence_breakdown = self._intelligence_breakdown(
            risk_index,
            network_signal,
            utilisation,
            research,
            quests,
            network,
        )
        backend_alignment = self._backend_alignment_score(
            risk_index,
            network_signal,
            utilisation,
            research,
            network,
        )
        guidance_backbone = self._guidance_backbone(
            managerial_threads,
            directives,
            intelligence_breakdown,
        )
        return {
            "risk_index": round(risk_index, 2),
            "priority": priority,
            "directives": directives,
            "processing_utilization_percent": round(utilisation, 2),
            "insight_chain": insight_chain,
            "network_signal": round(network_signal, 2),
            "general_intelligence_rating": intelligence_rating,
            "managerial_threads": managerial_threads,
            "self_evolution_vector": evolution_vector,
            "general_intelligence_score": intelligence_score,
            "backend_guidance_vector": backend_vector,
            "governance_outlook": governance_outlook,
            "intelligence_breakdown": intelligence_breakdown,
            "backend_alignment_score": backend_alignment,
            "guidance_backbone": guidance_backbone,
        }

    def _risk(
        self,
        threat: float,
        spawn_danger: float,
        utilisation: float,
        network_signal: float,
    ) -> float:
        weighted_threat = threat * self.threat_weight
        weighted_spawn = spawn_danger * (1.0 - self.threat_weight - self.processing_weight)
        weighted_processing = (utilisation / 100.0) * self.processing_weight
        weighted_network = network_signal * 0.15
        return max(0.0, weighted_threat + weighted_spawn + weighted_processing + weighted_network)

    def _directives(
        self,
        monsters: Sequence[dict[str, Any]] | None,
        mob_ai: dict[str, Any] | None,
        boss_plan: dict[str, Any] | None,
        quests: Sequence[dict[str, Any]] | None,
    ) -> Iterable[str]:
        if monsters:
            hazard_names = {monster.get("hazard", "general") for monster in monsters}
            yield f"Prioritise counters for {', '.join(sorted(hazard_names))} threats"
        if mob_ai and mob_ai.get("directives"):
            yield "Review AI coordination windows with encounter design"
        if boss_plan:
            boss_name = boss_plan.get("name", "the boss")
            yield f"Stage rehearsal fights for {boss_name}"
        if quests:
            yield "Align quest rewards with current crafting shortages"

    def _priority(self, risk_index: float) -> str:
        if risk_index >= 1.6:
            return "critical"
        if risk_index >= 1.1:
            return "high"
        if risk_index >= 0.7:
            return "medium"
        return "low"

    def _insight_chain(
        self,
        mob_ai: dict[str, Any] | None,
        quests: Sequence[dict[str, Any]] | None,
        boss_plan: dict[str, Any] | None,
    ) -> list[str]:
        chain: list[str] = []
        if mob_ai and mob_ai.get("directives"):
            chain.append("Mob AI emphasises coordinated responses to spawn surges")
        if quests:
            chain.append("Quest hooks reinforce trade skills tied to current hazards")
        if boss_plan:
            chain.append(
                f"Boss focus '{boss_plan.get('hazard', 'general')}' anchors the iteration roadmap"
            )
        return chain

    def _network_signal(self, network: dict[str, Any] | None) -> float:
        if not network:
            return 0.0
        health = network.get("network_health") or {}
        score = float(health.get("score", 0.0))
        resilience = network.get("resilience_matrix") or {}
        resilience_score = float(resilience.get("score", 0.0))
        return min(1.0, (score + resilience_score) / 200.0)

    def _intelligence_rating(
        self,
        risk_index: float,
        network_signal: float,
        quests: Sequence[dict[str, Any]] | None,
    ) -> str:
        quest_support = len(quests or ())
        modifier = network_signal * 2.5 + quest_support * 0.1
        score = risk_index + modifier
        if score >= 2.2:
            return "directive"
        if score >= 1.4:
            return "strategic"
        if score >= 0.9:
            return "tactical"
        return "observational"

    def _managerial_threads(
        self,
        monsters: Sequence[dict[str, Any]] | None,
        spawn_plan: dict[str, Any] | None,
        mob_ai: dict[str, Any] | None,
        boss_plan: dict[str, Any] | None,
        quests: Sequence[dict[str, Any]] | None,
        research: dict[str, Any] | None,
        network: dict[str, Any] | None,
    ) -> tuple[str, ...]:
        threads: list[str] = []
        if monsters:
            hazards = {monster.get("hazard", "general") for monster in monsters}
            threads.append(f"Hazard stewardship: {', '.join(sorted(hazards))}")
        if spawn_plan:
            threads.append(f"Spawn tempo: {spawn_plan.get('tempo', 'balanced')}")
        if mob_ai and mob_ai.get("coordination_matrix"):
            cadence = mob_ai["coordination_matrix"].get("coordination_cadence", 0.0)
            threads.append(f"AI cadence: {cadence}s cadence")
        if boss_plan:
            threads.append(f"Boss directive: {boss_plan.get('name', 'Unknown')}")
        if quests:
            threads.append(f"Quest pipeline: {len(quests)} active")
        if research:
            threads.append(
                f"Research load: {research.get('raw_percentage', research.get('utilization_percent', 0.0))}%"
            )
        if network:
            health = network.get("network_health", {}).get("status", "stable")
            threads.append(f"Network posture: {health}")
        return tuple(threads)

    def _self_evolution_vector(
        self,
        risk_index: float,
        research: dict[str, Any] | None,
        mob_ai: dict[str, Any] | None,
        network: dict[str, Any] | None,
    ) -> dict[str, Any]:
        research_percent = 0.0
        if research:
            research_percent = float(
                research.get("raw_percentage")
                or research.get("raw_utilization_percent")
                or research.get("utilization_percent")
                or 0.0
            )
        pressure_index = float(research.get("research_pressure_index", 0.0)) if research else 0.0
        evolution_threads = tuple(mob_ai.get("evolution_threads", ())) if mob_ai else ()
        network_score = 0.0
        if network:
            network_health = network.get("network_health", {})
            network_score = float(network_health.get("score", 0.0)) / 100.0
        intensity = min(1.0, (risk_index + research_percent / 100.0 + network_score) / 2.5)
        outlook = "stabilise"
        if intensity >= 0.75:
            outlook = "accelerate"
        elif intensity >= 0.45:
            outlook = "expand"
        return {
            "intensity": round(intensity, 2),
            "outlook": outlook,
            "evolution_threads": evolution_threads,
            "pressure_index": round(pressure_index, 2),
        }

    def _intelligence_score(
        self,
        risk_index: float,
        network_signal: float,
        quests: Sequence[dict[str, Any]] | None,
        research: dict[str, Any] | None,
        network: dict[str, Any] | None,
    ) -> float:
        quest_factor = min(25.0, len(quests or ()) * 6.0)
        research_pressure = float(research.get("research_pressure_index", 0.0)) if research else 0.0
        network_health = 0.0
        if network:
            network_health = float(network.get("network_health", {}).get("score", 0.0))
        score = (
            risk_index * 22.0
            + network_signal * 35.0
            + quest_factor
            + research_pressure * 0.4
            + network_health * 0.2
        )
        return round(max(0.0, min(100.0, score)), 2)

    def _backend_guidance_vector(
        self,
        research: dict[str, Any] | None,
        network: dict[str, Any] | None,
        directives: Iterable[str],
        risk_index: float,
    ) -> tuple[str, ...]:
        vector: list[str] = []
        if research:
            weaknesses = tuple(research.get("weakness_signals", ()))
            if weaknesses:
                vector.append(f"Research focus: {weaknesses[0]}")
            pressure = float(research.get("research_pressure_index", 0.0))
            vector.append(f"Research pressure index: {pressure}")
        if network:
            security = network.get("security_auto_dev", {})
            vector.append(
                "Network directive: " + security.get("directive", "stabilise")
            )
            security_score = network.get("network_security_score", 0.0)
            vector.append(f"Network security score: {security_score}")
        directive_list = list(dict.fromkeys(directives))
        if directive_list:
            vector.append(f"Encounter directives: {directive_list[0]}")
        vector.append(f"Risk index: {round(risk_index, 2)}")
        return tuple(vector)

    def _governance_outlook(self, intelligence_score: float, priority: str) -> str:
        if intelligence_score >= 80.0:
            return "guidance-autonomous"
        if intelligence_score >= 55.0:
            return "guidance-directed"
        if priority in {"high", "critical"}:
            return "guidance-oversight"
        return "guidance-monitor"

    def _intelligence_breakdown(
        self,
        risk_index: float,
        network_signal: float,
        utilisation: float,
        research: Mapping[str, Any] | None,
        quests: Sequence[dict[str, Any]] | None,
        network: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        research_pressure = float(research.get("research_pressure_index", 0.0)) if research else 0.0
        quest_weight = min(22.0, len(quests or ()) * 4.0)
        network_health = 0.0
        if network:
            network_health = float(network.get("network_health", {}).get("score", 0.0))
        components = {
            "risk": round(risk_index * 20.0, 2),
            "network": round(network_signal * 40.0, 2),
            "processing": round(utilisation, 2),
            "research": round(research_pressure, 2),
            "quests": round(quest_weight, 2),
            "network_health": round(network_health * 0.3, 2),
        }
        total = sum(components.values()) or 1.0
        distribution = {
            key: round(value / total, 2) for key, value in components.items()
        }
        return {
            "weights": components,
            "distribution": distribution,
            "total": round(total, 2),
        }

    def _backend_alignment_score(
        self,
        risk_index: float,
        network_signal: float,
        utilisation: float,
        research: Mapping[str, Any] | None,
        network: Mapping[str, Any] | None,
    ) -> float:
        pressure = float(research.get("research_pressure_index", 0.0)) if research else 0.0
        security_score = 0.0
        if network:
            security_score = float(network.get("network_security_score", 0.0))
        score = 55.0
        score += min(25.0, network_signal * 35.0)
        score += min(15.0, security_score * 0.15)
        score -= max(0.0, utilisation - 55.0) * 0.4
        score -= max(0.0, pressure - 60.0) * 0.35
        score -= risk_index * 6.5
        return round(max(0.0, min(100.0, score)), 2)

    def _guidance_backbone(
        self,
        threads: Sequence[str],
        directives: Sequence[str],
        breakdown: Mapping[str, Any],
    ) -> tuple[str, ...]:
        summary: list[str] = []
        weights = breakdown.get("distribution", {}) if breakdown else {}
        if weights:
            sorted_weights = sorted(
                weights.items(), key=lambda item: item[1], reverse=True
            )
            if sorted_weights:
                label, weight = sorted_weights[0]
                summary.append(f"Primary emphasis: {label} ({weight:.2f})")
        summary.extend(list(threads[:2]))
        if directives:
            summary.append(f"Directive focus: {directives[0]}")
        return tuple(dict.fromkeys(summary))
