"""Tests for network."""

import time
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.network import NetworkManager
from hololive_coliseum.state_sync import StateSync
from hololive_coliseum.node_registry import load_nodes, add_node
from hololive_coliseum.save_manager import load_settings
from hololive_coliseum import add_game, register_account, load_chain
from hololive_coliseum.ban_manager import BanManager


class MemoryNodeManager:
    """In-memory node store for tests."""

    def __init__(self) -> None:
        self.nodes: list[tuple[str, int]] = []

    def load_nodes(self) -> list[tuple[str, int]]:
        return list(self.nodes)

    def save_nodes(self, nodes: list[tuple[str, int]]) -> None:
        self.nodes = list(nodes)

    def add_node(self, node: tuple[str, int]) -> None:
        if node not in self.nodes:
            self.nodes.append(node)

    def prune_nodes(self, ping_func, timeout: float = 0.2) -> None:  # pragma: no cover
        self.nodes = [n for n in self.nodes if ping_func(n) is not None]


def test_network_send_receive():
    host = NetworkManager(host=True, address=("127.0.0.1", 0), encrypt_key=b"k", client_id="host")
    addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=addr, encrypt_key=b"k", client_id="client")
    client.register_client([addr])
    time.sleep(0.01)
    host.poll(); client.poll()
    sync = StateSync()
    msg = {"x": 1}
    client.send_state(msg)
    time.sleep(0.01)
    received = host.poll()
    assert received
    delta = received[0][1]
    for k in ("id", "token", "type"):
        delta.pop(k, None)
    state = sync.apply(delta)
    assert state == msg
    host.sock.close()
    client.sock.close()


def test_network_discovery():
    host = NetworkManager(host=True, address=("", 0), client_id="host")
    port = host.sock.getsockname()[1]
    time.sleep(0.01)
    servers = NetworkManager.discover(
        timeout=0.1,
        port=port,
        broadcast_address="127.0.0.1",
        process_host=host.poll,
    )
    assert any(addr[1] == port for addr in servers)
    host.sock.close()


def test_network_announce(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.node_registry.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.node_registry.NODES_FILE', tmp_path / 'nodes.json')
    monkeypatch.setattr('hololive_coliseum.node_registry.DEFAULT_NODES', [])
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host")
    host_addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=host_addr, client_id="client")
    client.broadcast_announce([host_addr])
    time.sleep(0.01)
    host.poll()
    nodes = load_nodes()
    assert nodes[0] == host_addr
    assert len(nodes) == 2
    host.sock.close()
    client.sock.close()


def test_ping_node():
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host")
    addr = host.sock.getsockname()

    def process():
        host.poll()

    latency = NetworkManager.ping_node(addr, timeout=0.5, process_host=process)
    assert latency is not None and latency < 0.5
    host.sock.close()


def test_select_best_node(monkeypatch):
    nodes = [("1.1.1.1", 1), ("2.2.2.2", 2)]
    latencies = {nodes[0]: 0.3, nodes[1]: 0.1}

    def fake_ping(node):
        return latencies[node]

    best = NetworkManager.select_best_node(nodes, ping_func=fake_ping)
    assert best == nodes[1]


def test_register_and_find_games():
    router = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="router")
    router_addr = router.sock.getsockname()
    host = NetworkManager(host=False, address=router_addr, client_id="host")
    host.register_game([router_addr])
    time.sleep(0.01)
    router.poll()

    games = NetworkManager.request_games(router_addr, timeout=0.1, process_host=router.poll)
    ports = [port for _, port in games]
    assert host.sock.getsockname()[1] in ports

    host.sock.close()
    router.sock.close()


def test_session_token_enforced():
    host = NetworkManager(host=True, address=("127.0.0.1", 0), encrypt_key=b"k", client_id="host")
    addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=addr, encrypt_key=b"k", client_id="client")
    client.register_client([addr])
    time.sleep(0.01)
    host.poll()
    client.poll()
    assert client.session_token == host.session_token
    bad = client.security.encode({"type": "state", "id": "client", "token": "bad"})
    client.sock.sendto(bad, addr)
    time.sleep(0.01)
    assert not host.poll()
    host.sock.close()
    client.sock.close()


def test_register_and_find_clients():
    router = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="router")
    router_addr = router.sock.getsockname()
    client = NetworkManager(host=False, address=router_addr, client_id="client")
    client.register_client([router_addr])
    time.sleep(0.01)
    router.poll()

    clients = NetworkManager.request_clients(router_addr, timeout=0.1, process_host=router.poll)
    ports = [port for _, port in clients]
    assert client.sock.getsockname()[1] in ports

    client.sock.close()
    router.sock.close()


def test_client_join_leave_updates_peers():
    router = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="router")
    addr = router.sock.getsockname()
    c1 = NetworkManager(host=False, address=addr, client_id="c1")
    c1.register_client([addr])
    time.sleep(0.01)
    router.poll(); c1.poll()
    c2 = NetworkManager(host=False, address=addr, client_id="c2")
    c2.register_client([addr])
    c2_addr = ("127.0.0.1", c2.sock.getsockname()[1])
    time.sleep(0.01)
    router.poll(); c1.poll()
    assert c2_addr in c1.peers
    c2.unregister_client([addr])
    time.sleep(0.01)
    router.poll(); c1.poll()
    assert c2_addr not in c1.peers
    assert c2_addr not in router.live_clients
    c1.sock.close(); c2.sock.close(); router.sock.close()

