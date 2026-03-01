"""Onboarding flow and tutorial tracking."""

class OnboardingManager:
    """Guide new players through initial setup."""

    def __init__(self):
        self.steps_shown = []

    def show(self, step: str) -> None:
        self.steps_shown.append(step)

    def history(self):
        return list(self.steps_shown)
