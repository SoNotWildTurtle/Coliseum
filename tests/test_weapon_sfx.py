"""Tests for weapon-tagged melee SFX events."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.player import GuraPlayer
from hololive_coliseum.item_manager import Sword


class DummySound:
    def __init__(self) -> None:
        self.last_event = None

    def play_event(self, event: str) -> None:
        self.last_event = event

    def play(self, name: str) -> None:
        pass


def test_weapon_tagged_melee_event():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = GuraPlayer(0, 0)
    player.sound_manager = DummySound()
    player.equipment.equip("weapon", Sword("Blade", {"attack": 2}))
    player.weapon_sfx_event = "sword"
    player.melee_attack(pygame.time.get_ticks())
    assert player.sound_manager.last_event == "melee_swing:gura:sword"
    pygame.quit()
