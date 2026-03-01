"""Tests for shared state manager."""

from hololive_coliseum.shared_state_manager import SharedStateManager


def test_shared_state_manager_roundtrip():
    a = SharedStateManager()
    delta = a.update(score=1)
    b = SharedStateManager()
    state = b.apply(delta)
    assert state["score"] == 1
    delta2 = a.update(score=2)
    state2 = b.apply(delta2)
    assert state2["score"] == 2
