"""Generate simple interactable templates."""

class InteractionGenerator:
    """Create interaction records with unique names."""

    def __init__(self) -> None:
        self._used: set[str] = set()

    def create(self, base_name: str, message: str) -> dict[str, str]:
        """Return an interaction dict with a unique ``name`` and ``message``."""
        name = base_name
        suffix = 1
        while name in self._used:
            name = f"{base_name}{suffix}"
            suffix += 1
        self._used.add(name)
        return {"name": name, "message": message}
