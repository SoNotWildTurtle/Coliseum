"""Skill definitions and cooldown tracking."""

class Skill:
    """Simple callable skill with a cooldown."""
    def __init__(self, cooldown_ms: int, execute):
        self.cooldown = cooldown_ms
        self.execute = execute
        self.last_used = -cooldown_ms

class SkillManager:
    """Manage a set of named skills and their cooldown timers."""
    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, name: str, cooldown_ms: int, callback) -> None:
        """Add a new skill."""
        self._skills[name] = Skill(cooldown_ms, callback)

    def use(self, name: str, now: int, *args, **kwargs):
        """Attempt to use a skill if its cooldown has elapsed."""
        skill = self._skills.get(name)
        if not skill:
            return None
        if now - skill.last_used >= skill.cooldown:
            skill.last_used = now
            return skill.execute(now, *args, **kwargs)
        return None
