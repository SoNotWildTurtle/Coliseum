"""Companion entity management."""

class CompanionManager:
    """Assign a single companion to each player."""
    def __init__(self):
        self.companions = {}

    def assign(self, player_id: str, companion: str) -> None:
        self.companions[player_id] = companion

    def get(self, player_id: str):
        return self.companions.get(player_id)
