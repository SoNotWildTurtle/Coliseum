"""Tests for weather effect."""

import pytest
import hololive_coliseum.environment_manager as env_mod


def test_rain_lowers_friction(monkeypatch):
    pygame = pytest.importorskip("pygame")
    from hololive_coliseum.game import Game

    monkeypatch.setattr(env_mod.random, "choice", lambda seq: "rain")
    g = Game()
    g.level_manager.setup_level()
    assert g.environment_manager.get("weather") == "rain"
    assert g.player.friction_multiplier == pytest.approx(0.8)


def test_snow_increases_friction(monkeypatch):
    pygame = pytest.importorskip("pygame")
    from hololive_coliseum.game import Game

    monkeypatch.setattr(env_mod.random, "choice", lambda seq: "snow")
    g = Game()
    g.level_manager.setup_level()
    assert g.environment_manager.get("weather") == "snow"
    assert g.player.friction_multiplier == pytest.approx(0.6)


def test_day_night_adjusts_light_level():
    manager = env_mod.EnvironmentManager(day_length_ms=1000)
    manager.set("weather", "clear")
    manager.update(0)
    night_overlay = manager.ambient_overlay()
    assert manager.get_light_level() == pytest.approx(0.0, abs=1e-6)
    assert night_overlay[3] > 0

    manager.update(500)
    day_overlay = manager.ambient_overlay()
    assert manager.get_light_level() == pytest.approx(1.0, rel=1e-6)
    assert day_overlay[3] < night_overlay[3]


def test_weather_changes_overlay_tint():
    manager = env_mod.EnvironmentManager(day_length_ms=1000)
    manager.set("weather", "snow")
    manager.update(250)
    snow_overlay = manager.ambient_overlay()
    assert snow_overlay[:3] == env_mod.WEATHER_TINTS["snow"]
