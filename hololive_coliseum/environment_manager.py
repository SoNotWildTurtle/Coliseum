"""Manage weather, day/night cycle, and resulting ambient lighting."""

from __future__ import annotations

import math
import random

from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - imported for type checking only
    from .weather_forecast_manager import WeatherForecastManager

WEATHER_FRICTION = {
    "clear": 1.0,
    "rain": 0.8,
    "snow": 0.6,
}

WEATHER_TINTS = {
    "clear": (15, 20, 40),
    "rain": (10, 25, 60),
    "snow": (120, 120, 150),
}

MAX_OVERLAY_ALPHA = 160


class EnvironmentManager:
    """Track weather, day/night cycle, and calculate ambient lighting."""

    def __init__(self, day_length_ms: int = 60000):
        self.settings: dict[str, object] = {}
        self.day_length_ms = day_length_ms
        self.time_ms = 0
        # Default lighting so callers receive consistent values before the first update.
        self.settings["light_level"] = 1.0
        self.settings["ambient_overlay"] = (0, 0, 0, 0)
        self._forecast: WeatherForecastManager | None = None

    def update(self, now: int) -> None:
        """Update the current time of day using the given timestamp."""
        self.time_ms = now % self.day_length_ms
        self.settings["is_day"] = self.time_ms < self.day_length_ms / 2
        self._update_lighting()

    def is_day(self) -> bool:
        """Return True when the environment is in daylight."""
        return self.settings.get("is_day", True)  # type: ignore[return-value]

    def set(self, key: str, value) -> None:
        self.settings[key] = value
        if key == "weather":
            # Recalculate lighting tint immediately when weather changes.
            self._update_lighting()

    def get(self, key: str, default=None):
        return self.settings.get(key, default)

    def attach_forecast_manager(self, forecast: "WeatherForecastManager | None") -> None:
        """Store a forecast manager so weather can sync with the MMO world."""
        self._forecast = forecast

    def upcoming_weather(self, steps: int = 3) -> list[str]:
        """Return the next few weather entries when a forecast is available."""
        if not self._forecast:
            return []
        return self._forecast.forecast(steps)

    def get_light_level(self) -> float:
        """Return a 0-1 multiplier describing how bright the arena currently is."""
        return float(self.settings.get("light_level", 1.0))

    def ambient_overlay(self) -> Tuple[int, int, int, int]:
        """Return RGBA values describing the ambient lighting overlay."""
        overlay = self.settings.get("ambient_overlay", (0, 0, 0, 0))
        return tuple(overlay)  # type: ignore[return-value]

    def randomize_weather(self) -> str:
        """Choose a random weather type and store its friction effect."""
        if self._forecast:
            weather = self._forecast.next_weather()
        else:
            weather = random.choice(list(WEATHER_FRICTION.keys()))
        self.settings["weather"] = weather
        self.settings["friction"] = WEATHER_FRICTION[weather]
        self._update_lighting()
        return weather

    def _update_lighting(self) -> None:
        """Recalculate lighting information from time of day and weather."""
        if self.day_length_ms <= 0:
            ratio = 0.0
        else:
            ratio = self.time_ms / self.day_length_ms
        # Use a sine curve so sunrise/sunset ease in and out of brightness.
        phase = ratio * 2 * math.pi
        light_level = 0.5 + 0.5 * math.sin(phase - math.pi / 2)
        light_level = max(0.0, min(1.0, light_level))
        weather = self.settings.get("weather", "clear")
        tint = WEATHER_TINTS.get(weather, WEATHER_TINTS["clear"])
        alpha = int((1 - light_level) * MAX_OVERLAY_ALPHA)
        self.settings["light_level"] = light_level
        self.settings["ambient_overlay"] = (*tint, alpha)
