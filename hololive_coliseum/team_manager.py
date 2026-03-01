"""Assign entities to teams and check ally relationships."""

from __future__ import annotations

class TeamManager:
    """Track team memberships to prevent friendly fire."""

    def __init__(self) -> None:
        self._teams: dict[object, int] = {}

    def set_team(self, actor: object, team: int) -> None:
        """Assign ``actor`` to ``team`` and tag it with a ``team`` attribute."""
        self._teams[actor] = team
        setattr(actor, "team", team)

    def get_team(self, actor: object) -> int | None:
        """Return the team for ``actor`` if known."""
        return self._teams.get(actor, getattr(actor, "team", None))

    def are_allies(self, a: object, b: object) -> bool:
        """True if both actors share the same team id."""
        return self.get_team(a) == self.get_team(b)

    def remove(self, actor: object) -> None:
        """Remove ``actor`` from tracking."""
        self._teams.pop(actor, None)
