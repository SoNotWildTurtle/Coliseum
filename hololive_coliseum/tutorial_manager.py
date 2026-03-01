"""Tutorial sequencing and completion tracking."""

class TutorialManager:
    """Track steps completed in the tutorial."""

    def __init__(self):
        self.steps = []

    def complete_step(self, step: str) -> None:
        self.steps.append(step)

    def progress(self):
        return list(self.steps)
