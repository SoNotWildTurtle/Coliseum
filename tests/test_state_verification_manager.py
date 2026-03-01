"""Tests for state verification manager."""

from hololive_coliseum.state_verification_manager import StateVerificationManager
from hololive_coliseum.shared_state_manager import SharedStateManager
import pytest


def test_state_verification_roundtrip():
    verifier = StateVerificationManager()
    a = SharedStateManager(verifier=verifier)
    delta = a.update(score=5)
    assert "verify" in delta
    b = SharedStateManager(verifier=verifier)
    state = b.apply(delta)
    assert state["score"] == 5


def test_state_verification_detects_tamper():
    verifier = StateVerificationManager()
    a = SharedStateManager(verifier=verifier)
    delta = a.update(score=1)
    tampered = delta.copy()
    tampered["score"] = 2
    b = SharedStateManager(verifier=verifier)
    with pytest.raises(ValueError):
        b.apply(tampered)
