"""Weekly reset and rewards tracking."""

class WeeklyManager:
    """Track weekly challenges with reset functionality."""

    def __init__(self):
        self.challenges = {}

    def add(self, name: str) -> None:
        self.challenges[name] = False

    def complete(self, name: str) -> None:
        if name in self.challenges:
            self.challenges[name] = True

    def reset(self) -> None:
        for k in self.challenges:
            self.challenges[k] = False
