"""Tests for special knockback tuning."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.player import (
    GuraPlayer,
    KiaraPlayer,
    FubukiPlayer,
    AquaPlayer,
    NoelPlayer,
)


def test_special_knockback_tiers():
    pygame.init()
    pygame.display.set_mode((1, 1))
    now = pygame.time.get_ticks()

    gura = GuraPlayer(0, 0)
    gura_proj = gura.special_attack(now)
    assert gura_proj.knockback >= 2.5

    kiara = KiaraPlayer(0, 0)
    kiara.special_attack(now)
    kiara.update(kiara.rect.bottom + 1, now + 10)
    blast = kiara.update(kiara.rect.bottom + 1, now + 20)
    if blast is None:
        blast = kiara.update(kiara.rect.bottom + 1, now + 30)
    assert blast is None or blast.knockback >= 3.0

    fubuki = FubukiPlayer(0, 0)
    fubuki_proj = fubuki.special_attack(now)
    assert fubuki_proj.knockback == 0.0

    aqua = AquaPlayer(0, 0)
    aqua_proj = aqua.special_attack(now)
    assert aqua_proj.knockback == 0.0

    noel = NoelPlayer(0, 0)
    noel_proj = noel.special_attack(now)
    assert noel_proj.knockback >= 2.5

    pygame.quit()
