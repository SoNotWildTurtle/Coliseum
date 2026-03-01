"""Tests for gathering manager."""

from hololive_coliseum.gathering_manager import GatheringManager
from hololive_coliseum.profession_manager import ProfessionManager
from hololive_coliseum.inventory_manager import InventoryManager


def test_gathering_timing_rewards():
    inv = InventoryManager()
    prof = ProfessionManager()
    gm = GatheringManager(prof, inv)
    gm.add_resource("mining", "stone", "gem")

    common = gm.gather("mining", 0.2)
    rare = gm.gather("mining", 0.51)

    assert common == "stone"
    assert rare == "gem"
    assert inv.count("stone") == 1
    assert inv.count("gem") == 1
    assert prof._xp["mining"] == 25
