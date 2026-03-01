"""Resource gathering flow and rewards."""

class GatheringManager:
    """Generate resource nodes and gather items via a timing mini-game."""

    def __init__(self, profession_manager, inventory) -> None:
        self.profession_manager = profession_manager
        self.inventory = inventory
        self.resources: dict[str, tuple[str, str]] = {}

    def add_resource(self, name: str, common: str, rare: str) -> None:
        """Register a gatherable resource with common and rare drops."""
        self.resources[name] = (common, rare)

    def gather(self, name: str, timing: float) -> str | None:
        """Gather ``name`` using ``timing`` between 0 and 1.

        Hitting close to ``0.5`` (within ``0.1``) yields the rare item and more
        profession experience; otherwise the common item is returned.
        Returns the gathered item or ``None`` if the resource is unknown."""
        items = self.resources.get(name)
        if not items:
            return None
        common, rare = items
        if abs(timing - 0.5) < 0.1:
            item, xp = rare, 20
        else:
            item, xp = common, 5
        self.inventory.add(item)
        self.profession_manager.gain_xp(name, xp)
        return item
