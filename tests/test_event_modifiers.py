"""Tests for event modifiers."""

import pytest


class DummyRegionManager:
    def __init__(self, regions):
        self._regions = list(regions)

    def get_regions(self):
        return list(self._regions)


def test_event_modifier_defaults():
    from hololive_coliseum.event_modifier_manager import EventModifierManager

    manager = EventModifierManager(DummyRegionManager([]))
    config = manager.refresh()
    assert config["xp_multiplier"] == 1.0
    assert config["stamina_regen_step"] == 1.0
    assert config["description"] == "Standard arena conditions."


def test_event_modifier_applies_to_game(tmp_path, monkeypatch):
    pygame = pytest.importorskip("pygame")
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    from hololive_coliseum.event_modifier_manager import EventModifierManager

    region = {
        "name": "region_desert",
        "biome": "desert",
        "recommended_level": 12,
        "feature": {"type": "monument"},
    }
    manager = EventModifierManager(DummyRegionManager([region]))
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.event_modifier_manager = manager
    game.match_modifiers = manager.get_config()
    game.selected_character = "Gawr Gura"
    game.selected_chapter = game.chapters[0]
    game._setup_level()
    assert game.match_modifiers["source_region"] == "region_desert"
    assert game.xp_multiplier > 1.0
    assert game.hazard_manager.damage_multiplier > 1.0
    stamina_manager = game.player.stamina_manager
    stamina_manager.use(2)
    baseline = stamina_manager.stamina
    stamina_manager.regen(1)
    after_first = stamina_manager.stamina
    stamina_manager.regen(1)
    after_second = stamina_manager.stamina
    assert after_first == baseline
    assert after_second == baseline + 1
    pygame.quit()


def test_event_modifier_tundra_high_level_monument():
    from hololive_coliseum.event_modifier_manager import EventModifierManager

    region = {
        "name": "region_tundra",
        "biome": "tundra",
        "recommended_level": 12,
        "feature": {"type": "monument"},
    }
    manager = EventModifierManager(DummyRegionManager([region]))
    config = manager.refresh()
    assert config["hazard_damage_multiplier"] == 1.35
    assert config["xp_multiplier"] == 1.05
    description = config["description"]
    assert "Tundra" in description
    assert "High level threats" in description
    assert "Faction monument" in description
