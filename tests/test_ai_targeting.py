"""Tests for AI target selection preferences."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.ai_manager import AIManager
from hololive_coliseum.ally_manager import AllyManager
from hololive_coliseum.ally_fighter import AllyFighter
from hololive_coliseum.player import Enemy, PlayerCharacter


def _make_player(x: int, health: int, max_health: int = 100) -> PlayerCharacter:
    player = PlayerCharacter(x, 0)
    player.max_health = max_health
    player.health = health
    return player


def test_enemy_focuses_low_health_target():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0, difficulty="Hard")
    low = _make_player(120, 20)
    high = _make_player(30, 80)
    target = AIManager._select_target(enemy, [high, low], now=0)
    assert target is low
    pygame.quit()


def test_enemy_prefers_nearest_when_no_low_health():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0, difficulty="Hard")
    a = _make_player(40, 80)
    b = _make_player(120, 80)
    target = AIManager._select_target(enemy, [a, b], now=0)
    assert target is a
    pygame.quit()


def test_ally_protects_low_health_player():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = _make_player(0, 40)
    ally = AllyFighter(300, 0)
    near_player = Enemy(20, 0)
    near_ally = Enemy(280, 0)
    allies = pygame.sprite.Group(ally)
    manager = AllyManager(allies)
    target = manager._select_target(ally, [near_player, near_ally], player)
    assert target is near_player
    pygame.quit()


def test_enemy_prefers_recently_hit_target():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0, difficulty="Hard")
    recent = _make_player(80, 70)
    other = _make_player(80, 70)
    recent.last_hit_time = 10
    other.last_hit_time = 0
    target = AIManager._select_target(enemy, [recent, other], now=20)
    assert target is recent
    pygame.quit()


def test_enemy_prefers_crowd_controlled_target():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0, difficulty="Hard")
    stunned = _make_player(140, 80)
    normal = _make_player(80, 80)
    stunned.stunned = True
    target = AIManager._select_target(enemy, [normal, stunned], now=50)
    assert target is stunned
    pygame.quit()


def test_enemy_prefers_staggered_target():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0, difficulty="Hard")
    staggered = _make_player(160, 80)
    normal = _make_player(80, 80)
    staggered.stagger_until = 200
    target = AIManager._select_target(enemy, [normal, staggered], now=50)
    assert target is staggered
    pygame.quit()


def test_ally_prefers_crowd_controlled_target():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = _make_player(0, 100)
    ally = AllyFighter(0, 0)
    stunned = Enemy(200, 0)
    normal = Enemy(60, 0)
    stunned.stunned = True
    allies = pygame.sprite.Group(ally)
    manager = AllyManager(allies)
    target = manager._select_target(ally, [normal, stunned], player)
    assert target is stunned
    pygame.quit()
