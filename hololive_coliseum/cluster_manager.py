"""Cluster coordination for distributed play."""

class ClusterManager:
    """Track servers participating in a multi-node cluster."""

    def __init__(self) -> None:
        self.nodes: list[str] = []

    def register(self, address: str) -> None:
        if address not in self.nodes:
            self.nodes.append(address)

    def unregister(self, address: str) -> None:
        if address in self.nodes:
            self.nodes.remove(address)
