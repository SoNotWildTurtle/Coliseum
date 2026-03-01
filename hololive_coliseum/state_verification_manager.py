"""State validation and verification checks."""

from __future__ import annotations

"""Low-memory helpers for verifying shared game state.

This manager computes compact hashes of arbitrary dictionaries so networked
clients can confirm they share the same state without storing entire history.
Two algorithms are provided: a fast CRC32 checksum and a stronger SHA256 hash.
"""

from typing import Any, Dict
import json
import zlib
import hashlib


class StateVerificationManager:
    """Compute checksums and hashes for verifying game state."""

    def _encode(self, state: Dict[str, Any]) -> bytes:
        """Return a deterministic byte representation of ``state``."""
        return json.dumps(state, sort_keys=True, separators=(",", ":")).encode()

    def compute(self, state: Dict[str, Any]) -> Dict[str, str]:
        """Return CRC32 and SHA256 digests for ``state``."""
        payload = self._encode(state)
        crc = zlib.crc32(payload) & 0xFFFFFFFF
        sha = hashlib.sha256(payload).hexdigest()
        return {"crc32": f"{crc:08x}", "sha256": sha}

    def verify(self, state: Dict[str, Any], digests: Dict[str, str]) -> bool:
        """Return True if ``state`` matches provided ``digests``."""
        expected = self.compute(state)
        return (
            digests.get("crc32") == expected["crc32"]
            and digests.get("sha256") == expected["sha256"]
        )
