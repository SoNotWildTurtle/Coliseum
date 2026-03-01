"""Load balancing policies and node assignment."""

class LoadBalancerManager:
    """Select the least busy server for new matches."""

    def __init__(self) -> None:
        self.loads: dict[str, int] = {}

    def update_load(self, server: str, load: int) -> None:
        self.loads[server] = load

    def best_server(self) -> str | None:
        if not self.loads:
            return None
        return min(self.loads, key=self.loads.get)
