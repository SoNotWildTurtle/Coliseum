"""Tests for weapon-specific impact scaling."""

import pytest

from hololive_coliseum.combat_manager import CombatManager


class Dummy:
    pass


def test_weapon_impact_scale_respects_weapon_and_difficulty():
    attacker = Dummy()
    attacker.difficulty = "Normal"
    attacker.weapon_sfx_event = "axe"
    axe_scale = CombatManager._impact_scale(attacker)

    attacker.weapon_sfx_event = "bow"
    bow_scale = CombatManager._impact_scale(attacker)

    assert axe_scale > bow_scale

    attacker.weapon_sfx_event = "spear"
    attacker.difficulty = "Hard"
    hard_scale = CombatManager._impact_scale(attacker)
    assert hard_scale == pytest.approx(1.1 * 1.05, rel=1e-3)
