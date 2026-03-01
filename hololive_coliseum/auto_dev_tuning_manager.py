"""Derive arena tuning directives from auto-dev telemetry."""

from __future__ import annotations

from typing import Dict, Iterable

from .auto_dev_feedback_manager import AutoDevFeedbackManager


class AutoDevTuningManager:
    """Translate auto-dev feedback into gameplay adjustments."""

    MIN_DELAY_MS = 2500
    COUNTER_POWERUPS: Dict[str, Iterable[str]] = {
        "fire": ("shield", "defense", "heal"),
        "lava": ("shield", "defense"),
        "spike": ("shield", "heal"),
        "poison": ("heal", "defense"),
        "acid": ("shield", "heal"),
        "lightning": ("defense", "shield"),
        "frost": ("speed", "stamina"),
        "ice": ("speed", "stamina"),
        "wind": ("stamina", "speed"),
        "quicksand": ("speed", "stamina"),
        "silence": ("attack", "xp"),
    }

    def __init__(self, feedback_manager: AutoDevFeedbackManager | None = None) -> None:
        self.feedback_manager = feedback_manager
        self.adaptive_multiplier = 1.0
        self.adaptive_focus = "stability"
        self.adaptive_risk_budget = "balanced"
        self.mob_interval_multiplier = 1.0
        self.mob_wave_delta = 0
        self.mob_max_delta = 0

    def recommend_spawn_timers(self, base_timers: Dict[str, int]) -> Dict[str, int]:
        """Return adjusted power-up spawn timers based on hazard trends."""

        plan = dict(base_timers)
        challenge = self._current_challenge()
        if not challenge:
            return plan
        counters = self.COUNTER_POWERUPS.get(challenge["hazard"])
        if not counters:
            return plan
        multiplier = self._multiplier_for_target(challenge["target"])
        multiplier *= self.adaptive_multiplier
        for powerup in counters:
            if powerup in plan:
                plan[powerup] = max(
                    self.MIN_DELAY_MS, int(plan[powerup] * multiplier)
                )
        return plan

    def support_plan(self) -> Dict[str, object] | None:
        """Return a summary of countermeasures for the current hazard trend."""

        challenge = self._current_challenge()
        if not challenge:
            return None
        counters = tuple(self.COUNTER_POWERUPS.get(challenge["hazard"], ()))
        if not counters:
            return None
        multiplier = self._multiplier_for_target(challenge["target"])
        multiplier *= self.adaptive_multiplier
        return {
            "hazard": challenge["hazard"],
            "target": challenge["target"],
            "recommended_powerups": counters,
            "spawn_multiplier": multiplier,
        }

    def apply_adaptive_tuning(self, adaptive_tuning: Dict[str, object] | None) -> None:
        """Apply self-evolution adaptive tuning to spawn pacing."""

        adaptive_tuning = adaptive_tuning or {}
        focus = str(adaptive_tuning.get("focus", "stability"))
        risk_budget = str(adaptive_tuning.get("risk_budget", "balanced"))
        multiplier = 1.0
        if focus in {"stability", "security"}:
            multiplier *= 1.1
        elif focus == "innovation":
            multiplier *= 1.1
        if risk_budget == "aggressive":
            multiplier *= 1.1
        elif risk_budget == "conservative":
            multiplier *= 0.9
        self.adaptive_multiplier = max(0.75, min(1.25, multiplier))
        self.adaptive_focus = focus
        self.adaptive_risk_budget = risk_budget
        mob_interval = 1.0
        wave_delta = 0
        max_delta = 0
        if focus in {"stability", "security"}:
            mob_interval *= 1.15
            wave_delta -= 1
            max_delta -= 1
        elif focus == "innovation":
            mob_interval *= 0.9
            wave_delta += 1
            max_delta += 1
        if risk_budget == "aggressive":
            mob_interval *= 0.9
            wave_delta += 1
            max_delta += 1
        elif risk_budget == "conservative":
            mob_interval *= 1.1
            wave_delta -= 1
            max_delta -= 1
        self.mob_interval_multiplier = max(0.75, min(1.35, mob_interval))
        self.mob_wave_delta = max(-2, min(2, wave_delta))
        self.mob_max_delta = max(-3, min(3, max_delta))

    def adjust_mob_spawn_config(self, config: Dict[str, int]) -> Dict[str, int]:
        """Return a mob spawn config adjusted by adaptive tuning."""

        if not config:
            return {}
        updated = dict(config)
        interval = int(updated.get("interval", 0))
        if interval > 0:
            updated["interval"] = max(
                self.MIN_DELAY_MS,
                int(interval * self.mob_interval_multiplier),
            )
        updated["wave"] = max(1, int(updated.get("wave", 1)) + self.mob_wave_delta)
        updated["max"] = max(1, int(updated.get("max", 1)) + self.mob_max_delta)
        return updated

    def _current_challenge(self) -> Dict[str, int] | None:
        if not self.feedback_manager:
            return None
        challenge = self.feedback_manager.hazard_challenge()
        if not isinstance(challenge, dict):
            return None
        hazard = str(challenge.get("hazard", "")).strip().lower()
        if not hazard:
            return None
        target = int(challenge.get("target", 0))
        return {"hazard": hazard, "target": target}

    @staticmethod
    def _multiplier_for_target(target: int) -> float:
        if target >= 10:
            return 0.5
        if target >= 7:
            return 0.6
        if target >= 5:
            return 0.7
        if target >= 3:
            return 0.8
        return 0.9
