"""Versioned profile persistence for core progression data."""

from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import save_manager

CURRENT_SCHEMA_VERSION = 4


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp_int(value: Any, minimum: int, maximum: int, default: int) -> int:
    number = _as_int(value, default)
    return max(minimum, min(maximum, number))


def _sanitize_profile_id(profile_id: str | None) -> str:
    raw = str(profile_id or "default").strip()
    if not raw:
        return "default"
    safe = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in raw)
    return safe[:64] or "default"


@dataclass
class Profile:
    """Core profile data persisted between runs."""

    schema_version: int
    created_utc: str
    updated_utc: str
    profile_id: str
    progression: dict[str, Any]
    inventory: dict[str, Any]
    economy: dict[str, Any]
    achievements: dict[str, Any]
    reputation: dict[str, Any]
    objectives: dict[str, Any]
    meta: dict[str, Any]
    validation_warnings: list[str] = field(default_factory=list)
    raw_payload: dict[str, Any] = field(default_factory=dict, repr=False)

    def to_dict(self) -> dict[str, Any]:
        payload = copy.deepcopy(self.raw_payload) if self.raw_payload else {}
        payload["schema_version"] = int(self.schema_version)
        payload["created_utc"] = str(self.created_utc)
        payload["updated_utc"] = str(self.updated_utc)
        payload["profile_id"] = str(self.profile_id)
        data = payload.setdefault("data", {})
        if not isinstance(data, dict):
            data = {}
            payload["data"] = data
        data["progression"] = copy.deepcopy(self.progression)
        data["inventory"] = copy.deepcopy(self.inventory)
        data["economy"] = copy.deepcopy(self.economy)
        data["achievements"] = copy.deepcopy(self.achievements)
        data["reputation"] = copy.deepcopy(self.reputation)
        data["objectives"] = copy.deepcopy(self.objectives)
        data["meta"] = copy.deepcopy(self.meta)
        return payload


def default_profile(profile_id: str | None = None) -> Profile:
    """Return a default profile object with safe baseline values."""

    now = _utc_now()
    pid = _sanitize_profile_id(profile_id)
    return Profile(
        schema_version=CURRENT_SCHEMA_VERSION,
        created_utc=now,
        updated_utc=now,
        profile_id=pid,
        progression={
            "level": 1,
            "xp": 0,
            "threshold": 100,
            "growth": 1.12,
            "max_threshold": 1200,
            "unlocks": {"mmo_unlocked": False},
        },
        inventory={"items": {}, "capacity": 30},
        economy={"balances": {"coins": 0}},
        achievements={"unlocked_ids": [], "unlocked_utc": {}},
        reputation={"factions": {}},
        objectives={
            "region_key": None,
            "region_name": "Arena",
            "region_biome": "arena",
            "objectives": {},
        },
        meta={
            "profile_display_name": "Player",
            "last_played_character": "",
            "last_played_utc": now,
            "session_count": 0,
        },
        validation_warnings=[],
        raw_payload={},
    )


def migrate_v1_to_v2(payload: dict[str, Any]) -> dict[str, Any]:
    """Migrate schema v1 payloads to v2 while preserving unknown fields."""

    out = copy.deepcopy(payload)
    data = out.setdefault("data", {})
    if not isinstance(data, dict):
        data = {}
        out["data"] = data
    meta = data.setdefault("meta", {})
    if not isinstance(meta, dict):
        meta = {}
        data["meta"] = meta
    if "profile_display_name" not in meta:
        meta["profile_display_name"] = "Player"
    meta.setdefault("migration_notes", [])
    notes = meta.get("migration_notes")
    if isinstance(notes, list):
        notes.append("v1_to_v2")
    out["schema_version"] = 2
    return out


