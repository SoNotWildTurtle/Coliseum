"""Tests for status effects."""

import os
import sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

pygame = pytest.importorskip("pygame")
from hololive_coliseum.player import Enemy
from hololive_coliseum.status_effects import (
    StatusEffectManager,
    FreezeEffect,
    SpeedEffect,
    ShieldEffect,
    PoisonEffect,
    BurnEffect,
    StunEffect,
)


def test_freeze_effect_expires():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0)
    manager = StatusEffectManager()
    enemy.velocity.x = 4
    manager.add_effect(enemy, FreezeEffect(duration_ms=50))
    assert enemy.speed_factor == 0.5
    now = pygame.time.get_ticks() + 60
    manager.update(now)
    assert enemy.speed_factor == 1.0
    pygame.quit()


def test_speed_effect_expires():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0)
    manager = StatusEffectManager()
    manager.add_effect(enemy, SpeedEffect(duration_ms=50, factor=2.0))
    assert enemy.speed_factor == 2.0
    now = pygame.time.get_ticks() + 60
    manager.update(now)
    assert enemy.speed_factor == 1.0
    pygame.quit()


def test_shield_effect_blocks_damage():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0)
    manager = StatusEffectManager()
    manager.add_effect(enemy, ShieldEffect(duration_ms=50))
    enemy.take_damage(20)
    assert enemy.health == enemy.max_health
    now = pygame.time.get_ticks() + 60
    manager.update(now)
    enemy.take_damage(20)
    assert enemy.health == enemy.max_health - 20
    pygame.quit()


def test_poison_effect_ticks_damage():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0)
    manager = StatusEffectManager()
    manager.add_effect(enemy, PoisonEffect(duration_ms=200, damage=1, interval_ms=50))
    start = pygame.time.get_ticks()
    manager.update(start + 60)
    assert enemy.health == enemy.max_health - 1
    manager.update(start + 120)
    assert enemy.health == enemy.max_health - 2
    manager.update(start + 300)
    assert enemy.health == enemy.max_health - 2
    pygame.quit()


def test_burn_effect_ticks_damage():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0)
    manager = StatusEffectManager()
    manager.add_effect(enemy, BurnEffect(duration_ms=200, damage=1, interval_ms=50))
    start = pygame.time.get_ticks()
    manager.update(start + 60)
    assert enemy.health == enemy.max_health - 1
    manager.update(start + 120)
    assert enemy.health == enemy.max_health - 2
    manager.update(start + 300)
    assert enemy.health == enemy.max_health - 2
    pygame.quit()


def test_stun_effect_prevents_movement():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0)
    manager = StatusEffectManager()
    enemy.velocity.x = 5
    manager.add_effect(enemy, StunEffect(duration_ms=50))
    assert getattr(enemy, "stunned", False)
    now = pygame.time.get_ticks() + 60
    manager.update(now)
    assert not getattr(enemy, "stunned", False)
    pygame.quit()


def test_status_effect_manager_active_effects_summary():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0)
    manager = StatusEffectManager()
    manager.add_effect(enemy, SpeedEffect(duration_ms=200))
    first_snapshot = manager.active_effects(enemy)
    assert first_snapshot
    start = first_snapshot[0]["effect"].start_time
    snapshot = manager.active_effects(enemy, now=start + 50)
    assert snapshot
    assert snapshot[0]["name"] == "Speed"
    assert 0 < snapshot[0]["remaining_ms"] <= 200
    pygame.quit()
