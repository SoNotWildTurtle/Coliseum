"""Season timing and rewards management."""

class SeasonManager:
    """Track the current season and reset logic."""

    def __init__(self, season: int = 1):
        self.season = season

    def next_season(self) -> None:
        self.season += 1

    def current(self) -> int:
        return self.season
