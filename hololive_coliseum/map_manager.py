"""Map loading, selection, and metadata helpers."""

class MapManager:
    """Store available maps with hazard definitions and track the active one."""

    def __init__(self) -> None:
        self.maps: dict[str, dict] = {}
        self.current: str | None = None

    def add_map(self, name: str, data: dict) -> None:
        """Register a map with optional hazard metadata."""
        self.maps[name] = data

    def set_current(self, name: str) -> bool:
        """Select the active map and return ``True`` if it exists."""
        if name in self.maps:
            self.current = name
            return True
        return False

    def get_current(self) -> dict | None:
        """Return the data for the active map if any."""
        return self.maps.get(self.current)
