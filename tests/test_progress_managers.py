"""Tests for progress managers."""

from hololive_coliseum.quest_manager import QuestManager
from hololive_coliseum.achievement_manager import AchievementManager


def test_quest_manager_basic():
    qm = QuestManager()
    qm.add('q1', 'Collect things')
    qm.update_progress('q1', 2)
    assert qm.get_progress('q1') == 2
    qm.complete('q1')
    assert qm.is_completed('q1')
    assert 'q1' not in qm.active


def test_achievement_manager_roundtrip():
    am = AchievementManager()
    am.unlock('first')
    assert am.is_unlocked('first')
    data = am.to_dict()
    am.unlock('second')
    am.load_from_dict(data)
    assert am.is_unlocked('first')
    assert not am.is_unlocked('second')