def test_nodes_share_games(tmp_path, monkeypatch):
    data_dir = tmp_path / 'nodes'
    monkeypatch.setattr('hololive_coliseum.node_registry.SAVE_DIR', data_dir)
    monkeypatch.setattr('hololive_coliseum.node_registry.NODES_FILE', data_dir / 'nodes.json')
    monkeypatch.setattr('hololive_coliseum.node_registry.DEFAULT_NODES', [])
    data_dir.mkdir()

    router1 = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="r1")
    router2 = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="r2")
    addr1 = router1.sock.getsockname()
    addr2 = router2.sock.getsockname()
    add_node(addr1)
    add_node(addr2)

    # announce each other so they learn peers
    router1.broadcast_announce([addr2])
    router2.broadcast_announce([addr1])
    time.sleep(0.01)
    router1.poll(); router2.poll()

    host = NetworkManager(host=False, address=addr1, client_id="host")
    host.register_game([addr1])
    time.sleep(0.01)
    router1.poll(); router2.poll()

    assert addr2 in load_nodes()
    host_port = host.sock.getsockname()[1]
    assert any(port == host_port for _, port in router2.games)

    host.sock.close()
    router1.sock.close()
    router2.sock.close()


def test_nodes_share_clients(tmp_path, monkeypatch):
    data_dir = tmp_path / 'nodes2'
    monkeypatch.setattr('hololive_coliseum.node_registry.SAVE_DIR', data_dir)
    monkeypatch.setattr('hololive_coliseum.node_registry.NODES_FILE', data_dir / 'nodes.json')
    monkeypatch.setattr('hololive_coliseum.node_registry.DEFAULT_NODES', [])
    data_dir.mkdir()

    router1 = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="r1")
    router2 = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="r2")
    addr1 = router1.sock.getsockname()
    addr2 = router2.sock.getsockname()
    add_node(addr1)
    add_node(addr2)

    router1.broadcast_announce([addr2])
    router2.broadcast_announce([addr1])
    time.sleep(0.01)
    router1.poll(); router2.poll()

    client = NetworkManager(host=False, address=addr1, client_id="client")
    client.register_client([addr1])
    time.sleep(0.01)
    router1.poll(); router2.poll()

    assert addr2 in load_nodes()
    assert any(port == client.sock.getsockname()[1] for _, port in router2.live_clients)

    client.sock.close()
    router1.sock.close()
    router2.sock.close()


def test_request_nodes():
    manager = MemoryNodeManager()
    router = NetworkManager(host=True, address=("127.0.0.1", 0), node_manager=manager, client_id="router")
    addr = router.sock.getsockname()
    manager.add_node(addr)
    nodes = NetworkManager.request_nodes(addr, timeout=0.1, process_host=router.poll)
    assert addr in nodes
    router.sock.close()


def test_nodes_update_gossip():
    m1 = MemoryNodeManager()
    m2 = MemoryNodeManager()
    router1 = NetworkManager(host=True, address=("127.0.0.1", 0), node_manager=m1, client_id="r1")
    router2 = NetworkManager(host=True, address=("127.0.0.1", 0), node_manager=m2, client_id="r2")
    addr1 = router1.sock.getsockname()
    addr2 = router2.sock.getsockname()
    m1.add_node(addr1)
    m1.add_node(addr2)
    router1.broadcast_nodes([addr2])
    time.sleep(0.01)
    router2.poll()
    assert addr1 in m2.load_nodes()
    router1.sock.close()
    router2.sock.close()


def test_block_broadcast(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'a.json')
    register_account('a', 'user', 'pubA')
    register_account('b', 'user', 'pubB')
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host")
    addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=addr, client_id="client")
    client.send_state({"ping": 1})
    time.sleep(0.01)
    host.poll()
    block = add_game(['a', 'b'], 'a')
    host.broadcast_block(block)
    time.sleep(0.01)
    client.poll()
    chain = load_chain()
    game_ids = [b.get('game_id') for b in chain if b.get('game_id')]
    assert block['game_id'] in game_ids
    host.sock.close()
    client.sock.close()


def test_chain_request(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'a.json')
    register_account('a', 'user', 'pubA')
    register_account('b', 'user', 'pubB')
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host")
    block = add_game(['a', 'b'], 'a')
    addr = host.sock.getsockname()
    chain = NetworkManager.request_chain(addr, process_host=host.poll)
    assert chain and chain[0]['game_id'] == block['game_id']
    host.sock.close()

def test_state_sync_delta():
    sync = StateSync()
    first = sync.encode({'x': 1, 'y': 2})
    assert sync.apply(first) == {'x': 1, 'y': 2}
    assert first['seq'] == 1
    second = sync.encode({'x': 1, 'y': 3})
    assert second == {'y': 3, 'seq': 2}
    state = sync.apply(second)
    assert state == {'x': 1, 'y': 3}


