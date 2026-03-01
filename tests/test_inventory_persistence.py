"""Tests for inventory persistence."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum import Game, save_inventory, load_inventory


def test_inventory_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    data = {"potion": 2}
    save_inventory(data)
    assert load_inventory() == data


def test_level_setup_loads_saved_inventory(tmp_path, monkeypatch):
    pytest.importorskip("pygame")
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    game = Game()
    game.selected_map = game.maps[0]
    game.selected_character = game.characters[0]
    game._setup_level()
    game.player.inventory.add("gem")
    game._setup_level()
    assert game.player.inventory.has("gem")
