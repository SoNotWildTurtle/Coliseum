"""Status buff tracking and application."""

from .status_effects import StatusEffectManager

class BuffManager:
    """Wrapper managing buff and debuff status effects."""

    def __init__(self) -> None:
        self.manager = StatusEffectManager()

    def add_buff(self, target, effect) -> None:
        self.manager.add_effect(target, effect)

    def update(self, now: int | None = None) -> None:
        self.manager.update(now)
