"""Deterministic LWW merge helpers for shard-scoped distributed state."""

from __future__ import annotations

import copy
from typing import Any, Mapping


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return copy.deepcopy(value)


def normalize_meta(
    incoming_meta: Mapping[str, Any] | None,
    *,
    sender_id: str,
    logical_ts: int,
    tombstone: bool = False,
) -> dict[str, Any]:
    """Return canonical metadata for a distributed key."""

    meta = incoming_meta if isinstance(incoming_meta, Mapping) else {}
    resolved_ts = _safe_int(meta.get("logical_ts"), logical_ts)
    resolved_sender = str(meta.get("sender_id", sender_id) or sender_id)
    resolved_tombstone = bool(meta.get("tombstone", tombstone))
    if resolved_ts < 0:
        raise ValueError("logical_ts must be >= 0")
    if not resolved_sender:
        raise ValueError("sender_id must not be empty")
    return {
        "logical_ts": resolved_ts,
        "sender_id": resolved_sender,
        "tombstone": resolved_tombstone,
    }


def should_replace(
    meta_current: Mapping[str, Any] | None,
    meta_incoming: Mapping[str, Any] | None,
) -> bool:
    """Return True when the incoming metadata should win deterministically."""

    if meta_incoming is None:
        return False
    if meta_current is None:
        return True
    current_ts = _safe_int(meta_current.get("logical_ts"), -1)
    incoming_ts = _safe_int(meta_incoming.get("logical_ts"), -1)
    if incoming_ts != current_ts:
        return incoming_ts > current_ts
    current_sender = str(meta_current.get("sender_id", ""))
    incoming_sender = str(meta_incoming.get("sender_id", ""))
    if incoming_sender != current_sender:
        return incoming_sender > current_sender
    current_tombstone = bool(meta_current.get("tombstone", False))
    incoming_tombstone = bool(meta_incoming.get("tombstone", False))
    if incoming_tombstone != current_tombstone:
        return incoming_tombstone
    return False


def apply_update(
    state: dict[str, Any],
    meta: dict[str, dict[str, Any]],
    key: str,
    incoming_value: Any,
    incoming_meta: Mapping[str, Any],
) -> None:
    """Apply a single deterministic update to ``state`` and ``meta``."""

    current_meta = meta.get(key)
    if not should_replace(current_meta, incoming_meta):
        return
    normalized = {
        "logical_ts": _safe_int(incoming_meta.get("logical_ts"), 0),
        "sender_id": str(incoming_meta.get("sender_id", "")),
        "tombstone": bool(incoming_meta.get("tombstone", False)),
    }
    meta[str(key)] = normalized
    if normalized["tombstone"]:
        state.pop(str(key), None)
        return
    state[str(key)] = _json_safe(incoming_value)


def _ensure_shard_match(shard_id: str, target_shard_id: str) -> None:
    if str(shard_id) != str(target_shard_id):
        raise ValueError(
            f"shard mismatch: incoming {shard_id!r} does not match target {target_shard_id!r}"
        )


def _iter_updates(
    payload: Mapping[str, Any],
    *,
    sender_id: str,
    logical_ts: int,
    default_tombstone: bool = False,
) -> list[tuple[str, Any, dict[str, Any]]]:
    updates: list[tuple[str, Any, dict[str, Any]]] = []
    raw_state = payload.get("state", payload.get("changes", {}))
    if isinstance(raw_state, Mapping):
        raw_meta = payload.get("meta", {})
        meta_map = raw_meta if isinstance(raw_meta, Mapping) else {}
        for key, value in raw_state.items():
            key_str = str(key)
            incoming_meta = meta_map.get(key_str)
            normalized = normalize_meta(
                incoming_meta if isinstance(incoming_meta, Mapping) else {},
                sender_id=sender_id,
                logical_ts=logical_ts,
                tombstone=default_tombstone,
            )
            updates.append((key_str, value, normalized))
    tombstones = payload.get("tombstones", {})
    if isinstance(tombstones, Mapping):
        for key, value in tombstones.items():
            key_str = str(key)
            incoming_meta = value if isinstance(value, Mapping) else {}
            normalized = normalize_meta(
                incoming_meta,
                sender_id=sender_id,
                logical_ts=logical_ts,
                tombstone=True,
            )
            normalized["tombstone"] = True
            updates.append((key_str, None, normalized))
    elif isinstance(tombstones, list):
        for entry in tombstones:
            if not isinstance(entry, Mapping):
                continue
            key = entry.get("key", entry.get("id"))
            if key in {None, ""}:
                continue
            normalized = normalize_meta(
                entry,
                sender_id=sender_id,
                logical_ts=logical_ts,
                tombstone=True,
            )
            normalized["tombstone"] = True
            updates.append((str(key), None, normalized))
    return updates


def merge_delta(
    state: dict[str, Any],
    meta: dict[str, dict[str, Any]],
    delta_payload: Mapping[str, Any],
    sender_id: str,
    logical_ts: int,
    *,
    shard_id: str,
    target_shard_id: str,
) -> None:
    """Merge a delta payload into ``state`` using deterministic LWW rules."""

    _ensure_shard_match(shard_id, target_shard_id)
    for key, value, incoming_meta in _iter_updates(
        delta_payload,
        sender_id=sender_id,
        logical_ts=logical_ts,
    ):
        apply_update(state, meta, key, value, incoming_meta)


def merge_snapshot(
    state: dict[str, Any],
    meta: dict[str, dict[str, Any]],
    snapshot_payload: Mapping[str, Any],
    sender_id: str,
    logical_ts: int,
    *,
    shard_id: str,
    target_shard_id: str,
) -> None:
    """Merge a snapshot payload into ``state`` using deterministic LWW rules."""

    _ensure_shard_match(shard_id, target_shard_id)
    for key, value, incoming_meta in _iter_updates(
        snapshot_payload,
        sender_id=sender_id,
        logical_ts=logical_ts,
    ):
        apply_update(state, meta, key, value, incoming_meta)
