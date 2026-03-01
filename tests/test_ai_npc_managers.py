"""Tests for ai npc managers."""

import os
import sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

pygame = pytest.importorskip("pygame")
from hololive_coliseum.player import PlayerCharacter, Enemy
from hololive_coliseum.ai_manager import AIManager
from hololive_coliseum.npc_manager import NPCManager
from hololive_coliseum.ally_manager import AllyManager
from hololive_coliseum.ally_fighter import AllyFighter
from hololive_coliseum.status_effects import StatusEffectManager


def test_ai_manager_actions(monkeypatch):
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(100, 100)
    enemy = Enemy(0, 100, difficulty="Hard")
    enemy.last_ai_action = -1000
    mgr = AIManager(pygame.sprite.Group(enemy))
    monkeypatch.setattr('random.random', lambda: 0.0)
    projs, melees = mgr.update(player, pygame.time.get_ticks(), [], [])
    assert projs or melees
    pygame.quit()


def test_npc_and_ally_manager_groups():
    mgr = NPCManager()
    ally_mgr = AllyManager(mgr.allies)
    p1 = PlayerCharacter(0, 0)
    p2 = PlayerCharacter(0, 0)
    mgr.add_enemy(p1)
    mgr.add_ally(p2)
    assert p1 in mgr.enemies
    assert p2 in mgr.allies
    ally_mgr.update(p1, mgr.enemies, [], [], 100, 0)


def test_ally_support_actions_trigger():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    player.health = 20
    player.max_health = 100
    ally = AllyFighter(10, 0)
    ally.support_last_time = -10000
    allies = pygame.sprite.Group(ally)
    ally_mgr = AllyManager(allies)
    status_manager = StatusEffectManager()
    _projs, _melees, zones, messages = ally_mgr.update(
        player,
        [],
        [],
        [],
        100,
        pygame.time.get_ticks(),
        status_manager=status_manager,
    )
    assert zones or messages or status_manager.active_effects(player)
    pygame.quit()
