"""Schema helpers for validating and normalizing event envelopes."""

from __future__ import annotations

import math
from typing import Any

from .event_types import EVENT_TYPES, REQUIRED_PAYLOAD_KEYS


def _is_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    return isinstance(value, (int, float))


def normalize_event(envelope: dict[str, Any]) -> dict[str, Any]:
    """Return a normalized event envelope without dropping extra fields."""

    normalized = dict(envelope or {})
    normalized["type"] = str(normalized.get("type", "unknown"))
    t_value = normalized.get("t", 0)
    frame_value = normalized.get("frame", 0)
    try:
        normalized["t"] = int(t_value)
    except (TypeError, ValueError):
        normalized["t"] = 0
    try:
        normalized["frame"] = int(frame_value)
    except (TypeError, ValueError):
        normalized["frame"] = 0
    payload = normalized.get("payload", {})
    if not isinstance(payload, dict):
        payload = {"value": payload}
    normalized["payload"] = payload
    return normalized


def validate_event(
    envelope: dict[str, Any],
    *,
    strict: bool = False,
) -> tuple[bool, list[str]]:
    """Validate an event envelope and payload keys/types."""

    errors: list[str] = []
    normalized = normalize_event(envelope)
    event_type = normalized.get("type", "unknown")
    payload = normalized.get("payload", {})

    for key in ("type", "t", "frame", "payload"):
        if key not in normalized:
            errors.append(f"missing envelope key '{key}'")
    if not isinstance(event_type, str) or not event_type:
        errors.append("event type must be a non-empty string")
    if not isinstance(payload, dict):
        errors.append("payload must be a mapping")
        payload = {}
    if strict and event_type not in EVENT_TYPES:
        errors.append(f"unknown event type '{event_type}'")

    required = REQUIRED_PAYLOAD_KEYS.get(str(event_type), ())
    for key in required:
        if key not in payload:
            errors.append(f"payload missing required key '{key}' for type '{event_type}'")

    if "amount" in payload and not _is_number(payload.get("amount")):
        errors.append("payload.amount must be numeric")
    if "delta" in payload and not _is_number(payload.get("delta")):
        errors.append("payload.delta must be numeric")
    for key in ("amount", "delta", "hp_before", "hp_after"):
        value = payload.get(key)
        if _is_number(value) and not math.isfinite(float(value)):
            errors.append(f"payload.{key} must be finite")

    return (len(errors) == 0), errors
