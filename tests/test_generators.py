"""Tests for generators."""

import pytest

from hololive_coliseum import (
    ClassGenerator,
    ClassManager,
    SkillGenerator,
    SubclassGenerator,
    TradeSkillGenerator,
    InteractionGenerator,
    InteractionManager,
    AutoBalancer,
)


def test_skill_generator():
    gen = SkillGenerator()
    skills = gen.generate("Warrior", 10)
    assert skills[0]["name"] == "Warrior Strike"
    assert skills[0]["damage"] == 15


def test_subclass_generator():
    gen = SubclassGenerator()
    base = {"name": "Warrior", "attack": 5}
    sub = gen.create(base, "Elite")
    assert sub["name"] == "Elite Warrior"
    assert sub["attack"] == 6


def test_trade_skill_generator():
    gen = TradeSkillGenerator()
    skill = gen.generate("Mining")
    assert skill["name"] == "Mining"
    assert skill["experience"] == 0
    assert "specialisations" in skill and skill["specialisations"]
    assert "recipes" in skill and skill["recipes"]
    recipe = skill["recipes"][0]
    assert recipe["product"] in {"weapon", "armor", "bow", "wand", "material"}
    assert skill["level_band"]["min"] <= skill["level_band"]["max"]
    assert skill["difficulty_tier"] in {"novice", "adept", "master"}


def test_trade_skill_generator_handles_new_specialisations() -> None:
    gen = TradeSkillGenerator()
    enchanting = gen.generate("Enchanting")
    assert enchanting["difficulty_tier"] == "master"
    assert any(recipe["product"] == "wand" for recipe in enchanting["recipes"])
    assert enchanting["level_band"]["min"] >= 30


def test_trade_skill_generator_includes_gatherers() -> None:
    gen = TradeSkillGenerator()
    herbalism = gen.generate("Herbalism")
    assert herbalism["gathering_synergy"]["armor"]["health"] >= 4
    assert herbalism["recipes"][0]["product"] == "material"
    bonuses = gen.collect_gathering_bonuses(["Herbalism", "Prospecting"])
    assert "weapon" in bonuses and bonuses["weapon"]["attack"] > 0


def test_auto_balancer():
    balancer = AutoBalancer()
    classes = {
        "A": {"attack": 10, "defense": 5, "health": 100},
        "B": {"attack": 20, "defense": 15, "health": 80},
    }
    result = balancer.balance(classes)
    assert result["A"]["attack"] > classes["A"]["attack"]
    assert result["B"]["attack"] < classes["B"]["attack"]


def test_class_generator_unique_and_balance():
    gen = ClassGenerator()
    c1 = gen.create("Rogue", {"attack": 5, "defense": 2, "health": 50})
    c2 = gen.create("Rogue", {"attack": 6, "defense": 3, "health": 60})
    assert c1["name"] != c2["name"]

    cm = ClassManager()
    cm.add_class(c1["name"], c1)
    cm.add_class(c2["name"], c2)
    balanced = AutoBalancer().balance(cm.classes)
    assert set(balanced) == {c1["name"], c2["name"]}


def test_interaction_generator_and_manager():
    gen = InteractionGenerator()
    mgr = InteractionManager()
    first = gen.create("Lever", "open")
    second = gen.create("Lever", "close")
    assert first["name"] != second["name"]
    mgr.register(first)
    mgr.register(second)
    assert mgr.interact(first["name"]) == "open"
    assert mgr.interact(second["name"]) == "close"
