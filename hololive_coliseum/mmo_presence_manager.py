"""Track MMO peer presence and prune stale entries."""

from __future__ import annotations

from typing import Dict, Iterable, Tuple


class MMOPresenceManager:
    """Track remote player positions with a configurable timeout."""

    def __init__(self, timeout_ms: int = 6000) -> None:
        self.timeout_ms = int(timeout_ms)
        self.positions: Dict[str, Tuple[float, float]] = {}
        self.last_seen: Dict[str, int] = {}

    def seen(self, player_id: str, pos: tuple[float, float], now: int) -> None:
        """Record ``player_id`` at ``pos`` and update the last seen time."""
        self.positions[player_id] = (float(pos[0]), float(pos[1]))
        self.last_seen[player_id] = int(now)

    def prune(self, now: int) -> list[str]:
        """Remove entries older than ``timeout_ms`` and return removed ids."""
        if self.timeout_ms <= 0:
            return []
        cutoff = int(now) - self.timeout_ms
        removed: list[str] = []
        for player_id, last in list(self.last_seen.items()):
            if last < cutoff:
                removed.append(player_id)
                self.last_seen.pop(player_id, None)
                self.positions.pop(player_id, None)
        return removed

    def drop(self, player_id: str) -> bool:
        """Remove a tracked player and return True when removed."""
        removed = False
        if player_id in self.positions:
            self.positions.pop(player_id, None)
            removed = True
        if player_id in self.last_seen:
            self.last_seen.pop(player_id, None)
            removed = True
        return removed

    def count(self) -> int:
        """Return the number of tracked peers."""
        return len(self.positions)

    def items(self) -> Iterable[tuple[str, Tuple[float, float]]]:
        """Return an iterator over (player_id, position) pairs."""
        return self.positions.items()
