"""Track and transition high-level game state."""

class GameStateManager:
    """Simple helper to track the current and previous game states."""

    def __init__(self, initial: str = "splash") -> None:
        self.state = initial
        self.previous = None

    def change(self, state: str) -> None:
        """Set a new state, remembering the old one."""
        self.previous = self.state
        self.state = state

    def revert(self) -> None:
        """Return to the previous state if available."""
        if self.previous is not None:
            self.state, self.previous = self.previous, self.state
