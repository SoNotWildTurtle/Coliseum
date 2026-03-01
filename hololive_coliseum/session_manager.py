"""Session lifecycle and analytics hooks."""

import uuid

class SessionManager:
    """Track login sessions and prevent duplicates."""

    def __init__(self) -> None:
        self.sessions: dict[str, str] = {}

    def create(self, user_id: str) -> str:
        token = uuid.uuid4().hex
        self.sessions[token] = user_id
        return token

    def remove(self, token: str) -> None:
        self.sessions.pop(token, None)

    def get_user(self, token: str) -> str | None:
        return self.sessions.get(token)
