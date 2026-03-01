"""Save per-run game state snapshots for future upgrades."""

from __future__ import annotations

import json
import os
import time
from typing import Any, List


class IterationManager:
    """Persist game state snapshots as timestamped `.gguf` files."""

    def __init__(self, directory: str | None = None) -> None:
        base = directory or os.path.join(os.path.dirname(__file__), '..', 'SavedGames', 'iterations')
        self.directory = os.path.abspath(base)
        os.makedirs(self.directory, exist_ok=True)

    def save(self, state: dict[str, Any]) -> str:
        """Save *state* to a new `.gguf` file and return its path."""
        ts = time.strftime('%Y%m%d-%H%M%S')
        path = os.path.join(self.directory, f'iteration_{ts}.gguf')
        os.makedirs(self.directory, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(state, f)
        return path

    def list(self) -> List[str]:
        """Return sorted paths of saved iteration files."""
        if not os.path.exists(self.directory):
            return []
        files = [
            os.path.join(self.directory, f)
            for f in os.listdir(self.directory)
            if f.endswith('.gguf')
        ]
        return sorted(files)

    def load(self, path: str) -> dict[str, Any]:
        """Load and return the snapshot stored at *path*."""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
