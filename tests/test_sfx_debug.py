"""Tests for SFX debug HUD enablement."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")


def test_sfx_debug_flag_toggles(monkeypatch, tmp_path):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    assert game.debug_sfx is False
    game._set_state("settings_audio")
    game.menu_index = game.settings_audio_options.index("SFX Debug")
    game._handle_menu_selection(game.settings_audio_options)
    assert game.debug_sfx is True
    pygame.quit()
