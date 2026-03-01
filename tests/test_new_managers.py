"""Tests for new managers."""

import os
import sys
import pytest

pygame = pytest.importorskip("pygame")
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.combat_manager import CombatManager
from hololive_coliseum.damage_manager import DamageManager
from hololive_coliseum.threat_manager import ThreatManager
from hololive_coliseum.loot_manager import LootManager
from hololive_coliseum.buff_manager import BuffManager
from hololive_coliseum.status_effects import FreezeEffect

class Dummy:
    def __init__(self):
        self.hp = 100
        class V:
            x = 0
            y = 0
        self.velocity = V()
    def take_damage(self, amt):
        self.hp -= amt


def test_combat_manager_order():
    cm = CombatManager()
    cm.add("a")
    cm.add("b")
    cm.add("c")
    assert cm.next_actor() == "a"
    assert cm.next_actor() == "b"
    assert cm.next_actor() == "c"
    assert cm.next_actor() == "a"


def test_damage_manager_apply():
    dm = DamageManager()
    dummy = Dummy()
    dm.apply(dummy, 20, defense=5)
    assert dummy.hp == 85


def test_threat_manager_highest():
    tm = ThreatManager()
    tm.add_threat("p1", 5)
    tm.add_threat("p2", 10)
    assert tm.highest_threat() == "p2"


def test_loot_manager_roll(monkeypatch):
    lm = LootManager({"orc": ["gold", "axe"]})
    monkeypatch.setattr("random.choice", lambda seq: seq[1])
    assert lm.roll_loot("orc") == "axe"


def test_buff_manager_update():
    bm = BuffManager()
    dummy = Dummy()
    dummy.speed_factor = 1.0
    bm.add_buff(dummy, FreezeEffect(duration_ms=10))
    assert dummy.speed_factor < 1.0
    bm.update(pygame_time(dummy))
    assert dummy.speed_factor == 1.0


def pygame_time(dummy):
    pygame.init()
    pygame.display.set_mode((1,1))
    now = pygame.time.get_ticks() + 20
    pygame.quit()
    return now
