"""Tests for team manager."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.team_manager import TeamManager
from hololive_coliseum.combat_manager import CombatManager
from hololive_coliseum.player import PlayerCharacter


def setup_pygame():
    pygame = pytest.importorskip("pygame")
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    return pygame


def test_team_assignment_allies():
    tm = TeamManager()
    class Dummy:  # simple actor
        pass

    p1 = Dummy()
    p2 = Dummy()
    tm.set_team(p1, 0)
    tm.set_team(p2, 0)
    assert tm.are_allies(p1, p2)


def test_friendly_fire_ignored():
    pygame = setup_pygame()
    tm = TeamManager()
    cm = CombatManager(team_manager=tm)
    p1 = PlayerCharacter(0, 0)
    p2 = PlayerCharacter(0, 0)
    tm.set_team(p1, 0)
    tm.set_team(p2, 0)
    proj = p1.shoot(0, p2.rect.center)
    assert proj is not None
    proj.rect.center = p2.rect.center
    projectiles = pygame.sprite.Group(proj)
    enemies = pygame.sprite.Group(p2)
    cm.handle_collisions(p1, enemies, projectiles, pygame.sprite.Group(), 0)
    assert p2.health_manager.health == p2.health_manager.max_health

