"""Tests for deterministic distributed merge rules."""

from __future__ import annotations

import pytest

from hololive_coliseum.distributed_merge import (
    apply_update,
    merge_delta,
    merge_snapshot,
    normalize_meta,
    should_replace,
)


def test_lww_prefers_higher_logical_ts() -> None:
    state = {"coins": 10}
    meta = {"coins": {"logical_ts": 2, "sender_id": "a", "tombstone": False}}
    apply_update(
        state,
        meta,
        "coins",
        25,
        normalize_meta({}, sender_id="b", logical_ts=3),
    )
    assert state["coins"] == 25
    assert meta["coins"]["logical_ts"] == 3


def test_tie_breaker_uses_sender_id_deterministically() -> None:
    current = {"logical_ts": 5, "sender_id": "alpha", "tombstone": False}
    incoming = {"logical_ts": 5, "sender_id": "omega", "tombstone": False}
    assert should_replace(current, incoming) is True
    assert should_replace(incoming, current) is False


def test_tombstone_beats_older_live_value() -> None:
    state = {"route": {"status": "active"}}
    meta = {"route": {"logical_ts": 3, "sender_id": "alpha", "tombstone": False}}
    apply_update(
        state,
        meta,
        "route",
        None,
        normalize_meta({}, sender_id="beta", logical_ts=4, tombstone=True),
    )
    assert "route" not in state
    assert meta["route"]["tombstone"] is True


def test_older_tombstone_does_not_delete_newer_live_value() -> None:
    state = {"route": {"status": "active"}}
    meta = {"route": {"logical_ts": 7, "sender_id": "omega", "tombstone": False}}
    apply_update(
        state,
        meta,
        "route",
        None,
        normalize_meta({}, sender_id="beta", logical_ts=6, tombstone=True),
    )
    assert state["route"]["status"] == "active"
    assert meta["route"]["tombstone"] is False


def test_shard_mismatch_is_rejected() -> None:
    with pytest.raises(ValueError, match="shard mismatch"):
        merge_delta(
            {},
            {},
            {"changes": {"coins": 5}},
            "sender-a",
            1,
            shard_id="shard-b",
            target_shard_id="shard-a",
        )

    with pytest.raises(ValueError, match="shard mismatch"):
        merge_snapshot(
            {},
            {},
            {"state": {"coins": 5}},
            "sender-a",
            1,
            shard_id="shard-b",
            target_shard_id="shard-a",
        )
