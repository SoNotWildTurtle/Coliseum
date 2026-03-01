"""Synthesize MMO auto-dev focus areas from existing insights."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any, Dict, List


def _clean_hazard(value: object) -> str:
    """Return a normalised hazard string."""

    text = str(value or "").strip()
    return text.lower() if text else ""


class AutoDevFocusManager:
    """Calculate sprint focus priorities from auto-development data."""

    def __init__(self, max_focus: int = 5, history_limit: int = 6) -> None:
        self.max_focus = max(1, int(max_focus))
        self.history_limit = max(1, int(history_limit))
        self._history: list[Dict[str, Any]] = []

    def analyse(
        self,
        *,
        roadmap: Dict[str, Any] | None = None,
        feedback: Dict[str, Any] | None = None,
        projection: Dict[str, Any] | None = None,
        scenarios: Sequence[Dict[str, Any]] | None = None,
        support_plan: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Return a prioritised focus summary from available signals."""

        scoreboard: Dict[str, Dict[str, Any]] = {}
        feedback = dict(feedback or {})
        scenarios = list(scenarios or [])
        projection_focus = list(self._extract_projection_focus(projection))

        def bump(hazard: str, weight: float, source: str, danger: float = 0.0) -> None:
            hazard_key = _clean_hazard(hazard)
            if not hazard_key:
                return
            entry = scoreboard.setdefault(
                hazard_key,
                {"score": 0.0, "sources": set(), "danger": 0.0},
            )
            entry["score"] += float(weight)
            entry["danger"] = max(entry["danger"], float(danger))
            entry["sources"].add(source)

        if roadmap:
            bump(roadmap.get("focus"), 6.0, "roadmap")
            for action in roadmap.get("priority_actions", []):
                hazard = action.get("hazard") or roadmap.get("focus")
                bump(hazard, 2.0, "roadmap_action")

        trending = feedback.get("trending_hazard")
        if trending:
            bump(trending, 3.0, "feedback")
        challenge = feedback.get("hazard_challenge")
        if isinstance(challenge, dict):
            bump(challenge.get("hazard"), 2.5, "feedback_challenge")

        if support_plan:
            bump(support_plan.get("hazard"), 2.0, "support_plan")

        for focus_entry in projection_focus:
            hazard = focus_entry.get("hazard")
            danger = float(focus_entry.get("danger_score", 0.0))
            weight = 1.5 + danger / 25.0
            bump(hazard, weight, "projection", danger)

        for scenario in scenarios:
            bump(scenario.get("hazard"), 1.0, "scenario")

        if not scoreboard:
            return {}

        priorities = self._build_priorities(scoreboard)
        report = {
            "top_focus": priorities[0]["hazard"],
            "priorities": priorities,
            "context": self._build_context(
                roadmap=roadmap,
                projection=projection,
                scenarios=scenarios,
                support_plan=support_plan,
                feedback=feedback,
            ),
        }
        snapshot = self._clone(report)
        self._history.append(snapshot)
        if len(self._history) > self.history_limit:
            self._history = self._history[-self.history_limit :]
        return self._clone(report)

    def recent_focus(self) -> List[Dict[str, Any]]:
        """Return the stored focus history."""

        return [self._clone(entry) for entry in self._history]

    def latest(self) -> Dict[str, Any] | None:
        """Return the most recent focus entry, if present."""

        if not self._history:
            return None
        return self._clone(self._history[-1])

    def _clone(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        clone = {
            "top_focus": entry["top_focus"],
            "priorities": [dict(item) for item in entry["priorities"]],
            "context": dict(entry["context"]),
        }
        return clone

    def _build_priorities(self, scoreboard: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        ordered = sorted(
            (
                {
                    "hazard": hazard,
                    "score": round(data["score"], 2),
                    "danger": round(data["danger"], 2),
                    "sources": tuple(sorted(data["sources"])),
                }
                for hazard, data in scoreboard.items()
            ),
            key=lambda item: (-item["score"], -item["danger"], item["hazard"]),
        )
        return ordered[: self.max_focus]

    def _build_context(
        self,
        *,
        roadmap: Dict[str, Any] | None,
        projection: Dict[str, Any] | None,
        scenarios: Sequence[Dict[str, Any]],
        support_plan: Dict[str, Any] | None,
        feedback: Dict[str, Any],
    ) -> Dict[str, Any]:
        context: Dict[str, Any] = {
            "scenario_count": len(scenarios),
        }
        if roadmap and roadmap.get("iteration"):
            context["roadmap_iteration"] = int(roadmap["iteration"])
        if projection and projection.get("matches_considered"):
            context["matches_considered"] = int(projection["matches_considered"])
        if support_plan and support_plan.get("hazard"):
            context["support_plan_hazard"] = _clean_hazard(support_plan["hazard"])
        if feedback.get("trending_hazard"):
            context["trending_hazard"] = _clean_hazard(feedback["trending_hazard"])
        return context

    def _extract_projection_focus(
        self, projection: Dict[str, Any] | None
    ) -> Iterable[Dict[str, Any]]:
        if not projection:
            return []
        focus_entries = projection.get("focus")
        if isinstance(focus_entries, dict):
            return [focus_entries]
        if isinstance(focus_entries, Iterable):
            return list(focus_entries)
        return []
