"""Tests for inventory equipment."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest

pygame = pytest.importorskip("pygame")

from hololive_coliseum.item_manager import (
    Axe,
    Bow,
    Helmet,
    Orb,
    Quiver,
    Shield,
    Spear,
    Sword,
    Tome,
    Wand,
    Weapon,
)


def test_inventory_equip_and_unequip(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game.player.inventory.add("Sword")
    game.item_manager.add_item(Weapon("Sword", {}))

    choice = list(game.player.inventory.items.keys())[0]
    item = game.item_manager.get(choice)
    assert game.player.inventory.remove(choice)
    game.player.equipment.equip(item.slot, item.name)
    assert game.player.equipment.get("weapon") == "Sword"
    assert game.player.inventory.count("Sword") == 0

    stored = game.player.equipment.get("weapon")
    game.player.equipment.unequip("weapon")
    game.player.inventory.add(stored)
    assert game.player.equipment.get("weapon") is None
    assert game.player.inventory.count("Sword") == 1


def test_head_slot(tmp_path, monkeypatch):
    """Helmet items equip to the head slot."""
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game.player.inventory.add("Cap")
    game.item_manager.add_item(Helmet("Cap", {"def": 1}))

    choice = list(game.player.inventory.items.keys())[0]
    item = game.item_manager.get(choice)
    assert game.player.inventory.remove(choice)
    game.player.equipment.equip(item.slot, item.name)
    assert game.player.equipment.get("head") == "Cap"


def test_weapon_subclasses_use_weapon_slot():
    items = [
        Sword("Iron Sword", {}),
        Bow("Short Bow", {}),
        Wand("Oak Wand", {}),
        Axe("Hatchet", {}),
        Spear("Wooden Spear", {}),
    ]
    for item in items:
        assert item.slot == "weapon"


def test_offhand_subclasses_use_offhand_slot():
    items = [
        Shield("Buckler", {}),
        Tome("Spell Tome", {}),
        Orb("Crystal Orb", {}),
        Quiver("Leather Quiver", {}),
    ]
    for item in items:
        assert item.slot == "offhand"
