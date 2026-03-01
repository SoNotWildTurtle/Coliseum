"""Tests for crumbling platform."""

import pytest

pygame = pytest.importorskip("pygame")

from hololive_coliseum.platform import CrumblingPlatform
from hololive_coliseum.player import PlayerCharacter


def test_crumbling_platform_disappears():
    pygame.init()
    plat = CrumblingPlatform(pygame.Rect(0, 0, 100, 20), delay=2)
    player = PlayerCharacter(10, -20)
    player.platforms.add(plat)
    player.rect.midbottom = (plat.rect.centerx, plat.rect.top - 1)
    player.pos = pygame.math.Vector2(player.rect.topleft)
    player.velocity.y = 5
    player.update(200)
    assert plat.timer == 2
    plat.update()
    assert plat.alive()
    plat.update()
    assert not plat.alive()
    pygame.quit()
