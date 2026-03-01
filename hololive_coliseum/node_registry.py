"""Registry helpers for network nodes."""

import json
import os
from typing import List, Tuple

# Directory used by save_manager; ensure it exists
SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'SavedGames')
os.makedirs(SAVE_DIR, exist_ok=True)
NODES_FILE = os.path.join(SAVE_DIR, 'nodes.json')

# Built-in nodes that ship with the game for discovery
DEFAULT_NODES: List[Tuple[str, int]] = [("127.0.0.1", 50007)]


def load_nodes() -> List[Tuple[str, int]]:
    """Return a list of known nodes from file plus defaults."""
    nodes: List[Tuple[str, int]] = list(DEFAULT_NODES)
    if os.path.exists(NODES_FILE):
        try:
            with open(NODES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for host, port in data:
                nodes.append((host, int(port)))
        except (json.JSONDecodeError, ValueError, TypeError):
            pass
    # remove duplicates preserving order
    unique: List[Tuple[str, int]] = []
    for node in nodes:
        if node not in unique:
            unique.append(node)
    return unique


def save_nodes(nodes: List[Tuple[str, int]]) -> None:
    """Persist the node list to disk."""
    os.makedirs(os.path.dirname(NODES_FILE), exist_ok=True)
    with open(NODES_FILE, 'w', encoding='utf-8') as f:
        json.dump(nodes, f)


def add_node(node: Tuple[str, int]) -> None:
    """Add a node to the registry if not already present."""
    nodes = load_nodes()
    if node not in nodes:
        nodes.append(node)
        save_nodes(nodes)


def prune_nodes(ping_func, timeout: float = 0.2) -> None:
    """Remove nodes that do not respond to a ping."""
    nodes = load_nodes()
    alive: List[Tuple[str, int]] = []
    for node in nodes:
        if ping_func(node) is not None:
            alive.append(node)
    save_nodes(alive)
