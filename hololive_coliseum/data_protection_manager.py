"""Encryption and signing helpers for network packets."""

import hmac
import hashlib
import json
import os
import time
import uuid
from typing import Any, Callable

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .transmission_manager import TransmissionManager


class DataProtectionManager:
    """Manage packet encryption, signing and basic replay protection."""

    def __init__(
        self,
        key: bytes | None = None,
        secret: bytes | None = None,
        level: int = 6,
        algorithm: str = "zlib",
        sign_key=None,
        max_age: float = 5.0,
        time_func: Callable[[], float] | None = None,
        sanitize_fields: set[str] | None = None,
    ) -> None:
        self.key = key
        self.secret = secret
        aes_key = hashlib.blake2s(key).digest() if key else None
        self._aesgcm = AESGCM(aes_key) if aes_key else None
        self.tx = TransmissionManager(level=level, algorithm=algorithm, sign_key=sign_key)
        self._nonces: set[str] = set()
        self.max_age = max_age
        self.time = time_func or time.time
        self.sanitize_fields = sanitize_fields or set()

    def encrypt(self, data: bytes) -> bytes:
        """Return ``data`` encrypted with AES-GCM using ``key``."""
        if not self._aesgcm:
            return data
        nonce = os.urandom(12)
        return nonce + self._aesgcm.encrypt(nonce, data, None)

    def decrypt(self, data: bytes) -> bytes:
        """Decrypt ``data`` encrypted via :meth:`encrypt`."""
        if not self._aesgcm:
            return data
        nonce, payload = data[:12], data[12:]
        return self._aesgcm.decrypt(nonce, payload, None)

    def _sign(self, msg: dict[str, Any]) -> str:
        raw = json.dumps(msg, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hmac.new(self.secret or b"", raw, hashlib.sha256).hexdigest()

    def _sanitize(self, msg: dict[str, Any]) -> None:
        """Remove sensitive fields from ``msg`` before encoding."""
        for field in self.sanitize_fields:
            msg.pop(field, None)

    def encode(self, msg: dict[str, Any]) -> bytes:
        """Compress and sign ``msg`` for transmission."""
        msg = msg.copy()
        self._sanitize(msg)
        msg["nonce"] = uuid.uuid4().hex
        msg["ts"] = int(self.time())
        if self.secret is not None:
            msg["sig"] = self._sign(msg)
        packet = self.tx.compress(msg)
        return self.encrypt(packet)

    def decode(self, packet: bytes) -> dict[str, Any] | None:
        """Return the decoded packet or ``None`` if verification fails."""
        try:
            packet = self.decrypt(packet)
        except Exception:
            return None
        msg = self.tx.decompress(packet)
        if msg is None:
            return None
        if self.secret is not None:
            sig = msg.pop("sig", None)
            if sig is None or not hmac.compare_digest(self._sign(msg), sig):
                return None
        nonce = msg.pop("nonce", None)
        ts = msg.pop("ts", None)
        if ts is None or self.time() - ts > self.max_age:
            return None
        if nonce is None or nonce in self._nonces:
            return None
        self._nonces.add(nonce)
        return msg

    def rotate_keys(
        self,
        key: bytes | None = None,
        secret: bytes | None = None,
        sign_key=None,
    ) -> None:
        """Replace encryption or signing keys and clear cached nonces."""
        if key is not None:
            self.key = key
            aes_key = hashlib.blake2s(key).digest()
            self._aesgcm = AESGCM(aes_key)
        if secret is not None:
            self.secret = secret
        if sign_key is not None:
            self.tx.sign_key = sign_key
        self._nonces.clear()
