"""State synchronization utilities for networking."""

from __future__ import annotations

from typing import Any, Dict

class StateSync:
    """Compute diffs between game state snapshots for efficient networking.

    Small floating‑point changes can be ignored by supplying per-field
    tolerances. This keeps packets tiny and reduces latency by avoiding
    updates for insignificant jitter.
    """

    def __init__(self, tolerances: Dict[str, float] | None = None) -> None:
        self.last_state: Dict[str, Any] = {}
        self.seq: int = 0
        self.tolerances: Dict[str, float] = tolerances or {}

    def _has_changed(self, key: str, prev: Any, new: Any) -> bool:
        """Return True if ``new`` differs from ``prev`` beyond tolerance."""
        if prev is None:
            return True
        if isinstance(new, (int, float)) and isinstance(prev, (int, float)):
            tol = self.tolerances.get(key, 0.0)
            return abs(new - prev) > tol
        return prev != new

    def encode(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Return the delta from the previous state with a sequence number."""
        self.seq += 1
        delta = {
            k: v
            for k, v in state.items()
            if self._has_changed(k, self.last_state.get(k), v)
        }
        delta["seq"] = self.seq
        self.last_state = state.copy()
        return delta

    def apply(self, delta: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a delta update and return the resulting state."""
        if "seq" in delta:
            self.seq = delta["seq"]
        for k, v in delta.items():
            if k == "seq":
                continue
            self.last_state[k] = v
        return self.last_state.copy()
