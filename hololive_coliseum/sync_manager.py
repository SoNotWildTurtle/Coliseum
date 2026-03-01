"""Synchronization helpers for multiplayer state."""

class SyncManager:
    """Maintain a time offset for client prediction."""

    def __init__(self) -> None:
        self.offset = 0

    def update(self, remote_time: int, local_time: int) -> None:
        self.offset = remote_time - local_time

    def to_local(self, remote_time: int) -> int:
        return remote_time - self.offset
