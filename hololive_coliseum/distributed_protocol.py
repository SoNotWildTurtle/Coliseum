"""Canonical protocol envelopes for distributed state synchronization."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

PROTOCOL_VERSION = 1
SUPPORTED_PROTOCOL_VERSIONS = {PROTOCOL_VERSION}
MESSAGE_TYPES = {"snapshot", "delta", "tombstone"}


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _mapping_copy(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        return {}
    return {str(key): item for key, item in value.items()}


@dataclass(frozen=True)
class DistributedMessage:
    """Base distributed envelope shared by snapshot, delta, and tombstones."""

    protocol_version: int = PROTOCOL_VERSION
    type: str = "delta"
    shard_id: str = ""
    sender_id: str = ""
    seq: int = 0
    logical_ts: int = 0
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return the canonical dictionary form of the message."""

        return {
            "protocol_version": int(self.protocol_version),
            "type": str(self.type),
            "shard_id": str(self.shard_id),
            "sender_id": str(self.sender_id),
            "seq": int(self.seq),
            "logical_ts": int(self.logical_ts),
            "payload": dict(self.payload),
        }


@dataclass(frozen=True)
class SnapshotMessage(DistributedMessage):
    """Canonical full-state snapshot envelope."""

    type: str = "snapshot"


@dataclass(frozen=True)
class DeltaMessage(DistributedMessage):
    """Canonical incremental update envelope."""

    type: str = "delta"


@dataclass(frozen=True)
class TombstoneMessage(DistributedMessage):
    """Canonical delete/tombstone envelope."""

    type: str = "tombstone"


def normalize_message(message: dict[str, Any] | None) -> dict[str, Any]:
    """Return a normalized protocol message with safe defaults."""

    incoming = message if isinstance(message, Mapping) else {}
    normalized = {
        "protocol_version": _safe_int(
            incoming.get("protocol_version"),
            PROTOCOL_VERSION,
        ),
        "type": str(incoming.get("type", "") or ""),
        "shard_id": str(incoming.get("shard_id", "") or ""),
        "sender_id": str(incoming.get("sender_id", "") or ""),
        "seq": max(0, _safe_int(incoming.get("seq"), 0)),
        "logical_ts": max(0, _safe_int(incoming.get("logical_ts"), 0)),
        "payload": _mapping_copy(incoming.get("payload")),
    }
    for key, value in incoming.items():
        if key not in normalized:
            normalized[str(key)] = value
    return normalized


def validate_message(
    message: dict[str, Any] | None,
    strict: bool = False,
) -> tuple[bool, list[str]]:
    """Validate a protocol message and optionally raise on errors."""

    errors: list[str] = []
    if not isinstance(message, Mapping):
        errors.append("message must be a mapping")
    else:
        for field_name in (
            "protocol_version",
            "type",
            "shard_id",
            "sender_id",
            "seq",
            "logical_ts",
            "payload",
        ):
            if field_name not in message:
                errors.append(f"missing required field: {field_name}")
        protocol_version = message.get("protocol_version")
        if "protocol_version" in message and not isinstance(protocol_version, int):
            try:
                protocol_version = int(protocol_version)
            except (TypeError, ValueError):
                errors.append("protocol_version must be an int")
                protocol_version = None
        if protocol_version is not None and protocol_version not in SUPPORTED_PROTOCOL_VERSIONS:
            errors.append(f"unsupported protocol_version: {protocol_version}")
        message_type = message.get("type")
        if "type" in message and not isinstance(message_type, str):
            errors.append("type must be a str")
        elif isinstance(message_type, str) and message_type not in MESSAGE_TYPES:
            errors.append(f"unsupported message type: {message_type}")
        for field_name in ("shard_id", "sender_id"):
            value = message.get(field_name)
            if field_name in message and not isinstance(value, str):
                errors.append(f"{field_name} must be a str")
            elif isinstance(value, str) and not value:
                errors.append(f"{field_name} must not be empty")
        for field_name in ("seq", "logical_ts"):
            value = message.get(field_name)
            if field_name in message and not isinstance(value, int):
                try:
                    value = int(value)
                except (TypeError, ValueError):
                    errors.append(f"{field_name} must be an int")
                    value = None
            if isinstance(value, int) and value < 0:
                errors.append(f"{field_name} must be >= 0")
        payload = message.get("payload")
        if "payload" in message and not isinstance(payload, Mapping):
            errors.append("payload must be a mapping")
    if strict and errors:
        raise ValueError("; ".join(errors))
    return not errors, errors