def migrate_v2_to_v3(payload: dict[str, Any]) -> dict[str, Any]:
    """Migrate schema v2 payloads to v3 while preserving unknown fields."""

    out = copy.deepcopy(payload)
    data = out.setdefault("data", {})
    if not isinstance(data, dict):
        data = {}
        out["data"] = data
    economy = data.setdefault("economy", {})
    if not isinstance(economy, dict):
        economy = {}
        data["economy"] = economy
    balances = economy.get("balances")
    if not isinstance(balances, dict):
        balances = {}
    if "coins" not in balances:
        balances["coins"] = _as_int(economy.get("coins"), 0)
    economy["balances"] = balances
    progression = data.setdefault("progression", {})
    if not isinstance(progression, dict):
        progression = {}
        data["progression"] = progression
    progression.setdefault("unlocks", {"mmo_unlocked": False})
    out["schema_version"] = 3
    return out


def migrate_v3_to_v4(payload: dict[str, Any]) -> dict[str, Any]:
    """Migrate schema v3 payloads to v4 while preserving unknown fields."""

    out = copy.deepcopy(payload)
    data = out.setdefault("data", {})
    if not isinstance(data, dict):
        data = {}
        out["data"] = data
    objectives = data.get("objectives")
    if not isinstance(objectives, dict):
        objectives = {}
    objectives.setdefault("region_key", None)
    objectives.setdefault("region_name", "Arena")
    objectives.setdefault("region_biome", "arena")
    raw_objectives = objectives.get("objectives")
    if not isinstance(raw_objectives, dict):
        objectives["objectives"] = {}
    data["objectives"] = objectives
    out["schema_version"] = 4
    return out


_MIGRATIONS: dict[int, Any] = {
    1: migrate_v1_to_v2,
    2: migrate_v2_to_v3,
    3: migrate_v3_to_v4,
}


def _run_migrations(payload: dict[str, Any]) -> dict[str, Any]:
    migrated = copy.deepcopy(payload)
    version = _as_int(migrated.get("schema_version"), 1)
    while version < CURRENT_SCHEMA_VERSION:
        migrate = _MIGRATIONS.get(version)
        if migrate is None:
            break
        migrated = migrate(migrated)
        version = _as_int(migrated.get("schema_version"), version + 1)
    return migrated


