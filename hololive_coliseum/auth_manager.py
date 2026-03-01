"""Authentication helper storing salted password hashes and expiring tokens."""

from __future__ import annotations

import hashlib
import secrets
import time
from typing import Callable, Dict, Tuple


class AuthManager:
    """Handle account credentials with hashed passwords and login limits."""

    def __init__(
        self,
        max_attempts: int = 3,
        token_lifetime: int = 3600,
        time_func: Callable[[], float] | None = None,
    ) -> None:
        self.users: Dict[str, Dict[str, str]] = {}
        self.tokens: Dict[str, Tuple[str, float]] = {}
        self.attempts: Dict[str, int] = {}
        self.max_attempts = max_attempts
        self.token_lifetime = token_lifetime
        self.time_func = time_func or time.time

    @staticmethod
    def _hash(password: str, salt: str) -> str:
        """Return a PBKDF2 hash for ``password`` and ``salt``."""
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt), 100000
        )
        return digest.hex()

    def register(self, username: str, password: str) -> None:
        """Store a salted password hash for ``username``."""
        salt = secrets.token_hex(16)
        self.users[username] = {"salt": salt, "hash": self._hash(password, salt)}
        self.attempts.pop(username, None)

    def login(self, username: str, password: str) -> str | None:
        """Return a session token when credentials are valid."""
        record = self.users.get(username)
        if not record:
            return None
        if self.attempts.get(username, 0) >= self.max_attempts:
            return None
        if secrets.compare_digest(
            self._hash(password, record["salt"]), record["hash"]
        ):
            token = f"{username}-token"
            expiry = self.time_func() + self.token_lifetime
            self.tokens[token] = (username, expiry)
            self.attempts[username] = 0
            return token
        self.attempts[username] = self.attempts.get(username, 0) + 1
        return None

    def verify(self, token: str) -> bool:
        """Return ``True`` if ``token`` exists and hasn't expired."""
        record = self.tokens.get(token)
        if not record:
            return False
        if self.time_func() > record[1]:
            self.tokens.pop(token, None)
            return False
        return True

    def logout(self, token: str) -> None:
        """Invalidate ``token`` if it exists."""
        self.tokens.pop(token, None)
