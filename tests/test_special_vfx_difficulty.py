"""Tests for special VFX styles that vary by difficulty."""

import pytest

pygame = pytest.importorskip("pygame")

from hololive_coliseum.player import GuraPlayer, WatsonPlayer, MikoPlayer


def test_special_vfx_style_changes_with_difficulty():
    cases = [
        (GuraPlayer, "pulse_ring", "star_twinkle"),
        (WatsonPlayer, "time_dash", "time_guard"),
        (MikoPlayer, "shrine_beam", "shockwave_expand"),
    ]

    for cls, normal_style, hard_style in cases:
        player = cls(0, 0)
        player.difficulty = "Normal"
        player.mana = player.max_mana
        normal = player.special_attack(0)
        assert normal is not None
        assert getattr(normal, "anim_style", None) == normal_style

        player.difficulty = "Hard"
        player.mana = player.max_mana
        hard = player.special_attack(2000)
        assert hard is not None
        assert getattr(hard, "anim_style", None) == hard_style
