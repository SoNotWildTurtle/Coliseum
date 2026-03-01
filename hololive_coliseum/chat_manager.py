"""Chat channel routing and message handling."""

class ChatManager:
    """Manage an in-game chat box with message history."""

    def __init__(self, max_messages: int = 50):
        self.max_messages = max_messages
        self.messages: list[tuple[str, str]] = []
        self.open = False

    def toggle(self) -> None:
        self.open = not self.open

    def show(self) -> None:
        self.open = True

    def hide(self) -> None:
        self.open = False

    def send(self, user: str, msg: str) -> None:
        self.messages.append((user, msg))
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def history(self, limit: int | None = None):
        if limit is None:
            return list(self.messages)
        return self.messages[-limit:]

    def clear(self) -> None:
        self.messages.clear()
