"""Tests for resource managers."""

from hololive_coliseum.health_manager import HealthManager
from hololive_coliseum.mana_manager import ManaManager
from hololive_coliseum.stamina_manager import StaminaManager
from hololive_coliseum.equipment_manager import EquipmentManager
from hololive_coliseum.inventory_manager import InventoryManager
from hololive_coliseum.keybind_manager import KeybindManager
from hololive_coliseum.stats_manager import StatsManager
from hololive_coliseum.experience_manager import ExperienceManager


def test_health_manager_basic():
    mgr = HealthManager(100)
    assert mgr.take_damage(30) == 70
    assert mgr.heal(20) == 90
    assert mgr.take_damage(200) == 0


def test_mana_manager_usage():
    mgr = ManaManager(50)
    assert mgr.use(20)
    assert mgr.mana == 30
    assert not mgr.use(40)
    mgr.regen(10)
    assert mgr.mana == 40


def test_stamina_manager_usage():
    mgr = StaminaManager(50)
    assert mgr.use(30)
    assert mgr.stamina == 20
    assert not mgr.use(25)
    mgr.regen(10)
    assert mgr.stamina == 30


def test_equipment_manager():
    mgr = EquipmentManager()
    mgr.equip("weapon", "Sword")
    assert mgr.get("weapon") == "Sword"
    mgr.unequip("weapon")
    assert mgr.get("weapon") is None


def test_inventory_manager_add_remove():
    mgr = InventoryManager()
    mgr.add("Potion")
    assert mgr.has("Potion")
    assert mgr.count("Potion") == 1
    mgr.add("Potion", 2)
    assert mgr.count("Potion") == 3
    assert mgr.remove("Potion", 2)
    assert mgr.count("Potion") == 1
    assert mgr.remove("Potion")
    assert not mgr.has("Potion")


def test_keybind_manager_basic():
    defaults = {"jump": 32}
    mgr = KeybindManager(defaults)
    assert mgr.get("jump") == 32
    mgr.set("jump", 10)
    assert mgr.get("jump") == 10
    saved = mgr.to_dict()
    mgr.set("shoot", 5)
    mgr.load_from_dict(saved)
    assert "shoot" not in mgr.bindings
    mgr.reset()
    assert mgr.get("jump") == 32


def test_stats_manager_modifiers():
    mgr = StatsManager({"str": 10, "dex": 5})
    assert mgr.get("str") == 10
    mgr.apply_modifier("str", 5)
    assert mgr.get("str") == 15
    mgr.remove_modifier("str", 3)
    assert mgr.get("str") == 12


def test_experience_manager_levels():
    mgr = ExperienceManager(level=1, xp=90, threshold=100)
    assert not mgr.add_xp(5)
    assert mgr.level == 1 and mgr.xp == 95
    assert mgr.add_xp(10)
    assert mgr.level == 2 and mgr.xp == 5
