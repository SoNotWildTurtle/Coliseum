"""Tests for node registry."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.node_registry import load_nodes, save_nodes, add_node, prune_nodes


def test_add_node_dedup(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.node_registry.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.node_registry.NODES_FILE', tmp_path / 'nodes.json')
    monkeypatch.setattr('hololive_coliseum.node_registry.DEFAULT_NODES', [])
    add_node(('1.2.3.4', 1234))
    assert load_nodes() == [('1.2.3.4', 1234)]
    add_node(('1.2.3.4', 1234))
    assert load_nodes() == [('1.2.3.4', 1234)]


def test_prune_nodes(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.node_registry.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.node_registry.NODES_FILE', tmp_path / 'nodes.json')
    monkeypatch.setattr('hololive_coliseum.node_registry.DEFAULT_NODES', [])
    save_nodes([('1.1.1.1', 1), ('2.2.2.2', 2)])

    def fake_ping(addr):
        return 0.1 if addr[0] == '1.1.1.1' else None

    prune_nodes(fake_ping)
    assert load_nodes() == [('1.1.1.1', 1)]


def test_load_nodes_falls_back_to_defaults(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.node_registry.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.node_registry.NODES_FILE', tmp_path / 'nodes.json')
    monkeypatch.setattr('hololive_coliseum.node_registry.DEFAULT_NODES', [('4.4.4.4', 4444)])
    # No nodes.json file yet
    assert load_nodes() == [('4.4.4.4', 4444)]
