"""Determine boss encounters for the auto-development pipeline."""

from __future__ import annotations

from typing import Any, Sequence


class AutoDevBossManager:
    """Select thematic bosses based on monster and roadmap data."""

    def select_boss(
        self,
        monsters: Sequence[dict[str, Any]] | None,
        *,
        roadmap: dict[str, Any] | None = None,
        projection: dict[str, Any] | None = None,
        spawn_plan: dict[str, Any] | None = None,
        trade_skills: Sequence[str] | None = None,
    ) -> dict[str, Any]:
        """Return a boss plan that mirrors the current regional focus."""

        monsters = list(monsters or [])
        if not monsters:
            return {}
        focus_hazard = None
        if roadmap and roadmap.get("focus"):
            focus_hazard = str(roadmap["focus"]).lower()
        if not focus_hazard and projection:
            focus_entries = projection.get("focus") or []
            if focus_entries:
                focus_hazard = str(focus_entries[0].get("hazard", "general")).lower()
        chosen = monsters[0]
        if focus_hazard:
            chosen = max(
                monsters,
                key=lambda monster: 1 if monster.get("hazard") == focus_hazard else 0,
            )
        enrage = self._enrage_condition(projection or {}, chosen)
        threat = float(chosen.get("threat", 1.1))
        interval = max(6.0, 12.0 - threat * 3.0)
        strategies = self._strategies(chosen, threat)
        spawn_support = self._spawn_support(spawn_plan or {}, chosen)
        phase_transitions = self._phase_transitions(threat, spawn_plan or {}, projection or {})
        trade_hooks = self._trade_hooks(trade_skills, chosen)
        return {
            "name": f"{chosen.get('hazard', 'general').title()} Sovereign",
            "hazard": chosen.get("hazard", "general"),
            "threat": round(threat, 2),
            "enrage_condition": enrage,
            "recommended_counters": chosen.get("recommended_counter"),
            "spawn_interval": round(interval, 2),
            "strategies": strategies,
            "spawn_support": spawn_support,
            "phase_transitions": phase_transitions,
            "trade_skill_hooks": trade_hooks,
        }

    def _enrage_condition(self, projection: dict[str, Any], monster: dict[str, Any]) -> str:
        focus_entries = projection.get("focus") or []
        for entry in focus_entries:
            if entry.get("hazard") == monster.get("hazard"):
                spawn_multiplier = float(entry.get("spawn_multiplier", 1.0))
                if spawn_multiplier > 0.8:
                    return "Bolsters minions when health drops below 50%"
        return "Empowered after each defeated adventurer"

    def _strategies(self, monster: dict[str, Any], threat: float) -> tuple[str, ...]:
        hazard = str(monster.get("hazard", "general")).title()
        strategies = [f"Exploit {hazard} terrain"]
        if threat >= 1.3:
            strategies.append("Rotate defensive phases")
        if monster.get("spawn_synergy") in {"reinforcement", "overwhelming"}:
            strategies.append("Summon elite reinforcements")
        return tuple(dict.fromkeys(strategies))

    def _spawn_support(self, spawn_plan: dict[str, Any], monster: dict[str, Any]) -> dict[str, Any]:
        """Return boss summon and support channel guidance."""

        lanes = tuple(spawn_plan.get("lanes", ()))
        cohort = spawn_plan.get("cohort_matrix", {})
        hazard = monster.get("hazard")
        hazard_view = cohort.get(hazard, {}) if isinstance(cohort, dict) else {}
        summons = "minimal"
        synergy = str(monster.get("spawn_synergy", "skirmish"))
        if hazard_view and hazard_view.get("groups", 0) >= 2:
            summons = "coordinated"
        if synergy in {"reinforcement", "overwhelming"}:
            summons = "overwatch"
        return {
            "lanes": lanes or ("central",),
            "summons": summons,
            "hazard_roles": tuple(hazard_view.get("roles", ())) if hazard_view else (),
            "synergies": tuple(hazard_view.get("synergies", ())) if hazard_view else (synergy,),
        }

    def _phase_transitions(
        self,
        threat: float,
        spawn_plan: dict[str, Any],
        projection: dict[str, Any],
    ) -> dict[str, Any]:
        """Return phase transitions tuned to spawn pressure."""

        danger = float(spawn_plan.get("danger", 1.0))
        cadence = tuple(float(x) for x in spawn_plan.get("reinforcement_curve", ()))
        projection_focus = projection.get("focus") or []
        focus_count = sum(1 for entry in projection_focus if entry.get("spawn_multiplier", 0) > 1)
        evolution = "stable"
        if danger >= 1.8 or threat >= 1.4:
            evolution = "escalating"
        if focus_count >= 2:
            evolution = "volatile"
        transition_points = []
        base = 100 / max(1, len(cadence) or 1)
        for index in range(1, max(2, len(cadence) + 1)):
            transition_points.append(round(base * index, 2))
        return {
            "mode": evolution,
            "transition_points": tuple(transition_points),
            "spawn_cadence_reference": cadence,
        }

    def _trade_hooks(
        self,
        trade_skills: Sequence[str] | None,
        monster: dict[str, Any],
    ) -> tuple[str, ...]:
        """Return trade skill hooks relevant to the boss encounter."""

        if not trade_skills:
            trade_skills = (monster.get("weakness"),)  # type: ignore[assignment]
        hooks: list[str] = []
        hazard = str(monster.get("hazard", "general")).title()
        for skill in trade_skills or ():
            if not skill:
                continue
            hooks.append(f"{skill} ritual to counter {hazard}")
        unique_hooks = tuple(dict.fromkeys(hooks))
        return unique_hooks
