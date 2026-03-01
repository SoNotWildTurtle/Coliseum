"""Game event scheduling and dispatch helpers."""

class EventManager:
    """Track triggered world events."""
    def __init__(self):
        self.history = []

    def trigger(self, name: str) -> None:
        self.history.append(name)

    def get_history(self):
        return list(self.history)
