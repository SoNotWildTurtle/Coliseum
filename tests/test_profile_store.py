"""Tests for versioned profile persistence and recovery."""

from __future__ import annotations

import json
from pathlib import Path

from hololive_coliseum.profile_store import ProfileStore, default_profile


def test_profile_round_trip(tmp_path) -> None:
    store = ProfileStore(load_root=tmp_path / "profiles")
    profile = default_profile("player_one")
    profile.progression["level"] = 7
    profile.progression["xp"] = 88
    profile.inventory["items"] = {"potion": 4, "gem": 2}
    profile.economy["balances"]["coins"] = 123
    profile.achievements["unlocked_ids"] = ["First Blood"]
    profile.reputation["factions"] = {"Arena": 9}
    store.save(profile)

    loaded = store.load("player_one")
    assert loaded.profile_id == "player_one"
    assert loaded.progression["level"] == 7
    assert loaded.progression["xp"] == 88
    assert loaded.inventory["items"] == {"potion": 4, "gem": 2}
    assert loaded.economy["balances"]["coins"] == 123
    assert loaded.achievements["unlocked_ids"] == ["First Blood"]
    assert loaded.reputation["factions"]["Arena"] == 9


def test_profile_migrates_v1_fixture(tmp_path) -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "profile_v1.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    profile_dir = tmp_path / "profiles" / "legacy"
    profile_dir.mkdir(parents=True, exist_ok=True)
    (profile_dir / "profile.json").write_text(json.dumps(fixture), encoding="utf-8")

    store = ProfileStore(load_root=tmp_path / "profiles")
    profile = store.load("legacy")
    assert profile.schema_version == 3
    assert profile.economy["balances"]["coins"] == 25
    assert profile.progression["unlocks"]["mmo_unlocked"] is False
    assert "profile_display_name" in profile.meta


def test_profile_corruption_falls_back_to_backup(tmp_path) -> None:
    store = ProfileStore(load_root=tmp_path / "profiles")
    profile = default_profile("recover")
    profile.economy["balances"]["coins"] = 41
    store.save(profile)
    profile_path = tmp_path / "profiles" / "recover" / "profile.json"
    backup_path = tmp_path / "profiles" / "recover" / "profile.json.bak"
    backup_path.write_text(profile_path.read_text(encoding="utf-8"), encoding="utf-8")
    profile_path.write_text("{broken json", encoding="utf-8")

    loaded = store.load("recover")
    assert loaded.economy["balances"]["coins"] == 41
    assert any("backup" in warning for warning in loaded.validation_warnings)


def test_profile_validation_clamps_invalid_values(tmp_path) -> None:
    profile_dir = tmp_path / "profiles" / "clamp"
    profile_dir.mkdir(parents=True, exist_ok=True)
    invalid_payload = {
        "schema_version": 3,
        "profile_id": "clamp",
        "data": {
            "inventory": {"items": {"potion": -4}},
            "economy": {"balances": {"coins": -100}},
            "progression": {"level": -9, "xp": -25, "threshold": 0},
        },
    }
    (profile_dir / "profile.json").write_text(
        json.dumps(invalid_payload),
        encoding="utf-8",
    )

    store = ProfileStore(load_root=tmp_path / "profiles")
    loaded = store.load("clamp")
    assert loaded.inventory["items"]["potion"] == 0
    assert loaded.economy["balances"]["coins"] == 0
    assert loaded.progression["level"] == 1
    assert loaded.progression["xp"] == 0
    assert loaded.progression["threshold"] == 1
    assert loaded.validation_warnings
