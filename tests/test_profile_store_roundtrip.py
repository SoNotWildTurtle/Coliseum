"""Tests for ProfileStore round-trip persistence."""

from __future__ import annotations

from hololive_coliseum.profile_store import ProfileStore, default_profile


def test_profile_store_round_trip(tmp_path) -> None:
    store = ProfileStore(load_root=tmp_path / "profiles")
    profile = default_profile("player_one")
    profile["build"]["git"] = "abc123"
    profile["data"]["inventory"]["items"] = {"potion": 4, "gem": 2}
    profile["data"]["economy"]["balances"]["coins"] = 123
    profile["data"]["progression"]["level"] = 7
    profile["data"]["progression"]["xp"] = 88
    profile["data"]["achievements"]["unlocked_ids"] = ["First Blood"]
    profile["data"]["reputation"]["factions"] = {"Arena": 9}
    profile["data"]["objectives"] = {"objectives": {"daily": {"progress": 1}}}

    store.save("player_one", profile)
    loaded, warnings = store.load("player_one")

    assert warnings == []
    assert loaded["profile_id"] == "player_one"
    assert loaded["schema_version"] == 1
    assert loaded["data"]["inventory"]["items"] == {"potion": 4, "gem": 2}
    assert loaded["data"]["economy"]["balances"]["coins"] == 123
    assert loaded["data"]["progression"]["level"] == 7
    assert loaded["data"]["achievements"]["unlocked_ids"] == ["First Blood"]
