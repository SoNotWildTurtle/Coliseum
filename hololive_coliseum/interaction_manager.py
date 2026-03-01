"""Manage simple interactable actions."""

class InteractionManager:
    """Register interactions and trigger their responses."""

    def __init__(self) -> None:
        self._actions: dict[str, str] = {}

    def register(self, interaction: dict[str, str]) -> None:
        """Store an interaction record."""
        self._actions[interaction["name"]] = interaction["message"]

    def interact(self, name: str) -> str:
        """Return the message for the given interaction name."""
        return self._actions.get(name, "")
