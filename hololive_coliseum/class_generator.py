"""Generate unique MMO class templates."""

class ClassGenerator:
    """Create class definitions while ensuring unique names."""

    def __init__(self) -> None:
        self._used: set[str] = set()

    def create(self, name: str, stats: dict[str, int]) -> dict[str, int]:
        """Return a class record with a unique ``name`` field."""
        base = name
        suffix = 1
        while name in self._used:
            name = f"{base}{suffix}"
            suffix += 1
        self._used.add(name)
        data = dict(stats)
        data["name"] = name
        return data
