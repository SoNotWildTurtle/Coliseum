"""Versioned profile persistence for gameplay progression."""

from __future__ import annotations

import argparse
import copy
import json
import math
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import save_manager

CURRENT_SCHEMA_VERSION = 1
DATA_KEYS = (
    "inventory",
    "economy",
    "progression",
    "reputation",
    "achievements",
    "objectives",
    "meta",
)
Profile = dict[str, Any]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        if isinstance(value, float) and not math.isfinite(value):
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    return number


def _clamp_int(value: Any, minimum: int, maximum: int, default: int) -> int:
    return max(minimum, min(maximum, _safe_int(value, default)))


def _json_safe(value: Any) -> Any:
    """Return a JSON-safe clone of ``value`` for forward-compatible storage."""

    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else 0.0
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return str(value)


def _sanitize_profile_id(profile_id: str | None) -> str:
    raw = str(profile_id or "default").strip()
    if not raw:
        return "default"
    safe = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in raw)
    return safe[:64] or "default"


def default_profile(profile_id: str | None = None) -> Profile:
    """Return the default schema v1 profile payload."""

    now = _utc_now()
    return {
        "schema_version": CURRENT_SCHEMA_VERSION,
        "profile_id": _sanitize_profile_id(profile_id),
        "created_utc": now,
        "updated_utc": now,
        "build": {
            "git": "",
            "python": sys.version.split()[0],
        },
        "data": {
            "inventory": {"items": {}, "capacity": 30, "equipment": {}},
            "economy": {"balances": {"coins": 0}},
            "progression": {
                "level": 1,
                "xp": 0,
                "threshold": 100,
                "growth": 1.12,
                "max_threshold": 1200,
                "stat_points": 0,
                "unlocks": {"mmo_unlocked": False},
                "unlocked_characters": [],
                "unlocked_skills": [],
            },
            "reputation": {"factions": {}, "last_updated_utc": {}},
            "achievements": {"unlocked_ids": [], "unlocked_utc": {}},
            "objectives": {},
            "meta": {
                "profile_display_name": "Player",
                "last_played_character": "",
                "last_played_utc": now,
                "session_count": 0,
            },
        },
    }


def migrate_v1_to_v2(payload: dict[str, Any]) -> dict[str, Any]:
    """Scaffold for future migrations while preserving unknown keys."""

    migrated = copy.deepcopy(payload)
    migrated["schema_version"] = 2
    return migrated


def migrate(profile_dict: dict[str, Any] | None) -> dict[str, Any]:
    """Return a migrated profile payload upgraded to the supported schema."""

    payload = copy.deepcopy(profile_dict) if isinstance(profile_dict, dict) else {}
    version = _safe_int(payload.get("schema_version"), CURRENT_SCHEMA_VERSION)
    if version <= 0:
        payload["schema_version"] = CURRENT_SCHEMA_VERSION
    return payload


