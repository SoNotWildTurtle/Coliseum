"""Character appearance configuration and styling."""

class AppearanceManager:
    """Store visual appearance selections for entities."""

    def __init__(self) -> None:
        self.skins: dict = {}

    def set_skin(self, entity, skin: str) -> None:
        self.skins[entity] = skin

    def get_skin(self, entity) -> str | None:
        return self.skins.get(entity)
