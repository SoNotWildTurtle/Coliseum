"""Tests for autoplay allies and mobs."""

import os

import pytest

pytest.importorskip("pygame")

from hololive_coliseum.game import Game


def test_autoplay_spawns_allies(monkeypatch):
    monkeypatch.setenv("HOLO_AUTOPLAY", "1")
    monkeypatch.delenv("HOLO_AUTOPLAY_ALLIES", raising=False)
    game = Game(width=200, height=200)
    assert game.autoplay
    assert len(game.allies) >= 1
    assert game.player.lives >= 5


def test_mob_wave_spawn():
    game = Game(width=200, height=200)
    game.enemies.empty()
    game.ai_manager.enemies = game.enemies
    game.mob_spawn_enabled = True
    game.mob_spawn_config = {"wave": 2, "max": 4}
    game.mob_spawn_max = 4
    game._spawn_mob_wave(0)
    assert len(game.enemies) == 2
