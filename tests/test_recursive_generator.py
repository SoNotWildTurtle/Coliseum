"""Tests for recursive generator."""

import pytest

from hololive_coliseum.recursive_generator import RecursiveGenerator


def test_recursive_generator_builds_data():
    rg = RecursiveGenerator()
    base = {"Warrior": {"attack": 10, "defense": 5, "health": 100}}
    data = rg.generate_all(base, ["Mining"])
    assert "classes" in data and "Warrior" in data["classes"]
    assert "subclasses" in data and "Warrior" in data["subclasses"]
    assert data["skills"]["Warrior"][0]["name"].startswith("Warrior")
    assert "Mining" in data["trade_skills"]
