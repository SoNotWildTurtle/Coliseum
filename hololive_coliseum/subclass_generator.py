"""Generate subclasses from base class templates."""

class SubclassGenerator:
    """Produce subclass definitions with simple stat tweaks."""

    def create(self, base: dict[str, int], variant: str) -> dict[str, int]:
        """Return a subclass dict with a modified name and attack value."""
        stats = base.copy()
        stats["name"] = f"{variant} {base['name']}"
        stats["attack"] = base.get("attack", 0) + 1
        return stats
