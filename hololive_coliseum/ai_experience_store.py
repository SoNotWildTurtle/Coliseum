"""Persist AI experience snapshots for analysis across playthroughs."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

from . import save_manager


class AIExperienceStore:
    """Append AI experience snapshots to disk for later review."""

    def __init__(self, path: str | os.PathLike[str] | None = None) -> None:
        if path is None:
            path = Path(save_manager.SAVE_DIR) / "ai_experiences.json"
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.history: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return
        if isinstance(data, list):
            self.history = data

    def _save(self) -> None:
        self.path.write_text(json.dumps(self.history, indent=2), encoding="utf-8")

    def append_snapshot(self, snapshot: dict[str, Any], *, keep: int = 200) -> None:
        """Append a new snapshot and prune history."""
        self.history.append(snapshot)
        if keep > 0 and len(self.history) > keep:
            self.history = self.history[-keep:]
        self._save()

    @staticmethod
    def build_snapshot(
        *,
        mode: str,
        difficulty: str,
        playthrough: int,
        level_index: int,
        ai_level: int,
        agents: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Create a structured snapshot entry."""
        return {
            "timestamp": time.time(),
            "mode": mode,
            "difficulty": difficulty,
            "playthrough": int(playthrough),
            "level_index": int(level_index),
            "ai_level": int(ai_level),
            "agents": agents,
        }
