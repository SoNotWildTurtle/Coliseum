"""Tests for per-character melee VFX palettes."""

import pytest

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


def test_character_melee_palettes():
    cases = [
        (GuraPlayer, (0, 235, 235)),
        (WatsonPlayer, (120, 200, 255)),
        (InaPlayer, (150, 90, 210)),
        (KiaraPlayer, (255, 140, 60)),
        (CalliopePlayer, (200, 200, 220)),
        (FaunaPlayer, (140, 255, 190)),
        (KroniiPlayer, (170, 200, 255)),
        (IRySPlayer, (210, 170, 255)),
        (MumeiPlayer, (180, 180, 240)),
        (BaelzPlayer, (255, 160, 210)),
        (FubukiPlayer, (200, 240, 255)),
        (MatsuriPlayer, (255, 210, 120)),
        (MikoPlayer, (255, 90, 120)),
        (AquaPlayer, (80, 150, 255)),
        (PekoraPlayer, (250, 150, 70)),
        (MarinePlayer, (210, 120, 160)),
        (SuiseiPlayer, (120, 210, 255)),
        (AyamePlayer, (200, 90, 90)),
        (NoelPlayer, (190, 190, 210)),
        (FlarePlayer, (255, 140, 60)),
        (SubaruPlayer, (255, 230, 120)),
        (SoraPlayer, (160, 210, 255)),
    ]

    for cls, expected in cases:
        player = cls(0, 0)
        assert player.melee_vfx_color == expected

    enemy = Enemy(0, 0)
    assert enemy.melee_vfx_color == (255, 170, 120)
