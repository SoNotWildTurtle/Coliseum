"""Emote definitions and playback helpers."""

class EmoteManager:
    """Keep a table of available emotes."""

    def __init__(self):
        self.emotes = {"wave": ":)", "dance": "<(^_^<)"}

    def get(self, name: str):
        return self.emotes.get(name)

    def add(self, name: str, value: str) -> None:
        self.emotes[name] = value
