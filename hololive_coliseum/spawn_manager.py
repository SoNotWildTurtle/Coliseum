"""Spawn timing and entity placement helpers."""

class SpawnManager:
    """Schedule NPC or item spawns."""
    def __init__(self):
        self.spawns: list[tuple[int, object]] = []

    def schedule(self, obj, time_ms: int) -> None:
        self.spawns.append((time_ms, obj))

    def get_ready(self, now: int):
        ready = [o for t, o in self.spawns if t <= now]
        self.spawns = [(t, o) for t, o in self.spawns if t > now]
        return ready

    def clear(self) -> None:
        """Remove all scheduled spawns."""
        self.spawns.clear()
