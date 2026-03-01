"""Tests for hitstop behavior on damage."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.player import PlayerCharacter, Enemy


def test_player_hitstop_sets_timer():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    now = pygame.time.get_ticks()
    player.take_damage(10)
    assert player.hitstop_until > now
    pygame.quit()


def test_enemy_hitstop_sets_timer():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0)
    now = pygame.time.get_ticks()
    enemy.take_damage(5)
    assert enemy.hitstop_until > now
    pygame.quit()


def test_critical_hitstop_longer_than_normal():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    now = pygame.time.get_ticks()
    player.last_hit_critical = False
    player.take_damage(6)
    normal_duration = player.hitstop_until - now
    player.last_hit_critical = True
    player.take_damage(6)
    critical_duration = player.hitstop_until - now
    assert critical_duration >= normal_duration
    pygame.quit()
