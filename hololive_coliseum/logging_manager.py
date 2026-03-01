"""Centralized logging for gameplay events."""

class LoggingManager:
    """Collect log events for later analysis."""

    def __init__(self):
        self.events = []

    def log(self, event: str) -> None:
        self.events.append(event)
