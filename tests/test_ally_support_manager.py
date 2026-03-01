"""Tests for ally support behaviors."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.ally_fighter import AllyFighter
from hololive_coliseum.ally_manager import AllyManager
from hololive_coliseum.player import PlayerCharacter
from hololive_coliseum.status_effects import StatusEffectManager


def test_ally_support_shield_and_speed():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    player.max_health = 100
    player.health = 25
    ally = AllyFighter(10, 0)
    ally.support_last_time = -10000
    manager = AllyManager(pygame.sprite.Group(ally))
    status_manager = StatusEffectManager()

    _proj, _melee, zones, messages = manager.update(
        player,
        [],
        [],
        [],
        100,
        pygame.time.get_ticks(),
        status_manager=status_manager,
    )

    effects = status_manager.active_effects(player)
    effect_names = {entry["name"] for entry in effects}
    assert "Shield" in effect_names
    assert "Speed" in effect_names
    assert zones == []
    assert any("Shield" in msg for msg, _pos in messages)
    pygame.quit()


def test_ally_support_heal_zone():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    player.max_health = 100
    player.health = 50
    ally = AllyFighter(10, 0)
    ally.support_last_time = -10000
    manager = AllyManager(pygame.sprite.Group(ally))
    status_manager = StatusEffectManager()

    _proj, _melee, zones, messages = manager.update(
        player,
        [],
        [],
        [],
        100,
        pygame.time.get_ticks(),
        status_manager=status_manager,
    )

    assert zones
    assert any("Heal" in msg for msg, _pos in messages)
    assert status_manager.active_effects(player) == []
    pygame.quit()


def test_ally_support_respects_cooldown():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    player.max_health = 100
    player.health = 25
    ally = AllyFighter(10, 0)
    ally.support_last_time = -10000
    manager = AllyManager(pygame.sprite.Group(ally))
    status_manager = StatusEffectManager()

    now = pygame.time.get_ticks()
    _proj, _melee, zones, messages = manager.update(
        player,
        [],
        [],
        [],
        100,
        now,
        status_manager=status_manager,
    )
    assert zones == []
    assert messages
    before = len(status_manager.active_effects(player))

    _proj, _melee, zones2, messages2 = manager.update(
        player,
        [],
        [],
        [],
        100,
        now + 1000,
        status_manager=status_manager,
    )

    assert zones2 == []
    assert messages2 == []
    after = len(status_manager.active_effects(player))
    assert after == before
    pygame.quit()
