"""Tests for score manager."""

from hololive_coliseum.score_manager import ScoreManager


def test_score_manager():
    manager = ScoreManager(5)
    manager.add(3)
    manager.add(4)
    assert manager.score == 7
    manager.finalize()
    assert manager.best_score == 7
    manager.reset()
    assert manager.score == 0


def test_score_manager_combo():
    manager = ScoreManager()
    manager.record_kill(0.0)
    assert manager.score == 10 and manager.combo == 1
    manager.record_kill(1.0)
    assert manager.score == 30 and manager.combo == 2
    manager.update(5.0)
    assert manager.combo == 0
