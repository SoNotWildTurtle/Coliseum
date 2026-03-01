"""Shared state storage across subsystems."""

from __future__ import annotations

"""Helper for tracking shared game state.

This manager wraps :class:`StateSync` so gameplay modules can update a
central state dictionary and compute network deltas. Remote clients can
apply these deltas to stay in sync with minimal bandwidth usage.
"""

from typing import Any, Dict

from .state_sync import StateSync
from .state_verification_manager import StateVerificationManager


class SharedStateManager:
    """Store shared state and compute/apply deltas."""

    def __init__(
        self,
        tolerances: Dict[str, float] | None = None,
        verifier: StateVerificationManager | None = None,
    ) -> None:
        self.state: Dict[str, Any] = {}
        self._sync = StateSync(tolerances)
        self._verifier = verifier

    def update(self, **changes: Any) -> Dict[str, Any]:
        """Apply ``changes`` and return the delta for networking."""
        self.state.update(changes)
        delta = self._sync.encode(self.state)
        delta["type"] = "state"
        if self._verifier is not None:
            delta["verify"] = self._verifier.compute(self.state)
        return delta

    def apply(self, delta: Dict[str, Any]) -> Dict[str, Any]:
        """Merge a delta from the network into the current state."""
        delta = delta.copy()
        delta.pop("type", None)
        verify = delta.pop("verify", None)
        self.state = self._sync.apply(delta)
        if verify and self._verifier and not self._verifier.verify(self.state, verify):
            raise ValueError("state verification failed")
        return self.state.copy()

    def load_snapshot(self, snapshot: Dict[str, Any], sequence: int | None = None) -> Dict[str, Any]:
        """Replace the current state with ``snapshot`` and update the sequence."""

        self.state = dict(snapshot)
        self._sync.last_state = self.state.copy()
        if sequence is not None:
            self._sync.seq = int(sequence)
        return self.state.copy()

    def current_sequence(self) -> int:
        """Return the latest sequence number used for delta generation."""

        return int(getattr(self._sync, "seq", 0))
