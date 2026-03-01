"""Data migration helpers for saves and config."""

class MigrationManager:
    """Handle player transfers between servers."""

    def __init__(self) -> None:
        self.pending: dict[str, str] = {}

    def request_transfer(self, user_id: str, dest: str) -> None:
        self.pending[user_id] = dest

    def complete_transfer(self, user_id: str) -> str | None:
        return self.pending.pop(user_id, None)
