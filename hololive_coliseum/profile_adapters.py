"""Adapters between runtime managers and profile payload sections."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _profile_data(game: Any) -> dict[str, Any]:
    profile = getattr(game, "profile", {})
    if not isinstance(profile, dict):
        return {}
    data = profile.get("data", {})
    return data if isinstance(data, dict) else {}


def export_inventory(game: Any, *, player: Any | None = None) -> dict[str, Any]:
    current = deepcopy(_profile_data(game).get("inventory", {}))
    player = player if player is not None else getattr(game, "player", None)
    inventory = getattr(player, "inventory", None)
    if inventory is not None and hasattr(inventory, "to_dict"):
        current["items"] = dict(inventory.to_dict())
        current["capacity"] = getattr(inventory, "capacity", None)
    current.setdefault("items", {})
    current.setdefault("capacity", 30)
    current.setdefault("equipment", {})
    return current


def export_economy(game: Any, *, player: Any | None = None) -> dict[str, Any]:
    current = deepcopy(_profile_data(game).get("economy", {}))
    balances = dict(current.get("balances", {}))
    player = player if player is not None else getattr(game, "player", None)
    currency = getattr(player, "currency_manager", None)
    if currency is not None and hasattr(currency, "get_balance"):
        balances["coins"] = _safe_int(currency.get_balance(), 0)
    else:
        balances.setdefault("coins", _safe_int(getattr(game, "coins", 0), 0))
    current["balances"] = balances
    return current


def export_progression(game: Any, *, player: Any | None = None) -> dict[str, Any]:
    current = deepcopy(_profile_data(game).get("progression", {}))
    player = player if player is not None else getattr(game, "player", None)
    xp_manager = getattr(player, "experience_manager", None)
    if xp_manager is not None:
        current["level"] = max(1, _safe_int(getattr(xp_manager, "level", 1), 1))
        current["xp"] = max(0, _safe_int(getattr(xp_manager, "xp", 0), 0))
        current["threshold"] = max(
            1,
            _safe_int(getattr(xp_manager, "threshold", 100), 100),
        )
        current["growth"] = max(
            1.0,
            _safe_float(getattr(xp_manager, "growth", 1.12), 1.12),
        )
        current["max_threshold"] = getattr(xp_manager, "max_threshold", 1200)
    current.setdefault("unlocks", {})
    unlocks = current.get("unlocks")
    if not isinstance(unlocks, dict):
        unlocks = {}
    unlocks["mmo_unlocked"] = bool(getattr(game, "mmo_unlocked", False))
    current["unlocks"] = unlocks
    current.setdefault("stat_points", 0)
    current.setdefault("unlocked_characters", [])
    current.setdefault("unlocked_skills", [])
    return current


def export_reputation(game: Any) -> dict[str, Any]:
    current = deepcopy(_profile_data(game).get("reputation", {}))
    manager = getattr(game, "reputation_manager", None)
    if manager is not None and hasattr(manager, "to_dict"):
        current["factions"] = dict(manager.to_dict())
    current.setdefault("factions", {})
    current.setdefault("last_updated_utc", {})
    return current


def export_achievements(game: Any) -> dict[str, Any]:
    current = deepcopy(_profile_data(game).get("achievements", {}))
    manager = getattr(game, "achievement_manager", None)
    if manager is not None and hasattr(manager, "unlocked"):
        current["unlocked_ids"] = sorted(str(item) for item in manager.unlocked)
    current.setdefault("unlocked_ids", [])
    current.setdefault("unlocked_utc", {})
    return current


def export_objectives(game: Any) -> dict[str, Any]:
    current = deepcopy(_profile_data(game).get("objectives", {}))
    manager = getattr(game, "objective_manager", None)
    if manager is not None and hasattr(manager, "to_dict"):
        current = dict(manager.to_dict())
    return current


def import_inventory(game: Any, data: dict[str, Any], *, player: Any | None = None) -> list[str]:
    warnings: list[str] = []
    player = player if player is not None else getattr(game, "player", None)
    inventory = getattr(player, "inventory", None)
    if inventory is None:
        return warnings
    items = data.get("items", {})
    if not isinstance(items, dict):
        items = {}
        warnings.append("inventory.items was not a mapping")
    if hasattr(inventory, "load_from_dict"):
        inventory.load_from_dict(
            {
                str(key): max(0, _safe_int(value, 0))
                for key, value in items.items()
                if isinstance(key, str)
            }
        )
    if hasattr(inventory, "capacity"):
        capacity = data.get("capacity")
        inventory.capacity = None if capacity is None else max(0, _safe_int(capacity, 0))
    return warnings


def import_economy(game: Any, data: dict[str, Any], *, player: Any | None = None) -> list[str]:
    warnings: list[str] = []
    balances = data.get("balances", {})
    if not isinstance(balances, dict):
        balances = {}
        warnings.append("economy.balances was not a mapping")
    coins = max(0, _safe_int(balances.get("coins", 0), 0))
    game.coins = coins
    player = player if player is not None else getattr(game, "player", None)
    currency = getattr(player, "currency_manager", None)
    if currency is not None and hasattr(currency, "balance"):
        currency.balance = coins
    return warnings


def import_progression(game: Any, data: dict[str, Any], *, player: Any | None = None) -> list[str]:
    warnings: list[str] = []
    player = player if player is not None else getattr(game, "player", None)
    xp_manager = getattr(player, "experience_manager", None)
    if xp_manager is not None:
        xp_manager.level = max(1, _safe_int(data.get("level", 1), 1))
        xp_manager.xp = max(0, _safe_int(data.get("xp", 0), 0))
        xp_manager.threshold = max(1, _safe_int(data.get("threshold", 100), 100))
        xp_manager.growth = max(1.0, _safe_float(data.get("growth", 1.12), 1.12))
        max_threshold = data.get("max_threshold")
        xp_manager.max_threshold = None if max_threshold is None else max(
            1,
            _safe_int(max_threshold, 1),
        )
    unlocks = data.get("unlocks", {})
    if isinstance(unlocks, dict):
        game.mmo_unlocked = bool(unlocks.get("mmo_unlocked", False))
    return warnings


def import_reputation(game: Any, data: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    factions = data.get("factions", {})
    if not isinstance(factions, dict):
        factions = {}
        warnings.append("reputation.factions was not a mapping")
    manager = getattr(game, "reputation_manager", None)
    if manager is not None and hasattr(manager, "load_from_dict"):
        manager.load_from_dict({str(key): _safe_int(value, 0) for key, value in factions.items()})
    return warnings


def import_achievements(game: Any, data: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    unlocked_ids = data.get("unlocked_ids", [])
    if not isinstance(unlocked_ids, list):
        unlocked_ids = []
        warnings.append("achievements.unlocked_ids was not a list")
    manager = getattr(game, "achievement_manager", None)
    if manager is not None and hasattr(manager, "load_from_dict"):
        manager.load_from_dict({"achievements": [str(item) for item in unlocked_ids if str(item)]})
    return warnings


def import_objectives(game: Any, data: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    if not isinstance(data, dict):
        data = {}
        warnings.append("objectives payload was not a mapping")
    manager = getattr(game, "objective_manager", None)
    if manager is not None and hasattr(manager, "load_from_dict"):
        manager.load_from_dict(data)
    return warnings


def export_profile_data(game: Any, *, player: Any | None = None) -> dict[str, Any]:
    """Export a full profile data payload from the runtime managers."""

    meta = deepcopy(_profile_data(game).get("meta", {}))
    meta["last_played_character"] = str(getattr(game, "selected_character", "") or "")
    meta["last_played_utc"] = _utc_now()
    meta["session_count"] = max(0, _safe_int(meta.get("session_count", 0), 0)) + 1
    return {
        "inventory": export_inventory(game, player=player),
        "economy": export_economy(game, player=player),
        "progression": export_progression(game, player=player),
        "reputation": export_reputation(game),
        "achievements": export_achievements(game),
        "objectives": export_objectives(game),
        "meta": meta,
    }


def hydrate_profile_data(
    game: Any,
    data: dict[str, Any],
    *,
    player: Any | None = None,
) -> list[str]:
    """Hydrate runtime managers from a full profile data payload."""

    payload = data if isinstance(data, dict) else {}
    warnings: list[str] = []
    warnings.extend(import_economy(game, payload.get("economy", {}), player=player))
    warnings.extend(import_progression(game, payload.get("progression", {}), player=player))
    warnings.extend(import_reputation(game, payload.get("reputation", {})))
    warnings.extend(import_achievements(game, payload.get("achievements", {})))
    warnings.extend(import_objectives(game, payload.get("objectives", {})))
    warnings.extend(import_inventory(game, payload.get("inventory", {}), player=player))
    return warnings
