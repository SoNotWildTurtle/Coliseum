"""Integration test for MMO world snapshot messages over the network."""

import time

from hololive_coliseum.mmo_world_state_manager import MMOWorldStateManager
from hololive_coliseum.network import NetworkManager


def test_mmo_world_snapshot_over_network():
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host")
    addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=addr, client_id="client")

    client.register_client([addr])
    time.sleep(0.01)
    host.poll()
    client.poll()

    host_state = MMOWorldStateManager()
    snapshot = MMOWorldStateManager.build_snapshot(
        regions=[{"name": "r2", "position": [1.0, 2.0]}],
        influence={"r2": 21},
        world_events=[],
        outposts=[{"region": "r2", "level": 2}],
        operations=[],
        trade_routes=[],
        directives=[],
        bounties=[],
        tombstones=[],
        updated_at=22,
        shard="public",
    )
    host_state.load_snapshot(snapshot, sequence=3)
    payload = {
        "type": "mmo_world_snapshot",
        "shard": "public",
        "seq": host_state.current_sequence(),
        "state": dict(host_state.state),
        "verify": {},
    }
    host.send_reliable(payload)

    messages = []
    for _ in range(4):
        time.sleep(0.01)
        messages.extend(client.poll())

    delivered = None
    for _addr, msg in messages:
        if msg.get("type") == "mmo_world_snapshot":
            delivered = msg
            break

    assert delivered is not None
    client_state = MMOWorldStateManager()
    state = client_state.load_snapshot(
        delivered["state"],
        sequence=delivered.get("seq"),
        verify=None,
    )
    assert state["regions"][0]["name"] == "r2"
    assert state["influence"]["r2"] == 21

    client.poll()
    host.poll()
    host.sock.close()
    client.sock.close()
