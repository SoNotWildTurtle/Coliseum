"""Generate monster rosters for MMO auto-development planning."""

from __future__ import annotations

from collections import Counter
from typing import Any, Sequence


def _normalise(text: object) -> str:
    value = str(text or "").strip().lower()
    return value or "general"


class AutoDevMonsterManager:
    """Create monster templates from hazards and trade skill data."""

    def __init__(self, max_monsters: int = 4) -> None:
        self.max_monsters = max(1, int(max_monsters))

    def generate_monsters(
        self,
        *,
        focus: dict[str, Any] | None = None,
        scenarios: Sequence[dict[str, Any]] | None = None,
        trade_skills: Sequence[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Return themed monster entries derived from current insights."""

        hazard_candidates = []
        if focus and focus.get("top_focus"):
            hazard_candidates.append(focus["top_focus"])
        for scenario in scenarios or ():
            hazard_candidates.append(scenario.get("hazard"))
        hazards = [_normalise(hazard) for hazard in hazard_candidates if hazard is not None]
        if not hazards:
            hazards = ["general"]
        hazard_counts = Counter(hazards)
        skills = list(trade_skills or ()) or ["Crafting", "Mining", "Gathering"]
        monsters: list[dict[str, Any]] = []
        for index, (hazard, count) in enumerate(
            hazard_counts.most_common(self.max_monsters),
            start=1,
        ):
            weakness = self._select_trade_skill(hazard, skills)
            ai_focus = self._ai_focus(hazard, weakness)
            spawn_synergy = self._spawn_synergy(count, hazard)
            group_role = self._group_role(index, hazard, count)
            blueprint = self._creation_blueprint(hazard, weakness, spawn_synergy, group_role)
            ai_path = self._ai_development_path(ai_focus, blueprint)
            monster = {
                "name": f"{hazard.title()} Vanguard",
                "hazard": hazard,
                "role": "elite" if hazard == hazards[0] else "support",
                "group_role": group_role,
                "threat": round(0.6 + 0.1 * count, 2),
                "weakness": weakness,
                "recommended_counter": f"Deploy {weakness} specialists",
                "ai_focus": ai_focus,
                "ai_development_path": ai_path,
                "spawn_synergy": spawn_synergy,
                "creation_blueprint": blueprint,
            }
            monsters.append(monster)
        return monsters

    def _select_trade_skill(self, hazard: str, trade_skills: Sequence[str]) -> str:
        if not trade_skills:
            return "General Training"
        index = sum(ord(char) for char in hazard) % len(trade_skills)
        return trade_skills[index]

    def _ai_focus(self, hazard: str, weakness: str) -> str:
        """Return a deterministic AI focus for the given hazard."""

        combined = sum(ord(char) for char in hazard + weakness)
        focus_cycle = ("aggressive", "adaptive", "tactical", "coordinated")
        return focus_cycle[combined % len(focus_cycle)]

    def _spawn_synergy(self, count: int, hazard: str) -> str:
        """Return a spawn synergy label derived from roster pressure."""

        pressure = count + (sum(ord(char) for char in hazard) % 3)
        if pressure >= 6:
            return "overwhelming"
        if pressure >= 4:
            return "reinforcement"
        return "skirmish"

    def _group_role(self, index: int, hazard: str, count: int) -> str:
        """Return a role tag for group spawning heuristics."""

        band = (index + count + len(hazard)) % 4
        if band == 0:
            return "vanguard"
        if band == 1:
            return "controller"
        if band == 2:
            return "support"
        return "harrier"

    def _creation_blueprint(
        self,
        hazard: str,
        weakness: str,
        synergy: str,
        group_role: str,
    ) -> dict[str, Any]:
        """Return a deterministic creation blueprint for the monster."""

        hazard_key = sum(ord(char) for char in hazard)
        mutation_index = hazard_key % 5
        mutation_track = (
            "volatile",
            "resilient",
            "adaptive",
            "spectral",
            "primordial",
        )[mutation_index]
        tradecraft = f"Channel {weakness} artisans to stabilise cores"
        spawn_thread = f"{synergy} {group_role}"
        return {
            "mutation_track": mutation_track,
            "tradecraft": tradecraft,
            "spawn_thread": spawn_thread,
            "signature_attack": f"{hazard.title()} pulse",
        }

    def _ai_development_path(
        self,
        ai_focus: str,
        blueprint: dict[str, Any],
    ) -> dict[str, Any]:
        """Return a staged AI development outline for the monster."""

        stages = [
            "baseline reactions",
            f"{ai_focus} counter-loops",
            f"sync with {blueprint['spawn_thread']}",
        ]
        return {
            "stages": tuple(stages),
            "reinforcement_ready": "overwhelming" in blueprint["spawn_thread"],
        }
