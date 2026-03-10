"""Manage MMO world state sync snapshots and deltas."""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Tuple

from .distributed_merge import merge_snapshot
from .shared_state_manager import SharedStateManager
from .state_verification_manager import StateVerificationManager


class MMOWorldStateManager:
    """Build, diff, and verify MMO world state for networking."""

    def __init__(self, verifier: StateVerificationManager | None = None) -> None:
        self._verifier = verifier
        self._shared = SharedStateManager(verifier=verifier)

    @staticmethod
    def build_snapshot(
        regions: Iterable[Dict[str, Any]],
        influence: Dict[str, int],
        world_events: List[Dict[str, Any]],
        outposts: List[Dict[str, Any]],
        operations: List[Dict[str, Any]],
        trade_routes: List[Dict[str, Any]],
        directives: List[Dict[str, Any]],
        bounties: List[Dict[str, Any]],
        tombstones: List[Dict[str, Any]],
        updated_at: int,
        shard: str,
    ) -> Dict[str, Any]:
        """Return a normalized MMO world snapshot."""
        return {
            "regions": list(regions),
            "influence": dict(influence),
            "world_events": list(world_events),
            "outposts": list(outposts),
            "operations": list(operations),
            "trade_routes": list(trade_routes),
            "directives": list(directives),
            "bounties": list(bounties),
            "tombstones": list(tombstones),
            "updated_at": int(updated_at),
            "shard": str(shard),
        }

    @staticmethod
    def has_payload_changes(delta: Dict[str, Any]) -> bool:
        """Return True if ``delta`` contains changes beyond metadata keys."""
        return any(key not in {"seq", "type", "verify"} for key in delta)

    def update(self, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        """Return a delta for ``snapshot`` and update internal state."""
        return self._shared.update(**snapshot)

    def apply_delta(self, delta: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a delta from the network and return the new state."""
        incoming = self._shared.apply(delta)
        merged = self.merge_states(self.state, incoming)
        self._shared.load_snapshot(merged, sequence=self._shared.current_sequence())
        return merged

    def load_snapshot(
        self,
        snapshot: Dict[str, Any],
        sequence: int | None = None,
        verify: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        """Load ``snapshot`` after optional verification."""
        if verify and self._verifier and not self._verifier.verify(snapshot, verify):
            raise ValueError("world state verification failed")
        merged = self.merge_states(self.state, snapshot)
        return self._shared.load_snapshot(merged, sequence=sequence)

    def current_sequence(self) -> int:
        """Return the latest sequence number used for deltas."""
        return self._shared.current_sequence()

    @property
    def state(self) -> Dict[str, Any]:
        """Return the latest stored state."""
        return dict(self._shared.state)

    @staticmethod
    def _entry_key(entry: Dict[str, Any], keys: Tuple[str, ...]) -> Tuple[Any, ...]:
        return tuple(entry.get(key) for key in keys)

    @staticmethod
    def _merge_key(entry: Dict[str, Any], key_fields: Tuple[str, ...]) -> str:
        return json.dumps(
            [entry.get(key) for key in key_fields],
            ensure_ascii=True,
            separators=(",", ":"),
        )

    @staticmethod
    def _merge_records(
        local: List[Dict[str, Any]],
        incoming: List[Dict[str, Any]],
        key_fields: Tuple[str, ...],
        *,
        shard: str,
        ts_field: str = "updated_at",
        origin_field: str = "origin",
    ) -> List[Dict[str, Any]]:
        state: Dict[str, Any] = {}
        meta: Dict[str, Dict[str, Any]] = {}

        def _to_payload(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
            payload_state: Dict[str, Any] = {}
            payload_meta: Dict[str, Dict[str, Any]] = {}
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                key = MMOWorldStateManager._merge_key(entry, key_fields)
                payload_state[key] = dict(entry)
                payload_meta[key] = {
                    "logical_ts": int(entry.get(ts_field, 0) or 0),
                    "sender_id": str(entry.get(origin_field, "")),
                    "tombstone": False,
                }
            return {"state": payload_state, "meta": payload_meta}

        merge_snapshot(
            state,
            meta,
            _to_payload(local),
            "local",
            0,
            shard_id=shard,
            target_shard_id=shard,
        )
        merge_snapshot(
            state,
            meta,
            _to_payload(incoming),
            "incoming",
            0,
            shard_id=shard,
            target_shard_id=shard,
        )
        return [dict(state[key]) for key in sorted(state)]

    @staticmethod
    def merge_list(
        local: List[Dict[str, Any]],
        incoming: List[Dict[str, Any]],
        key_fields: Tuple[str, ...],
        ts_field: str = "updated_at",
        origin_field: str = "origin",
        shard: str = "public",
    ) -> List[Dict[str, Any]]:
        """Merge two lists by key and timestamp."""
        return MMOWorldStateManager._merge_records(
            local,
            incoming,
            key_fields,
            shard=shard,
            ts_field=ts_field,
            origin_field=origin_field,
        )

    def merge_states(
        self,
        local: Dict[str, Any],
        incoming: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Merge two world snapshots into a single resolved state."""
        local_shard = (
            str(local.get("shard")) if local.get("shard") is not None else ""
        )
        incoming_shard = (
            str(incoming.get("shard")) if incoming.get("shard") is not None else ""
        )
        if local_shard and incoming_shard and local_shard != incoming_shard:
            raise ValueError(
                f"shard mismatch: incoming {incoming_shard!r} does not match local {local_shard!r}"
            )
        local_updated = int(local.get("updated_at", 0) or 0)
        incoming_updated = int(incoming.get("updated_at", 0) or 0)
        merged = dict(local)
        target_shard = incoming_shard or local_shard or "public"
        merged.update(
            {
                "updated_at": max(local_updated, incoming_updated),
                "shard": incoming.get("shard", local.get("shard")),
            }
        )
        local_regions = local.get("regions") or []
        incoming_regions = incoming.get("regions") or []
        if isinstance(local_regions, list) and isinstance(incoming_regions, list):
            merged["regions"] = self.merge_list(
                local_regions, incoming_regions, ("name",), shard=target_shard
            )
        local_events = local.get("world_events") or []
        incoming_events = incoming.get("world_events") or []
        if isinstance(local_events, list) and isinstance(incoming_events, list):
            merged["world_events"] = self.merge_list(
                local_events, incoming_events, ("id",), shard=target_shard
            )
        local_outposts = local.get("outposts") or []
        incoming_outposts = incoming.get("outposts") or []
        if isinstance(local_outposts, list) and isinstance(incoming_outposts, list):
            merged["outposts"] = self.merge_list(
                local_outposts, incoming_outposts, ("region",), shard=target_shard
            )
        local_ops = local.get("operations") or []
        incoming_ops = incoming.get("operations") or []
        if isinstance(local_ops, list) and isinstance(incoming_ops, list):
            merged["operations"] = self.merge_list(
                local_ops, incoming_ops, ("name",), shard=target_shard
            )
        local_routes = local.get("trade_routes") or []
        incoming_routes = incoming.get("trade_routes") or []
        if isinstance(local_routes, list) and isinstance(incoming_routes, list):
            merged["trade_routes"] = self.merge_list(
                local_routes,
                incoming_routes,
                ("origin", "destination"),
                shard=target_shard,
            )
        local_directives = local.get("directives") or []
        incoming_directives = incoming.get("directives") or []
        if isinstance(local_directives, list) and isinstance(incoming_directives, list):
            merged["directives"] = self.merge_list(
                local_directives, incoming_directives, ("id",), shard=target_shard
            )
        local_bounties = local.get("bounties") or []
        incoming_bounties = incoming.get("bounties") or []
        if isinstance(local_bounties, list) and isinstance(incoming_bounties, list):
            merged["bounties"] = self.merge_list(
                local_bounties, incoming_bounties, ("id",), shard=target_shard
            )
        local_tombstones = local.get("tombstones") or []
        incoming_tombstones = incoming.get("tombstones") or []
        if isinstance(local_tombstones, list) and isinstance(incoming_tombstones, list):
            merged["tombstones"] = self.merge_list(
                local_tombstones,
                incoming_tombstones,
                ("kind", "id"),
                shard=target_shard,
            )
        tombstones = merged.get("tombstones", [])
        if isinstance(tombstones, list):
            merged["world_events"] = self._apply_tombstones(
                merged.get("world_events", []),
                tombstones,
                kind="world_event",
            )
            merged["outposts"] = self._apply_tombstones(
                merged.get("outposts", []),
                tombstones,
                kind="outpost",
            )
            merged["operations"] = self._apply_tombstones(
                merged.get("operations", []),
                tombstones,
                kind="operation",
            )
            merged["trade_routes"] = self._apply_tombstones(
                merged.get("trade_routes", []),
                tombstones,
                kind="trade_route",
            )
            merged["directives"] = self._apply_tombstones(
                merged.get("directives", []),
                tombstones,
                kind="directive",
            )
            merged["bounties"] = self._apply_tombstones(
                merged.get("bounties", []),
                tombstones,
                kind="bounty",
            )
        local_influence = local.get("influence")
        incoming_influence = incoming.get("influence")
        if isinstance(incoming_influence, dict) and isinstance(local_influence, dict):
            merged["influence"] = (
                dict(incoming_influence)
                if incoming_updated >= local_updated
                else dict(local_influence)
            )
        elif isinstance(incoming_influence, dict):
            merged["influence"] = dict(incoming_influence)
        return merged

    @staticmethod
    def _apply_tombstones(
        entries: Any,
        tombstones: List[Dict[str, Any]],
        *,
        kind: str,
    ) -> List[Dict[str, Any]]:
        if not isinstance(entries, list):
            return []
        removals = {
            str(tombstone.get("id")): int(tombstone.get("updated_at", 0) or 0)
            for tombstone in tombstones
            if tombstone.get("kind") == kind
        }
        filtered: List[Dict[str, Any]] = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            entry_id = entry.get("id")
            if entry_id is None:
                filtered.append(entry)
                continue
            tombstone_ts = removals.get(str(entry_id))
            if tombstone_ts is None:
                filtered.append(entry)
                continue
            entry_ts = int(entry.get("updated_at", 0) or 0)
            if tombstone_ts < entry_ts:
                filtered.append(entry)
        return filtered
