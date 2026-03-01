"""Tests for crafting station."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.inventory_manager import InventoryManager
from hololive_coliseum.crafting_manager import CraftingManager
from hololive_coliseum.crafting_station import CraftingStation


def test_crafting_station_interaction():
    inv = InventoryManager()
    inv.add("wood", 2)
    cm = CraftingManager()
    cm.add_recipe("stick", {"wood": 2}, "stick")
    station = CraftingStation(cm, "stick")
    result = station.interact(inv)
    assert result == "stick"
    assert inv.count("stick") == 1
