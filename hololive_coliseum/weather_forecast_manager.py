"""Produce deterministic weather forecasts for shared worlds and arenas."""

from __future__ import annotations

import random
from typing import Iterable, List, Sequence

DEFAULT_WEATHER: tuple[str, ...] = ("clear", "rain", "snow")


class WeatherForecastManager:
    """Generate reproducible weather schedules for MMO regions and arenas."""

    def __init__(self, seed: int | str, weather_types: Iterable[str] | None = None):
        self._rng = random.Random(seed)
        types: Sequence[str] = tuple(weather_types) if weather_types else DEFAULT_WEATHER
        if not types:
            raise ValueError("weather_types must include at least one entry")
        self._weather_types: tuple[str, ...] = tuple(types)
        self._schedule: List[str] = []
        self._index = 0

    @property
    def weather_types(self) -> tuple[str, ...]:
        """Return the ordered tuple of possible weather states."""
        return self._weather_types

    def forecast(self, steps: int) -> list[str]:
        """Return the next ``steps`` weather entries without advancing the cursor."""
        if steps <= 0:
            return []
        target = self._index + steps
        self._ensure_cache(target)
        return self._schedule[self._index:target]

    def next_weather(self) -> str:
        """Advance and return the next weather entry from the forecast."""
        self._ensure_cache(self._index + 1)
        weather = self._schedule[self._index]
        self._index += 1
        return weather

    def upcoming(self, steps: int) -> list[str]:
        """Alias for :meth:`forecast` to improve readability at call sites."""
        return self.forecast(steps)

    def reset(self) -> None:
        """Reset iteration so callers can replay the forecast from the start."""
        self._index = 0

    def _ensure_cache(self, target: int) -> None:
        """Populate the schedule with at least ``target`` entries."""
        while len(self._schedule) < target:
            choice = self._rng.choice(self._weather_types)
            self._schedule.append(choice)