def _validate_payload(
    payload: dict[str, Any],
    *,
    profile_id: str | None = None,
) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    root = copy.deepcopy(payload)
    root["schema_version"] = CURRENT_SCHEMA_VERSION
    root["profile_id"] = _sanitize_profile_id(profile_id or root.get("profile_id"))
    root["created_utc"] = str(root.get("created_utc") or _utc_now())
    root["updated_utc"] = str(root.get("updated_utc") or _utc_now())
    data = root.get("data")
    if not isinstance(data, dict):
        data = {}
        root["data"] = data

    progression = data.get("progression")
    if not isinstance(progression, dict):
        progression = {}
    progression["level"] = _clamp_int(progression.get("level"), 1, 10000, 1)
    progression["xp"] = _clamp_int(progression.get("xp"), 0, 10_000_000, 0)
    progression["threshold"] = _clamp_int(progression.get("threshold"), 1, 1_000_000, 100)
    growth = _as_float(progression.get("growth"), 1.12)
    progression["growth"] = max(1.0, min(10.0, growth))
    max_threshold = progression.get("max_threshold")
    if max_threshold is None:
        progression["max_threshold"] = None
    else:
        progression["max_threshold"] = _clamp_int(max_threshold, 10, 1_000_000, 1200)
    unlocks = progression.get("unlocks")
    if not isinstance(unlocks, dict):
        unlocks = {}
    progression["unlocks"] = {
        str(key): bool(value) for key, value in unlocks.items() if isinstance(key, str)
    }
    progression["unlocks"].setdefault("mmo_unlocked", False)
    data["progression"] = progression

    inventory = data.get("inventory")
    if not isinstance(inventory, dict):
        inventory = {}
    items_raw = inventory.get("items")
    if not isinstance(items_raw, dict):
        items_raw = {}
        warnings.append("inventory.items was not a dict; defaulted to empty mapping")
    items: dict[str, int] = {}
    for key, value in items_raw.items():
        if not isinstance(key, str):
            warnings.append("inventory item key was non-string and was ignored")
            continue
        count = _as_int(value, 0)
        if count < 0:
            warnings.append(f"inventory.{key} was negative and was clamped to 0")
            count = 0
        items[key] = count
    inventory["items"] = items
    cap = inventory.get("capacity")
    if cap is None:
        inventory["capacity"] = None
    else:
        inventory["capacity"] = _clamp_int(cap, 0, 100000, 30)
    data["inventory"] = inventory

    economy = data.get("economy")
    if not isinstance(economy, dict):
        economy = {}
    balances = economy.get("balances")
    if not isinstance(balances, dict):
        balances = {"coins": _as_int(economy.get("coins"), 0)}
    normalized_balances: dict[str, int] = {}
    for key, value in balances.items():
        if not isinstance(key, str):
            warnings.append("economy balance key was non-string and was ignored")
            continue
        amount = _as_int(value, 0)
        if amount < 0:
            warnings.append(f"economy.{key} was negative and was clamped to 0")
            amount = 0
        normalized_balances[key] = amount
    normalized_balances.setdefault("coins", 0)
    economy["balances"] = normalized_balances
    data["economy"] = economy

    achievements = data.get("achievements")
    if not isinstance(achievements, dict):
        achievements = {}
    unlocked_ids = achievements.get("unlocked_ids")
    if not isinstance(unlocked_ids, list):
        unlocked_ids = achievements.get("achievements", [])
    if not isinstance(unlocked_ids, list):
        unlocked_ids = []
    deduped = sorted({str(item) for item in unlocked_ids if str(item)})
    achievements["unlocked_ids"] = deduped
    unlocked_utc = achievements.get("unlocked_utc")
    if not isinstance(unlocked_utc, dict):
        unlocked_utc = {}
    achievements["unlocked_utc"] = {
        str(k): str(v) for k, v in unlocked_utc.items() if isinstance(k, str)
    }
    data["achievements"] = achievements

    reputation = data.get("reputation")
    if not isinstance(reputation, dict):
        reputation = {}
    factions = reputation.get("factions")
    if not isinstance(factions, dict):
        factions = reputation
    if not isinstance(factions, dict):
        factions = {}
    reputation["factions"] = {
        str(k): _clamp_int(v, -1_000_000, 1_000_000, 0)
        for k, v in factions.items()
        if isinstance(k, str)
    }
    data["reputation"] = reputation

    objectives = data.get("objectives")
    if not isinstance(objectives, dict):
        objectives = {}
    objectives["region_key"] = (
        None
        if objectives.get("region_key") is None
        else str(objectives.get("region_key"))
    )
    objectives["region_name"] = str(objectives.get("region_name", "Arena") or "Arena")
    objectives["region_biome"] = str(
        objectives.get("region_biome", "arena") or "arena"
    )
    raw_objectives = objectives.get("objectives")
    if not isinstance(raw_objectives, dict):
        raw_objectives = {}
    normalized_objectives: dict[str, Any] = {}
    for key, value in raw_objectives.items():
        if not isinstance(key, str) or not isinstance(value, dict):
            warnings.append("objectives entry was invalid and was ignored")
            continue
        entry = dict(value)
        entry["description"] = str(entry.get("description", ""))
        entry["target"] = _clamp_int(entry.get("target"), 0, 1_000_000, 0)
        entry["progress"] = _clamp_int(entry.get("progress"), 0, 1_000_000, 0)
        entry["scope"] = str(entry.get("scope", "daily") or "daily")
        rewards = entry.get("rewards")
        if not isinstance(rewards, dict):
            rewards = {}
        entry["rewards"] = {
            str(r_key): max(0, _as_int(r_value, 0))
            for r_key, r_value in rewards.items()
            if isinstance(r_key, str)
        }
        entry["rewarded"] = bool(entry.get("rewarded", False))
        normalized_objectives[key] = entry
    objectives["objectives"] = normalized_objectives
    data["objectives"] = objectives

    meta = data.get("meta")
    if not isinstance(meta, dict):
        meta = {}
    meta["profile_display_name"] = str(meta.get("profile_display_name", "Player") or "Player")
    meta["last_played_character"] = str(meta.get("last_played_character", "") or "")
    meta["last_played_utc"] = str(meta.get("last_played_utc", root["updated_utc"]))
    meta["session_count"] = _clamp_int(meta.get("session_count"), 0, 1_000_000, 0)
    data["meta"] = meta
    root["data"] = data
    return root, warnings


