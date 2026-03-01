"""Tests for item use."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.player import PlayerCharacter


def test_use_potion_consumes_and_heals():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    player.health = 50
    player.inventory.add("potion")
    assert player.use_item("potion")
    assert player.health == 70
    assert not player.inventory.has("potion")
    pygame.quit()


def test_use_mana_potion_consumes_and_restores_mana():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    player.mana = 10
    player.inventory.add("mana_potion")
    assert player.use_item("mana_potion")
    assert player.mana == 30
    assert not player.inventory.has("mana_potion")
    pygame.quit()
