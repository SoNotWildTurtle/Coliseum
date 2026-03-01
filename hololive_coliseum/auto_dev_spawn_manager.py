"""Plan monster group spawns for MMO auto-development."""

from __future__ import annotations

from typing import Any, Sequence


class AutoDevSpawnManager:
    """Create spawn schedules that respond to projected danger."""

    def __init__(self, base_group_size: int = 4) -> None:
        self.base_group_size = max(1, int(base_group_size))

    def plan_groups(
        self,
        monsters: Sequence[dict[str, Any]] | None,
        *,
        scenarios: Sequence[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Return spawn timing and sizing for the supplied monsters."""

        monsters = list(monsters or [])
        if not monsters:
            return {}
        danger_scale = self._danger_from_scenarios(scenarios or [])
        groups = []
        lanes: list[str] = []
        reinforcement_curve: list[float] = []
        for index, monster in enumerate(monsters, start=1):
            threat = float(monster.get("threat", 0.6))
            size = max(1, round(self.base_group_size * threat * danger_scale))
            interval = round(max(4.0, 8.0 / max(0.5, danger_scale)) + index, 2)
            lane = self._entry_point(index)
            groups.append(
                {
                    "monster": monster.get("name", f"monster_{index}"),
                    "size": int(size),
                    "spawn_interval": interval,
                    "entry_point": lane,
                    "synergy": monster.get("spawn_synergy", "skirmish"),
                }
            )
            reinforcement_curve.append(interval)
            if lane not in lanes:
                lanes.append(lane)
        formation = "staggered"
        if len(groups) >= 3 and danger_scale >= 1.4:
            formation = "onslaught"
        elif len(groups) <= 2:
            formation = "incursion"
        tempo = "balanced"
        if danger_scale >= 2.0:
            tempo = "furious"
        elif danger_scale <= 0.8:
            tempo = "cautious"
        cohort_matrix = self._cohort_matrix(monsters, groups)
        escalation = self._escalation_plan(reinforcement_curve, danger_scale)
        group_roles = self._group_roles(monsters)
        group_threads = self._group_threads(monsters)
        return {
            "group_count": len(groups),
            "danger": round(danger_scale, 2),
            "groups": groups,
            "lanes": tuple(lanes) or ("central",),
            "reinforcement_curve": tuple(reinforcement_curve),
            "formation": formation,
            "tempo": tempo,
            "cohort_matrix": cohort_matrix,
            "escalation_plan": escalation,
            "group_roles": group_roles,
            "group_threads": group_threads,
        }

    def _danger_from_scenarios(self, scenarios: Sequence[dict[str, Any]]) -> float:
        if not scenarios:
            return 1.0
        values = [float(s.get("danger_score", 40.0)) for s in scenarios]
        average = sum(values) / len(values)
        return max(0.5, min(3.0, average / 40.0))

    def _entry_point(self, index: int) -> str:
        points = ["north", "south", "east", "west"]
        return points[(index - 1) % len(points)]

    def _cohort_matrix(
        self,
        monsters: Sequence[dict[str, Any]],
        groups: Sequence[dict[str, Any]],
    ) -> dict[str, Any]:
        """Return a hazard keyed summary of spawn cohesion."""

        matrix: dict[str, dict[str, Any]] = {}
        for index, monster in enumerate(monsters):
            hazard = str(monster.get("hazard", "general"))
            bucket = matrix.setdefault(
                hazard,
                {"groups": 0, "synergies": set(), "roles": set()},
            )
            bucket["groups"] += 1
            bucket["roles"].add(str(monster.get("group_role") or monster.get("role", "support")))
            try:
                group = groups[index]
            except IndexError:
                group = {}
            bucket["synergies"].add(
                str(group.get("synergy", monster.get("spawn_synergy", "skirmish")))
            )
        return {
            hazard: {
                "groups": value["groups"],
                "synergies": tuple(sorted(value["synergies"])),
                "roles": tuple(sorted(value["roles"])),
            }
            for hazard, value in matrix.items()
        }

    def _escalation_plan(
        self,
        reinforcement_curve: Sequence[float],
        danger_scale: float,
    ) -> dict[str, Any]:
        """Return an escalation model for mob waves."""

        cadence = tuple(round(interval, 2) for interval in reinforcement_curve)
        if not cadence:
            return {"mode": "static", "cadence": (), "escalation_index": 0.0}
        pivot = max(cadence)
        escalation_index = min(1.0, danger_scale / 2.5 + len(cadence) * 0.05)
        mode = "steady"
        if escalation_index >= 0.75:
            mode = "surge"
        elif escalation_index >= 0.45:
            mode = "press"
        return {
            "mode": mode,
            "cadence": cadence,
            "pivot": pivot,
            "escalation_index": round(escalation_index, 2),
        }

    def _group_roles(self, monsters: Sequence[dict[str, Any]]) -> tuple[str, ...]:
        roles = {
            str(monster.get("group_role") or monster.get("role", "support"))
            for monster in monsters
        }
        return tuple(sorted(roles))

    def _group_threads(self, monsters: Sequence[dict[str, Any]]) -> tuple[str, ...]:
        threads: set[str] = set()
        for monster in monsters:
            blueprint = monster.get("creation_blueprint") or {}
            thread = blueprint.get("spawn_thread")
            if thread:
                threads.add(str(thread))
        return tuple(sorted(threads))
