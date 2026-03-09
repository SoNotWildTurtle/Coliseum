"""Adapters that map runtime managers to profile persistence payloads."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


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


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def export_profile_data(game: Any, *, player: Any | None = None) -> dict[str, Any]:
    """Extract JSON-safe profile sections from the current game state."""

    current = getattr(game, "profile", None)
    current_inventory = deepcopy(getattr(current, "inventory", {}) or {})
    current_economy = deepcopy(getattr(current, "economy", {}) or {})
    current_progression = deepcopy(getattr(current, "progression", {}) or {})
    current_reputation = deepcopy(getattr(current, "reputation", {}) or {})
    current_achievements = deepcopy(getattr(current, "achievements", {}) or {})
    current_objectives = deepcopy(getattr(current, "objectives", {}) or {})
    current_meta = deepcopy(getattr(current, "meta", {}) or {})

    inventory = dict(current_inventory)
    economy = dict(current_economy)
    progression = dict(current_progression)
    reputation = dict(current_reputation)
    achievements = dict(current_achievements)
    objectives = dict(current_objectives)
    meta = dict(current_meta)

    if player is not None:
        player_inventory = getattr(player, "inventory", None)
        if player_inventory is not None and hasattr(player_inventory, "to_dict"):
            inventory["items"] = dict(player_inventory.to_dict())
            inventory["capacity"] = getattr(player_inventory, "capacity", None)

        currency_manager = getattr(player, "currency_manager", None)
        if currency_manager is not None and hasattr(currency_manager, "get_balance"):
            balances = dict(economy.get("balances", {}))
            balances["coins"] = _safe_int(currency_manager.get_balance(), 0)
            economy["balances"] = balances

        xp_manager = getattr(player, "experience_manager", None)
        if xp_manager is not None:
            progression["level"] = max(1, _safe_int(getattr(xp_manager, "level", 1), 1))
            progression["xp"] = max(0, _safe_int(getattr(xp_manager, "xp", 0), 0))
            progression["threshold"] = max(
                1,
                _safe_int(getattr(xp_manager, "threshold", 100), 100),
            )
            progression["growth"] = max(
                1.0,
                _safe_float(getattr(xp_manager, "growth", 1.0), 1.0),
            )
            progression["max_threshold"] = getattr(xp_manager, "max_threshold", None)

    progression.setdefault("unlocks", {})
    unlocks = progression.get("unlocks")
    if not isinstance(unlocks, dict):
        unlocks = {}
    unlocks["mmo_unlocked"] = bool(getattr(game, "mmo_unlocked", False))
    progression["unlocks"] = unlocks

    rep_manager = getattr(game, "reputation_manager", None)
    if rep_manager is not None and hasattr(rep_manager, "to_dict"):
        reputation["factions"] = dict(rep_manager.to_dict())

    ach_manager = getattr(game, "achievement_manager", None)
    if ach_manager is not None and hasattr(ach_manager, "unlocked"):
        achievements["unlocked_ids"] = sorted(str(x) for x in ach_manager.unlocked)

    obj_manager = getattr(game, "objective_manager", None)
    if obj_manager is not None and hasattr(obj_manager, "to_dict"):
        objectives = dict(obj_manager.to_dict())

    selected = getattr(game, "selected_character", "")
    meta["last_played_character"] = str(selected or "")
    meta["last_played_utc"] = _utc_now()
    meta["session_count"] = max(0, _safe_int(meta.get("session_count", 0), 0)) + 1

    return {
        "inventory": inventory,
        "economy": economy,
        "progression": progression,
        "reputation": reputation,
        "achievements": achievements,
        "objectives": objectives,
        "meta": meta,
    }


def hydrate_profile_data(
    game: Any,
    data: dict[str, Any],
    *,
    player: Any | None = None,
) -> None:
    """Apply persisted profile sections to managers and runtime state."""

    inventory = data.get("inventory", {})
    if not isinstance(inventory, dict):
        inventory = {}
    economy = data.get("economy", {})
    if not isinstance(economy, dict):
        economy = {}
    progression = data.get("progression", {})
    if not isinstance(progression, dict):
        progression = {}
    reputation = data.get("reputation", {})
    if not isinstance(reputation, dict):
        reputation = {}
    achievements = data.get("achievements", {})
    if not isinstance(achievements, dict):
        achievements = {}
    objectives = data.get("objectives", {})
    if not isinstance(objectives, dict):
        objectives = {}

    balances = economy.get("balances", {})
    if not isinstance(balances, dict):
        balances = {}
    profile_coins = max(0, _safe_int(balances.get("coins", 0), 0))
    game.coins = max(_safe_int(getattr(game, "coins", 0), 0), profile_coins)

    unlocks = progression.get("unlocks", {})
    if isinstance(unlocks, dict):
        game.mmo_unlocked = bool(unlocks.get("mmo_unlocked", False))

    ach_manager = getattr(game, "achievement_manager", None)
    if ach_manager is not None and hasattr(ach_manager, "load_from_dict"):
        ach_manager.load_from_dict({"achievements": achievements.get("unlocked_ids", [])})

    rep_manager = getattr(game, "reputation_manager", None)
    factions = reputation.get("factions", {})
    if not isinstance(factions, dict):
        factions = {}
    if rep_manager is not None and hasattr(rep_manager, "load_from_dict"):
        rep_manager.load_from_dict({str(k): _safe_int(v, 0) for k, v in factions.items()})

    obj_manager = getattr(game, "objective_manager", None)
    if obj_manager is not None and hasattr(obj_manager, "load_from_dict"):
        obj_manager.load_from_dict(objectives)

    if player is None:
        return

    items = inventory.get("items", {})
    if not isinstance(items, dict):
        items = {}
    player_inventory = getattr(player, "inventory", None)
    if player_inventory is not None and hasattr(player_inventory, "load_from_dict"):
        player_inventory.load_from_dict(
            {
                str(k): max(0, _safe_int(v, 0))
                for k, v in items.items()
                if isinstance(k, str)
            }
        )
        capacity = inventory.get("capacity")
        player_inventory.capacity = None if capacity is None else max(0, _safe_int(capacity, 0))

    currency_manager = getattr(player, "currency_manager", None)
    if currency_manager is not None and hasattr(currency_manager, "balance"):
        currency_manager.balance = game.coins

    xp_manager = getattr(player, "experience_manager", None)
    if xp_manager is not None:
        xp_manager.level = max(1, _safe_int(progression.get("level", 1), 1))
        xp_manager.xp = max(0, _safe_int(progression.get("xp", 0), 0))
        xp_manager.threshold = max(1, _safe_int(progression.get("threshold", 100), 100))
        xp_manager.growth = max(1.0, _safe_float(progression.get("growth", 1.0), 1.0))
        max_threshold = progression.get("max_threshold")
        xp_manager.max_threshold = None if max_threshold is None else max(
            1,
            _safe_int(max_threshold, 1),
        )
