"""Faction reputation tracking and rewards."""

class ReputationManager:
    """Track faction reputation values for long-term progression."""

    def __init__(self) -> None:
        self.rep: dict[str, int] = {}

    def modify(self, faction: str, amount: int) -> int:
        """Adjust reputation for ``faction`` and return the new value."""

        self.rep[faction] = self.rep.get(faction, 0) + amount
        return self.rep[faction]

    def get(self, faction: str) -> int:
        """Return the current reputation score for ``faction``."""

        return self.rep.get(faction, 0)

    def top(self, limit: int = 3) -> list[tuple[str, int]]:
        """Return the leading factions sorted by reputation."""

        return sorted(self.rep.items(), key=lambda item: item[1], reverse=True)[:limit]

    def to_dict(self) -> dict[str, int]:
        """Serialize stored reputation values."""

        return dict(self.rep)

    def load_from_dict(self, data: dict[str, int]) -> None:
        """Restore reputation values from ``data``."""

        self.rep = {k: int(v) for k, v in data.items()}
