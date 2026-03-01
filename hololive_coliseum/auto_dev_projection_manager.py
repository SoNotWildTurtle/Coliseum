"""Forecast MMO auto-dev focus areas from recent telemetry."""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, Iterable, List, Sequence

if False:  # pragma: no cover - import only for type checking tools
    from .auto_dev_tuning_manager import AutoDevTuningManager

from .auto_dev_feedback_manager import AutoDevFeedbackManager


class AutoDevProjectionManager:
    """Convert auto-dev telemetry into short-term hazard projections."""

    def __init__(
        self,
        feedback_manager: AutoDevFeedbackManager | None = None,
        tuning_manager: "AutoDevTuningManager" | None = None,
        window: int = 10,
    ) -> None:
        self.feedback_manager = feedback_manager
        self.tuning_manager = tuning_manager
        self.window = max(1, int(window))

    def projection_summary(self, limit: int = 3) -> Dict[str, Any]:
        """Return a snapshot of the most pressing hazards to plan around."""

        focus = self._focus(limit)
        if not focus:
            return {}
        return {
            "matches_considered": len(self._recent_history()),
            "focus": focus,
        }

    def _focus(self, limit: int) -> List[Dict[str, Any]]:
        hazards = self._aggregate_hazards()
        if not hazards:
            return []
        most_common = hazards.most_common(max(1, limit))
        total = sum(count for _, count in hazards.items()) or 1
        focus: List[Dict[str, Any]] = []
        for hazard, count in most_common:
            weight = count / total
            entry: Dict[str, Any] = {
                "hazard": hazard,
                "weight": round(weight, 3),
                "danger_score": int(round(weight * 100)),
            }
            recommendation = self._recommended_powerups(hazard)
            if recommendation:
                entry["recommended_powerups"] = recommendation
                entry["spawn_multiplier"] = self._spawn_multiplier_for_weight(weight)
            focus.append(entry)
        return focus

    def _aggregate_hazards(self) -> Counter[str]:
        counter: Counter[str] = Counter()
        for entry in self._recent_history():
            hazards = entry.get("hazards", {})
            if not isinstance(hazards, dict):
                continue
            for name, amount in hazards.items():
                hazard = str(name).strip().lower()
                if not hazard:
                    continue
                counter[hazard] += int(amount)
        if counter or not self.feedback_manager:
            return counter
        totals = getattr(self.feedback_manager, "hazard_totals", Counter())
        for name, amount in totals.items():
            hazard = str(name).strip().lower()
            if not hazard:
                continue
            counter[hazard] += int(amount)
        return counter

    def _recent_history(self) -> Sequence[Dict[str, Any]]:
        if not self.feedback_manager:
            return []
        history = getattr(self.feedback_manager, "history", [])
        if not isinstance(history, list):
            return []
        if not history:
            return []
        return history[-self.window :]

    def _recommended_powerups(self, hazard: str) -> tuple[str, ...]:
        tuning = self.tuning_manager
        if not tuning:
            return ()
        counters: Iterable[str] | None = getattr(
            tuning, "COUNTER_POWERUPS", {}
        ).get(hazard)
        if not counters:
            return ()
        return tuple(str(power).strip() for power in counters if str(power).strip())

    @staticmethod
    def _spawn_multiplier_for_weight(weight: float) -> float:
        if weight >= 0.6:
            return 0.5
        if weight >= 0.45:
            return 0.6
        if weight >= 0.3:
            return 0.7
        if weight >= 0.15:
            return 0.8
        return 0.9
