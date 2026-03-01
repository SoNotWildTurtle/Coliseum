"""Auto-generate skills using level and stat inputs."""


class AutoSkillManager:
    """Generate skills based on level and stats."""

    def __init__(self) -> None:
        self.generated: dict[str, dict] = {}

    def generate(self, base_name: str, level: int, stats: dict[str, int]) -> dict:
        """Return a new skill dict using ``level`` and ``stats`` values."""
        power = stats.get("attack", 0) + level * 2
        skill = {"name": f"{base_name} Lv{level}", "power": power}
        self.generated[base_name] = skill
        return skill
