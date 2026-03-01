"""Tests for SFX profile cycling."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")


def test_sfx_profile_cycles(monkeypatch, tmp_path):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    start = game.sfx_profile
    game._set_state("settings_audio")
    game.menu_index = game.settings_audio_options.index("SFX Profile")
    game._handle_menu_selection(game.settings_audio_options)
    assert game.sfx_profile != start
    pygame.quit()
