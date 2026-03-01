"""Generate basic skills for player classes."""

class SkillGenerator:
    """Create skill templates for classes."""

    def generate(self, class_name: str, base_attack: float) -> list[dict[str, float]]:
        """Return a list of skills scaled from a base attack value."""
        damage = base_attack * 1.5
        return [{"name": f"{class_name} Strike", "damage": damage}]
