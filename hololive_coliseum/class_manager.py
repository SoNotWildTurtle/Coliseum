"""Class progression and class metadata management."""

class ClassManager:
    """Store MMO character classes and their base stats."""

    def __init__(self) -> None:
        self.classes: dict[str, dict[str, int]] = {}

    def add_class(self, name: str, stats: dict[str, int]) -> None:
        """Register a class with its starting stats.

        Raises:
            ValueError: If ``name`` is already registered.
        """
        if name in self.classes:
            raise ValueError(f"class '{name}' already exists")
        self.classes[name] = dict(stats)

    def get_stats(self, name: str) -> dict[str, int] | None:
        """Return the base stats for ``name`` if it exists."""
        return self.classes.get(name)

    def list_classes(self) -> list[str]:
        """Return a list of all registered class names."""
        return list(self.classes)
