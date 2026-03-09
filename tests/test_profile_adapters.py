"""Tests for profile adapter export/hydration helpers."""

from __future__ import annotations

from types import SimpleNamespace

from hololive_coliseum.profile_adapters import export_profile_data, hydrate_profile_data
from hololive_coliseum.profile_store import default_profile


class _Inventory:
    def __init__(self) -> None:
        self.items = {}
        self.capacity = None

    def to_dict(self) -> dict[str, int]:
        return dict(self.items)

    def load_from_dict(self, data: dict[str, int]) -> None:
        self.items = dict(data)


class _Currency:
    def __init__(self, balance: int = 0) -> None:
        self.balance = balance

    def get_balance(self) -> int:
        return self.balance


class _XP:
    def __init__(self) -> None:
        self.level = 1
        self.xp = 0
        self.threshold = 100
        self.growth = 1.0
        self.max_threshold = None


class _Achievements:
    def __init__(self) -> None:
        self.unlocked = set()

    def load_from_dict(self, data: dict[str, object]) -> None:
        self.unlocked = set(data.get("achievements", []))


class _Reputation:
    def __init__(self) -> None:
        self.rep = {}

    def to_dict(self) -> dict[str, int]:
        return dict(self.rep)

    def load_from_dict(self, data: dict[str, int]) -> None:
        self.rep = dict(data)


class _Objectives:
    def __init__(self) -> None:
        self.data = {"objectives": {}}
        self.objectives = {}

    def to_dict(self) -> dict[str, object]:
        return dict(self.data)

    def load_from_dict(self, data: dict[str, object]) -> None:
        self.data = dict(data)
        self.objectives = dict(data.get("objectives", {}))


def _game_and_player():
    profile = default_profile("adapter")
    game = SimpleNamespace(
        profile=profile,
        coins=0,
        mmo_unlocked=False,
        selected_character="Gura",
        achievement_manager=_Achievements(),
        reputation_manager=_Reputation(),
        objective_manager=_Objectives(),
    )
    player = SimpleNamespace(
        inventory=_Inventory(),
        currency_manager=_Currency(),
        experience_manager=_XP(),
    )
    return game, player


def test_export_profile_data_reads_from_managers() -> None:
    game, player = _game_and_player()
    player.inventory.items = {"potion": 3}
    player.inventory.capacity = 20
    player.currency_manager.balance = 77
    player.experience_manager.level = 5
    player.experience_manager.xp = 22
    game.achievement_manager.unlocked = {"First Blood"}
    game.reputation_manager.rep = {"Arena": 9}
    game.objective_manager.data = {"objectives": {"daily": {"progress": 1}}}
    game.mmo_unlocked = True

    data = export_profile_data(game, player=player)

    assert data["inventory"]["items"] == {"potion": 3}
    assert data["economy"]["balances"]["coins"] == 77
    assert data["progression"]["level"] == 5
    assert data["reputation"]["factions"]["Arena"] == 9
    assert data["achievements"]["unlocked_ids"] == ["First Blood"]
    assert data["progression"]["unlocks"]["mmo_unlocked"] is True


def test_hydrate_profile_data_applies_manager_state() -> None:
    game, player = _game_and_player()
    payload = {
        "inventory": {"items": {"gem": 2}, "capacity": 10},
        "economy": {"balances": {"coins": 42}},
        "progression": {
            "level": 3,
            "xp": 11,
            "threshold": 120,
            "growth": 1.2,
            "max_threshold": 900,
            "unlocks": {"mmo_unlocked": True},
        },
        "reputation": {"factions": {"Forge Guild": 4}},
        "achievements": {"unlocked_ids": ["First Blood"]},
        "objectives": {"objectives": {"daily": {"progress": 1}}},
    }

    hydrate_profile_data(game, payload, player=player)

    assert player.inventory.items == {"gem": 2}
    assert player.inventory.capacity == 10
    assert player.currency_manager.balance == 42
    assert game.coins == 42
    assert player.experience_manager.level == 3
    assert player.experience_manager.xp == 11
    assert game.mmo_unlocked is True
    assert game.reputation_manager.rep == {"Forge Guild": 4}
    assert game.achievement_manager.unlocked == {"First Blood"}
    assert game.objective_manager.objectives == {"daily": {"progress": 1}}