def validate_and_sanitize(
    profile_dict: dict[str, Any] | None,
    *,
    profile_id: str | None = None,
) -> tuple[dict[str, Any], list[str]]:
    """Normalize a profile payload and return warnings instead of crashing."""

    warnings: list[str] = []
    root = default_profile(profile_id)
    if isinstance(profile_dict, dict):
        root.update({k: copy.deepcopy(v) for k, v in profile_dict.items() if k != "data"})
    root["schema_version"] = CURRENT_SCHEMA_VERSION
    root["profile_id"] = _sanitize_profile_id(profile_id or root.get("profile_id"))
    root["created_utc"] = str(root.get("created_utc") or _utc_now())
    root["updated_utc"] = str(root.get("updated_utc") or _utc_now())

    build = root.get("build")
    if not isinstance(build, dict):
        build = {}
        warnings.append("build was not a mapping; defaulted")
    root["build"] = {
        "git": str(build.get("git", "") or ""),
        "python": str(build.get("python", sys.version.split()[0]) or sys.version.split()[0]),
    }

    incoming_data = {}
    if isinstance(profile_dict, dict):
        raw_data = profile_dict.get("data")
        if isinstance(raw_data, dict):
            incoming_data = copy.deepcopy(raw_data)
        elif raw_data is not None:
            warnings.append("data was not a mapping; defaulted")
    data = root["data"]
    for key, value in incoming_data.items():
        if key not in DATA_KEYS:
            data[str(key)] = _json_safe(value)

    inventory = incoming_data.get("inventory", {})
    if not isinstance(inventory, dict):
        inventory = {}
        warnings.append("inventory was not a mapping; defaulted")
    items_raw = inventory.get("items", {})
    if not isinstance(items_raw, dict):
        items_raw = {}
        warnings.append("inventory.items was not a mapping; defaulted")
    inventory_items: dict[str, int] = {}
    for key, value in items_raw.items():
        if not isinstance(key, str):
            continue
        amount = _safe_int(value, 0)
        if amount < 0:
            warnings.append(f"inventory.items.{key} was negative and was clamped to 0")
            amount = 0
        inventory_items[str(key)] = amount
    data["inventory"]["items"] = inventory_items
    equipment_raw = inventory.get("equipment", {})
    if not isinstance(equipment_raw, dict):
        equipment_raw = {}
    data["inventory"]["equipment"] = {
        str(slot): str(item)
        for slot, item in equipment_raw.items()
        if isinstance(slot, str)
    }
    capacity = inventory.get("capacity", data["inventory"]["capacity"])
    data["inventory"]["capacity"] = (
        None if capacity is None else _clamp_int(capacity, 0, 100_000, 30)
    )

    economy = incoming_data.get("economy", {})
    if not isinstance(economy, dict):
        economy = {}
        warnings.append("economy was not a mapping; defaulted")
    balances = economy.get("balances")
    if not isinstance(balances, dict):
        legacy_coins = economy.get("coins", 0)
        balances = {"coins": legacy_coins}
    normalized_balances: dict[str, int] = {}
    for key, value in balances.items():
        if not isinstance(key, str):
            warnings.append("economy balance key was non-string and was ignored")
            continue
        amount = _safe_int(value, 0)
        if amount < 0:
            warnings.append(f"economy.{key} was negative and was clamped to 0")
            amount = 0
        normalized_balances[key] = amount
    normalized_balances.setdefault("coins", 0)
    data["economy"]["balances"] = normalized_balances

    progression = incoming_data.get("progression", {})
    if not isinstance(progression, dict):
        progression = {}
        warnings.append("progression was not a mapping; defaulted")
    level_value = _safe_int(progression.get("level"), 1)
    if level_value < 1:
        warnings.append("progression.level was below 1 and was clamped")
    data["progression"]["level"] = _clamp_int(level_value, 1, 10_000, 1)
    xp_value = _safe_int(progression.get("xp"), 0)
    if xp_value < 0:
        warnings.append("progression.xp was negative and was clamped to 0")
    data["progression"]["xp"] = _clamp_int(xp_value, 0, 10_000_000, 0)
    data["progression"]["threshold"] = _clamp_int(
        progression.get("threshold"),
        1,
        1_000_000,
        100,
    )
    data["progression"]["growth"] = max(
        1.0,
        min(10.0, _safe_float(progression.get("growth"), 1.12)),
    )
    max_threshold = progression.get("max_threshold")
    data["progression"]["max_threshold"] = (
        None if max_threshold is None else _clamp_int(max_threshold, 1, 1_000_000, 1200)
    )
    data["progression"]["stat_points"] = _clamp_int(
        progression.get("stat_points"),
        0,
        1_000_000,
        0,
    )
    unlocks = progression.get("unlocks", {})
    if not isinstance(unlocks, dict):
        unlocks = {}
    data["progression"]["unlocks"] = {
        str(key): bool(value) for key, value in unlocks.items() if isinstance(key, str)
    }
    data["progression"]["unlocks"].setdefault("mmo_unlocked", False)
    for list_key in ("unlocked_characters", "unlocked_skills"):
        raw_list = progression.get(list_key, [])
        if not isinstance(raw_list, list):
            raw_list = []
        data["progression"][list_key] = sorted({str(item) for item in raw_list if str(item)})

    reputation = incoming_data.get("reputation", {})
    if not isinstance(reputation, dict):
        reputation = {}
        warnings.append("reputation was not a mapping; defaulted")
    factions = reputation.get("factions", reputation)
    if not isinstance(factions, dict):
        factions = {}
    data["reputation"]["factions"] = {
        str(key): _clamp_int(value, -1_000_000, 1_000_000, 0)
        for key, value in factions.items()
        if isinstance(key, str)
    }
    last_updated = reputation.get("last_updated_utc", {})
    if not isinstance(last_updated, dict):
        last_updated = {}
    data["reputation"]["last_updated_utc"] = {
        str(key): str(value) for key, value in last_updated.items() if isinstance(key, str)
    }

    achievements = incoming_data.get("achievements", {})
    if not isinstance(achievements, dict):
        achievements = {}
        warnings.append("achievements was not a mapping; defaulted")
    unlocked_ids = achievements.get("unlocked_ids", achievements.get("achievements", []))
    if not isinstance(unlocked_ids, list):
        unlocked_ids = []
    data["achievements"]["unlocked_ids"] = sorted(
        {str(item) for item in unlocked_ids if str(item)}
    )
    unlocked_utc = achievements.get("unlocked_utc", {})
    if not isinstance(unlocked_utc, dict):
        unlocked_utc = {}
    data["achievements"]["unlocked_utc"] = {
        str(key): str(value) for key, value in unlocked_utc.items() if isinstance(key, str)
    }

    objectives = incoming_data.get("objectives", {})
    if not isinstance(objectives, dict):
        objectives = {}
        warnings.append("objectives was not a mapping; defaulted")
    data["objectives"] = _json_safe(objectives)

    meta = incoming_data.get("meta", {})
    if not isinstance(meta, dict):
        meta = {}
        warnings.append("meta was not a mapping; defaulted")
    data["meta"]["profile_display_name"] = str(
        meta.get("profile_display_name", data["meta"]["profile_display_name"]) or "Player"
    )
    data["meta"]["last_played_character"] = str(meta.get("last_played_character", "") or "")
    data["meta"]["last_played_utc"] = str(
        meta.get("last_played_utc", root["updated_utc"]) or root["updated_utc"]
    )
    data["meta"]["session_count"] = _clamp_int(meta.get("session_count"), 0, 1_000_000, 0)

    root["data"] = data
    return root, warnings


