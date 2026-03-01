"""Mana tracking and regeneration utilities."""

class ManaManager:
    """Track and spend a character's mana resource."""

    def __init__(self, max_mana: int) -> None:
        self.max_mana = max_mana
        self.mana = max_mana

    def use(self, amount: int) -> bool:
        """Attempt to spend mana, returning True if enough was available."""
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False

    def regen(self, amount: int) -> int:
        """Regenerate mana and return the new value."""
        self.mana = min(self.max_mana, self.mana + amount)
        return self.mana
