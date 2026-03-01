"""Voice chat channel management helpers."""

class VoiceChatManager:
    """Track users joined to voice chat channels."""

    def __init__(self):
        self.channels = {}

    def join(self, user: str, channel: str) -> None:
        self.channels.setdefault(channel, set()).add(user)

    def leave(self, user: str, channel: str) -> None:
        if channel in self.channels:
            self.channels[channel].discard(user)
            if not self.channels[channel]:
                del self.channels[channel]
