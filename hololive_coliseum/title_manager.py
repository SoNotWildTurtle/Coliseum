"""Title unlocks and display helpers."""

class TitleManager:
    """Manage unlockable titles and the active one."""
    def __init__(self):
        self.unlocked = set()
        self.active = None

    def unlock(self, title: str) -> None:
        self.unlocked.add(title)

    def set_active(self, title: str) -> bool:
        if title in self.unlocked:
            self.active = title
            return True
        return False

    def get_active(self):
        return self.active
