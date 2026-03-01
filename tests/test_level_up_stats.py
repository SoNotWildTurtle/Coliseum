"""Tests for level up stats."""

import pytest


def test_level_up_boosts_stats(monkeypatch, tmp_path):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.player import PlayerCharacter

    player = PlayerCharacter(0, 0)
    attack = player.stats.get("attack")
    max_hp = player.health_manager.max_health
    leveled = player.gain_xp(100)
    assert leveled
    assert player.stats.get("attack") == attack + 1
    assert player.health_manager.max_health == max_hp + 5
    assert player.health_manager.health == max_hp + 5
    pygame.quit()
