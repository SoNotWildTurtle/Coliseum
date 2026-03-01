"""Tests for currency persistence."""

import pytest


def test_currency_persists_between_sessions(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game
    from hololive_coliseum import save_settings

    game = Game()
    game.selected_character = game.characters[0]
    game._setup_level()
    game.player.currency_manager.add(5)
    save_settings({"coins": game.player.currency_manager.get_balance()})
    pygame.quit()

    game2 = Game()
    game2.selected_character = game2.characters[0]
    game2._setup_level()
    assert game2.player.currency_manager.get_balance() == 5
    pygame.quit()
