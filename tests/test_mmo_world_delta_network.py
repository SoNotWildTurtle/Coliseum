"""Integration test for MMO world delta messages over the network."""

import time

from hololive_coliseum.mmo_world_state_manager import MMOWorldStateManager
from hololive_coliseum.network import NetworkManager


def test_mmo_world_delta_over_network():
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host")
    addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=addr, client_id="client")

    client.register_client([addr])
    time.sleep(0.01)
    host.poll()
    client.poll()

    host_state = MMOWorldStateManager()
    client_state = MMOWorldStateManager()

    snapshot = MMOWorldStateManager.build_snapshot(
        regions=[{"name": "r1", "position": [0.0, 0.0]}],
        influence={"r1": 12},
        world_events=[{"id": "event:r1", "updated_at": 5}],
        outposts=[],
        operations=[],
        trade_routes=[],
        directives=[],
        bounties=[],
        tombstones=[],
        updated_at=10,
        shard="public",
    )
    delta = host_state.update(snapshot)
    host.send_reliable({"type": "mmo_world_delta", "shard": "public", "delta": delta})

    messages = []
    for _ in range(4):
        time.sleep(0.01)
        messages.extend(client.poll())

    payload = None
    for _addr, msg in messages:
        if msg.get("type") == "mmo_world_delta":
            payload = msg
            break

    assert payload is not None
    state = client_state.apply_delta(payload["delta"])
    assert state["regions"][0]["name"] == "r1"
    assert state["influence"]["r1"] == 12

    client.poll()
    host.poll()
    host.sock.close()
    client.sock.close()