def test_reliable_packets():
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host")
    addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=addr, client_id="client")

    client.send_reliable({"type": "hello"}, max_retries=1, importance=2)
    # wait less than ack_timeout to trigger resend check
    time.sleep(client.ack_timeout / 2 + 0.01)
    client.process_reliable()
    key = list(client._pending_acks.keys())[0]
    # after one resend a retry was consumed
    assert client._pending_acks[key][2] == 1
    # host processes message and sends ack
    host.poll()
    time.sleep(0.01)
    client.poll()
    assert not client._pending_acks
    host.sock.close()
    client.sock.close()

def test_records_update(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.node_registry.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.node_registry.NODES_FILE', tmp_path / 'nodes.json')
    monkeypatch.setattr('hololive_coliseum.node_registry.DEFAULT_NODES', [])
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host")
    client = NetworkManager(host=False, address=host.sock.getsockname(), client_id="client")
    # send records from host to client
    host.broadcast_records(5.0, 12, [client.sock.getsockname()])
    time.sleep(0.01)
    client.poll()
    data = load_settings()
    assert data['best_time'] == 5.0 and data['best_score'] == 12
    host.sock.close()
    client.sock.close()


def test_relay_forwarding():
    relay = NetworkManager(host=True, address=("127.0.0.1", 0), relay_mode=True, client_id="relay")
    relay_addr = relay.sock.getsockname()
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host")
    host_addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=relay_addr, relay_addr=relay_addr, client_id="client")

    client.send_via_relay({"type": "hello"}, host_addr)
    time.sleep(0.01)
    relay.poll()
    msgs = host.poll()
    assert msgs and msgs[0][1]["type"] == "hello"

    client.sock.close()
    host.sock.close()
    relay.sock.close()


def test_select_best_node_empty():
    assert NetworkManager.select_best_node([]) is None


def test_network_chat():
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host")
    addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=addr, client_id="client")
    client.register_client([addr])
    time.sleep(0.01)
    host.poll(); client.poll()
    client.send_chat("p1", "hi")
    time.sleep(0.01)
    msgs = host.poll()
    assert msgs and msgs[0][1]["type"] == "chat" and msgs[0][1]["msg"] == "hi"

    client.sock.close()
    host.sock.close()


def test_time_sync():
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host")
    addr = host.sock.getsockname()
    offset = NetworkManager.sync_time(addr, timeout=0.2, process_host=host.poll)
    assert offset is not None and abs(offset) < 0.5
    host.sock.close()


def test_state_bridging():
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host")
    addr = host.sock.getsockname()
    c1 = NetworkManager(host=False, address=addr, client_id="c1")
    c2 = NetworkManager(host=False, address=addr, client_id="c2")

    c1.register_client([addr])
    c2.register_client([addr])
    time.sleep(0.01)
    host.poll(); c1.poll(); c2.poll()

    c1.send_state({"a": 1})
    time.sleep(0.01)
    host.poll()
    c1.poll()

    c2.send_state({"b": 2})
    time.sleep(0.01)
    host.poll()
    c1.poll()
    c2.poll()

    assert {p[1] for p in c1.peers} == {c2.sock.getsockname()[1]}
    assert {p[1] for p in c2.peers} == {c1.sock.getsockname()[1]}

    c1.send_state({"x": 5})
    time.sleep(0.01)
    msgs = c2.poll()
    assert any("x" in m[1] for m in msgs)

    for sock in (host.sock, c1.sock, c2.sock):
        sock.close()


def test_rate_limit():
    host = NetworkManager(host=True, address=("127.0.0.1", 0), rate_limit=1, client_id="host")
    addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=addr, rate_limit=1, client_id="client")
    packet = host._encode({"type": "chat", "msg": "hi"})
    # send two packets quickly; second should be dropped by rate limiter
    client.sock.sendto(packet, addr)
    client.sock.sendto(packet, addr)
    time.sleep(0.01)
    messages = host.poll()
    assert len(messages) == 1
    host.sock.close()
    client.sock.close()


def test_anti_spoofing():
    host = NetworkManager(host=True, address=("127.0.0.1", 0), secret=b"s", client_id="host")
    addr = host.sock.getsockname()
    client = NetworkManager(address=addr, secret=b"s", client_id="alice")
    client.send_state({"x": 1})
    time.sleep(0.01)
    host.poll()
    fake = client.security.encode({"type": "state", "id": "mallory", "x": 2})
    client.sock.sendto(fake, addr)
    time.sleep(0.01)
    assert host.poll() == []
    host.sock.close()
    client.sock.close()


def test_banned_user_ignored():
    ban = BanManager()
    ban.ban("evil")
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host", ban_manager=ban)
    addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=addr, client_id="evil")
    client.register_client([addr])
    time.sleep(0.01)
    host.poll()
    client.poll()
    client.send_chat("evil", "hi")
    time.sleep(0.01)
    assert host.poll() == []
    host.sock.close()
    client.sock.close()
