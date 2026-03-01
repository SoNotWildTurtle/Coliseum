"""Instance creation and routing helpers."""

class InstanceManager:
    """Create and destroy simple gameplay instances."""

    def __init__(self) -> None:
        self.instances: dict[int, list] = {}
        self._next_id = 1

    def create(self, players=None) -> int:
        iid = self._next_id
        self._next_id += 1
        self.instances[iid] = players or []
        return iid

    def destroy(self, iid: int) -> None:
        self.instances.pop(iid, None)
