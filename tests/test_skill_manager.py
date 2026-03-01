"""Tests for skill manager."""

import pytest

pygame = pytest.importorskip("pygame")
from hololive_coliseum.skill_manager import SkillManager


def test_skill_manager_cooldown():
    pygame.init()
    manager = SkillManager()
    calls = []

    def ability(now):
        calls.append(now)
        return "ok"

    manager.register("special", 100, ability)
    now = pygame.time.get_ticks()
    assert manager.use("special", now) == "ok"
    assert manager.use("special", now + 50) is None
    assert manager.use("special", now + 150) == "ok"
    pygame.quit()
