"""Tests for moving platform."""

import pytest

pygame = pytest.importorskip("pygame")

from hololive_coliseum.platform import MovingPlatform
from hololive_coliseum.player import PlayerCharacter


def test_moving_platform_moves():
    pygame.init()
    plat = MovingPlatform(pygame.Rect(0, 0, 100, 20), (50, 0), 10)
    plat.update()
    assert plat.rect.x == 10
    for _ in range(5):
        plat.update()
    assert plat.rect.x > 10
    pygame.quit()


def test_player_moves_with_platform():
    pygame.init()
    plat = MovingPlatform(pygame.Rect(0, 100, 100, 20), (50, 0), 5)
    player = PlayerCharacter(10, 40)
    player.platforms.add(plat)
    player.rect.bottom = plat.rect.top
    player.pos = pygame.math.Vector2(player.rect.topleft)
    player.on_ground = True
    player.current_platform = plat
    plat.update()
    player.pos += plat.velocity
    player.rect.topleft = (int(player.pos.x), int(player.pos.y))
    player.update(200)
    assert player.rect.x > 10
    pygame.quit()
