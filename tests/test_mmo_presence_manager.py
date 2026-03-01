"""Tests for mmo presence manager."""

from hololive_coliseum.mmo_presence_manager import MMOPresenceManager


def test_presence_tracks_and_prunes():
    manager = MMOPresenceManager(timeout_ms=100)
    manager.seen("alpha", (1.25, 2.5), now=10)
    assert manager.positions["alpha"] == (1.25, 2.5)
    assert manager.prune(50) == []
    removed = manager.prune(200)
    assert removed == ["alpha"]
    assert manager.count() == 0


def test_presence_drop_removes_entries():
    manager = MMOPresenceManager(timeout_ms=100)
    manager.seen("alpha", (0.0, 0.0), now=0)
    assert manager.drop("alpha") is True
    assert manager.drop("alpha") is False
