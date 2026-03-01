"""Bot orchestration and lifecycle helpers."""

class BotManager:
    """Spawn and update automated bot players for testing."""

    def __init__(self):
        self.bots = []

    def add_bot(self, name: str) -> None:
        self.bots.append(name)

    def remove_bot(self, name: str) -> None:
        if name in self.bots:
            self.bots.remove(name)

    def list_bots(self):
        return list(self.bots)
