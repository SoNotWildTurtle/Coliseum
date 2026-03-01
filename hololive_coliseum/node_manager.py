"""Network node lifecycle and tracking."""

from __future__ import annotations
from typing import List, Tuple, Callable

from .node_registry import (
    load_nodes as _load_nodes,
    save_nodes as _save_nodes,
    add_node as _add_node,
    prune_nodes as _prune_nodes,
)


class NodeManager:
    """Wrapper class managing known network nodes."""

    def load_nodes(self) -> List[Tuple[str, int]]:
        """Return the list of known nodes."""
        return _load_nodes()

    def save_nodes(self, nodes: List[Tuple[str, int]]) -> None:
        """Persist the node list."""
        _save_nodes(nodes)

    def add_node(self, node: Tuple[str, int]) -> None:
        """Add a node if not already present."""
        _add_node(node)

    def prune_nodes(self, ping_func: Callable[[Tuple[str, int]], float | None], timeout: float = 0.2) -> None:
        """Remove nodes that do not respond to the ping_func."""
        _prune_nodes(ping_func, timeout)
