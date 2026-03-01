"""Tests for autoplay skill audit."""

from __future__ import annotations

import pytest


@pytest.mark.usefixtures("monkeypatch")
def test_autoplay_skill_audit_records_actions(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    monkeypatch.setenv("HOLO_AUTOPLAY", "1")
    monkeypatch.setenv("HOLO_AUTOPLAY_SKILL_AUDIT", "1")
    monkeypatch.setenv("HOLO_AUTOPLAY_TRACE", "0")
    from hololive_coliseum.game import Game

    game = Game(width=100, height=100)
    game.selected_character = "Gura"
    game._autoplay_reset_character_audit("Gura")

    game._autoplay_record_character_action("shoot")
    missing = game._autoplay_character_missing_actions("Gura")

    assert "shoot" not in missing
    assert "special" in missing
