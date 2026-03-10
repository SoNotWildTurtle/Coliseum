"""Tests for canonical distributed protocol validation and normalization."""

from __future__ import annotations

from hololive_coliseum.distributed_protocol import (
    PROTOCOL_VERSION,
    normalize_message,
    validate_message,
)


def test_valid_snapshot_and_delta_messages_pass() -> None:
    snapshot = {
        "protocol_version": PROTOCOL_VERSION,
        "type": "snapshot",
        "shard_id": "public",
        "sender_id": "node-a",
        "seq": 7,
        "logical_ts": 9,
        "payload": {"state": {"coins": 10}},
    }
    delta = {
        "protocol_version": PROTOCOL_VERSION,
        "type": "delta",
        "shard_id": "public",
        "sender_id": "node-b",
        "seq": 8,
        "logical_ts": 10,
        "payload": {"changes": {"coins": 11}},
    }
    assert validate_message(snapshot) == (True, [])
    assert validate_message(delta) == (True, [])


def test_missing_required_fields_fail_with_clear_errors() -> None:
    ok, errors = validate_message({"type": "delta"})
    assert ok is False
    assert "missing required field: protocol_version" in errors
    assert "missing required field: shard_id" in errors
    assert "missing required field: sender_id" in errors


def test_wrong_protocol_version_fails() -> None:
    ok, errors = validate_message(
        {
            "protocol_version": 99,
            "type": "snapshot",
            "shard_id": "public",
            "sender_id": "node-a",
            "seq": 1,
            "logical_ts": 1,
            "payload": {},
        }
    )
    assert ok is False
    assert errors == ["unsupported protocol_version: 99"]


def test_normalization_adds_safe_defaults() -> None:
    normalized = normalize_message({"type": "tombstone", "payload": None})
    assert normalized["protocol_version"] == PROTOCOL_VERSION
    assert normalized["seq"] == 0
    assert normalized["logical_ts"] == 0
    assert normalized["payload"] == {}
