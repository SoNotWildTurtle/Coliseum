"""Tests for order-independent deterministic distributed convergence."""

from __future__ import annotations

from hololive_coliseum.distributed_merge import merge_delta


def _apply_sequence(
    events: list[tuple[str, int, dict[str, object]]],
) -> tuple[dict[str, object], dict[str, dict[str, object]]]:
    state: dict[str, object] = {}
    meta: dict[str, dict[str, object]] = {}
    for sender_id, logical_ts, payload in events:
        merge_delta(
            state,
            meta,
            payload,
            sender_id,
            logical_ts,
            shard_id="public",
            target_shard_id="public",
        )
    return state, meta


def test_two_nodes_converge_despite_different_delta_order() -> None:
    events = [
        ("node-a", 1, {"changes": {"coins": 5}}),
        ("node-b", 2, {"changes": {"coins": 7}}),
        ("node-a", 3, {"changes": {"xp": 10}}),
        ("node-b", 4, {"tombstones": {"coins": {}}}),
        ("node-a", 4, {"changes": {"xp": 11}}),
    ]
    node_one = _apply_sequence(events)
    node_two = _apply_sequence(
        [
            events[1],
            events[0],
            events[3],
            events[4],
            events[2],
        ]
    )
    assert node_one == node_two
    state, meta = node_one
    assert "coins" not in state
    assert state["xp"] == 11
    assert meta["coins"]["tombstone"] is True
