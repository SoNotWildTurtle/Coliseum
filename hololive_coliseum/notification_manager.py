"""Player notification routing and throttling."""

class NotificationManager:
    """Manage popup notifications for the UI."""

    def __init__(self):
        self.queue = []

    def push(self, message: str) -> None:
        self.queue.append(message)

    def pop(self):
        return self.queue.pop(0) if self.queue else None
