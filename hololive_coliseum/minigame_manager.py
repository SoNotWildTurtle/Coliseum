"""Mini-games that award bonuses for quick reactions."""


class ReactionMinigame:
    """Reaction test that awards a crafting material on success."""

    def __init__(
        self, target_ms: int, material: str, inventory, tolerance: int = 100
    ) -> None:
        self.target_ms = target_ms
        self.material = material
        self.inventory = inventory
        self.tolerance = tolerance

    def attempt(self, reaction_ms: int) -> str | None:
        """Add the material to ``inventory`` when timing is close enough."""
        if abs(self.target_ms - reaction_ms) <= self.tolerance:
            self.inventory.add(self.material)
            return self.material
        return None


class MinigameManager:
    """Run small standalone mini-games."""

    def play_reaction(
        self, target_ms: int, reaction_ms: int, material: str, inventory
    ) -> str | None:
        """Play a reaction game and award a crafting material on success."""
        game = ReactionMinigame(target_ms, material, inventory)
        return game.attempt(reaction_ms)
