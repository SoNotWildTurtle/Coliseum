"""Tests for world player manager."""

import math

from hololive_coliseum.world_player_manager import WorldPlayerManager


class DummyRegionManager:
    def __init__(self):
        self.regions = [{"radius": 1, "angle": 0, "position": [1, 0]}]

    def get_regions(self):
        return self.regions


def test_move_player_is_clamped_to_radius():
    region_mgr = DummyRegionManager()
    manager = WorldPlayerManager(region_manager=region_mgr)
    manager.set_position("p1", (0, 0))
    manager.move_player("p1", 0.5, 0)
    assert manager.get_position("p1") == (0.5, 0)
    manager.move_player("p1", 1.0, 0)
    # radius is 1 so position should clamp at (1, 0)
    assert manager.get_position("p1") == (1.0, 0.0)


def test_get_position_defaults_to_origin():
    manager = WorldPlayerManager()
    assert manager.get_position("missing") == (0.0, 0.0)


def test_move_player_relative_uses_yaw():
    region_mgr = DummyRegionManager()
    region_mgr.regions[0]["radius"] = 5
    manager = WorldPlayerManager(region_manager=region_mgr)
    manager.set_position("p1", (0, 0))
    manager.move_player_relative("p1", 1.0, 0.0, math.pi / 2)
    x, y = manager.get_position("p1")
    assert math.isclose(x, 0.0, abs_tol=1e-6)
    assert math.isclose(y, 1.0, abs_tol=1e-6)
