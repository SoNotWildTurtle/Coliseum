"""Tests for minigame autoskill."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.minigame_manager import MinigameManager
from hololive_coliseum.auto_skill_manager import AutoSkillManager
from hololive_coliseum.inventory_manager import InventoryManager


def test_reaction_minigame_awards_material():
    inv = InventoryManager()
    mgr = MinigameManager()
    material = mgr.play_reaction(500, 520, "ore", inv)
    assert material == "ore"
    assert inv.count("ore") == 1
    assert mgr.play_reaction(500, 800, "ore", inv) is None


def test_auto_skill_generation():
    asm = AutoSkillManager()
    skill = asm.generate("Strike", 3, {"attack": 5})
    assert skill == {"name": "Strike Lv3", "power": 11}
