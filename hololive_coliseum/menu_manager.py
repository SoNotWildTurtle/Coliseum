"""Menu state, selection, and navigation helpers."""

class MenuManager:
    """Track the current menu index and provide navigation helpers."""

    def __init__(self) -> None:
        self.index = 0

    def reset(self) -> None:
        """Reset the menu selection index to zero."""
        self.index = 0

    def move(self, direction: int, count: int) -> None:
        """Move the selection index up or down within ``count`` options."""
        if count:
            self.index = (self.index + direction) % count
