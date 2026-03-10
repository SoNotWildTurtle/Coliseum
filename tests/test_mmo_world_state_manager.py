"""Tests for mmo world state manager."""

import pytest

from hololive_coliseum.mmo_world_state_manager import MMOWorldStateManager
from hololive_coliseum.state_verification_manager import StateVerificationManager


def test_world_state_delta_roundtrip():
    verifier = StateVerificationManager()
    mgr = MMOWorldStateManager(verifier=verifier)
    snapshot = MMOWorldStateManager.build_snapshot(
        regions=[{"name": "r1", "position": [0.0, 0.0]}],
        influence={"r1": 50},
        world_events=[{"name": "Storm", "region": "r1", "expires_at": 1}],
        outposts=[{"region": "r1", "level": 1}],
        operations=[{"name": "Op-1", "region": "r1", "status": "active"}],
        trade_routes=[{"origin": "r1", "destination": "r2", "status": "active"}],
        directives=[{"id": "D-1", "status": "open"}],
        bounties=[{"id": "B-1", "status": "open"}],
        tombstones=[],
        updated_at=100,
        shard="public",
    )
    delta = mgr.update(snapshot)
    assert MMOWorldStateManager.has_payload_changes(delta)
    other = MMOWorldStateManager(verifier=verifier)
    state = other.apply_delta(delta)
    assert state["regions"][0]["name"] == "r1"


def test_world_state_snapshot_verification():
    verifier = StateVerificationManager()
    mgr = MMOWorldStateManager(verifier=verifier)
    snapshot = MMOWorldStateManager.build_snapshot(
        regions=[{"name": "r1"}],
        influence={},
        world_events=[],
        outposts=[],
        operations=[],
        trade_routes=[],
        directives=[],
        bounties=[],
        tombstones=[],
        updated_at=50,
        shard="public",
    )
    verify = verifier.compute(snapshot)
    mgr.load_snapshot(snapshot, sequence=5, verify=verify)
    with pytest.raises(ValueError):
        mgr.load_snapshot(snapshot, verify={"crc32": "bad", "sha256": "bad"})


def test_world_state_merge_prefers_newer_entries():
    mgr = MMOWorldStateManager()
    local = MMOWorldStateManager.build_snapshot(
        regions=[{"name": "r1", "updated_at": 1, "origin": "a"}],
        influence={"r1": 10},
        world_events=[],
        outposts=[{"region": "r1", "level": 1, "updated_at": 1, "origin": "a"}],
        operations=[],
        trade_routes=[],
        directives=[{"id": "D-1", "updated_at": 1, "origin": "a"}],
        bounties=[{"id": "B-1", "updated_at": 1, "origin": "a"}],
        tombstones=[],
        updated_at=10,
        shard="public",
    )
    incoming = MMOWorldStateManager.build_snapshot(
        regions=[{"name": "r1", "updated_at": 2, "origin": "b"}],
        influence={"r1": 20},
        world_events=[],
        outposts=[{"region": "r1", "level": 2, "updated_at": 2, "origin": "b"}],
        operations=[],
        trade_routes=[],
        directives=[{"id": "D-1", "updated_at": 2, "origin": "b"}],
        bounties=[{"id": "B-1", "updated_at": 2, "origin": "b"}],
        tombstones=[],
        updated_at=20,
        shard="public",
    )
    merged = mgr.merge_states(local, incoming)
    assert merged["regions"][0]["origin"] == "b"
    assert merged["outposts"][0]["level"] == 2
    assert merged["influence"]["r1"] == 20


def test_world_state_merge_rejects_shard_change():
    mgr = MMOWorldStateManager()
    local = MMOWorldStateManager.build_snapshot(
        regions=[{"name": "r1", "updated_at": 1, "origin": "a"}],
        influence={"r1": 10},
        world_events=[],
        outposts=[],
        operations=[],
        trade_routes=[],
        directives=[],
        bounties=[],
        tombstones=[],
        updated_at=10,
        shard="shard-1",
    )
    incoming = MMOWorldStateManager.build_snapshot(
        regions=[{"name": "r2", "updated_at": 2, "origin": "b"}],
        influence={"r2": 20},
        world_events=[],
        outposts=[],
        operations=[],
        trade_routes=[],
        directives=[],
        bounties=[],
        tombstones=[],
        updated_at=20,
        shard="shard-2",
    )
    with pytest.raises(ValueError, match="shard mismatch"):
        mgr.merge_states(local, incoming)


def test_world_state_tombstones_remove_entries():
    mgr = MMOWorldStateManager()
    local = MMOWorldStateManager.build_snapshot(
        regions=[],
        influence={},
        world_events=[{"id": "event:r1", "updated_at": 5, "origin": "a"}],
        outposts=[],
        operations=[],
        trade_routes=[],
        directives=[],
        bounties=[],
        tombstones=[],
        updated_at=5,
        shard="public",
    )
    incoming = MMOWorldStateManager.build_snapshot(
        regions=[],
        influence={},
        world_events=[],
        outposts=[],
        operations=[],
        trade_routes=[],
        directives=[],
        bounties=[],
        tombstones=[{"kind": "world_event", "id": "event:r1", "updated_at": 6}],
        updated_at=6,
        shard="public",
    )
    merged = mgr.merge_states(local, incoming)
    assert merged["world_events"] == []


def test_world_state_tombstones_remove_directives():
    mgr = MMOWorldStateManager()
    local = MMOWorldStateManager.build_snapshot(
        regions=[],
        influence={},
        world_events=[],
        outposts=[],
        operations=[],
        trade_routes=[],
        directives=[{"id": "D-1", "updated_at": 5, "origin": "a"}],
        bounties=[],
        tombstones=[],
        updated_at=5,
        shard="public",
    )
    incoming = MMOWorldStateManager.build_snapshot(
        regions=[],
        influence={},
        world_events=[],
        outposts=[],
        operations=[],
        trade_routes=[],
        directives=[],
        bounties=[],
        tombstones=[{"kind": "directive", "id": "D-1", "updated_at": 6}],
        updated_at=6,
        shard="public",
    )
    merged = mgr.merge_states(local, incoming)
    assert merged["directives"] == []
