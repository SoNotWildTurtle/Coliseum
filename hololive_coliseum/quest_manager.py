"""Quest definitions and completion tracking."""

class QuestManager:
    """Track active and completed quests."""

    def __init__(self) -> None:
        self.active: dict[str, dict[str, int]] = {}
        self.completed: set[str] = set()

    def add(self, quest_id: str, objective: str) -> None:
        """Add a new quest with its objective."""
        self.active[quest_id] = {"objective": objective, "progress": 0}

    def update_progress(self, quest_id: str, amount: int = 1) -> None:
        """Increase progress for a quest."""
        if quest_id in self.active:
            self.active[quest_id]["progress"] += amount

    def complete(self, quest_id: str) -> None:
        """Mark a quest as completed."""
        if quest_id in self.active:
            self.active.pop(quest_id)
            self.completed.add(quest_id)

    def is_completed(self, quest_id: str) -> bool:
        return quest_id in self.completed

    def get_progress(self, quest_id: str) -> int:
        return self.active.get(quest_id, {}).get("progress", 0)

    def to_dict(self) -> dict:
        return {
            "active": self.active,
            "completed": list(self.completed),
        }

    def load_from_dict(self, data: dict) -> None:
        self.active = {k: dict(v) for k, v in data.get("active", {}).items()}
        self.completed = set(data.get("completed", []))
