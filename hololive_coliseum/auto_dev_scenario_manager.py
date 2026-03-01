"""Build actionable auto-dev scenarios from projections and objectives."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Sequence

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - used for static checking only
    from .auto_dev_projection_manager import AutoDevProjectionManager
    from .objective_manager import ObjectiveManager


class AutoDevScenarioManager:
    """Synthesize MMO auto-dev scenario briefs for designers."""

    DEFAULT_OBJECTIVES: Sequence[str] = (
        "hazard_mastery",
        "collect_powerups",
        "defeat_enemies",
    )

    def __init__(
        self,
        projection_manager: "AutoDevProjectionManager" | None = None,
        objective_manager: "ObjectiveManager" | None = None,
    ) -> None:
        self.projection_manager = projection_manager
        self.objective_manager = objective_manager

    def scenario_briefs(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Return designer-friendly scenarios derived from recent telemetry."""

        focus_entries = self._focus_entries(limit)
        briefs: List[Dict[str, Any]] = []
        for entry in focus_entries:
            hazard = str(entry.get("hazard", "")).strip() or "general"
            scenario: Dict[str, Any] = {
                "hazard": hazard,
                "danger_score": int(entry.get("danger_score", 0)),
            }
            counter_plan = self._counter_plan(entry)
            if counter_plan:
                scenario["counter_plan"] = counter_plan
            objectives = self._objective_recommendations(hazard)
            if objectives:
                scenario["recommended_objectives"] = objectives
            scenario["training_focus"] = self._training_focus(hazard, objectives)
            briefs.append(scenario)
        if not briefs:
            fallback = self._fallback_brief()
            if fallback:
                briefs.append(fallback)
        return briefs

    def _focus_entries(self, limit: int) -> List[Dict[str, Any]]:
        if limit <= 0 or not self.projection_manager:
            return []
        try:
            summary = self.projection_manager.projection_summary(limit=limit)
        except TypeError:
            summary = self.projection_manager.projection_summary()
        if not isinstance(summary, dict):
            return []
        focus = summary.get("focus")
        if not isinstance(focus, Sequence):
            return []
        entries: List[Dict[str, Any]] = []
        for raw in focus:
            if not isinstance(raw, dict):
                continue
            entries.append(dict(raw))
            if len(entries) >= limit:
                break
        return entries

    def _counter_plan(self, focus_entry: Dict[str, Any]) -> Dict[str, Any]:
        plan: Dict[str, Any] = {}
        powerups = focus_entry.get("recommended_powerups")
        if powerups:
            plan["powerups"] = tuple(str(p) for p in powerups if str(p).strip())
        if "spawn_multiplier" in focus_entry:
            plan["spawn_multiplier"] = focus_entry["spawn_multiplier"]
        return plan

    def _objective_recommendations(self, hazard: str) -> List[Dict[str, Any]]:
        manager = self.objective_manager
        if not manager:
            return []
        objectives = getattr(manager, "objectives", {})
        if not isinstance(objectives, dict):
            return []
        recommendations: List[Dict[str, Any]] = []
        for key in self.DEFAULT_OBJECTIVES:
            objective = objectives.get(key)
            if not objective:
                continue
            remaining = max(0, objective.target - objective.progress)
            entry = {
                "objective": key,
                "description": objective.description,
                "remaining": remaining,
            }
            if key == "hazard_mastery":
                entry["focus_hazard"] = hazard
            recommendations.append(entry)
        return recommendations

    @staticmethod
    def _training_focus(hazard: str, objectives: Iterable[Dict[str, Any]]) -> str:
        if hazard == "general":
            return "Review arena objectives to stay ready for shifting hazards"
        if objectives:
            return f"Practice countering {hazard} while completing tracked objectives"
        return f"Run drills against {hazard} hazards"

    def _fallback_brief(self) -> Dict[str, Any] | None:
        objectives = self._objective_recommendations("general")
        if not objectives:
            return None
        return {
            "hazard": "general",
            "danger_score": 0,
            "recommended_objectives": objectives,
            "training_focus": self._training_focus("general", objectives),
        }
