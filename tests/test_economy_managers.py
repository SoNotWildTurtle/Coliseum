"""Tests for economy managers."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.crafting_manager import CraftingManager
from hololive_coliseum.profession_manager import ProfessionManager
from hololive_coliseum.trade_manager import TradeManager
from hololive_coliseum.economy_manager import EconomyManager
from hololive_coliseum.inventory_manager import InventoryManager


def test_crafting_manager_craft():
    inv = InventoryManager()
    inv.add("wood", 2)
    cm = CraftingManager()
    cm.add_recipe("stick", {"wood": 2}, "stick")
    crafted = cm.craft("stick", inv)
    assert crafted == "stick" and inv.count("stick") == 1


def test_profession_levels():
    pm = ProfessionManager()
    pm.gain_xp("mining", 250)
    assert pm.level_of("mining") == 2


def test_trade_manager_accept():
    tm = TradeManager()
    tid = tm.propose_trade("a", "b", "gem")
    assert tm.accept_trade(tid) == ("a", "b", "gem")
    assert tm.accept_trade(tid) is None


def test_economy_manager_prices():
    em = EconomyManager()
    em.set_price("sword", 100)
    assert em.get_price("sword") == 100
    em.remove_price("sword")
    assert em.get_price("sword") == 0
