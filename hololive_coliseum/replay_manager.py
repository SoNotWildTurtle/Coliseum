"""Replay capture and playback helpers."""

class ReplayManager:
    """Store and retrieve match replays."""

    def __init__(self):
        self.replays = []

    def record(self, data: dict) -> None:
        self.replays.append(data)

    def list_replays(self):
        return list(self.replays)