class ProfileStore:
    """Load and save versioned profile dictionaries with backups."""

    def __init__(self, load_root: str | os.PathLike[str] | None = None) -> None:
        base = Path(load_root) if load_root is not None else Path(save_manager.SAVE_DIR) / "profiles"
        self.load_root = base
        self.load_root.mkdir(parents=True, exist_ok=True)

    def _profile_paths(self, profile_id: str | None) -> tuple[Path, Path, Path]:
        pid = _sanitize_profile_id(profile_id)
        profile_dir = self.load_root / pid
        profile_dir.mkdir(parents=True, exist_ok=True)
        return (
            profile_dir / "profile.json",
            profile_dir / "profile.json.bak",
            profile_dir / "profile.json.tmp",
        )

    def load(self, profile_id: str = "default") -> tuple[dict[str, Any], list[str]]:
        """Load a profile payload and return it with validation warnings."""

        pid = _sanitize_profile_id(profile_id)
        profile_path, backup_path, _ = self._profile_paths(pid)
        warnings: list[str] = []
        payload: dict[str, Any] | None = None
        source = profile_path
        if not profile_path.exists() and not backup_path.exists():
            payload = default_profile(pid)
            warnings.append("profile missing; created default profile")
            self.save(pid, payload)
            return payload, warnings
        try:
            payload = json.loads(profile_path.read_text(encoding="utf-8"))
        except Exception as exc:
            warnings.append(f"primary profile unreadable: {exc}")
        if payload is None and backup_path.exists():
            source = backup_path
            try:
                payload = json.loads(backup_path.read_text(encoding="utf-8"))
                warnings.append("loaded profile from backup")
            except Exception as exc:
                warnings.append(f"backup profile unreadable: {exc}")
        if payload is None:
            payload = default_profile(pid)
            warnings.append("falling back to default profile")
            self.save(pid, payload)
            return payload, warnings
        migrated = migrate(payload)
        sanitized, extra = validate_and_sanitize(migrated, profile_id=pid)
        warnings.extend(extra)
        if source == backup_path or sanitized != payload:
            self.save(pid, sanitized)
        return sanitized, warnings

    def save(self, profile_id: str, profile_dict: dict[str, Any]) -> None:
        """Atomically persist a profile payload."""

        pid = _sanitize_profile_id(profile_id)
        payload, _warnings = validate_and_sanitize(profile_dict, profile_id=pid)
        profile_path, backup_path, temp_path = self._profile_paths(pid)
        if not payload.get("created_utc"):
            payload["created_utc"] = _utc_now()
        payload["updated_utc"] = _utc_now()
        encoded = json.dumps(payload, indent=2, sort_keys=True)
        with temp_path.open("w", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            try:
                os.fsync(handle.fileno())
            except OSError:
                pass
        if profile_path.exists():
            shutil.copy2(profile_path, backup_path)
        os.replace(temp_path, profile_path)

    def reset(self, profile_id: str = "default") -> None:
        """Reset a profile to defaults."""

        self.save(profile_id, default_profile(profile_id))

    def export(self, profile_id: str, path: str | os.PathLike[str]) -> None:
        """Export the current profile JSON to an arbitrary path."""

        payload, _warnings = self.load(profile_id)
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def import_profile(self, profile_id: str, path: str | os.PathLike[str]) -> list[str]:
        """Import a compatible profile payload from disk."""

        incoming = json.loads(Path(path).read_text(encoding="utf-8"))
        payload, warnings = validate_and_sanitize(migrate(incoming), profile_id=profile_id)
        self.save(profile_id, payload)
        return warnings


def _build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect and maintain profile saves.")
    parser.add_argument("--profile", default="default", help="Profile ID (default: default)")
    parser.add_argument("--root", default=None, help="Optional profile root path override")
    parser.add_argument("--print", action="store_true", dest="print_profile", help="Print profile JSON")
    parser.add_argument("--validate", action="store_true", help="Validate and print warnings")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero if warnings exist")
    parser.add_argument("--reset", action="store_true", help="Reset profile to defaults")
    parser.add_argument("--export", default=None, help="Export profile JSON to a path")
    parser.add_argument("--import", dest="import_path", default=None, help="Import profile JSON from a path")
    return parser


def _cli_main(argv: list[str]) -> int:
    parser = _build_cli_parser()
    args = parser.parse_args(argv)
    store = ProfileStore(load_root=args.root)
    warnings: list[str] = []
    if args.reset:
        store.reset(args.profile)
    if args.import_path:
        warnings.extend(store.import_profile(args.profile, args.import_path))
    payload, load_warnings = store.load(args.profile)
    warnings.extend(load_warnings)
    if args.validate:
        if warnings:
            for item in warnings:
                print(f"[WARN] {item}")
        else:
            print("[OK] profile validation passed")
    if args.export:
        store.export(args.profile, args.export)
    if args.print_profile:
        print(json.dumps(payload, indent=2, sort_keys=True))
    if args.strict and warnings:
        return 1
    if not (
        args.print_profile
        or args.validate
        or args.export
        or args.reset
        or args.import_path
    ):
        parser.print_help()
    return 0


def main() -> int:
    """CLI entry point used by ``python -m hololive_coliseum.profile_store``."""

    return _cli_main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
