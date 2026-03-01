"""Store proof-of-work hashes as seeds for future MMO world generation."""

from __future__ import annotations

import json
import os
from typing import List

from .blockchain import load_chain

SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'SavedGames')
SEED_FILE = os.path.join(SAVE_DIR, 'seeds.json')
os.makedirs(SAVE_DIR, exist_ok=True)


def load_seeds() -> List[str]:
    """Return the saved list of world seeds."""
    if os.path.exists(SEED_FILE):
        try:
            with open(SEED_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_seeds(seeds: List[str]) -> None:
    """Persist ``seeds`` to disk."""
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(SEED_FILE, 'w', encoding='utf-8') as f:
        json.dump(seeds, f)


class WorldSeedManager:
    """Collect hashes from background mining to seed future MMO worlds."""

    def __init__(self) -> None:
        self.seeds: List[str] = load_seeds()

    def add_seed(self, seed: str) -> None:
        """Store ``seed`` and persist it."""
        self.seeds.append(seed)
        save_seeds(self.seeds)

    def get_seeds(self) -> List[str]:
        """Return a copy of collected seeds."""
        return list(self.seeds)

    def sync_with_blockchain(self) -> None:
        """Merge any seed blocks from the blockchain into local storage."""

        for block in load_chain():
            if block.get('type') == 'seed':
                seed = block.get('seed')
                if seed not in self.seeds:
                    self.seeds.append(seed)
        save_seeds(self.seeds)
