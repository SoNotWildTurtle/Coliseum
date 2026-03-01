"""Handle weekly blockchain votes exposed through the menu system."""

from __future__ import annotations

import json
import os
import random
import time
from typing import Any, Dict, List, Sequence

from .blockchain import add_vote, load_chain

SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'SavedGames')
VOTE_FILE = os.path.join(SAVE_DIR, 'votes.json')
WEEK_SECONDS = 7 * 24 * 60 * 60


DEFAULT_CATEGORY = "character"


def _normalize_votes(raw: Any) -> Dict[str, Dict[str, int]]:
    """Return a mapping of account IDs to per-category vote timestamps."""

    if not isinstance(raw, dict):
        return {}
    normalized: Dict[str, Dict[str, int]] = {}
    for account, value in raw.items():
        account_key = str(account)
        per_category: Dict[str, int] = {}
        if isinstance(value, dict):
            for category, timestamp in value.items():
                if isinstance(timestamp, (int, float)):
                    per_category[str(category)] = int(timestamp)
        elif isinstance(value, (int, float)):
            per_category[DEFAULT_CATEGORY] = int(value)
        if per_category:
            normalized[account_key] = per_category
    return normalized


def _load_votes() -> Dict[str, Dict[str, int]]:
    if os.path.exists(VOTE_FILE):
        try:
            with open(VOTE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
        return _normalize_votes(data)
    return {}


def _save_votes(data: Dict[str, Dict[str, int]]) -> None:
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(VOTE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f)


class VotingManager:
    """Provide weekly voting for a given category with per-category cooldowns."""

    def __init__(
        self,
        choices: Sequence[str] | None = None,
        category: str = "character",
    ) -> None:
        self._votes = _load_votes()
        self._choices = list(choices) if choices else None
        self.category = category

    def get_options(self, limit: int = 3) -> List[str]:
        """Return ``limit`` random characters for the weekly vote.

        When ``characters`` were supplied to the constructor the sample is taken
        from that list. Otherwise the function scans seed blocks for all
        characters that have appeared in matches and shuffles the result.
        """
        if self._choices is not None:
            population = list(self._choices)
        elif self.category == "character":
            counts: Dict[str, int] = {}
            for block in load_chain():
                if block.get('type') == 'seed' or block.get('characters'):
                    for name in block.get('characters', []):
                        counts[name] = counts.get(name, 0) + 1
            population = list(counts)
        else:
            population = []
        random.shuffle(population)
        return population[:limit]

    def can_vote(self, account_id: str) -> bool:
        """Return ``True`` if ``account_id`` has not voted in the last week."""
        account_votes = self._votes.get(account_id, {})
        last = account_votes.get(self.category, 0)
        return time.time() - last >= WEEK_SECONDS

    def cast_vote(self, account_id: str, choice: str) -> Dict[str, object]:
        """Record ``choice`` for ``account_id`` and return the vote block."""
        if not self.can_vote(account_id):
            raise ValueError("vote already cast this week")
        block = add_vote(account_id, choice, self.category)
        account_votes = self._votes.setdefault(account_id, {})
        account_votes[self.category] = int(time.time())
        _save_votes(self._votes)
        return block

    def get_vote_counts(
        self, include_choices: Sequence[str] | None = None
    ) -> Dict[str, int]:
        """Return aggregated vote totals for the managed category."""

        counts: Dict[str, int] = {}
        for block in load_chain():
            if block.get('type') != 'vote' or block.get('category') != self.category:
                continue
            choice = block.get('choice')
            if choice:
                counts[choice] = counts.get(choice, 0) + 1
        if include_choices is not None:
            for choice in include_choices:
                counts.setdefault(choice, 0)
        return counts

    def get_winner(self) -> str | None:
        """Return the most-voted option or ``None`` when no ballots exist."""

        counts = self.get_vote_counts()
        if not counts:
            return None
        return max(counts, key=counts.get)
