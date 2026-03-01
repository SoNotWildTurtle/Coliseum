"""Tests for distributed state manager."""

from hololive_coliseum.distributed_state_manager import DistributedStateManager
from hololive_coliseum.shared_state_manager import SharedStateManager
from hololive_coliseum.transmission_manager import TransmissionManager
from hololive_coliseum.cluster_manager import ClusterManager


class MemoryNodeManager:
    """In-memory node registry for tests."""

    def __init__(self) -> None:
        self.nodes: list[tuple[str, int]] = []

    def load_nodes(self) -> list[tuple[str, int]]:
        return list(self.nodes)

    def add_node(self, node: tuple[str, int]) -> None:
        if node not in self.nodes:
            self.nodes.append(node)


def test_distributed_state_broadcast_and_apply_roundtrip() -> None:
    node_manager = MemoryNodeManager()
    cluster = ClusterManager()
    transmission = TransmissionManager()
    manager = DistributedStateManager(
        state=SharedStateManager(),
        nodes=node_manager,
        transmission=transmission,
        cluster=cluster,
    )
    manager.register_node("10.0.0.1", 7000)
    manager.register_node("10.0.0.2", 7001)

    packets = manager.broadcast(score=5, online=32)
    assert len(packets) == 2

    remote_nodes = MemoryNodeManager()
    remote_cluster = ClusterManager()
    remote = DistributedStateManager(
        state=SharedStateManager(),
        nodes=remote_nodes,
        transmission=transmission,
        cluster=remote_cluster,
    )

    state = remote.apply_remote(packets[0]["packet"])
    assert state["score"] == 5
    assert state["online"] == 32
    assert ("10.0.0.1", 7000) in remote_nodes.load_nodes()
    assert "10.0.0.1:7000" in remote_cluster.nodes


def test_distributed_state_ack_tracking() -> None:
    node_manager = MemoryNodeManager()
    transmission = TransmissionManager()
    manager = DistributedStateManager(
        nodes=node_manager,
        transmission=transmission,
    )
    node_manager.add_node(("10.0.0.3", 7002))

    packets = manager.broadcast(score=9)
    node = packets[0]["node"]
    seq = packets[0]["delta"]["seq"]
    assert manager.nodes_pending_ack() == [node]

    manager.acknowledge(node, seq)
    assert manager.nodes_pending_ack() == []


def test_distributed_state_resend_and_snapshot_fallback() -> None:
    node_manager = MemoryNodeManager()
    transmission = TransmissionManager()
    manager = DistributedStateManager(
        nodes=node_manager,
        transmission=transmission,
        history_size=1,
    )
    node_manager.add_node(("10.0.0.4", 7003))
    packets = manager.broadcast(score=11)
    node = packets[0]["node"]
    resends = manager.resend_pending()
    assert len(resends) == 1
    assert resends[0]["kind"] == "resend"
    assert resends[0]["node"] == node
    manager.acknowledge(node, packets[0]["delta"]["seq"])
    assert manager.resend_pending() == []

    snapshot_manager = DistributedStateManager(
        nodes=MemoryNodeManager(),
        transmission=transmission,
        history_size=0,
    )
    snapshot_manager.register_node("10.0.0.5", 7004)
    snapshot_manager.broadcast(score=22)
    fallback = snapshot_manager.resend_pending()
    assert len(fallback) == 1
    assert fallback[0]["kind"] == "snapshot"


def test_distributed_state_handshake_bootstraps_new_node() -> None:
    transmission = TransmissionManager()
    manager = DistributedStateManager(
        state=SharedStateManager(),
        nodes=MemoryNodeManager(),
        transmission=transmission,
    )
    manager.broadcast(level=3)
    handshake_packets = manager.prepare_handshake("10.0.0.6", 7005)
    remote = DistributedStateManager(
        state=SharedStateManager(),
        nodes=MemoryNodeManager(),
        transmission=transmission,
    )
    for packet in handshake_packets:
        remote.apply_remote(packet["packet"])
    assert remote.state_copy()["level"] == 3


def test_distributed_state_sync_plan_reports_cluster() -> None:
    node_manager = MemoryNodeManager()
    cluster = ClusterManager()
    manager = DistributedStateManager(
        state=SharedStateManager(),
        nodes=node_manager,
        transmission=TransmissionManager(),
        cluster=cluster,
    )
    manager.register_node("10.0.0.7", 7006)
    manager.broadcast(score=5)
    plan = manager.sync_plan()
    assert plan["nodes"] == [["10.0.0.7", 7006]]
    assert plan["pending"] == [["10.0.0.7", 7006]]
    assert plan["sequence"] >= 1
    assert "10.0.0.7:7006" in plan["cluster"]
    assert plan["peers"][0]["pending"] is True


def test_distributed_state_prepare_catch_up_returns_history() -> None:
    nodes = MemoryNodeManager()
    transmission = TransmissionManager()
    manager = DistributedStateManager(
        state=SharedStateManager(),
        nodes=nodes,
        transmission=transmission,
        history_size=4,
    )
    manager.broadcast(score=1)
    manager.broadcast(score=2)
    manager.broadcast(score=3)

    catch_up = manager.prepare_catch_up("10.0.0.8", 7007, sequence=1)
    assert len(catch_up) == 2
    assert all(packet["kind"] == "catch_up" for packet in catch_up)
    assert all(packet["delta"]["seq"] > 1 for packet in catch_up)


def test_distributed_state_prepare_catch_up_snapshot_on_gap() -> None:
    nodes = MemoryNodeManager()
    transmission = TransmissionManager()
    manager = DistributedStateManager(
        state=SharedStateManager(),
        nodes=nodes,
        transmission=transmission,
        history_size=1,
    )
    manager.broadcast(score=10)
    manager.broadcast(score=11)

    catch_up = manager.prepare_catch_up("10.0.0.9", 7008, sequence=0)
    assert len(catch_up) == 1
    assert catch_up[0]["kind"] == "snapshot"


def test_distributed_state_peer_status_tracks_lag() -> None:
    nodes = MemoryNodeManager()
    transmission = TransmissionManager()
    manager = DistributedStateManager(nodes=nodes, transmission=transmission)
    nodes.add_node(("10.0.0.10", 7009))
    packets = manager.broadcast(score=15)
    node = packets[0]["node"]
    status = manager.peer_status()
    assert status[0]["pending"] is True
    assert status[0]["lag"] >= 1

    manager.acknowledge(node, packets[0]["delta"]["seq"])
    status = manager.peer_status()
    assert status[0]["pending"] is False
    assert status[0]["lag"] == 0
