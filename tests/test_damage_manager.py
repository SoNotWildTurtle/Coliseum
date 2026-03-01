"""Tests for damage manager calculations and application."""

from hololive_coliseum.damage_manager import DamageManager


class DummyTarget:
    def __init__(self) -> None:
        self.last_damage = None

    def take_damage(self, amount: int) -> None:
        self.last_damage = amount


def test_damage_manager_applies_defense_and_multiplier():
    dm = DamageManager()
    damage = dm.calculate(10, defense=3, multiplier=1.5)
    assert damage == 10


def test_damage_manager_defense_can_zero_out():
    dm = DamageManager()
    damage = dm.calculate(5, defense=10)
    assert damage == 0


def test_damage_manager_apply_calls_target():
    dm = DamageManager()
    target = DummyTarget()
    dealt = dm.apply(target, 8)
    assert dealt == 8
    assert target.last_damage == 8
