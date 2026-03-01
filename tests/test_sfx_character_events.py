"""Tests for per-character SFX event routing."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.player import GuraPlayer


class DummySound:
    def __init__(self) -> None:
        self.last_played = None
        self.last_event = None

    def play(self, name: str) -> None:
        self.last_played = name

    def play_event(self, event: str) -> None:
        self.last_event = event
        self.play("special_cast")


def test_special_sfx_event_uses_character_tag():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = GuraPlayer(0, 0)
    sound = DummySound()
    player.sound_manager = sound
    player.special_attack(pygame.time.get_ticks())
    assert sound.last_event == "special_cast:gura"
    pygame.quit()


def test_melee_sfx_event_uses_character_tag():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = GuraPlayer(0, 0)
    sound = DummySound()
    player.sound_manager = sound
    player.melee_attack(pygame.time.get_ticks())
    assert sound.last_event == "melee_swing:gura"
    pygame.quit()
