"""Networking helpers for discovery and game state synchronization.

Packets include a claimed sender ID and the manager cross-checks it against the
socket address to provide basic anti-spoofing protection. After a brief
handshake, all packets carry a session token so unsolicited traffic is ignored."""

import json
import os
import socket
import time
import uuid
from typing import Any, List, Tuple

from .data_protection_manager import DataProtectionManager

from .state_sync import StateSync
from .sync_manager import SyncManager

from .node_manager import NodeManager
from .ban_manager import BanManager
from .matchmaking_manager import MatchmakingManager

from .save_manager import merge_records
from .blockchain import load_chain, save_chain, verify_chain, merge_chain


class NetworkManager:
    """Simple UDP networking manager for multiplayer.

    Hosts respond to broadcast discovery packets so clients can automatically
    find available games on the local network. Router nodes keep track of game
    hosts **and** individual clients so the mesh knows which players are online
    at any moment. After an initial handshake, peers exchange a session token
    which is attached to all future packets so strangers cannot inject data.
    Hosts consult a ban list to drop packets from abusive IDs. Compression,
    encryption and signing are performed via a dedicated
    :class:`DataProtectionManager` instance for efficient packet handling that
    can also strip sensitive fields before encoding. State updates run through
    :class:`StateSync` which supports per-field tolerances to avoid transmitting
    insignificant changes.
    """

    def __init__(
        self,
        host: bool = False,
        address: Tuple[str, int] = ("", 50007),
        secret: bytes | None = None,
        encrypt_key: bytes | None = None,
        sign_key=None,
        relay_mode: bool = False,
        relay_addr: Tuple[str, int] | None = None,
        node_manager: NodeManager | None = None,
        tolerances: dict[str, float] | None = None,
        rate_limit: int = 60,
        sanitize_fields: set[str] | None = None,
        client_id: str | None = None,
        ban_manager: BanManager | None = None,
    ) -> None:
        self.host = host
        self.address = address
        self.node_manager = node_manager or NodeManager()
        self.security = DataProtectionManager(
            key=encrypt_key,
            secret=secret,
            sign_key=sign_key,
            sanitize_fields=sanitize_fields,
        )
        self.ban_manager = ban_manager or BanManager()
        self.client_id = client_id
        self.addr_to_id: dict[Tuple[str, int], str] = {}
        self.id_to_addr: dict[str, Tuple[str, int]] = {}
        self.session_token = uuid.uuid4().hex if host else None
        self.relay_mode = relay_mode
        self.relay_addr = relay_addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        if os.name == "nt":
            try:
                self.sock.ioctl(socket.SIO_UDP_CONNRESET, False)
            except (AttributeError, OSError):
                pass
        if host:
            self.sock.bind(address)
            self.clients: set[Tuple[str, int]] = set()
            # addresses of connected game hosts
            self.games: set[Tuple[str, int]] = set()
            # addresses of individual clients registered with this router
            self.live_clients: set[Tuple[str, int]] = set()
            # available relay nodes
            self.relays: set[Tuple[str, int]] = set()
            self.node_manager.add_node(self.sock.getsockname())
            self.matchmaking_queues: dict[tuple[str, int], MatchmakingManager] = {}
            self.matchmaking_pending: dict[str, dict[str, Any]] = {}
        else:
            self.sock.bind(("", 0))
            # addresses of other clients for direct peer communication
            self.peers: set[Tuple[str, int]] = set()

        # allow broadcast for discovery
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._sync = StateSync(tolerances)
        self._reliable_seq = 0
        self._pending_acks: dict[
            Tuple[Tuple[str, int], int], tuple[bytes, float, int, int]
        ] = {}
        self.ack_timeout = 0.2
        self.rate_limit = rate_limit
        self._msg_counts: dict[Tuple[str, int], tuple[int, float]] = {}
        
        # store most recent time offset from remote host
        self.sync = SyncManager()
    def _encode(self, msg: dict[str, Any]) -> bytes:
        msg = msg.copy()
        if self.client_id is not None:
            msg.setdefault("id", self.client_id)
        if self.session_token is not None:
            msg.setdefault("token", self.session_token)
        return self.security.encode(msg)

    def _decode(self, data: bytes) -> dict[str, Any] | None:
        return self.security.decode(data)

    def rotate_keys(
        self,
        key: bytes | None = None,
        secret: bytes | None = None,
        sign_key=None,
    ) -> None:
        """Rotate encryption or signing keys used for packet security."""
        self.security.rotate_keys(key, secret, sign_key)

    def broadcast_announce(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Broadcast our presence to known nodes."""
        if nodes is None:
            nodes = self.node_manager.load_nodes()
        msg = self._encode({"type": "announce"})
        for node in nodes:
            try:
                self.sock.sendto(msg, tuple(node))
            except OSError:
                pass

    def register_game(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Register this host with router nodes so players can find the game."""
        if nodes is None:
            nodes = self.node_manager.load_nodes()
        msg = self._encode({"type": "register"})
        for node in nodes:
            try:
                self.sock.sendto(msg, tuple(node))
            except OSError:
                pass

    def register_client(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Register this client with router nodes for discovery."""
        if nodes is None:
            nodes = self.node_manager.load_nodes()
        msg = self._encode({"type": "client_join"})
        for node in nodes:
            try:
                self.sock.sendto(msg, tuple(node))
            except OSError:
                pass

    def unregister_client(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Remove this client from router nodes so others drop the peer."""
        if nodes is None:
            nodes = self.node_manager.load_nodes()
        msg = self._encode({"type": "client_leave"})
        for node in nodes:
            try:
                self.sock.sendto(msg, tuple(node))
            except OSError:
                pass

    def refresh_nodes(self) -> None:
        """Prune unreachable nodes from the registry."""
        self.node_manager.prune_nodes(lambda n: NetworkManager.ping_node(n, timeout=self.ack_timeout))

    def broadcast_games(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Share our current game list with other nodes."""
        if not self.host:
            return
        if nodes is None:
            nodes = self.node_manager.load_nodes()
        payload = self._encode({"type": "games_update", "games": list(self.games)})
        for node in nodes:
            if node == self.sock.getsockname():
                continue
            try:
                self.sock.sendto(payload, tuple(node))
            except OSError:
                pass

    def broadcast_clients(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Share our active client list with other nodes."""
        if not self.host:
            return
        if nodes is None:
            nodes = self.node_manager.load_nodes()
        payload = self._encode({"type": "clients_update", "clients": list(self.live_clients)})
        for node in nodes:
            if node == self.sock.getsockname():
                continue
            try:
                self.sock.sendto(payload, tuple(node))
            except OSError:
                pass

    def broadcast_relays(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Share known relay nodes with peers."""
        if not self.host:
            return
        if nodes is None:
            nodes = self.node_manager.load_nodes()
        payload = self._encode({"type": "relays_update", "relays": list(self.relays)})
        for node in nodes:
            if node == self.sock.getsockname():
                continue
            try:
                self.sock.sendto(payload, tuple(node))
            except OSError:
                pass

    def broadcast_nodes(self, targets: List[Tuple[str, int]] | None = None) -> None:
        """Share our known node list with peers."""
        if not self.host:
            return
        if targets is None:
            targets = self.node_manager.load_nodes()
        payload = self._encode({"type": "nodes_update", "nodes": self.node_manager.load_nodes()})
        for node in targets:
            if node == self.sock.getsockname():
                continue
            try:
                self.sock.sendto(payload, tuple(node))
            except OSError:
                pass

    def broadcast_block(self, block: dict[str, Any], nodes: List[Tuple[str, int]] | None = None) -> None:
        """Broadcast a new blockchain block to clients and peers."""
        if not self.host:
            return
        packet = self._encode({"type": "block_update", "block": block})
        for client in list(self.clients):
            try:
                self.sock.sendto(packet, client)
            except OSError:
                pass
        if nodes is None:
            nodes = self.node_manager.load_nodes()
        for node in nodes:
            if node == self.sock.getsockname():
                continue
            try:
                self.sock.sendto(packet, tuple(node))
            except OSError:
                pass

    def send_chain(self, addr: Tuple[str, int]) -> None:
        """Send the entire blockchain to ``addr``."""
        if not self.host:
            return
        packet = self._encode({"type": "chain_response", "chain": load_chain()})
        try:
            self.sock.sendto(packet, addr)
        except OSError:
            pass

    def offer_relay(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Announce ourselves as a relay node."""
        if nodes is None:
            nodes = self.node_manager.load_nodes()
        payload = self._encode({"type": "relay_offer"})
        for node in nodes:
            try:
                self.sock.sendto(payload, tuple(node))
            except OSError:
                pass

    @staticmethod
    def request_relays(
        node: Tuple[str, int],
        timeout: float = 0.5,
        process_host=None,
        secret: bytes | None = None,
    ) -> List[Tuple[str, int]]:
        """Ask a router node for known relays."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        enc = NetworkManager(secret=secret, client_id="helper")
        msg = enc._encode({"type": "get_relays"})
        sock.sendto(msg, node)
        relays: List[Tuple[str, int]] = []
        start = time.monotonic()
        while True:
            if process_host is not None:
                process_host()
            try:
                packet, _ = sock.recvfrom(4096)
            except socket.timeout:
                break
            data = enc._decode(packet)
            if data is None:
                continue
            if data.get("type") == "relays":
                for host, port in data.get("relays", []):
                    relays.append((host, int(port)))
            if time.monotonic() - start > timeout:
                break
        sock.close()
        return relays

    @staticmethod
    def request_chain(
        node: Tuple[str, int],
        timeout: float = 0.5,
        process_host=None,
        secret: bytes | None = None,
    ) -> List[dict[str, Any]]:
        """Fetch the blockchain from ``node`` and merge it locally."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        poll_interval = min(0.05, max(0.01, timeout))
        sock.settimeout(poll_interval)
        enc = NetworkManager(secret=secret, client_id="helper")
        msg = enc._encode({"type": "chain_request"})
        sock.sendto(msg, node)
        chain: List[dict[str, Any]] = []
        start = time.monotonic()
        while True:
            if process_host is not None:
                process_host()
            try:
                packet, _ = sock.recvfrom(65535)
            except socket.timeout:
                if time.monotonic() - start > timeout:
                    break
                continue
            data = enc._decode(packet)
            if data and data.get("type") == "chain_response":
                chain = data.get("chain", [])
                break
            if time.monotonic() - start > timeout:
                break
        sock.close()
        if chain:
            merge_chain(chain)
        return chain

    def send_via_relay(self, data: dict[str, Any], dest: Tuple[str, int]) -> None:
        """Send a packet through our configured relay address."""
        payload = self._encode(data)
        if self.relay_addr is None:
            self.sock.sendto(payload, dest)
            return
        outer = self._encode({"type": "relay_data", "dest": dest, "payload": payload.hex()})
        try:
            self.sock.sendto(outer, self.relay_addr)
        except OSError:
            pass

    @staticmethod
    def _normalize_addr(addr: Tuple[str, int]) -> Tuple[str, int]:
        host, port = addr
        if host in {"0.0.0.0", ""}:
            host = "127.0.0.1"
        return host, int(port)

    def broadcast_records(
        self,
        best_time: float,
        best_score: int,
        nodes: List[Tuple[str, int]] | None = None,
    ) -> None:
        """Send our current records to other nodes."""
        if nodes is None:
            nodes = self.node_manager.load_nodes()
        payload = self._encode(
            {"type": "records_update", "best_time": best_time, "best_score": best_score}
        )
        for node in nodes:
            if node == self.sock.getsockname():
                continue
            try:
                self.sock.sendto(payload, self._normalize_addr(tuple(node)))
            except OSError:
                pass

    @staticmethod
    def request_games(
        node: Tuple[str, int],
        timeout: float = 0.5,
        process_host=None,
        secret: bytes | None = None,
    ) -> List[Tuple[str, int]]:
        """Ask a router node for known game hosts."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        enc = NetworkManager(secret=secret, client_id="helper")
        msg = enc._encode({"type": "find"})
        sock.sendto(msg, node)
        games: List[Tuple[str, int]] = []
        start = time.monotonic()
        while True:
            if process_host is not None:
                process_host()
            try:
                packet, _ = sock.recvfrom(4096)
            except socket.timeout:
                break
            data = enc._decode(packet)
            if data is None:
                continue
            if data.get("type") == "games":
                for host, port in data.get("games", []):
                    games.append((host, int(port)))
            if time.monotonic() - start > timeout:
                break
        sock.close()
        return games

    @staticmethod
    def request_clients(
        node: Tuple[str, int],
        timeout: float = 0.5,
        process_host=None,
        secret: bytes | None = None,
    ) -> List[Tuple[str, int]]:
        """Ask a router node for known live clients."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        enc = NetworkManager(secret=secret, client_id="helper")
        msg = enc._encode({"type": "list_clients"})
        sock.sendto(msg, node)
        clients: List[Tuple[str, int]] = []
        start = time.monotonic()
        while True:
            if process_host is not None:
                process_host()
            try:
                packet, _ = sock.recvfrom(4096)
            except socket.timeout:
                break
            data = enc._decode(packet)
            if data is None:
                continue
            if data.get("type") == "clients":
                for host, port in data.get("clients", []):
                    clients.append((host, int(port)))
            if time.monotonic() - start > timeout:
                break
        sock.close()
        return clients

    @staticmethod
    def request_nodes(
        node: Tuple[str, int],
        timeout: float = 0.5,
        process_host=None,
        secret: bytes | None = None,
    ) -> List[Tuple[str, int]]:
        """Request a router's known node list."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        enc = NetworkManager(secret=secret, client_id="helper")
        msg = enc._encode({"type": "get_nodes"})
        sock.sendto(msg, node)
        nodes: List[Tuple[str, int]] = []
        start = time.monotonic()
        while True:
            if process_host is not None:
                process_host()
            try:
                packet, _ = sock.recvfrom(4096)
            except socket.timeout:
                break
            data = enc._decode(packet)
            if data is None:
                continue
            if data.get("type") == "nodes":
                for host, port in data.get("nodes", []):
                    nodes.append((host, int(port)))
            if time.monotonic() - start > timeout:
                break
        sock.close()
        return nodes

    @staticmethod
    def sync_time(
        node: Tuple[str, int],
        timeout: float = 0.5,
        process_host=None,
        secret: bytes | None = None,
    ) -> float | None:
        """Return time offset in seconds between ``node`` and local machine."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        enc = NetworkManager(secret=secret, client_id="helper")
        msg = enc._encode({"type": "time_request", "time": time.time()})
        sock.sendto(msg, node)
        offset = None
        start = time.monotonic()
        while True:
            if process_host is not None:
                process_host()
            try:
                packet, _ = sock.recvfrom(4096)
            except socket.timeout:
                break
            data = enc._decode(packet)
            if data and data.get("type") == "time_response":
                offset = data.get("time", 0.0) - time.time()
                break
            if time.monotonic() - start > timeout:
                break
        sock.close()
        return offset

    def send_state(self, data: dict[str, Any]) -> None:
        """Send a state update using delta compression."""
        delta = data if "seq" in data else self._sync.encode(data)
        delta["type"] = "state"
        payload = self._encode(delta)
        if self.host:
            for client in list(self.clients):
                try:
                    self.sock.sendto(payload, client)
                except OSError:
                    pass
        else:
            self.sock.sendto(payload, self.address)
            for peer in list(self.peers):
                try:
                    self.sock.sendto(payload, peer)
                except OSError:
                    self.peers.discard(peer)

    def send_reliable(
        self,
        data: dict[str, Any],
        addr: Tuple[str, int] | None = None,
        max_retries: int = 5,
        importance: int = 1,
    ) -> None:
        """Send a packet that will be resent until acknowledged.

        ``importance`` controls how quickly resends occur and how many
        attempts are made. Higher values mean more frequent retries.
        """
        self._reliable_seq += 1
        seq = self._reliable_seq
        packet = data.copy()
        packet["reliable"] = True
        packet["seq"] = seq
        payload = self._encode(packet)
        if addr is None:
            dests = list(self.clients) if self.host else [self.address]
        else:
            dests = [addr]
        now = time.monotonic()
        for dest in dests:
            try:
                self.sock.sendto(payload, dest)
                self._pending_acks[(dest, seq)] = (
                    payload,
                    now,
                    max_retries * importance,
                    importance,
                )
            except OSError:
                pass

    def send_chat(
        self,
        user: str,
        msg: str,
        addr: Tuple[str, int] | None = None,
        reliable: bool = False,
    ) -> None:
        """Send a chat message to another player or broadcast to all."""
        packet = {"type": "chat", "user": user, "msg": msg}
        if reliable:
            self.send_reliable(packet, addr)
            return
        payload = self._encode(packet)
        if addr is None:
            dests = list(self.clients) if self.host else [self.address]
        else:
            dests = [addr]
        for dest in dests:
            try:
                self.sock.sendto(payload, dest)
            except OSError:
                pass

    def send_match_join(
        self,
        size: int = 2,
        shard: str | None = None,
        addr: Tuple[str, int] | None = None,
    ) -> None:
        packet = {"type": "match_join", "size": int(size)}
        if shard is not None:
            packet["shard"] = shard
        self.send_reliable(packet, addr)

    def send_match_leave(
        self,
        size: int = 2,
        shard: str | None = None,
        addr: Tuple[str, int] | None = None,
    ) -> None:
        packet = {"type": "match_leave", "size": int(size)}
        if shard is not None:
            packet["shard"] = shard
        self.send_reliable(packet, addr)

    def send_match_accept(
        self,
        match_id: str,
        shard: str | None = None,
        addr: Tuple[str, int] | None = None,
    ) -> None:
        packet = {"type": "match_accept", "match_id": match_id}
        if shard is not None:
            packet["shard"] = shard
        self.send_reliable(packet, addr)

    def send_match_decline(
        self,
        match_id: str,
        shard: str | None = None,
        addr: Tuple[str, int] | None = None,
    ) -> None:
        packet = {"type": "match_decline", "match_id": match_id}
        if shard is not None:
            packet["shard"] = shard
        self.send_reliable(packet, addr)
    def process_reliable(self) -> None:
        """Resend any unacknowledged reliable packets."""
        now = time.monotonic()
        for key, (payload, sent, retries, importance) in list(
            self._pending_acks.items()
        ):
            if now - sent < self.ack_timeout / importance:
                continue
            addr, seq = key
            if retries <= 0:
                del self._pending_acks[key]
                continue
            try:
                self.sock.sendto(payload, addr)
                self._pending_acks[key] = (
                    payload,
                    now,
                    retries - 1,
                    importance,
                )
            except OSError:
                del self._pending_acks[key]

    def poll(self) -> List[Tuple[Tuple[str, int], dict[str, Any]]]:
        messages = []
        while True:
            try:
                packet, addr = self.sock.recvfrom(4096)
            except BlockingIOError:
                break
            except ConnectionResetError:
                # Windows UDP sockets can raise when remote endpoints close.
                continue
            except OSError:
                continue
            now = time.monotonic()
            count, start = self._msg_counts.get(addr, (0, now))
            if now - start > 1:
                count, start = 0, now
            count += 1
            self._msg_counts[addr] = (count, start)
            if count > self.rate_limit:
                continue
            data = self._decode(packet)
            if data is None:
                continue
            msg_type = data.get("type")
            token = data.get("token")
            secure_types = {
                "state",
                "chat",
                "mmo_state",
                "mmo_join",
                "mmo_leave",
                "mmo_snapshot",
                "mmo_snapshot_request",
                "mmo_world_request",
                "mmo_world_snapshot",
                "mmo_world_delta",
                "match_join",
                "match_leave",
                "match_found",
                "match_accept",
                "match_decline",
                "match_ready",
                "match_cancel",
                "mmo_shard_announce",
            }
            if self.host:
                if (
                    msg_type in secure_types
                    and token is not None
                    and token != self.session_token
                ):
                    continue
            else:
                if self.session_token is None and token is not None:
                    self.session_token = token
                elif msg_type in secure_types and token != self.session_token:
                    continue
            sender = data.get("id")
            if sender is None:
                continue
            known = self.addr_to_id.get(addr)
            if known and known != sender:
                continue
            if self.ban_manager.is_banned(sender):
                continue
            other = self.id_to_addr.get(sender)
            if other and other != addr:
                continue
            self.addr_to_id[addr] = sender
            self.id_to_addr[sender] = addr
            if msg_type == "ack":
                self._pending_acks.pop((addr, data.get("seq")), None)
                continue
            if self.host:
                self.clients.add(addr)
            if data.get("reliable") and "seq" in data:
                ack = self._encode({"type": "ack", "seq": data["seq"]})
                self.sock.sendto(ack, addr)
            if msg_type == "announce":
                self.node_manager.add_node(addr)
                if self.host:
                    self.clients.add(addr)
                    # share our known games, clients and nodes with peers
                    self.broadcast_games()
                    self.broadcast_clients()
                    self.broadcast_relays()
                    self.broadcast_nodes()
                continue
            if msg_type == "register" and self.host:
                # save address of a game host for DNS-like routing
                self.games.add(addr)
                # notify peers about the updated list
                self.broadcast_games()
                continue
            if msg_type == "client_join" and self.host:
                self.live_clients.add(addr)
                peers = [c for c in self.live_clients if c != addr]
                resp = self._encode({"type": "clients", "clients": peers})
                try:
                    self.sock.sendto(resp, addr)
                except OSError:
                    pass
                add_msg = self._encode({"type": "client_add", "peer": addr})
                for peer in peers:
                    try:
                        self.sock.sendto(add_msg, peer)
                    except OSError:
                        pass
                self.broadcast_clients()
                continue
            if msg_type == "client_leave" and self.host:
                if addr in self.live_clients:
                    self.live_clients.discard(addr)
                    rm_msg = self._encode({"type": "client_remove", "peer": addr})
                    for peer in list(self.live_clients):
                        try:
                            self.sock.sendto(rm_msg, peer)
                        except OSError:
                            pass
                    self.broadcast_clients()
                continue
            if msg_type == "relay_offer" and self.host:
                self.relays.add(addr)
                self.broadcast_relays()
                continue
            if msg_type == "match_join" and self.host:
                shard = str(data.get("shard", "public"))
                size = int(data.get("size", 2))
                key = (shard, size)
                queue = self.matchmaking_queues.setdefault(key, MatchmakingManager())
                queue.join(sender)
                match = queue.match(size)
                if match:
                    match_id = uuid.uuid4().hex
                    self.matchmaking_pending[match_id] = {
                        "players": list(match),
                        "accepts": set(),
                        "size": size,
                        "shard": shard,
                        "created_at": time.monotonic(),
                    }
                    packet = {
                        "type": "match_found",
                        "match_id": match_id,
                        "players": list(match),
                        "size": size,
                        "shard": shard,
                    }
                    for player_id in match:
                        dest = self.id_to_addr.get(player_id)
                        if dest is None:
                            continue
                        self.send_reliable(packet, addr=dest, importance=2)
                continue
            if msg_type == "match_leave" and self.host:
                shard = str(data.get("shard", "public"))
                size = int(data.get("size", 2))
                key = (shard, size)
                queue = self.matchmaking_queues.setdefault(key, MatchmakingManager())
                queue.leave(sender)
                for match_id, pending in list(self.matchmaking_pending.items()):
                    players = pending.get("players", [])
                    if sender not in players:
                        continue
                    shard = str(pending.get("shard", "public"))
                    size = int(pending.get("size", 2))
                    queue = self.matchmaking_queues.setdefault(
                        (shard, size), MatchmakingManager()
                    )
                    for player_id in players:
                        if player_id == sender:
                            continue
                        queue.join(player_id)
                        dest = self.id_to_addr.get(player_id)
                        if dest:
                            self.send_reliable(
                                {
                                    "type": "match_cancel",
                                    "match_id": match_id,
                                    "shard": shard,
                                },
                                addr=dest,
                                importance=2,
                            )
                    self.matchmaking_pending.pop(match_id, None)
                continue
            if msg_type == "match_accept" and self.host:
                match_id = str(data.get("match_id", ""))
                pending = self.matchmaking_pending.get(match_id)
                if not pending:
                    continue
                players = pending.get("players", [])
                if sender not in players:
                    continue
                pending["accepts"].add(sender)
                if len(pending["accepts"]) >= len(players):
                    packet = {
                        "type": "match_ready",
                        "match_id": match_id,
                        "players": list(players),
                        "size": int(pending.get("size", 2)),
                        "shard": str(pending.get("shard", "public")),
                    }
                    for player_id in players:
                        dest = self.id_to_addr.get(player_id)
                        if dest:
                            self.send_reliable(packet, addr=dest, importance=2)
                    self.matchmaking_pending.pop(match_id, None)
                continue
            if msg_type == "match_decline" and self.host:
                match_id = str(data.get("match_id", ""))
                pending = self.matchmaking_pending.get(match_id)
                if not pending:
                    continue
                players = pending.get("players", [])
                shard = str(pending.get("shard", "public"))
                size = int(pending.get("size", 2))
                queue = self.matchmaking_queues.setdefault(
                    (shard, size), MatchmakingManager()
                )
                for player_id in players:
                    if player_id == sender:
                        continue
                    queue.join(player_id)
                    dest = self.id_to_addr.get(player_id)
                    if dest:
                        self.send_reliable(
                            {
                                "type": "match_cancel",
                                "match_id": match_id,
                                "shard": shard,
                            },
                            addr=dest,
                            importance=2,
                        )
                self.matchmaking_pending.pop(match_id, None)
                continue
            if msg_type == "find" and self.host:
                resp = self._encode({"type": "games", "games": list(self.games)})
                self.sock.sendto(resp, addr)
                continue
            if msg_type == "games_update" and self.host:
                for host_port in data.get("games", []):
                    self.games.add(tuple(host_port))
                continue
            if msg_type == "nodes_update":
                for host_port in data.get("nodes", []):
                    self.node_manager.add_node(tuple(host_port))
                continue
            if msg_type == "clients_update" and self.host:
                for host_port in data.get("clients", []):
                    self.live_clients.add(tuple(host_port))
                continue
            if msg_type == "relays_update" and self.host:
                for host_port in data.get("relays", []):
                    self.relays.add(tuple(host_port))
                continue
            if msg_type == "records_update":
                merge_records(
                    {
                        "best_time": data.get("best_time"),
                        "best_score": data.get("best_score"),
                    }
                )
                continue
            if msg_type == "block_update":
                chain = load_chain()
                chain.append(data.get("block"))
                if verify_chain(chain):
                    save_chain(chain)
                continue
            if msg_type == "chain_request" and self.host:
                self.send_chain(addr)
                continue
            if msg_type == "chain_response":
                merge_chain(data.get("chain", []))
                continue
            if msg_type == "list_clients" and self.host:
                resp = self._encode({"type": "clients", "clients": list(self.live_clients)})
                self.sock.sendto(resp, addr)
                continue
            if msg_type == "get_nodes" and self.host:
                resp = self._encode({"type": "nodes", "nodes": self.node_manager.load_nodes()})
                self.sock.sendto(resp, addr)
                continue
            if msg_type == "get_relays" and self.host:
                resp = self._encode({"type": "relays", "relays": list(self.relays)})
                self.sock.sendto(resp, addr)
                continue
            if msg_type == "relay_data" and self.relay_mode:
                dest = tuple(data.get("dest"))
                payload = bytes.fromhex(data.get("payload", ""))
                self.sock.sendto(payload, dest)
                continue
            if msg_type == "ping":
                # reply with a pong for latency checks
                resp = self._encode({"type": "pong"})
                self.sock.sendto(resp, addr)
                continue
            if msg_type == "time_request" and self.host:
                resp = self._encode({"type": "time_response", "time": time.time()})
                self.sock.sendto(resp, addr)
                continue
            if msg_type == "time_response" and not self.host:
                remote = data.get("time")
                if isinstance(remote, (int, float)):
                    self.sync.update(remote, time.time())
                continue
            if msg_type == "clients" and not self.host:
                self.peers = {tuple(p) for p in data.get("clients", [])}
                continue
            if msg_type == "client_add" and not self.host:
                peer = data.get("peer")
                if isinstance(peer, list) and len(peer) == 2:
                    self.peers.add((peer[0], int(peer[1])))
                continue
            if msg_type == "client_remove" and not self.host:
                peer = data.get("peer")
                if isinstance(peer, list) and len(peer) == 2:
                    self.peers.discard((peer[0], int(peer[1])))
                continue
            if msg_type == "peer_list" and not self.host:
                self.peers = {tuple(p) for p in data.get("peers", [])}
                continue
            if msg_type == "peer_add" and not self.host:
                peer = data.get("peer")
                if isinstance(peer, list) and len(peer) == 2:
                    self.peers.add((peer[0], int(peer[1])))
                continue
            if self.host:
                if msg_type == "discover":
                    # respond to discovery with address for client to connect
                    resp = self._encode({"type": "host"})
                    self.sock.sendto(resp, addr)
                    continue
                new_client = addr not in self.clients
                self.clients.add(addr)
                if new_client:
                    peers = [c for c in self.clients if c != addr]
                    payload = self._encode({"type": "peer_list", "peers": peers})
                    self.sock.sendto(payload, addr)
                    add_msg = self._encode({"type": "peer_add", "peer": addr})
                    for peer in peers:
                        try:
                            self.sock.sendto(add_msg, peer)
                        except OSError:
                            pass
            messages.append((addr, data))
        return messages

    @staticmethod
    def discover(
        timeout: float = 0.5,
        port: int = 50007,
        broadcast_address: str = "255.255.255.255",
        process_host=None,
        secret: bytes | None = None,
    ) -> List[Tuple[str, int]]:
        """Broadcast a discovery packet and return responding server addresses."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("", 0))
        sock.settimeout(timeout)
        enc = NetworkManager(secret=secret, client_id="helper")
        msg = enc._encode({"type": "discover"})
        sock.sendto(msg, (broadcast_address, port))
        hosts: List[Tuple[str, int]] = []
        start = time.monotonic()
        while True:
            if process_host is not None:
                process_host()
            try:
                packet, addr = sock.recvfrom(4096)
            except socket.timeout:
                break
            data = enc._decode(packet)
            if data is None:
                continue
            if data.get("type") == "host":
                hosts.append(addr)
            if time.monotonic() - start > timeout:
                break
        sock.close()
        return hosts

    @staticmethod
    def ping_node(
        addr: Tuple[str, int],
        timeout: float = 0.2,
        process_host=None,
        secret: bytes | None = None,
    ) -> float | None:
        """Return round-trip latency to addr in seconds or None if unreachable."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        enc = NetworkManager(secret=secret, client_id="helper")
        msg = enc._encode({"type": "ping"})
        start = time.monotonic()
        try:
            sock.sendto(msg, addr)
            while True:
                if process_host is not None:
                    process_host()
                packet, _ = sock.recvfrom(4096)
                break
        except (socket.timeout, OSError):
            sock.close()
            return None
        sock.close()
        try:
            data = enc._decode(packet)
        except json.JSONDecodeError:
            return None
        if data.get("type") != "pong":
            return None
        return time.monotonic() - start

    @staticmethod
    def select_best_node(
        nodes: List[Tuple[str, int]],
        ping_func=None,
        timeout: float = 0.2,
    ) -> Tuple[str, int] | None:
        """Return the node with the lowest latency from a list of addresses."""
        if ping_func is None:
            ping_func = lambda n: NetworkManager.ping_node(n, timeout)
        best = None
        best_latency = float("inf")
        for node in nodes:
            latency = ping_func(node)
            if latency is not None and latency < best_latency:
                best = node
                best_latency = latency
        return best
