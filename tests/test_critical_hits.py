"""Tests for critical hits."""

import random
import pytest

from hololive_coliseum.damage_manager import DamageManager


def test_critical_hit_doubles_damage(monkeypatch):
    dm = DamageManager()
    monkeypatch.setattr(random, "random", lambda: 0.0)
    dmg = dm.calculate(10, crit_chance=100)
    assert dmg == 20


def test_calculate_returns_crit_flag(monkeypatch):
    dm = DamageManager()
    monkeypatch.setattr(random, "random", lambda: 0.0)
    dmg, critical = dm.calculate(10, crit_chance=100, return_crit=True)
    assert dmg == 20 and critical is True


def test_critical_hit_respects_multiplier(monkeypatch):
    dm = DamageManager()
    monkeypatch.setattr(random, "random", lambda: 0.0)
    dmg = dm.calculate(10, crit_chance=100, crit_multiplier=3)
    assert dmg == 30
