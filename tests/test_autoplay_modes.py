"""Tests for autoplay modes."""

from __future__ import annotations

import os

import pytest


@pytest.mark.usefixtures("monkeypatch")
def test_autoplay_flow_mode(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    monkeypatch.setenv("HOLO_AUTOPLAY", "1")
    monkeypatch.setenv("HOLO_AUTOPLAY_FLOW", "1")
    monkeypatch.setenv("HOLO_AUTOPLAY_TRACE", "0")
    from hololive_coliseum.game import Game

    game = Game(width=100, height=100)

    assert game.autoplay is True
    assert game.autoplay_flow is True
    assert game.autoplayer is not None


@pytest.mark.usefixtures("monkeypatch")
def test_autoplay_agent_mode(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    monkeypatch.setenv("HOLO_AUTOPLAY", "1")
    monkeypatch.setenv("HOLO_AUTOPLAY_FLOW", "0")
    monkeypatch.setenv("HOLO_AUTOPLAY_TRACE", "0")
    from hololive_coliseum.game import Game

    game = Game(width=100, height=100)

    assert game.autoplay is True
    assert game.autoplay_flow is False
    assert game.autoplayer is not None
