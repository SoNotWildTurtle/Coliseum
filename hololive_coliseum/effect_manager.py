"""Visual effect orchestration."""

class EffectManager:
    """Track triggered visual effects."""

    def __init__(self):
        self.active = []

    def trigger(self, effect: str) -> None:
        self.active.append(effect)
