"""Track MMO player experience and levels."""

from __future__ import annotations

from typing import Dict

from .experience_manager import ExperienceManager


class LevelingManager:
    """Store :class:`ExperienceManager` instances for MMO players."""

    def __init__(self) -> None:
        # map of player_id to their experience data
        self._players: Dict[str, ExperienceManager] = {}

    def _get_mgr(self, player_id: str) -> ExperienceManager:
        """Return the experience manager for ``player_id`` creating one if needed."""
        if player_id not in self._players:
            self._players[player_id] = ExperienceManager()
        return self._players[player_id]

    def add_xp(self, player_id: str, amount: int) -> bool:
        """Add ``amount`` experience and return True if a level up occurred."""
        return self._get_mgr(player_id).add_xp(amount)

    def get_level(self, player_id: str) -> int:
        """Return the current level for ``player_id``."""
        return self._get_mgr(player_id).level

    def get_xp(self, player_id: str) -> int:
        """Return the current experience for ``player_id``."""
        return self._get_mgr(player_id).xp
