"""Tests for squad focus and staggered specials."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.ai_manager import AIManager


class DummyTarget:
    def __init__(self, x: int, health: int = 100, max_health: int = 100) -> None:
        self.rect = pygame.Rect(x, 0, 10, 10)
        self.health = health
        self.max_health = max_health
        self.velocity = pygame.math.Vector2(0, 0)


class DummyEnemy:
    def __init__(self, x: int) -> None:
        self.rect = pygame.Rect(x, 0, 10, 10)
        self.focus_low_health = False
        self.focus_threshold = 0.35
        self.focus_range = 260
        self.preferred_target = None
        self.last_target = None
        self.specials_fired = 0

    def handle_ai(
        self,
        target,
        now,
        hazards,
        projectiles,
        *,
        squad_focus=None,
        allow_special=True,
    ):
        self.last_target = target
        if allow_special:
            proj = type("Proj", (), {})()
            proj.is_special = True
            self.specials_fired += 1
            return proj, None
        return None, None


class DummyPassiveEnemy(DummyEnemy):
    def handle_ai(
        self,
        target,
        now,
        hazards,
        projectiles,
        *,
        squad_focus=None,
        allow_special=True,
    ):
        self.last_target = target
        return None, None


def test_squad_focus_and_staggered_specials():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy_a = DummyEnemy(0)
    enemy_b = DummyEnemy(40)
    target_a = DummyTarget(120, health=90)
    target_b = DummyTarget(220, health=90)
    target_b.stunned = True
    manager = AIManager([enemy_a, enemy_b])

    projectiles, _melees = manager.update(
        None,
        1000,
        hazards=[],
        projectiles=[],
        targets=[target_a, target_b],
    )

    assert len(projectiles) == 1
    assert enemy_a.last_target is target_b
    assert enemy_b.last_target is target_b

    projectiles, _melees = manager.update(
        None,
        1200,
        hazards=[],
        projectiles=[],
        targets=[target_a, target_b],
    )

    assert projectiles == []
    pygame.quit()


def test_squad_focus_holds_within_margin():
    pygame.init()
    pygame.display.set_mode((1, 1))
    target_a = DummyTarget(100)
    target_b = DummyTarget(130)
    manager = AIManager([])
    manager._squad_focus_target = target_a
    manager._squad_focus_time = 800

    focus = manager._resolve_squad_focus(
        [target_a, target_b],
        {target_a: 0.76, target_b: 0.83},
        now=1200,
    )

    assert focus is target_a
    pygame.quit()


def test_squad_focus_switches_when_current_is_no_longer_viable():
    pygame.init()
    pygame.display.set_mode((1, 1))
    target_a = DummyTarget(100)
    target_b = DummyTarget(130)
    manager = AIManager([])
    manager._squad_focus_target = target_a
    manager._squad_focus_time = 1000

    focus = manager._resolve_squad_focus(
        [target_a, target_b],
        {target_a: 0.1, target_b: 0.82},
        now=1300,
    )

    assert focus is target_b
    pygame.quit()


def test_special_gap_scales_with_enemy_count_and_focus():
    manager_low = AIManager([DummyPassiveEnemy(0), DummyPassiveEnemy(30)])
    manager_high = AIManager(
        [
            DummyPassiveEnemy(0),
            DummyPassiveEnemy(30),
            DummyPassiveEnemy(60),
            DummyPassiveEnemy(90),
        ]
    )
    low_gap = manager_low._special_gap_ms({object(): 0.5})
    high_gap = manager_high._special_gap_ms({object(): 1.3})
    assert high_gap < low_gap
    assert high_gap >= 420


def test_high_pressure_allows_earlier_next_special():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy_a = DummyEnemy(0)
    enemy_b = DummyEnemy(40)
    enemy_c = DummyEnemy(80)
    enemy_d = DummyEnemy(120)
    target = DummyTarget(100)
    target.stunned = True
    manager = AIManager([enemy_a, enemy_b, enemy_c, enemy_d])

    projectiles, _ = manager.update(
        None,
        1000,
        hazards=[],
        projectiles=[],
        targets=[target],
    )
    assert len(projectiles) == 1

    projectiles, _ = manager.update(
        None,
        1600,
        hazards=[],
        projectiles=[],
        targets=[target],
    )
    assert len(projectiles) == 1
    pygame.quit()
