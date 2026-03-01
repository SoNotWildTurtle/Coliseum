"""Ensure enemies render a small green health bar when undamaged."""

import pygame
import pytest

from hololive_coliseum.player import Enemy

pytest.importorskip("pygame")


def test_enemy_health_bar_draws_green_pixel(tmp_path):
    pygame.init()
    enemy = Enemy(10, 10)
    surf = pygame.Surface((100, 100))
    enemy.draw_health_bar(surf)
    pixel = surf.get_at((enemy.rect.x + 1, enemy.rect.y - 3))
    assert pixel[:3] == (0, 255, 0)
    pygame.quit()
