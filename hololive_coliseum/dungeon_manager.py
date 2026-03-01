"""Dungeon encounter orchestration."""

class DungeonManager:
    """Handle dungeon lockouts for players."""
    def __init__(self):
        self.lockouts = {}

    def set_lockout(self, player_id: str, dungeon: str, expires: int) -> None:
        self.lockouts[(player_id, dungeon)] = expires

    def can_enter(self, player_id: str, dungeon: str, now: int) -> bool:
        end = self.lockouts.get((player_id, dungeon))
        return end is None or now >= end
