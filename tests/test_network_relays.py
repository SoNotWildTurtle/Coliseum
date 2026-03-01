"""Tests for relay discovery and relay offers."""

import time

from hololive_coliseum.network import NetworkManager


def test_relay_offer_updates_router_relays():
    router = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="router")
    relay = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="relay")
    router_addr = router.sock.getsockname()
    relay_addr = relay.sock.getsockname()

    relay.offer_relay([router_addr])
    time.sleep(0.01)
    router.poll()

    assert relay_addr in router.relays

    relay.sock.close()
    router.sock.close()


def test_request_relays_returns_known_relays():
    router = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="router")
    relay = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="relay")
    relay_addr = relay.sock.getsockname()
    router.relays.add(relay_addr)

    relays = NetworkManager.request_relays(
        router.sock.getsockname(),
        timeout=0.2,
        process_host=router.poll,
    )

    assert relay_addr in relays

    relay.sock.close()
    router.sock.close()