def _payload_to_profile(payload: dict[str, Any], warnings: list[str]) -> Profile:
    data = payload.get("data", {})
    if not isinstance(data, dict):
        data = {}
    return Profile(
        schema_version=_as_int(payload.get("schema_version"), CURRENT_SCHEMA_VERSION),
        created_utc=str(payload.get("created_utc") or _utc_now()),
        updated_utc=str(payload.get("updated_utc") or _utc_now()),
        profile_id=_sanitize_profile_id(payload.get("profile_id")),
        progression=copy.deepcopy(data.get("progression", {})),
        inventory=copy.deepcopy(data.get("inventory", {})),
        economy=copy.deepcopy(data.get("economy", {})),
        achievements=copy.deepcopy(data.get("achievements", {})),
        reputation=copy.deepcopy(data.get("reputation", {})),
        objectives=copy.deepcopy(data.get("objectives", {})),
        meta=copy.deepcopy(data.get("meta", {})),
        validation_warnings=list(warnings),
        raw_payload=copy.deepcopy(payload),
    )


class ProfileStore:
    """Load/save versioned profile snapshots with migrations and backups."""

    def __init__(self, load_root: str | os.PathLike[str] | None = None) -> None:
        if load_root is None:
            load_root = Path(save_manager.SAVE_DIR) / "profiles"
        self.load_root = Path(load_root)
        self.load_root.mkdir(parents=True, exist_ok=True)

    def _profile_paths(self, profile_id: str | None) -> tuple[Path, Path]:
        pid = _sanitize_profile_id(profile_id)
        profile_dir = self.load_root / pid
        profile_dir.mkdir(parents=True, exist_ok=True)
        return profile_dir / "profile.json", profile_dir / "profile.json.bak"

    def migrate(self, save_dict: dict[str, Any]) -> dict[str, Any]:
        """Return a migrated payload upgraded to the current schema."""

        return _run_migrations(save_dict)

    def load(self, profile_id: str | None = None) -> Profile:
        """Load, migrate, validate, and return a profile."""

        profile_path, backup_path = self._profile_paths(profile_id)
        pid = _sanitize_profile_id(profile_id)

        if not profile_path.exists() and not backup_path.exists():
            profile = default_profile(pid)
            self.save(profile)
            return profile

        primary_error: str | None = None
        payload: dict[str, Any] | None = None
        source = profile_path
        try:
            payload = json.loads(profile_path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - exercised via tests
            primary_error = str(exc)

        if payload is None and backup_path.exists():
            source = backup_path
            try:
                payload = json.loads(backup_path.read_text(encoding="utf-8"))
            except Exception as exc:
                primary_error = f"{primary_error or 'primary load failed'}; backup failed: {exc}"

        if payload is None:
            profile = default_profile(pid)
            profile.validation_warnings.append(
                f"profile and backup unreadable; created default profile ({primary_error})"
            )
            self.save(profile)
            return profile

        migrated = _run_migrations(payload)
        validated, warnings = _validate_payload(migrated, profile_id=pid)
        profile = _payload_to_profile(validated, warnings)
        if source == backup_path:
            profile.validation_warnings.append("loaded profile from backup after primary read failed")
            self.save(profile)
        return profile

    def save(
        self,
        profile: Profile | str,
        data: dict[str, Any] | None = None,
    ) -> None:
        """Atomically persist a ``Profile`` or ``profile_id`` + ``data`` payload."""

        if isinstance(profile, Profile):
            profile_obj = profile
        else:
            profile_obj = default_profile(profile)
            if isinstance(data, dict):
                source_data = data.get("data", data)
                if not isinstance(source_data, dict):
                    source_data = {}
                profile_obj.progression = copy.deepcopy(
                    source_data.get("progression", profile_obj.progression)
                )
                profile_obj.inventory = copy.deepcopy(
                    source_data.get("inventory", profile_obj.inventory)
                )
                profile_obj.economy = copy.deepcopy(
                    source_data.get("economy", profile_obj.economy)
                )
                profile_obj.achievements = copy.deepcopy(
                    source_data.get("achievements", profile_obj.achievements)
                )
                profile_obj.reputation = copy.deepcopy(
                    source_data.get("reputation", profile_obj.reputation)
                )
                profile_obj.objectives = copy.deepcopy(
                    source_data.get("objectives", profile_obj.objectives)
                )
                profile_obj.meta = copy.deepcopy(source_data.get("meta", profile_obj.meta))
                if data.get("created_utc"):
                    profile_obj.created_utc = str(data.get("created_utc"))

        profile_obj.profile_id = _sanitize_profile_id(profile_obj.profile_id)
        profile_obj.schema_version = CURRENT_SCHEMA_VERSION
        if not profile_obj.created_utc:
            profile_obj.created_utc = _utc_now()
        profile_obj.updated_utc = _utc_now()
        payload, warnings = _validate_payload(
            profile_obj.to_dict(),
            profile_id=profile_obj.profile_id,
        )
        merged_warnings = list(profile_obj.validation_warnings)
        merged_warnings.extend(item for item in warnings if item not in merged_warnings)
        profile_obj.validation_warnings = merged_warnings
        profile_obj.raw_payload = copy.deepcopy(payload)
        profile_path, backup_path = self._profile_paths(profile_obj.profile_id)
        temp_path = profile_path.with_suffix(".json.tmp")
        payload_json = json.dumps(payload, indent=2, sort_keys=True)
        with temp_path.open("w", encoding="utf-8") as handle:
            handle.write(payload_json)
            handle.flush()
            os.fsync(handle.fileno())
        if profile_path.exists():
            shutil.copy2(profile_path, backup_path)
        os.replace(temp_path, profile_path)

    def reset(self, profile_id: str | None = None) -> None:
        """Reset a profile to default values and overwrite existing files."""

        profile = default_profile(profile_id)
        profile_path, backup_path = self._profile_paths(profile.profile_id)
        if backup_path.exists():
            backup_path.unlink()
        if profile_path.exists():
            profile_path.unlink()
        self.save(profile)

    def export(self, profile_id: str | None, path: str | os.PathLike[str]) -> None:
        """Export profile JSON to a custom path."""

        profile = self.load(profile_id=profile_id)
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(profile.to_dict(), indent=2, sort_keys=True),
            encoding="utf-8",
        )


