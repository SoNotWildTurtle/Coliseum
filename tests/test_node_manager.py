"""Tests for node manager."""

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.node_manager import NodeManager
import hololive_coliseum.node_registry as nr


def test_add_node_dedup(tmp_path, monkeypatch):
    monkeypatch.setattr(nr, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(nr, 'NODES_FILE', tmp_path / 'nodes.json')
    monkeypatch.setattr(nr, 'DEFAULT_NODES', [])
    manager = NodeManager()
    manager.add_node(('1.2.3.4', 1234))
    assert manager.load_nodes() == [('1.2.3.4', 1234)]
    manager.add_node(('1.2.3.4', 1234))
    assert manager.load_nodes() == [('1.2.3.4', 1234)]


def test_prune_nodes(tmp_path, monkeypatch):
    monkeypatch.setattr(nr, 'SAVE_DIR', tmp_path)
    monkeypatch.setattr(nr, 'NODES_FILE', tmp_path / 'nodes.json')
    monkeypatch.setattr(nr, 'DEFAULT_NODES', [])
    manager = NodeManager()
    manager.save_nodes([('1.1.1.1', 1), ('2.2.2.2', 2)])

    def fake_ping(addr):
        return 0.1 if addr[0] == '1.1.1.1' else None

    manager.prune_nodes(fake_ping)
    assert manager.load_nodes() == [('1.1.1.1', 1)]
