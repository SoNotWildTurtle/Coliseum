"""Moderation checks for AI-driven content."""

class AIModerationManager:
    """Use simple rules to flag toxic chat messages."""

    def __init__(self, banned_words=None):
        self.banned_words = set(banned_words or [])
        self.flags = []

    def check(self, message: str) -> bool:
        for word in self.banned_words:
            if word in message.lower():
                self.flags.append(message)
                return True
        return False

    def flagged(self):
        return list(self.flags)
