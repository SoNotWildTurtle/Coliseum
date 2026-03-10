"""Tests for ProfileStore corruption fallback behavior."""

from __future__ import annotations

import json

from hololive_coliseum.profile_store import ProfileStore, default_profile


def test_profile_store_uses_backup_when_primary_is_corrupt(tmp_path) -> None:
    store = ProfileStore(load_root=tmp_path / "profiles")
    profile = default_profile("recover")
    profile["data"]["economy"]["balances"]["coins"] = 41
    store.save("recover", profile)

    profile_path = tmp_path / "profiles" / "recover" / "profile.json"
    backup_path = tmp_path / "profiles" / "recover" / "profile.json.bak"
    backup_path.write_text(profile_path.read_text(encoding="utf-8"), encoding="utf-8")
    profile_path.write_text("{broken json", encoding="utf-8")

    loaded, warnings = store.load("recover")

    assert loaded["data"]["economy"]["balances"]["coins"] == 41
    assert any("backup" in item for item in warnings)
