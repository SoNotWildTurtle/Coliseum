"""Tests for ally role assignment and stance switching."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.ally_fighter import AllyFighter
from hololive_coliseum.ally_manager import AllyManager
from hololive_coliseum.player import PlayerCharacter


def test_ally_roles_and_stances_assign_for_three_allies():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    player.max_health = 100
    player.health = 85
    ally_a = AllyFighter(-40, 0)
    ally_b = AllyFighter(40, 0)
    ally_c = AllyFighter(120, 0)
    allies = pygame.sprite.Group(ally_a, ally_b, ally_c)
    manager = AllyManager(allies)

    manager.update(player, [], [], [], 100, 10000, status_manager=None)

    roles = {ally.role for ally in allies}
    assert roles == {"tank", "support", "intercept"}
    for ally in allies:
        if ally.role == "tank":
            assert ally.stance == "defensive"
        elif ally.role == "support":
            assert ally.stance == "balanced"
        elif ally.role == "intercept":
            assert ally.stance == "aggressive"
    pygame.quit()
