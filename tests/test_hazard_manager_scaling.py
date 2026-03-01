"""Tests for hazard manager scaling behavior."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.hazard_manager import HazardManager
from hololive_coliseum.hazards import LavaZone
from hololive_coliseum.player import PlayerCharacter


def test_hazard_manager_scales_damage():
    pygame.init()
    pygame.display.set_mode((1, 1))
    manager = HazardManager()
    manager.set_damage_multiplier(2.0)
    player = PlayerCharacter(0, 0)
    lava = LavaZone(player.rect.copy(), damage=3, interval=0)
    manager.hazards.add(lava)
    start = player.health
    manager.last_damage = -1000
    manager.apply_to_player(player, pygame.time.get_ticks())
    assert player.health == start - 6
    pygame.quit()


def test_scaled_damage_minimum_is_one():
    manager = HazardManager()
    manager.set_damage_multiplier(0.1)
    assert manager._scaled_damage(1) == 1
    assert manager._scaled_damage(0) == 0
