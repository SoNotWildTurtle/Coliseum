"""Track achievements and unlock criteria."""

class AchievementManager:
    """Record unlocked achievements."""

    def __init__(self) -> None:
        self.unlocked: set[str] = set()

    def unlock(self, name: str) -> None:
        self.unlocked.add(name)

    def is_unlocked(self, name: str) -> bool:
        return name in self.unlocked

    def to_dict(self) -> dict:
        return {"achievements": list(self.unlocked)}

    def load_from_dict(self, data: dict) -> None:
        self.unlocked = set(data.get("achievements", []))
