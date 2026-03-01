"""Tests for class item manager."""

import pytest

from hololive_coliseum.class_manager import ClassManager
from hololive_coliseum.item_manager import Item, ItemManager


def test_class_manager_basic():
    cm = ClassManager()
    cm.add_class("mage", {"attack": 1, "defense": 2})
    assert cm.get_stats("mage") == {"attack": 1, "defense": 2}
    assert "mage" in cm.list_classes()


def test_class_manager_rejects_duplicates():
    cm = ClassManager()
    cm.add_class("mage", {"attack": 1})
    with pytest.raises(ValueError):
        cm.add_class("mage", {"attack": 2})


def test_item_manager_basic():
    im = ItemManager()
    item = Item("sword", "weapon", {"attack": 5})
    im.add_item(item)
    fetched = im.get("sword")
    assert fetched is item
    assert im.list_items() == [item]
