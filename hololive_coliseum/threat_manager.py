"""Threat evaluation and encounter scaling."""

class ThreatManager:
    """Maintain simple threat tables for AI focus."""

    def __init__(self) -> None:
        self.table: dict = {}

    def add_threat(self, actor, amount: int) -> None:
        self.table[actor] = self.table.get(actor, 0) + amount

    def highest_threat(self):
        if not self.table:
            return None
        return max(self.table, key=self.table.get)
