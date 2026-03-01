"""Tests for melee VFX styling based on weapon tags."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.player import GuraPlayer
from hololive_coliseum.item_manager import Axe


def test_melee_vfx_style_changes_with_weapon():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = GuraPlayer(0, 0)
    player.equipment.equip("weapon", Axe("Chopper", {"attack": 3}))
    player.weapon_sfx_event = "axe"
    attack = player.melee_attack(pygame.time.get_ticks())
    assert attack.vfx_style == "slash_spike"
    pygame.quit()
