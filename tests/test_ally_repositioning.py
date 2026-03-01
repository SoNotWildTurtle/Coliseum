"""Tests for ally repositioning behavior."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.ally_fighter import AllyFighter
from hololive_coliseum.ally_manager import AllyManager
from hololive_coliseum.player import Enemy, PlayerCharacter


def test_ally_repositions_toward_player_under_threat():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    player.max_health = 100
    player.health = 40
    ally = AllyFighter(200, 0)
    enemy = Enemy(60, 0)
    allies = pygame.sprite.Group(ally)
    manager = AllyManager(allies)

    _proj, _melee, _zones, _messages = manager.update(
        player,
        [enemy],
        [],
        [],
        100,
        pygame.time.get_ticks(),
        status_manager=None,
    )

    assert ally.velocity.x < 0
    pygame.quit()
