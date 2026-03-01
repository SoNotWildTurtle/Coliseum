"""Tests for gravity zone."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

pygame = pytest.importorskip("pygame")
from hololive_coliseum.player import PlayerCharacter
from hololive_coliseum.gravity_zone import GravityZone


def test_player_gravity_zone():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    zone = GravityZone(pygame.Rect(0, 0, 100, 100), 0.1)
    # player inside zone
    assert zone.rect.colliderect(player.rect)
    player.set_gravity_multiplier(1.0)
    if zone.rect.colliderect(player.rect):
        player.set_gravity_multiplier(zone.multiplier)
    player.apply_gravity()
    assert player.velocity.y == 0.05  # GRAVITY * 0.1
    pygame.quit()


def test_high_gravity_zone():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    zone = GravityZone(pygame.Rect(0, 0, 100, 100), 2.0)
    assert zone.rect.colliderect(player.rect)
    player.set_gravity_multiplier(1.0)
    if zone.rect.colliderect(player.rect):
        player.set_gravity_multiplier(zone.multiplier)
    player.apply_gravity()
    assert player.velocity.y == 1.0  # GRAVITY * 2
    pygame.quit()
