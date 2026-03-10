"""Tests for migration scaffolding and legacy fixture loading."""

from __future__ import annotations

import json
from pathlib import Path

from hololive_coliseum.profile_store import ProfileStore, migrate


def test_profile_store_migration_scaffold_preserves_required_sections(tmp_path) -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "profile_v1.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    migrated = migrate(fixture)

    assert migrated["schema_version"] >= 1

    profile_dir = tmp_path / "profiles" / "legacy"
    profile_dir.mkdir(parents=True, exist_ok=True)
    (profile_dir / "profile.json").write_text(json.dumps(fixture), encoding="utf-8")

    store = ProfileStore(load_root=tmp_path / "profiles")
    loaded, warnings = store.load("legacy")

    assert loaded["schema_version"] == 1
    for key in (
        "inventory",
        "economy",
        "progression",
        "reputation",
        "achievements",
        "objectives",
        "meta",
    ):
        assert key in loaded["data"]
    assert isinstance(warnings, list)
