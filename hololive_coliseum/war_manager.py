"""War event coordination and outcomes."""

class WarManager:
    """Track faction war scores."""

    def __init__(self):
        self.scores = {}

    def add_points(self, faction: str, points: int) -> None:
        self.scores[faction] = self.scores.get(faction, 0) + points

    def leading(self):
        return max(self.scores, key=self.scores.get) if self.scores else None
