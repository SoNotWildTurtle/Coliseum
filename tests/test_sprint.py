"""Tests for sprint."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pytest.importorskip("pygame")
import pygame

from hololive_coliseum.player import PlayerCharacter


def test_sprint_uses_stamina_and_boosts_speed():
    pygame.init()
    pygame.display.set_mode((1, 1))
    now = pygame.time.get_ticks()
    base = PlayerCharacter(0, 0)
    runner = PlayerCharacter(0, 0)

    class Keys(dict):
        def __getitem__(self, key):
            return key in self

    right = Keys({pygame.K_RIGHT: True})
    right_shift = Keys({pygame.K_RIGHT: True, pygame.K_RSHIFT: True})

    base.handle_input(right, now, action_pressed=lambda a: False)
    runner.handle_input(right_shift, now, action_pressed=lambda a: a == "sprint")
    base.update(ground_y=0)
    runner.update(ground_y=0)
    assert runner.velocity.x > base.velocity.x
    assert runner.stamina < runner.max_stamina
    pygame.quit()
