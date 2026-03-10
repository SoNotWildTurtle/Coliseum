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


def _event_for_objective(objective_type: str) -> str:
    return {
        "defeat_enemies": "enemy_defeated",
        "collect_powerups": "powerup_collected",
        "earn_coins": "coins_earned",
        "win_matches": "match_won",
        "deal_damage": "damage_dealt",
        "hazard_mastery": "hazard_logged",
    }[objective_type]


def test_reputation_and_objectives_persist(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.selected_character = "Gawr Gura"
    game.selected_map = game.maps[0]
    game._setup_level()

    game.reputation_manager.modify("Arena", 12)
    objective = next(iter(game.objective_manager.objectives.values()))
    game.objective_manager.record_event(_event_for_objective(objective.objective_type), 3)

    _run_and_save(game)
    settings = load_settings()

    assert settings["reputation"]["Arena"] == 12
    objectives = settings["objectives"]["objectives"]
    objective_data = objectives[objective.objective_type]
    assert objective_data["progress"] >= 1

    pygame.display.set_mode((1, 1))
    reload_game = Game()
    assert reload_game.reputation_manager.get("Arena") == 12
    reloaded = ObjectiveManager()
    reloaded.load_from_dict(settings["objectives"])
    loaded = reloaded.objectives[objective.objective_type]
    assert loaded.progress >= 1
    pygame.quit()


def test_objective_rewards_persisted_state(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.selected_character = "Gawr Gura"
    game.selected_map = game.maps[0]
    game._setup_level()

    objective = next(iter(game.objective_manager.objectives.values()))
    game.objective_manager.record_event(
        _event_for_objective(objective.objective_type),
        objective.target,
    )

    _run_and_save(game)
    settings = load_settings()
    objective_data = settings["objectives"]["objectives"][objective.objective_type]
    assert objective_data["rewarded"] is True

    pygame.display.set_mode((1, 1))
    reload_game = Game()
    assert reload_game.reputation_manager.get("Arena") == 0
    reloaded = ObjectiveManager()
    reloaded.load_from_dict(settings["objectives"])
    loaded = reloaded.objectives[objective.objective_type]
    assert loaded.rewarded is True
    pygame.quit()
