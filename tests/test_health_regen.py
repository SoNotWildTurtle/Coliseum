"""Tests for health regen."""

from hololive_coliseum.health_manager import HealthManager


def test_health_regenerates_after_delay():
    mgr = HealthManager(10)
    mgr.take_damage(5, now=0)
    mgr.update(now=2999)
    assert mgr.health == 5
    mgr.update(now=3000)
    assert mgr.health == 6
    mgr.update(now=3999)
    assert mgr.health == 6
    mgr.update(now=4000)
    assert mgr.health == 7
