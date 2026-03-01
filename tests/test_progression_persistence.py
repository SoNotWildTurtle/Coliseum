"""Tests for progression persistence through settings."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.game import Game
from hololive_coliseum.objective_manager import ObjectiveManager
from hololive_coliseum.save_manager import load_settings


def _run_and_save(game: Game) -> None:
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()


def test_reputation_and_objectives_persist(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.selected_character = "Gawr Gura"
    game.selected_map = game.maps[0]
    game._setup_level()

    game.reputation_manager.modify("Arena", 12)
    game.objective_manager.record_event("enemy_defeated", 3)

    _run_and_save(game)
    settings = load_settings()

    assert settings["reputation"]["Arena"] == 12
    objectives = settings["objectives"]["objectives"]
    assert objectives["defeat_enemies"]["progress"] >= 3

    pygame.display.set_mode((1, 1))
    reload_game = Game()
    assert reload_game.reputation_manager.get("Arena") == 12
    reloaded = ObjectiveManager()
    reloaded.load_from_dict(settings["objectives"])
    loaded = reloaded.objectives["defeat_enemies"]
    assert loaded.progress >= 3
    pygame.quit()


def test_objective_rewards_persisted_state(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.selected_character = "Gawr Gura"
    game.selected_map = game.maps[0]
    game._setup_level()

    objective = game.objective_manager.objectives["defeat_enemies"]
    game.objective_manager.record_event("enemy_defeated", objective.target)

    _run_and_save(game)
    settings = load_settings()
    objective_data = settings["objectives"]["objectives"]["defeat_enemies"]
    assert objective_data["rewarded"] is True

    pygame.display.set_mode((1, 1))
    reload_game = Game()
    assert reload_game.reputation_manager.get("Arena") == 0
    reloaded = ObjectiveManager()
    reloaded.load_from_dict(settings["objectives"])
    loaded = reloaded.objectives["defeat_enemies"]
    assert loaded.rewarded is True
    pygame.quit()
