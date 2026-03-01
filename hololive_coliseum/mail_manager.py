"""In-game mail delivery and retrieval."""

class MailManager:
    """Simple per-user mailbox."""
    def __init__(self):
        self.boxes = {}

    def send_mail(self, to: str, message: str) -> None:
        self.boxes.setdefault(to, []).append(message)

    def inbox(self, user: str):
        return list(self.boxes.get(user, []))

    def clear(self, user: str) -> None:
        self.boxes.pop(user, None)
