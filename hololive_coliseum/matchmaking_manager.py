"""Matchmaking queue and pairing helpers."""

class MatchmakingManager:
    """Pair players into groups for matches."""

    def __init__(self) -> None:
        self.queue: list[str] = []

    def join(self, player_id: str) -> None:
        if player_id not in self.queue:
            self.queue.append(player_id)

    def leave(self, player_id: str) -> None:
        if player_id in self.queue:
            self.queue.remove(player_id)

    def match(self, size: int = 2) -> list[str] | None:
        if len(self.queue) >= size:
            group = self.queue[:size]
            self.queue = self.queue[size:]
            return group
        return None
