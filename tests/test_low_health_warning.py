"""Tests for low health warning."""

import pytest

pygame = pytest.importorskip("pygame")
from hololive_coliseum.hud_manager import HUDManager


class DummyPlayer:
    def __init__(self) -> None:
        self.health = 5
        self.max_health = 20
        self.last_hit_time = -1000

    def draw_status(self, surface) -> None:
        pass


def test_low_health_warning(monkeypatch):
    pygame.display.set_mode((10, 10))
    pygame.font.init()
    hud = HUDManager()
    player = DummyPlayer()
    surface = pygame.Surface((5, 5))
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 0)
    hud.draw(surface, player, 0, 0)
    assert surface.get_at((0, 0)).r > 0
    surface.fill((0, 0, 0))
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 250)
    hud.draw(surface, player, 0, 0)
    assert surface.get_at((0, 0)).r == 0
