"""Pet companion management and upgrades."""

class PetManager:
    """Manage collectible pets for each player."""
    def __init__(self):
        self.pets = {}

    def add_pet(self, player_id: str, pet: str) -> None:
        self.pets.setdefault(player_id, []).append(pet)

    def list_pets(self, player_id: str):
        return self.pets.get(player_id, [])
