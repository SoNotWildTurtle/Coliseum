"""Tests for SFX debug text formatting."""

from hololive_coliseum.hud_manager import HUDManager


def test_sfx_debug_text_includes_impact_scale():
    text = HUDManager._sfx_debug_text("melee_swing", "Arcade", 1.1)
    assert "SFX: melee_swing" in text
    assert "(Arcade)" in text
    assert "Impact x1.10" in text


def test_sfx_debug_text_handles_missing_fields():
    text = HUDManager._sfx_debug_text(None, None, None)
    assert text == "SFX:"
