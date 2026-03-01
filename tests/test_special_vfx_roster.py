"""Tests that special VFX styles change across difficulty for the roster."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.player import (
    GuraPlayer,
    WatsonPlayer,
    InaPlayer,
    KiaraPlayer,
    CalliopePlayer,
    FaunaPlayer,
    KroniiPlayer,
    IRySPlayer,
    MumeiPlayer,
    BaelzPlayer,
    FubukiPlayer,
    MatsuriPlayer,
    MikoPlayer,
    AquaPlayer,
    PekoraPlayer,
    MarinePlayer,
    SuiseiPlayer,
    AyamePlayer,
    NoelPlayer,
    FlarePlayer,
    SubaruPlayer,
    SoraPlayer,
    Enemy,
)


def _style_of(effect):
    if effect is None:
        return None
    if hasattr(effect, "pulse_style"):
        return effect.pulse_style
    return getattr(effect, "anim_style", None)


def _spawn_special(player, now, *, monkeypatch=None):
    player.mana = player.max_mana
    if isinstance(player, BaelzPlayer) and monkeypatch is not None:
        monkeypatch.setattr(
            "hololive_coliseum.player.random.choice", lambda seq: "invert"
        )
    result = player.special_attack(now)
    if result is not None:
        return result
    if isinstance(player, KiaraPlayer):
        player.diving = True
        player.velocity.y = 0
        player.pos.y = 0
        player.rect.top = 0
        ground_y = player.rect.bottom
        return player.update(ground_y, now + 1)
    return None


@pytest.mark.parametrize(
    "cls,normal_style,hard_style",
    [
        (GuraPlayer, "pulse_ring", "star_twinkle"),
        (WatsonPlayer, "time_dash", "time_guard"),
        (InaPlayer, "ripple", "pulse_ring"),
        (KiaraPlayer, "phoenix_flare", "shockwave_expand"),
        (CalliopePlayer, "scythe_spin", "oni_slash"),
        (FaunaPlayer, "grove", "bloom"),
        (KroniiPlayer, "time_guard", "crystal_shield"),
        (IRySPlayer, "crystal_shield", "star_twinkle"),
        (MumeiPlayer, "flock_flutter", "star_twinkle"),
        (BaelzPlayer, "chaos_glitch", "festival_burst"),
        (FubukiPlayer, "frost_glint", "star_twinkle"),
        (MatsuriPlayer, "festival_burst", "phoenix_flare"),
        (MikoPlayer, "shrine_beam", "shockwave_expand"),
        (AquaPlayer, "water_bubble", "ripple"),
        (PekoraPlayer, "carrot_wiggle", "scythe_spin"),
        (MarinePlayer, "anchor_swing", "scythe_spin"),
        (SuiseiPlayer, "star_twinkle", "festival_burst"),
        (AyamePlayer, "oni_slash", "scythe_spin"),
        (NoelPlayer, "shockwave_expand", "festival_burst"),
        (FlarePlayer, "flame_flicker", "phoenix_flare"),
        (SubaruPlayer, "stun_zap", "shockwave_expand"),
        (SoraPlayer, "melody_wave", "star_twinkle"),
        (Enemy, "pulse_ring", "stun_zap"),
    ],
)
def test_special_vfx_style_roster(monkeypatch, cls, normal_style, hard_style):
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = cls(0, 0)

    player.difficulty = "Normal"
    normal = _spawn_special(player, 0, monkeypatch=monkeypatch)
    assert _style_of(normal) == normal_style

    player.difficulty = "Hard"
    hard = _spawn_special(player, 2000, monkeypatch=monkeypatch)
    assert _style_of(hard) == hard_style

    pygame.quit()
