"""Player housing management and upgrades."""

class HousingManager:
    """Track player houses and data."""
    def __init__(self):
        self.houses = {}

    def add_house(self, player_id: str, data) -> None:
        self.houses[player_id] = data

    def get_house(self, player_id: str):
        return self.houses.get(player_id)
