"""Analyze `.gguf` snapshot chains to mark completed goals.

This manager simulates running an auxiliary neural network over a series of
saved game snapshots.  For the prototype it simply searches for goal text
inside each `.gguf` file, but the structure allows a real model to be plugged
in later.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Dict


class GoalAnalysisManager:
    """Determines which goals have been satisfied by examining snapshots."""

    def __init__(self, goal_file: str | Path):
        self.goal_file = Path(goal_file)

    def analyze(self, snapshots: Iterable[str | Path]) -> Dict[str, bool]:
        """Return a mapping of goal text to completion status.

        Each snapshot is scanned for the goal text.  A real implementation
        could load the `.gguf` file into a neural network; the stub keeps the
        method lightweight for tests.
        """
        goals = self._load_goals()
        results: Dict[str, bool] = {g: False for g in goals}
        for snap in snapshots:
            path = Path(snap)
            if not path.exists():
                continue
            try:
                data = path.read_bytes()
            except OSError:
                continue
            for goal in goals:
                if goal.encode() in data:
                    results[goal] = True
        return results

    def _load_goals(self) -> list[str]:
        lines = self.goal_file.read_text().splitlines()
        goals = []
        for line in lines:
            if line.startswith("- [") and "] " in line:
                goals.append(line.split("] ", 1)[1].strip())
        return goals

    def mark_completed(self, completion: Dict[str, bool]) -> None:
        """Update the goal file, checking off completed goals."""
        lines = self.goal_file.read_text().splitlines()
        new_lines = []
        for line in lines:
            if line.startswith("- [") and "] " in line:
                prefix, text = line.split("] ", 1)
                text = text.strip()
                if completion.get(text):
                    line = "- [x] " + text
            new_lines.append(line)
        self.goal_file.write_text("\n".join(new_lines) + "\n")
