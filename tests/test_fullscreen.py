"""Tests for the fullscreen toggle in the settings menu."""

import pytest

pygame = pytest.importorskip("pygame")


from hololive_coliseum.game import Game


def test_toggle_fullscreen():
    game = Game()
    initial = game.fullscreen
    game._toggle_fullscreen()
    assert game.fullscreen != initial
    if pygame.display.get_driver() != "dummy":
        assert game.screen.get_flags() & pygame.FULLSCREEN
    game._toggle_fullscreen()
    assert game.fullscreen == initial
    if pygame.display.get_driver() != "dummy":
        assert not (game.screen.get_flags() & pygame.FULLSCREEN)
