"""Shared state synchronization across nodes."""

from __future__ import annotations

"""Coordinate shared game state across a distributed server cluster."""

from typing import Any, Dict, Iterable, List, Tuple

from .cluster_manager import ClusterManager
from .node_manager import NodeManager
from .shared_state_manager import SharedStateManager
from .transmission_manager import TransmissionManager


class DistributedStateManager:
    """Share game state deltas with peer servers and ingest remote updates."""

    def __init__(
        self,
        state: SharedStateManager | None = None,
        nodes: NodeManager | None = None,
        transmission: TransmissionManager | None = None,
        cluster: ClusterManager | None = None,
        history_size: int = 32,
    ) -> None:
        self._state = state or SharedStateManager()
        self._nodes = nodes or NodeManager()
        self._transmission = transmission or TransmissionManager()
        self._cluster = cluster or ClusterManager()
        self._last_sent: Dict[Tuple[str, int], int] = {}
        self._last_ack: Dict[Tuple[str, int], int] = {}
        self._history: Dict[int, Dict[str, Any]] = {}
        self._history_packets: Dict[int, bytes] = {}
        self._history_limit = max(0, int(history_size))

    # ------------------------------------------------------------------
    # Node coordination helpers
    # ------------------------------------------------------------------
    def register_node(self, host: str, port: int) -> None:
        """Register a peer server that should receive state updates."""

        node = (host, int(port))
        adder = getattr(self._nodes, "add_node", None)
        if callable(adder):
            adder(node)
        address = f"{host}:{int(port)}"
        registrar = getattr(self._cluster, "register", None)
        if callable(registrar):
            registrar(address)
        self._last_sent.setdefault(node, 0)
        self._last_ack.setdefault(node, 0)

    def unregister_node(self, host: str, port: int) -> None:
        """Forget a peer server and clear pending acknowledgements."""

        node = (host, int(port))
        self._last_sent.pop(node, None)
        self._last_ack.pop(node, None)
        registrar = getattr(self._cluster, "unregister", None)
        if callable(registrar):
            registrar(f"{host}:{int(port)}")

    # ------------------------------------------------------------------
    # Broadcast helpers
    # ------------------------------------------------------------------
    def broadcast(self, **changes: Any) -> List[Dict[str, Any]]:
        """Return packets that push ``changes`` to every known peer."""

        delta = self._state.update(**changes)
        node_list = self._load_nodes()
        payload = self._build_state_payload(delta, node_list)
        packet = self._transmission.compress(payload)
        seq = int(delta.get("seq", 0))
        self._record_history(seq, delta, packet)
        transmissions: List[Dict[str, Any]] = []
        for node in node_list:
            self._last_sent[node] = seq
            transmissions.append(
                self._build_transmission(node, packet, delta, kind="delta")
            )
        return transmissions

    def nodes_pending_ack(self) -> List[Tuple[str, int]]:
        """Return nodes that have not acknowledged the latest sequence."""

        pending: List[Tuple[str, int]] = []
        for node, seq in self._last_sent.items():
            if self._last_ack.get(node, 0) < seq:
                pending.append(node)
        return pending

    def acknowledge(self, node: Tuple[str, int], sequence: int) -> None:
        """Record that ``node`` confirmed reception of ``sequence``."""

        if node in self._last_sent and sequence >= self._last_sent[node]:
            self._last_ack[node] = sequence

    def resend_pending(self) -> List[Dict[str, Any]]:
        """Return resend packets for nodes still awaiting acknowledgement."""

        transmissions: List[Dict[str, Any]] = []
        for node in self.nodes_pending_ack():
            seq = self._last_sent.get(node, 0)
            packet = self._history_packets.get(seq)
            delta = self._history.get(seq)
            if packet is None or delta is None:
                transmissions.append(self._build_snapshot_transmission(node))
                continue
            transmissions.append(
                self._build_transmission(node, packet, delta, kind="resend")
            )
        return transmissions

    def prepare_handshake(self, host: str, port: int) -> List[Dict[str, Any]]:
        """Create snapshot/history packets to bootstrap a new peer."""

        node = (host, int(port))
        self.register_node(host, port)
        transmissions = [self._build_snapshot_transmission(node)]
        for seq in sorted(self._history):
            packet = self._history_packets.get(seq)
            delta = self._history.get(seq)
            if packet is None or delta is None:
                continue
            transmissions.append(
                self._build_transmission(node, packet, delta, kind="history")
            )
        return transmissions

    def prepare_catch_up(
        self, host: str, port: int, sequence: int | None
    ) -> List[Dict[str, Any]]:
        """Return packets that advance ``host``/``port`` beyond ``sequence``.

        When the provided ``sequence`` is missing, invalid, or outside our
        retained history, the method falls back to delivering a full snapshot so
        the remote peer can resynchronise quickly. Otherwise, contiguous deltas
        newer than ``sequence`` are packaged with the ``catch_up`` kind so
        callers can distinguish them from normal broadcasts.
        """

        node = (host, int(port))
        self.register_node(host, port)
        if sequence is None:
            return self.prepare_handshake(host, port)
        try:
            last_sequence = int(sequence)
        except (TypeError, ValueError):
            return self.prepare_handshake(host, port)
        if last_sequence < 0:
            return self.prepare_handshake(host, port)
        available = [seq for seq in sorted(self._history) if seq > last_sequence]
        if not available:
            return [self._build_snapshot_transmission(node)]
        transmissions: List[Dict[str, Any]] = []
        expected = last_sequence + 1
        for seq in available:
            if seq != expected:
                return [self._build_snapshot_transmission(node)]
            packet = self._history_packets.get(seq)
            delta = self._history.get(seq)
            if packet is None or delta is None:
                return [self._build_snapshot_transmission(node)]
            transmissions.append(
                self._build_transmission(node, packet, delta, kind="catch_up")
            )
            self._last_sent[node] = seq
            expected += 1
        return transmissions

    # ------------------------------------------------------------------
    # Remote ingestion
    # ------------------------------------------------------------------
    def apply_remote(self, packet: bytes) -> Dict[str, Any]:
        """Apply a remote packet and return the resulting shared state."""

        message = self._transmission.decompress(packet)
        if not message:
            raise ValueError("invalid distributed state packet")
        mtype = message.get("type")
        if mtype == "distributed_state":
            self._ingest_nodes(message.get("nodes", []))
            self._ingest_cluster(message.get("cluster", []))
            delta = message.get("delta", {})
            if not isinstance(delta, dict):
                raise ValueError("missing delta in distributed state packet")
            state = self._state.apply(delta)
            return state
        if mtype == "distributed_snapshot":
            self._ingest_nodes(message.get("nodes", []))
            self._ingest_cluster(message.get("cluster", []))
            snapshot = message.get("state", {})
            if not isinstance(snapshot, dict):
                raise ValueError("invalid snapshot payload")
            sequence = message.get("seq")
            state = self._state.load_snapshot(snapshot, sequence if sequence is not None else None)
            return state
        raise ValueError("invalid distributed state packet")

    def state_copy(self) -> Dict[str, Any]:
        """Return a copy of the current shared state."""

        return dict(self._state.state)

    def sync_plan(self) -> Dict[str, Any]:
        """Return a summary of the distributed state synchronisation plan."""

        nodes = self._load_nodes()
        pending = self.nodes_pending_ack()
        return {
            "nodes": self._serialise_nodes(nodes),
            "pending": self._serialise_nodes(pending),
            "sequence": self._state.current_sequence(),
            "cluster": list(getattr(self._cluster, "nodes", [])),
            "history": sorted(self._history.keys()),
            "peers": self.peer_status(),
        }

    def peer_status(self) -> List[Dict[str, Any]]:
        """Return acknowledgement status for each registered peer."""

        status: List[Dict[str, Any]] = []
        for host, port in self._load_nodes():
            node = (host, port)
            last_sent = int(self._last_sent.get(node, 0))
            last_ack = int(self._last_ack.get(node, 0))
            status.append(
                {
                    "node": self._serialise_nodes([node])[0],
                    "last_sent": last_sent,
                    "last_ack": last_ack,
                    "lag": max(0, last_sent - last_ack),
                    "pending": last_ack < last_sent,
                }
            )
        return status

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _load_nodes(self) -> List[Tuple[str, int]]:
        loader = getattr(self._nodes, "load_nodes", None)
        if callable(loader):
            nodes = loader()
            return [(str(host), int(port)) for host, port in nodes]
        return []

    @staticmethod
    def _serialise_nodes(nodes: Iterable[Tuple[str, int]]) -> List[List[Any]]:
        return [[host, int(port)] for host, port in nodes]

    def _ingest_nodes(self, nodes: Iterable[Iterable[Any]]) -> None:
        adder = getattr(self._nodes, "add_node", None)
        if not callable(adder):
            return
        for host, port in nodes:
            adder((str(host), int(port)))

    def _ingest_cluster(self, addresses: Iterable[Any]) -> None:
        registrar = getattr(self._cluster, "register", None)
        if not callable(registrar):
            return
        for address in addresses:
            registrar(str(address))

    def _build_state_payload(
        self, delta: Dict[str, Any], nodes: Iterable[Tuple[str, int]]
    ) -> Dict[str, Any]:
        return {
            "type": "distributed_state",
            "delta": dict(delta),
            "nodes": self._serialise_nodes(nodes),
            "cluster": list(getattr(self._cluster, "nodes", [])),
        }

    def _build_transmission(
        self,
        node: Tuple[str, int],
        packet: bytes,
        delta: Dict[str, Any],
        *,
        kind: str | None = None,
    ) -> Dict[str, Any]:
        transmission: Dict[str, Any] = {
            "node": node,
            "packet": packet,
            "delta": dict(delta),
        }
        if kind:
            transmission["kind"] = kind
        return transmission

    def _build_snapshot_transmission(self, node: Tuple[str, int]) -> Dict[str, Any]:
        nodes = self._load_nodes()
        payload = {
            "type": "distributed_snapshot",
            "state": self.state_copy(),
            "seq": self._state.current_sequence(),
            "nodes": self._serialise_nodes(nodes),
            "cluster": list(getattr(self._cluster, "nodes", [])),
        }
        packet = self._transmission.compress(payload)
        seq = int(payload.get("seq", 0))
        if node not in self._last_sent or self._last_sent[node] < seq:
            self._last_sent[node] = seq
        return {
            "node": node,
            "packet": packet,
            "state": payload["state"],
            "delta": {"seq": seq},
            "kind": "snapshot",
        }

    def _record_history(self, sequence: int, delta: Dict[str, Any], packet: bytes) -> None:
        if sequence <= 0 or self._history_limit <= 0:
            return
        self._history[sequence] = dict(delta)
        self._history_packets[sequence] = packet
        if len(self._history) > self._history_limit:
            for seq in sorted(self._history)[:-self._history_limit]:
                self._history.pop(seq, None)
                self._history_packets.pop(seq, None)
