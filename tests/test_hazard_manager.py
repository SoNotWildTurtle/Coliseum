"""Tests for hazard manager."""

import os
import sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

pygame = pytest.importorskip("pygame")
from hololive_coliseum.hazard_manager import HazardManager
from hololive_coliseum.hazards import SpikeTrap
from hololive_coliseum.player import PlayerCharacter


def test_hazard_manager_player_damage(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1,1))
    hm = HazardManager()
    hm.hazards.add(SpikeTrap(pygame.Rect(0,0,10,10), damage=5))
    hm.last_damage = -1000
    player = PlayerCharacter(0,0)
    now = pygame.time.get_ticks()
    hm.apply_to_player(player, now)
    assert player.health < player.max_health
    pygame.quit()


def test_hazard_manager_records_hazards(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))

    class DummyAnalytics:
        def __init__(self) -> None:
            self.events: list[str] = []

        def record_hazard(self, hazard_type: str) -> None:
            self.events.append(hazard_type)

    analytics = DummyAnalytics()

    class DummyObjectives:
        def __init__(self) -> None:
            self.events: list[tuple[str, int]] = []

        def record_event(self, event: str, amount: int = 1):
            self.events.append((event, amount))
            return []

    objectives = DummyObjectives()
    hm = HazardManager(analytics=analytics, objective_manager=objectives)
    hm.hazards.add(SpikeTrap(pygame.Rect(0, 0, 10, 10), damage=5))
    hm.last_damage = -1000
    player = PlayerCharacter(0, 0)
    now = pygame.time.get_ticks()
    hm.apply_to_player(player, now)
    assert 'spike' in analytics.events
    assert ('hazard_logged', 1) in objectives.events
    pygame.quit()
