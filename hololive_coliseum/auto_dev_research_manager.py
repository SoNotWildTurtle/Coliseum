"""Track background research that powers the auto-dev roadmap."""

from __future__ import annotations

import os
from statistics import pstdev
from typing import Dict, Sequence


class AutoDevResearchManager:
    """Record processing budgets used to study other games."""

    def __init__(self, default_percent: float = 20.0) -> None:
        self._samples: list[float] = []
        self._sources: Dict[str, float] = {}
        self._other_games: Dict[str, list[float]] = {}
        self._last_sample: float | None = None
        self.record_utilization(default_percent, source="baseline")

    def record_utilization(self, percent: float, *, source: str = "auto_dev") -> None:
        """Store a utilisation percentage for later reporting."""

        value = max(0.0, float(percent))
        self._samples.append(value)
        self._last_sample = value
        self._sources[source] = self._sources.get(source, 0.0) + value

    def record_competitive_research(self, percent: float, *, game: str) -> None:
        """Track utilisation spent researching another live game."""

        name = game.strip() or "Unattributed Rival"
        value = max(0.0, float(percent))
        bucket = self._other_games.setdefault(name, [])
        bucket.append(value)
        self.record_utilization(value, source=f"other_game:{name}")

    def update_from_intensity(self, intensity: float, *, source: str = "mining") -> None:
        """Convert a 0-1 intensity value into a stored utilisation percentage."""

        self.record_utilization(max(0.0, float(intensity)) * 100.0, source=source)

    def capture_runtime_utilization(self, *, source: str = "runtime_probe") -> float:
        """Sample current system load and record it as a raw utilisation percentage."""

        value = self._runtime_percent()
        self.record_utilization(value, source=source)
        return value

    def intelligence_brief(self) -> Dict[str, object]:
        """Return a summary of research investment and next steps."""

        if not self._samples:
            return {
                "utilization_percent": 0.0,
                "latest_sample_percent": 0.0,
                "raw_utilization_percent": 0.0,
                "raw_percentage": 0.0,
                "recommendation": "Collect data",
                "raw_samples": [],
                "competitive_research": {
                    "raw_percent": 0.0,
                    "primary_game": None,
                    "games": {},
                },
                "competitive_raw_percent": 0.0,
                "competitive_share_percent": 0.0,
                "other_games_raw_percent": 0.0,
                "other_games_breakdown": {},
                "volatility_percent": 0.0,
                "trend_direction": "stable",
                "research_pressure_index": 0.0,
                "weakness_signals": (),
                "competitive_utilization_percent": 0.0,
            }
        average = sum(self._samples) / len(self._samples)
        top_source = max(self._sources.items(), key=lambda item: item[1])[0]
        recommendation = self._recommendation(average)
        recent_samples = self._samples[-5:]
        latest = self._last_sample if self._last_sample is not None else average
        latest_rounded = round(latest, 2)
        competitive = self._competitive_view()
        competitive_raw = competitive.get("raw_percent", 0.0)
        total_reference = latest_rounded or average or 0.0
        if total_reference <= 0.0:
            competitive_share = 0.0
        else:
            competitive_share = min(100.0, (competitive_raw / total_reference) * 100.0)
        volatility = self._volatility()
        trend_direction = self._trend_direction()
        pressure_index = self._pressure_index(latest_rounded, average, volatility)
        weakness_signals = self._weakness_signals(latest_rounded, pressure_index, volatility)
        return {
            "utilization_percent": round(average, 2),
            "latest_sample_percent": latest_rounded,
            "raw_utilization_percent": latest_rounded,
            "raw_percentage": latest_rounded,
            "samples": len(self._samples),
            "primary_source": top_source,
            "recommendation": recommendation,
            "intelligence_focus": self._focus_from_source(top_source),
            "raw_samples": [round(sample, 2) for sample in recent_samples],
            "competitive_research": competitive,
            "competitive_raw_percent": round(competitive_raw, 2),
            "competitive_share_percent": round(competitive_share, 2),
            "other_games_raw_percent": round(competitive_raw, 2),
            "other_games_breakdown": dict(competitive.get("games", {})),
            "volatility_percent": volatility,
            "trend_direction": trend_direction,
            "research_pressure_index": pressure_index,
            "weakness_signals": tuple(weakness_signals),
            "competitive_utilization_percent": round(competitive_raw, 2),
        }

    def _recommendation(self, average: float) -> str:
        if average < 15:
            return "Increase background research allocation"
        if average < 35:
            return "Maintain balanced auto-dev research"
        return "Throttle research to return resources to live play"

    def _focus_from_source(self, source: str) -> str:
        focus_map = {
            "mining": "Simulate emergent sandbox encounters",
            "auto_dev": "Analyse arena telemetry for MMO trends",
            "baseline": "Maintain knowledge base of peer titles",
            "runtime_probe": "Profile real-world performance patterns",
        }
        return focus_map.get(source, "Distribute insights across managers")

    def _competitive_view(self) -> Dict[str, object]:
        if not self._other_games:
            return {
                "raw_percent": 0.0,
                "primary_game": None,
                "games": {},
            }
        averages: Dict[str, float] = {}
        latest_total = 0.0
        for game, samples in self._other_games.items():
            if not samples:
                continue
            averages[game] = sum(samples) / len(samples)
            latest_total += samples[-1]
        if not averages:
            return {
                "raw_percent": 0.0,
                "primary_game": None,
                "games": {},
            }
        primary_game = max(averages.items(), key=lambda item: item[1])[0]
        return {
            "raw_percent": round(latest_total, 2),
            "primary_game": primary_game,
            "games": {game: round(value, 2) for game, value in averages.items()},
        }

    def _runtime_percent(self) -> float:
        """Return a best-effort CPU utilisation percentage for the host system."""

        try:
            load_avg = os.getloadavg()[0]
            cpu_count = max(1, os.cpu_count() or 1)
            percent = (load_avg / cpu_count) * 100.0
            return max(0.0, min(percent, 100.0))
        except (AttributeError, OSError):
            # ``os.getloadavg`` is not available on all platforms. Fall back to
            # the most recent manual sample or a balanced default.
            if self._last_sample is not None:
                return float(self._last_sample)
            return 25.0

    def _volatility(self) -> float:
        if len(self._samples) <= 1:
            return 0.0
        return round(pstdev(self._samples), 2)

    def _trend_direction(self) -> str:
        if len(self._samples) <= 1:
            return "stable"
        delta = self._samples[-1] - self._samples[-2]
        if delta > 2.5:
            return "increasing"
        if delta < -2.5:
            return "decreasing"
        return "stable"

    def _pressure_index(self, latest: float, average: float, volatility: float) -> float:
        base = latest * 0.55 + average * 0.35 + volatility * 1.2
        return round(max(0.0, min(100.0, base)), 2)

    def _weakness_signals(
        self,
        latest: float,
        pressure_index: float,
        volatility: float,
    ) -> list[str]:
        signals: list[str] = []
        if latest < 15.0:
            signals.append("Research coverage is below sustainability thresholds")
        if pressure_index > 70.0:
            signals.append("Processing pressure is stressing research budgets")
        if volatility > 20.0:
            signals.append("Utilisation volatility risks unstable insights")
        if not signals:
            signals.append("Research operations remain stable")
        return signals

    def sources(self) -> Dict[str, float]:
        """Return accumulated utilisation per source."""

        return dict(self._sources)

    def samples(self) -> Sequence[float]:
        """Return recorded utilisation percentages."""

        return tuple(self._samples)

    def latest_sample(self) -> float | None:
        """Return the most recent utilisation value if one exists."""

        return self._last_sample
