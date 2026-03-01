"""Collect Coliseum match telemetry to guide MMO auto-development."""

from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from . import save_manager


class AutoDevFeedbackManager:
    """Record arena feedback and surface insights for MMO generation."""

    def __init__(self, path: str | os.PathLike[str] | None = None, max_history: int = 100) -> None:
        self.max_history = max_history
        if path is None:
            path = Path(save_manager.SAVE_DIR) / "auto_dev_feedback.json"
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.history: list[dict[str, Any]] = []
        self.hazard_totals: Counter[str] = Counter()
        self.character_totals: Counter[str] = Counter()
        self.total_score = 0
        self.total_time = 0
        self.total_matches = 0
        self._current: dict[str, Any] | None = None
        self._load()

    def _load(self) -> None:
        """Load existing history if the feedback file is present."""

        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return
        if not isinstance(data, list):
            return
        self.history = data[-self.max_history :]
        for entry in self.history:
            hazards = entry.get("hazards", {})
            if isinstance(hazards, dict):
                for name, count in hazards.items():
                    self.hazard_totals[str(name)] += int(count)
            character = entry.get("character")
            if isinstance(character, str) and character:
                self.character_totals[character] += 1
            self.total_score += int(entry.get("score", 0))
            self.total_time += int(entry.get("time", 0))
            self.total_matches += 1

    def _save(self) -> None:
        """Persist the latest history to disk."""

        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(self.history, handle)

    def start_match(self, character: str, map_name: str) -> None:
        """Begin tracking telemetry for a new match."""

        self._current = {
            "character": character,
            "map": map_name,
            "hazards": defaultdict(int),
        }

    def record_hazard(self, hazard_type: str) -> None:
        """Record an interaction with ``hazard_type`` during the current match."""

        if not self._current:
            return
        hazards: defaultdict[str, int] = self._current["hazards"]
        hazards[str(hazard_type)] += 1

    def finalize(self, result: str, score: int, duration: int, account: str | None = None) -> dict[str, Any]:
        """Finalize the current match entry and append it to history."""

        if self._current is None:
            self.start_match("", "")
        assert self._current is not None  # for type checkers
        hazards: defaultdict[str, int] = self._current["hazards"]
        entry = {
            "result": result,
            "score": int(score),
            "time": int(duration),
            "character": self._current.get("character", ""),
            "map": self._current.get("map", ""),
            "account": account,
            "hazards": dict(hazards),
        }
        self.history.append(entry)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history :]
        if entry["character"]:
            self.character_totals[entry["character"]] += 1
        for name, count in entry["hazards"].items():
            self.hazard_totals[name] += int(count)
        self.total_score += entry["score"]
        self.total_time += entry["time"]
        self.total_matches += 1
        self._save()
        self._current = None
        return entry

    def get_trending_hazard(self) -> str | None:
        """Return the most frequently encountered hazard type."""

        if not self.hazard_totals:
            return None
        return max(self.hazard_totals.items(), key=lambda item: item[1])[0]

    def get_favorite_character(self) -> str | None:
        """Return the most played character across recorded matches."""

        if not self.character_totals:
            return None
        return max(self.character_totals.items(), key=lambda item: item[1])[0]

    def get_average_score(self) -> float:
        """Return the average score across recorded matches."""

        if self.total_matches == 0:
            return 0.0
        return self.total_score / self.total_matches

    def get_average_duration(self) -> float:
        """Return the average match duration in seconds."""

        if self.total_matches == 0:
            return 0.0
        return self.total_time / self.total_matches

    def hazard_challenge(self, base_target: int = 3) -> dict[str, object] | None:
        """Return a hazard challenge derived from recent telemetry."""

        if not self.hazard_totals:
            return None
        hazard, count = self.hazard_totals.most_common(1)[0]
        average = count / max(1, self.total_matches)
        target = max(base_target, int(round(average * 2)))
        return {"hazard": hazard, "target": target}

    def estimate_recommended_level(self, base_level: int = 1) -> int:
        """Estimate a recommended level using collected scores and durations."""

        level = max(1, int(base_level))
        if self.total_matches == 0:
            return level
        score_level = int(self.get_average_score() // 500) + 1
        time_level = int(self.get_average_duration() // 120) + 1
        return max(level, score_level, time_level)

    def region_insight(self) -> dict[str, Any]:
        """Return a summary of recent trends for world generation."""

        insight: dict[str, Any] = {}
        hazard = self.get_trending_hazard()
        if hazard:
            insight["trending_hazard"] = hazard
        favorite = self.get_favorite_character()
        if favorite:
            insight["favorite_character"] = favorite
        avg_score = self.get_average_score()
        if avg_score:
            insight["average_score"] = avg_score
        avg_time = self.get_average_duration()
        if avg_time:
            insight["average_time"] = avg_time
        challenge = self.hazard_challenge()
        if challenge:
            insight["hazard_challenge"] = challenge
        return insight

