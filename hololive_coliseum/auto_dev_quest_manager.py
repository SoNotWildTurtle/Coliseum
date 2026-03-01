"""Generate MMO quests from trade skills and encounter plans."""

from __future__ import annotations

from typing import Any, Sequence


class AutoDevQuestManager:
    """Assemble quest hooks that react to trade skills and bosses."""

    def __init__(self, max_quests: int = 3) -> None:
        self.max_quests = max(1, int(max_quests))

    def generate_quests(
        self,
        trade_skills: Sequence[str] | None,
        *,
        boss_plan: dict[str, Any] | None = None,
        spawn_plan: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Return a list of lightweight quest descriptors."""

        skills = list(trade_skills or ()) or ["Mining", "Smithing", "Alchemy"]
        boss = boss_plan or {}
        quests: list[dict[str, Any]] = []
        for index, skill in enumerate(skills, start=1):
            objective = self._objective(skill, boss)
            spawn_dependency = self._spawn_dependency(spawn_plan, skill, index)
            synergy = self._trade_synergy(skill, spawn_plan, boss)
            support_threads = self._support_threads(spawn_plan, boss)
            quests.append(
                {
                    "title": f"{skill} support {index}",
                    "trade_skill": skill,
                    "objective": objective,
                    "reward": self._reward(spawn_plan),
                    "supports_boss": self._supports_boss(objective, boss),
                    "difficulty": self._difficulty(spawn_plan, index),
                    "tags": self._tags(skill, boss),
                    "spawn_dependency": spawn_dependency,
                    "trade_synergy": synergy,
                    "support_threads": support_threads,
                }
            )
            if len(quests) >= self.max_quests:
                break
        if boss.get("name"):
            quests.append(
                {
                    "title": f"Challenge {boss['name']}",
                    "trade_skill": "Combat",
                    "objective": "Defeat the boss after preparing specialised gear",
                    "reward": "Legendary cache",
                    "supports_boss": True,
                    "difficulty": "legendary",
                    "tags": ("boss", "combat", "elite"),
                    "spawn_dependency": self._spawn_dependency(spawn_plan, "Combat", 0),
                    "trade_synergy": self._trade_synergy("Combat", spawn_plan, boss),
                    "support_threads": self._support_threads(spawn_plan, boss),
                }
            )
        return quests

    def _objective(self, skill: str, boss: dict[str, Any]) -> str:
        hazard = boss.get("hazard", "the arena")
        return f"Craft a countermeasure with {skill} to weaken {hazard} threats"

    def _reward(self, spawn_plan: dict[str, Any] | None) -> str:
        danger = float((spawn_plan or {}).get("danger", 1.0))
        if danger >= 2.0:
            return "Epic materials"
        if danger >= 1.2:
            return "Rare crafting reagents"
        return "Standard supplies"

    def _supports_boss(self, objective: str, boss: dict[str, Any]) -> bool:
        if not boss.get("name"):
            return False
        return boss["name"].lower() in objective.lower()

    def _difficulty(self, spawn_plan: dict[str, Any] | None, index: int) -> str:
        danger = float((spawn_plan or {}).get("danger", 1.0))
        tier = danger + index * 0.1
        if tier >= 2.2:
            return "heroic"
        if tier >= 1.5:
            return "veteran"
        if tier >= 1.1:
            return "standard"
        return "intro"

    def _tags(self, skill: str, boss: dict[str, Any]) -> tuple[str, ...]:
        tags = {skill.lower(), "trade"}
        if boss.get("hazard"):
            tags.add(str(boss["hazard"]).lower())
        if skill.lower() in {"combat", "defense", "shielding"}:
            tags.add("combat")
        return tuple(sorted(tags))

    def _spawn_dependency(
        self,
        spawn_plan: dict[str, Any] | None,
        skill: str,
        index: int,
    ) -> dict[str, Any]:
        """Return quest dependency information linking to spawn planning."""

        if not spawn_plan:
            return {"lane": "central", "wave": 1}
        lanes = list(spawn_plan.get("lanes", ())) or ["central"]
        lane = lanes[index % len(lanes)]
        curve = list(spawn_plan.get("reinforcement_curve", ()))
        wave = min(len(curve), index) or 1
        return {"lane": lane, "wave": wave, "tempo": spawn_plan.get("tempo", "balanced"), "skill": skill}

    def _trade_synergy(
        self,
        skill: str,
        spawn_plan: dict[str, Any] | None,
        boss: dict[str, Any],
    ) -> dict[str, Any]:
        """Return a trade synergy descriptor for quest planning."""

        hazard = boss.get("hazard", "general")
        synergy = str(hazard)
        tempo = str((spawn_plan or {}).get("tempo", "balanced"))
        formation = str((spawn_plan or {}).get("formation", "staggered"))
        return {
            "hazard": synergy,
            "formation": formation,
            "tempo": tempo,
            "skill_focus": skill,
        }

    def _support_threads(
        self,
        spawn_plan: dict[str, Any] | None,
        boss: dict[str, Any],
    ) -> tuple[str, ...]:
        """Return deterministic support threads binding quests to encounters."""

        threads: set[str] = set()
        if spawn_plan:
            for thread in spawn_plan.get("group_threads", ()):  # type: ignore[arg-type]
                if thread:
                    threads.add(str(thread))
        hazard = boss.get("hazard")
        if hazard:
            threads.add(f"boss:{hazard}")
        return tuple(sorted(threads))
