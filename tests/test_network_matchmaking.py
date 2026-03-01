"""Tests for network matchmaking."""

import time

from hololive_coliseum.network import NetworkManager


def test_matchmaking_queue_pairs_players():
    host = NetworkManager(host=True, address=("127.0.0.1", 0), client_id="host")
    addr = host.sock.getsockname()
    c1 = NetworkManager(host=False, address=addr, client_id="c1")
    c2 = NetworkManager(host=False, address=addr, client_id="c2")

    c1.register_client([addr])
    c2.register_client([addr])
    time.sleep(0.01)
    host.poll()
    c1.poll()
    c2.poll()

    c1.send_match_join(size=2, shard="public")
    c2.send_match_join(size=2, shard="public")
    time.sleep(0.02)
    host.poll()

    msgs1 = []
    msgs2 = []
    for _ in range(3):
        time.sleep(0.01)
        msgs1.extend(c1.poll())
        msgs2.extend(c2.poll())

    def found(messages):
        for _addr, msg in messages:
            if msg.get("type") == "match_found":
                return msg
        return None

    m1 = found(msgs1)
    m2 = found(msgs2)
    assert m1 and m2
    assert set(m1.get("players", [])) == {"c1", "c2"}
    assert set(m2.get("players", [])) == {"c1", "c2"}
    match_id = m1.get("match_id")
    assert match_id

    c1.send_match_accept(match_id, shard="public")
    c2.send_match_accept(match_id, shard="public")
    time.sleep(0.02)
    host.poll()
    ready1 = []
    ready2 = []
    for _ in range(3):
        time.sleep(0.01)
        ready1.extend(c1.poll())
        ready2.extend(c2.poll())

    def ready(messages):
        for _addr, msg in messages:
            if msg.get("type") == "match_ready":
                return msg
        return None

    assert ready(ready1)
    assert ready(ready2)

    for sock in (host.sock, c1.sock, c2.sock):
        sock.close()
