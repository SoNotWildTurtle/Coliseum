"""Tests for inventory capacity."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.inventory_manager import InventoryManager


def test_inventory_capacity_limit():
    inv = InventoryManager(capacity=2)
    assert inv.add("apple")
    assert inv.add("banana")
    assert not inv.add("cherry")
    assert inv.count("cherry") == 0
    assert inv.total_items() == 2
