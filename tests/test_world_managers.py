"""Tests for world managers."""

from hololive_coliseum.map_manager import MapManager
from hololive_coliseum.environment_manager import EnvironmentManager
from hololive_coliseum.spawn_manager import SpawnManager
from hololive_coliseum.event_manager import EventManager
from hololive_coliseum.dungeon_manager import DungeonManager
from hololive_coliseum.housing_manager import HousingManager
from hololive_coliseum.mount_manager import MountManager
from hololive_coliseum.pet_manager import PetManager
from hololive_coliseum.companion_manager import CompanionManager


def test_map_and_environment():
    mm = MapManager()
    mm.add_map("m1", {})
    assert mm.set_current("m1")
    assert mm.get_current() == {}
    env = EnvironmentManager()
    env.set("weather", "rain")
    assert env.get("weather") == "rain"


def test_spawn_and_event_manager():
    sm = SpawnManager()
    sm.schedule("orc", 5)
    assert not sm.get_ready(4)
    assert sm.get_ready(5) == ["orc"]
    em = EventManager()
    em.trigger("boss")
    assert em.get_history() == ["boss"]


def test_dungeon_and_housing():
    dm = DungeonManager()
    dm.set_lockout("p", "d", 10)
    assert not dm.can_enter("p", "d", 9)
    assert dm.can_enter("p", "d", 11)
    hm = HousingManager()
    hm.add_house("p", {"rooms": 1})
    assert hm.get_house("p") == {"rooms": 1}


def test_mount_pet_companion():
    mm = MountManager()
    mm.add_mount("p", "horse")
    assert mm.set_active("p", "horse")
    assert mm.get_active("p") == "horse"
    pm = PetManager()
    pm.add_pet("p", "cat")
    assert pm.list_pets("p") == ["cat"]
    cm = CompanionManager()
    cm.assign("p", "guide")
    assert cm.get("p") == "guide"


def test_day_night_cycle():
    env = EnvironmentManager(day_length_ms=1000)
    env.update(100)
    assert env.is_day()
    env.update(600)
    assert not env.is_day()
