"""Tests for leveling manager."""

import hololive_coliseum.world_generation_manager as wgm
from hololive_coliseum.leveling_manager import LevelingManager

class DummySeedManager:
    def get_seeds(self):
        return ["abcd1234"]

class DummyContentManager:
    def create(self, kind: str) -> str:
        return f"{kind}_1"

class DummyRegionManager:
    def __init__(self):
        self.added = []

    def add_region(self, region):
        self.added.append(region)

    def get_regions(self):
        return self.added


def test_region_grants_experience():
    lm = LevelingManager()
    wg = wgm.WorldGenerationManager(
        DummySeedManager(), DummyContentManager(), DummyRegionManager(), level_manager=lm
    )
    region = wg.generate_region(player_id="p1")
    assert region["recommended_level"] == 1
    assert lm.get_xp("p1") == 50
    wg.generate_region_from_seed("abcd0000", "p1")
    assert lm.get_level("p1") == 2

