"""User account registry storing public keys and access levels."""

from __future__ import annotations

import json
import os
from typing import Any, Dict

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'SavedGames')
os.makedirs(SAVE_DIR, exist_ok=True)
ACCOUNTS_FILE = os.path.join(SAVE_DIR, 'accounts.json')
KEY_FILE_FMT = os.path.join(SAVE_DIR, '{}_key.pem')


class AccountsManager:
    """Manage user accounts stored in ``accounts.json``."""

    def __init__(self, path: str | None = None) -> None:
        self.path = path or ACCOUNTS_FILE

    def load(self) -> Dict[str, Dict[str, str]]:
        """Return saved account data mapping user IDs to level and key."""
        return _load_json(self.path, {})

    def save(self, data: Dict[str, Dict[str, str]]) -> None:
        _save_json(self.path, data)

    def register(self, user_id: str, level: str, public_key_pem: str) -> None:
        accounts = self.load()
        accounts[user_id] = {"level": level, "public_key": public_key_pem}
        self.save(accounts)

    def delete(self, user_id: str) -> None:
        accounts = self.load()
        if user_id in accounts:
            del accounts[user_id]
            self.save(accounts)

    def get(self, user_id: str) -> Dict[str, str] | None:
        return self.load().get(user_id)

    def renew_key(self, user_id: str) -> bytes:
        """Generate a new key pair for ``user_id`` and update the registry."""
        key = ed25519.Ed25519PrivateKey.generate()
        priv_bytes = key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
        with open(KEY_FILE_FMT.format(user_id), "wb") as f:
            f.write(priv_bytes)
        pub_pem = key.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
        accounts = self.load()
        level = accounts.get(user_id, {}).get("level", "user")
        accounts[user_id] = {"level": level, "public_key": pub_pem}
        self.save(accounts)
        return priv_bytes


def _load_json(path: str, default: Any) -> Any:
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return default
    return default


def _save_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


_DEFAULT_MANAGER = AccountsManager()


def load_accounts() -> Dict[str, Dict[str, str]]:
    """Return saved account data mapping user IDs to level and public key."""
    return _DEFAULT_MANAGER.load()


def save_accounts(data: Dict[str, Dict[str, str]]) -> None:
    _DEFAULT_MANAGER.save(data)


def register_account(user_id: str, level: str, public_key_pem: str) -> None:
    _DEFAULT_MANAGER.register(user_id, level, public_key_pem)


def delete_account(user_id: str) -> None:
    """Remove ``user_id`` from the registry if present."""
    _DEFAULT_MANAGER.delete(user_id)


def get_account(user_id: str) -> Dict[str, str] | None:
    return _DEFAULT_MANAGER.get(user_id)


def renew_key(user_id: str) -> bytes:
    """Regenerate ``user_id``'s key pair and update the registry."""
    return _DEFAULT_MANAGER.renew_key(user_id)


def load_private_key(user_id: str) -> bytes | None:
    """Return the PEM encoded private key for ``user_id`` if it exists."""
    path = KEY_FILE_FMT.format(user_id)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    return None
