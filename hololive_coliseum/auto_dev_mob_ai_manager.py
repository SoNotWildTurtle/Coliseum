"""Generate AI behaviour directives for auto-generated mobs."""

from __future__ import annotations

from typing import Any, Sequence


class AutoDevMobAIManager:
    """Produce behavioural presets for monster groups."""

    def ai_directives(
        self,
        monsters: Sequence[dict[str, Any]] | None,
        *,
        spawn_plan: dict[str, Any] | None = None,
        projection: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return instructions that keep mobs reactive and varied."""

        monsters = list(monsters or [])
        if not monsters:
            return {}
        directives = []
        projection_focus = list((projection or {}).get("focus", []))
        spawn_danger = float((spawn_plan or {}).get("danger", 1.0))
        training_modules: set[str] = set()
        for monster in monsters:
            hazard = monster.get("hazard", "general")
            behaviour = self._behaviour(monster, spawn_danger)
            abilities = self._abilities(hazard, projection_focus)
            training_modules.add(f"{hazard.title()} counter drills")
            directives.append(
                {
                    "monster": monster.get("name", hazard.title()),
                    "hazard": hazard,
                    "behaviour": behaviour,
                    "abilities": abilities,
                    "ai_focus": monster.get("ai_focus", "adaptive"),
                }
            )
        learning = spawn_danger >= 1.1 or bool(projection_focus)
        adaptive = any("retreat" in (ability.lower()) for ability in sum(
            (list(d.get("abilities", ())) for d in directives),
            []
        ))
        coordination_matrix = self._coordination_matrix(directives, spawn_danger)
        evolution_threads = self._evolution_threads(monsters)
        group_support = self._group_support(monsters)
        return {
            "coordination_window": max(8.0, 12.0 / max(0.75, spawn_danger)),
            "directives": directives,
            "learning": learning,
            "adaptive": adaptive,
            "training_modules": tuple(sorted(training_modules)),
            "coordination_matrix": coordination_matrix,
            "evolution_threads": evolution_threads,
            "group_support_directives": group_support,
        }

    def _behaviour(self, monster: dict[str, Any], spawn_danger: float) -> str:
        threat = float(monster.get("threat", 0.6)) * spawn_danger
        if threat >= 1.2:
            return "coordinated assaults"
        if threat >= 0.9:
            return "flanking maneuvers"
        return "harassing strikes"

    def _abilities(self, hazard: str, projection_focus: Sequence[dict[str, Any]]) -> tuple[str, ...]:
        matches = [focus for focus in projection_focus if focus.get("hazard") == hazard]
        if matches:
            recommended = matches[0].get("recommended_powerups") or ()
            counters = tuple(str(item) for item in recommended)
            if counters:
                return counters
        return (f"{hazard.title()} surge", "coordinated retreat")

    def _coordination_matrix(
        self,
        directives: Sequence[dict[str, Any]],
        spawn_danger: float,
    ) -> dict[str, Any]:
        """Return a matrix describing squad coordination layers."""

        hazards = [str(directive.get("hazard", "general")) for directive in directives]
        unique_hazards = tuple(sorted(set(hazards)))
        density = min(1.0, max(0.1, len(directives) * spawn_danger / 10.0))
        cadence = round(max(6.0, 12.0 - spawn_danger * 2.5), 2)
        escalation = "agile"
        if spawn_danger >= 1.6:
            escalation = "relentless"
        elif spawn_danger <= 0.9:
            escalation = "measured"
        return {
            "hazards": unique_hazards,
            "density": round(density, 3),
            "coordination_cadence": cadence,
            "escalation": escalation,
        }

    def _evolution_threads(self, monsters: Sequence[dict[str, Any]]) -> tuple[str, ...]:
        """Return AI evolution threads from monster blueprints."""

        threads: set[str] = set()
        for monster in monsters:
            blueprint = monster.get("creation_blueprint") or {}
            ai_path = monster.get("ai_development_path") or {}
            mutation_track = blueprint.get("mutation_track")
            if mutation_track:
                threads.add(f"mutation:{mutation_track}")
            for stage in ai_path.get("stages", ()):  # type: ignore[arg-type]
                if isinstance(stage, str):
                    threads.add(stage)
            hazard = monster.get("hazard")
            if hazard:
                threads.add(f"hazard:{hazard}")
        return tuple(sorted(threads))

    def _group_support(self, monsters: Sequence[dict[str, Any]]) -> dict[str, Any]:
        """Return recommended group support directives for AI squads."""

        support_map: dict[str, list[str]] = {}
        for monster in monsters:
            role = str(monster.get("group_role") or monster.get("role", "support"))
            hazard = str(monster.get("hazard", "general"))
            support_map.setdefault(role, []).append(hazard)
        return {
            role: {
                "hazards": tuple(sorted(set(hazards))),
                "directives": (
                    "anchor lane" if role == "vanguard" else "flank support"
                ),
            }
            for role, hazards in support_map.items()
        }
