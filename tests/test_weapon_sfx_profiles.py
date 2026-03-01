"""Tests for weapon SFX profile mapping."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.sound_manager import SoundManager


def test_weapon_sfx_profile_mapping():
    pygame.init()
    pygame.display.set_mode((1, 1))
    sm = SoundManager(profile="Arcade")
    sm.play_event("melee_swing:gura:axe")
    assert sm.last_played == "hit_crit"
    pygame.quit()
