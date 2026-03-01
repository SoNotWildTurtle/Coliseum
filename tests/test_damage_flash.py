"""Tests for damage flash."""

import pytest

pygame = pytest.importorskip("pygame")
from hololive_coliseum.hud_manager import HUDManager, FLASH_DURATION


class DummyPlayer:
    def __init__(self) -> None:
        self.last_hit_time = 0

    def draw_status(self, screen) -> None:
        pass


def test_damage_flash(monkeypatch):
    pygame.display.set_mode((20, 20))
    pygame.font.init()
    hud = HUDManager()
    player = DummyPlayer()
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: FLASH_DURATION // 2)
    surface = pygame.Surface((5, 5))
    hud.draw(surface, player, 0, 0)
    assert surface.get_at((0, 0)).r > 0
    surface.fill((0, 0, 0))
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: FLASH_DURATION + 1)
    hud.draw(surface, player, 0, 0)
    assert surface.get_at((0, 0)).r == 0
