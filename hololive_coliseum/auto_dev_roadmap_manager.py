"""Aggregate auto-dev insights into actionable MMO roadmaps."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence


def _clean_powerups(raw: Iterable[Any] | None) -> tuple[str, ...]:
    """Return a tuple of non-empty power-up names."""

    if not raw:
        return ()
    return tuple(str(item).strip() for item in raw if str(item).strip())


@dataclass
class RoadmapEntry:
    """Container for a single roadmap iteration."""

    focus: str
    priority_actions: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    support_plan: Dict[str, Any] | None
    projection_focus: Sequence[Dict[str, Any]]
    scenarios: Sequence[Dict[str, Any]]
    iteration: int

    def as_dict(self) -> Dict[str, Any]:
        """Return a serialisable dictionary representation."""

        data: Dict[str, Any] = {
            "iteration": self.iteration,
            "focus": self.focus,
            "priority_actions": list(self.priority_actions),
        }
        if self.metrics:
            data["metrics"] = dict(self.metrics)
        if self.support_plan:
            data["support_plan"] = dict(self.support_plan)
        if self.projection_focus:
            data["projection_focus"] = [dict(entry) for entry in self.projection_focus]
        if self.scenarios:
            data["scenarios"] = [dict(entry) for entry in self.scenarios]
        return data


class AutoDevRoadmapManager:
    """Compile consolidated MMO auto-dev roadmaps from existing insights."""

    def __init__(self, max_history: int = 8) -> None:
        self.max_history = max(1, int(max_history))
        self.history: list[RoadmapEntry] = []

    def compile_iteration(
        self,
        *,
        feedback: Dict[str, Any] | None = None,
        feedback_manager: Any | None = None,
        projection: Dict[str, Any] | None = None,
        scenarios: Sequence[Dict[str, Any]] | None = None,
        support_plan: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Combine current auto-dev signals into a roadmap entry.

        Parameters mirror the existing managers so the caller can supply either
        raw summaries or the manager instances themselves. When a value is not
        provided the manager attempts to derive it from ``feedback_manager``.
        The resulting roadmap is appended to :attr:`history` and returned as a
        plain dictionary. If there is not enough information to produce a
        meaningful plan an empty dictionary is returned and the history is left
        unchanged.
        """

        feedback = dict(feedback or {})
        scenarios = list(scenarios or [])
        projection_focus = self._normalise_projection_focus(projection)
        metrics = self._gather_metrics(feedback, feedback_manager)
        hazard = self._determine_focus(feedback, projection_focus, scenarios, feedback_manager)
        priority_actions = self._build_priority_actions(
            hazard,
            feedback,
            projection_focus,
            support_plan,
        )

        if not (priority_actions or scenarios or support_plan or projection_focus or metrics):
            return {}

        iteration = len(self.history) + 1
        entry = RoadmapEntry(
            focus=hazard,
            priority_actions=priority_actions,
            metrics=metrics,
            support_plan=dict(support_plan) if support_plan else None,
            projection_focus=projection_focus,
            scenarios=scenarios,
            iteration=iteration,
        )
        self.history.append(entry)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history :]
        return entry.as_dict()

    def recent_history(self) -> List[Dict[str, Any]]:
        """Return all stored roadmap entries as dictionaries."""

        return [entry.as_dict() for entry in self.history]

    def latest(self) -> Dict[str, Any] | None:
        """Return the most recent roadmap entry, if available."""

        if not self.history:
            return None
        return self.history[-1].as_dict()

    def _determine_focus(
        self,
        feedback: Dict[str, Any],
        projection_focus: Sequence[Dict[str, Any]],
        scenarios: Sequence[Dict[str, Any]],
        feedback_manager: Any | None,
    ) -> str:
        hazard = str(feedback.get("trending_hazard", "")).strip()
        if not hazard:
            challenge = feedback.get("hazard_challenge")
            if isinstance(challenge, dict):
                hazard = str(challenge.get("hazard", "")).strip()
        if not hazard and feedback_manager:
            hazard = str(getattr(feedback_manager, "get_trending_hazard", lambda: "")() or "").strip()
        if not hazard and projection_focus:
            hazard = str(projection_focus[0].get("hazard", "")).strip()
        if not hazard and scenarios:
            hazard = str(scenarios[0].get("hazard", "")).strip()
        return hazard or "general"

    def _gather_metrics(
        self,
        feedback: Dict[str, Any],
        feedback_manager: Any | None,
    ) -> Dict[str, Any]:
        metrics: Dict[str, Any] = {}
        avg_score = feedback.get("average_score")
        if avg_score:
            metrics["average_score"] = float(avg_score)
        avg_time = feedback.get("average_time")
        if avg_time:
            metrics["average_time"] = float(avg_time)
        challenge = feedback.get("hazard_challenge")
        if isinstance(challenge, dict) and challenge.get("target"):
            metrics["challenge_target"] = int(challenge["target"])
        if feedback_manager:
            total = getattr(feedback_manager, "total_matches", 0)
            if total:
                metrics.setdefault("matches_tracked", int(total))
            if "average_score" not in metrics:
                value = getattr(feedback_manager, "get_average_score", lambda: 0.0)()
                if value:
                    metrics["average_score"] = float(value)
            if "average_time" not in metrics:
                value = getattr(feedback_manager, "get_average_duration", lambda: 0.0)()
                if value:
                    metrics["average_time"] = float(value)
        return metrics

    def _build_priority_actions(
        self,
        hazard: str,
        feedback: Dict[str, Any],
        projection_focus: Sequence[Dict[str, Any]],
        support_plan: Dict[str, Any] | None,
    ) -> List[Dict[str, Any]]:
        actions: List[Dict[str, Any]] = []
        challenge = feedback.get("hazard_challenge")
        if isinstance(challenge, dict):
            entry = {
                "source": "feedback",
                "hazard": hazard,
                "title": f"Stabilise {hazard} hazards",
                "target": int(challenge.get("target", 0)),
            }
            actions.append(entry)
        elif hazard and feedback.get("trending_hazard"):
            actions.append(
                {
                    "source": "feedback",
                    "hazard": hazard,
                    "title": f"Monitor {hazard} activity",
                }
            )
        for focus_entry in projection_focus:
            action = {
                "source": "projection",
                "hazard": focus_entry.get("hazard", hazard),
                "danger_score": int(focus_entry.get("danger_score", 0)),
            }
            recommended = _clean_powerups(focus_entry.get("recommended_powerups"))
            if recommended:
                action["recommended_powerups"] = recommended
            if "spawn_multiplier" in focus_entry:
                action["spawn_multiplier"] = focus_entry["spawn_multiplier"]
            actions.append(action)
        if support_plan:
            entry = {
                "source": "tuning",
                "hazard": support_plan.get("hazard", hazard),
                "recommended_powerups": _clean_powerups(support_plan.get("recommended_powerups")),
            }
            if "spawn_multiplier" in support_plan:
                entry["spawn_multiplier"] = support_plan["spawn_multiplier"]
            if support_plan.get("target"):
                entry["target"] = int(support_plan["target"])
            actions.append(entry)
        return actions

    @staticmethod
    def _normalise_projection_focus(projection: Dict[str, Any] | None) -> List[Dict[str, Any]]:
        if not projection:
            return []
        focus = projection.get("focus")
        if not isinstance(focus, Iterable):
            return []
        normalised: List[Dict[str, Any]] = []
        for raw in focus:
            if not isinstance(raw, dict):
                continue
            entry = dict(raw)
            if "hazard" in entry:
                entry["hazard"] = str(entry["hazard"]).strip()
            if "danger_score" in entry:
                try:
                    entry["danger_score"] = int(entry["danger_score"])
                except (TypeError, ValueError):
                    entry["danger_score"] = 0
            normalised.append(entry)
        return normalised