def _build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect and maintain profile saves.")
    parser.add_argument("--profile", default="default", help="Profile ID (default: default)")
    parser.add_argument("--root", default=None, help="Optional profile root path override")
    parser.add_argument("--print", action="store_true", dest="print_profile", help="Print profile JSON")
    parser.add_argument("--reset", action="store_true", help="Reset profile to defaults")
    parser.add_argument("--validate", action="store_true", help="Validate and print warnings")
    parser.add_argument("--export", default=None, help="Export profile JSON to a path")
    return parser


def _cli_main(argv: list[str]) -> int:
    parser = _build_cli_parser()
    args = parser.parse_args(argv)
    store = ProfileStore(load_root=args.root)
    if args.reset:
        store.reset(args.profile)
    profile = store.load(args.profile)
    if args.validate:
        if profile.validation_warnings:
            for item in profile.validation_warnings:
                print(f"[WARN] {item}")
        else:
            print("[OK] profile validation passed")
    if args.export:
        store.export(args.profile, args.export)
    if args.print_profile:
        print(json.dumps(profile.to_dict(), indent=2, sort_keys=True))
    if not (args.print_profile or args.validate or args.export or args.reset):
        parser.print_help()
    return 0


def main() -> int:
    """CLI entry point used by ``python -m hololive_coliseum.profile_store``."""

    return _cli_main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
