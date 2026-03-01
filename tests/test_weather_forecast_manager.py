"""Tests for the WeatherForecastManager and its environment integration."""

import random

from hololive_coliseum.environment_manager import EnvironmentManager, WEATHER_FRICTION
from hololive_coliseum.weather_forecast_manager import WeatherForecastManager


def test_forecast_matches_random_sequence():
    """Forecasts should be reproducible for the same seed."""
    seed = 7
    manager = WeatherForecastManager(seed)
    rng = random.Random(seed)
    expected = [rng.choice(manager.weather_types) for _ in range(5)]
    assert manager.forecast(5) == expected
    for weather in expected:
        assert manager.next_weather() == weather
    # After consuming entries, requesting more should extend deterministically.
    extended = manager.forecast(3)
    expected.extend(rng.choice(manager.weather_types) for _ in range(3))
    assert extended == expected[-3:]


def test_environment_randomize_uses_forecast_sequence():
    """EnvironmentManager should draw weather from the attached forecast."""
    forecast = WeatherForecastManager(seed=3)
    environment = EnvironmentManager()
    environment.attach_forecast_manager(forecast)
    upcoming = forecast.forecast(4)
    observed = [environment.randomize_weather() for _ in range(4)]
    assert observed == upcoming
    last = observed[-1]
    assert environment.get("friction") == WEATHER_FRICTION[last]
    # Upcoming preview should continue from the current forecast index.
    preview = environment.upcoming_weather(2)
    assert preview == forecast.forecast(2)
