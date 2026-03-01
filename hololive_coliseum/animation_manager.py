"""Sprite animation orchestration."""

class AnimationManager:
    """Track simple animation states and frames."""

    def __init__(self) -> None:
        self.state = "idle"
        self.frame = 0

    def set_state(self, state: str) -> None:
        if state != self.state:
            self.state = state
            self.frame = 0

    def update(self) -> None:
        self.frame += 1
