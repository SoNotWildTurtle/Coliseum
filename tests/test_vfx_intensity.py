"""Tests for VFX intensity scaling."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.combat_manager import CombatManager
from hololive_coliseum.player import Enemy, PlayerCharacter
from hololive_coliseum.projectile import Projectile


def test_projectile_vfx_intensity_scales_with_difficulty():
    pygame.init()
    pygame.display.set_mode((1, 1))
    combat = CombatManager()
    target = PlayerCharacter(0, 0)
    easy = Enemy(20, 0, difficulty="Easy")
    elite = Enemy(20, 0, difficulty="Elite")

    proj_easy = Projectile(target.rect.centerx, target.rect.centery, pygame.math.Vector2(1, 0))
    proj_easy.from_enemy = True
    proj_easy.owner = easy
    proj_easy.attack = 5

    proj_elite = Projectile(target.rect.centerx, target.rect.centery, pygame.math.Vector2(1, 0))
    proj_elite.from_enemy = True
    proj_elite.owner = elite
    proj_elite.attack = 5

    combat.handle_collisions(
        target,
        pygame.sprite.Group(),
        pygame.sprite.Group(proj_easy),
        pygame.sprite.Group(),
        pygame.time.get_ticks(),
    )
    easy_intensity = proj_easy.vfx_intensity

    combat.handle_collisions(
        target,
        pygame.sprite.Group(),
        pygame.sprite.Group(proj_elite),
        pygame.sprite.Group(),
        pygame.time.get_ticks(),
    )
    elite_intensity = proj_elite.vfx_intensity

    assert elite_intensity > easy_intensity
    pygame.quit()
