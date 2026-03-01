"""Synthesize auto-dev signals into actionable evolution plans."""

from __future__ import annotations

from statistics import mean
from typing import Any, Iterable, Sequence


def _threat_summary(monsters: Sequence[dict[str, Any]] | None) -> tuple[str, float]:
    if not monsters:
        return ("low", 0.0)
    threats = [float(monster.get("threat", 0.0)) for monster in monsters]
    avg = mean(threats) if threats else 0.0
    if avg >= 1.5:
        tier = "extreme"
    elif avg >= 1.0:
        tier = "high"
    elif avg >= 0.6:
        tier = "medium"
    else:
        tier = "low"
    return (tier, avg)


def _spawn_pressure(plan: dict[str, Any] | None) -> str:
    if not plan:
        return "steady"
    danger = float(plan.get("danger", 1.0))
    if danger >= 1.5:
        return "volatile"
    if danger >= 1.1:
        return "rising"
    return "steady"


class AutoDevEvolutionManager:
    """Create evolution roadmaps from auto-dev guidance and telemetry."""

    def __init__(self, horizon: int = 3) -> None:
        self.horizon = max(1, int(horizon))

    def evolution_brief(
        self,
        *,
        guidance: dict[str, Any] | None = None,
        roadmap: dict[str, Any] | None = None,
        focus: dict[str, Any] | None = None,
        research: dict[str, Any] | None = None,
        monsters: Sequence[dict[str, Any]] | None = None,
        spawn_plan: dict[str, Any] | None = None,
        quests: Sequence[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Return a managerial evolution plan pulling together all signals."""

        threat_tier, threat_index = _threat_summary(monsters)
        spawn_state = _spawn_pressure(spawn_plan)
        utilisation = self._utilisation_percent(guidance, research)
        objectives = tuple(self._objectives(guidance, roadmap, focus, quests))
        resource_focus = self._resource_focus(utilisation, spawn_state, quests)
        confidence = self._confidence(guidance, roadmap, focus, research, monsters, spawn_plan, quests)
        summary = self._summary(guidance, threat_tier, spawn_state)
        return {
            "summary": summary,
            "horizon": self.horizon,
            "threat_tier": threat_tier,
            "average_threat_index": round(threat_index, 2),
            "spawn_state": spawn_state,
            "next_objectives": objectives,
            "resource_focus": resource_focus,
            "confidence": confidence,
            "processing_utilization_percent": utilisation,
        }

    def _utilisation_percent(
        self, guidance: dict[str, Any] | None, research: dict[str, Any] | None
    ) -> float:
        if guidance and "processing_utilization_percent" in guidance:
            return float(guidance["processing_utilization_percent"])
        if research:
            latest = research.get("latest_sample_percent")
            if latest is not None:
                return float(latest)
            return float(research.get("utilization_percent", 0.0))
        return 0.0

    def _objectives(
        self,
        guidance: dict[str, Any] | None,
        roadmap: dict[str, Any] | None,
        focus: dict[str, Any] | None,
        quests: Sequence[dict[str, Any]] | None,
    ) -> Iterable[str]:
        if guidance and guidance.get("directives"):
            for directive in guidance["directives"]:
                yield directive
        if roadmap and roadmap.get("priority_actions"):
            yield roadmap["priority_actions"][0]
        if focus and focus.get("top_focus"):
            yield f"Align teams with {focus['top_focus']} initiatives"
        if quests:
            primary = quests[0]
            yield f"Promote trade skill: {primary.get('trade_skill', 'General Crafting')}"
        if guidance is None and roadmap is None and focus is None and not quests:
            yield "Collect additional telemetry to refine objectives"

    def _resource_focus(
        self,
        utilisation: float,
        spawn_state: str,
        quests: Sequence[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        quest_push = len(quests) if quests else 0
        return {
            "research_percent": round(utilisation, 2),
            "encounter_emphasis": spawn_state,
            "quest_development": "active" if quest_push else "pending",
        }

    def _confidence(
        self,
        guidance: dict[str, Any] | None,
        roadmap: dict[str, Any] | None,
        focus: dict[str, Any] | None,
        research: dict[str, Any] | None,
        monsters: Sequence[dict[str, Any]] | None,
        spawn_plan: dict[str, Any] | None,
        quests: Sequence[dict[str, Any]] | None,
    ) -> float:
        signals = [guidance, roadmap, focus, research, monsters, spawn_plan, quests]
        available = sum(1 for signal in signals if signal)
        return round(available / len(signals), 2)

    def _summary(
        self,
        guidance: dict[str, Any] | None,
        threat_tier: str,
        spawn_state: str,
    ) -> str:
        if guidance and guidance.get("priority"):
            priority = guidance["priority"]
        else:
            priority = "medium" if threat_tier in {"high", "extreme"} else "low"
        return (
            f"Priority {priority} evolution: threats are {threat_tier} and spawn pressure is {spawn_state}."
        )
