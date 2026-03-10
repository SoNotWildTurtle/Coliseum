"""Tests for ProfileStore validation and sanitization."""

from __future__ import annotations

import json

from hololive_coliseum.profile_store import ProfileStore


def test_profile_store_validation_clamps_and_fills_missing_sections(tmp_path) -> None:
    store = ProfileStore(load_root=tmp_path / "profiles")
    invalid = {
        "schema_version": 1,
        "profile_id": "clamp",
        "data": {
            "inventory": {"items": {"potion": -4}},
            "economy": {"balances": {"coins": -100}},
            "progression": {"level": -9, "xp": -25, "threshold": 0},
        },
    }

    profile_dir = tmp_path / "profiles" / "clamp"
    profile_dir.mkdir(parents=True, exist_ok=True)
    (profile_dir / "profile.json").write_text(json.dumps(invalid), encoding="utf-8")
    loaded, warnings = store.load("clamp")

    assert loaded["data"]["inventory"]["items"]["potion"] == 0
    assert loaded["data"]["economy"]["balances"]["coins"] == 0
    assert loaded["data"]["progression"]["level"] == 1
    assert loaded["data"]["progression"]["xp"] == 0
    assert loaded["data"]["progression"]["threshold"] == 1
    assert "achievements" in loaded["data"]
    assert "objectives" in loaded["data"]
    assert warnings
