"""Mount acquisition, storage, and movement helpers."""

class MountManager:
    """Store mounts and track which is active for each player."""
    def __init__(self):
        self.mounts = {}
        self.active = {}

    def add_mount(self, player_id: str, mount: str) -> None:
        self.mounts.setdefault(player_id, []).append(mount)

    def set_active(self, player_id: str, mount: str) -> bool:
        if mount in self.mounts.get(player_id, []):
            self.active[player_id] = mount
            return True
        return False

    def get_active(self, player_id: str):
        return self.active.get(player_id)
