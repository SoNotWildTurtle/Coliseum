"""Player stats aggregation and queries."""

class StatsManager:
    """Track base stats with temporary modifiers."""

    def __init__(self, base_stats: dict[str, int]):
        base_stats = base_stats.copy()
        base_stats.setdefault("crit_chance", 0)
        base_stats.setdefault("crit_multiplier", 2)
        self.base = base_stats
        self.mods: dict[str, int] = {stat: 0 for stat in base_stats}

    def apply_modifier(self, stat: str, amount: int) -> None:
        """Add a temporary modifier to a stat."""
        self.mods[stat] = self.mods.get(stat, 0) + amount

    def remove_modifier(self, stat: str, amount: int) -> None:
        """Remove part of a modifier from a stat."""
        self.mods[stat] = self.mods.get(stat, 0) - amount

    def get(self, stat: str) -> int:
        """Return the current value for ``stat``."""
        return self.base.get(stat, 0) + self.mods.get(stat, 0)

    def to_dict(self) -> dict[str, int]:
        """Return all stats including modifiers."""
        return {s: self.get(s) for s in self.base}
