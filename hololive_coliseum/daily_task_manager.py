"""Daily task scheduling and tracking."""

class DailyTaskManager:
    """Manage daily quests with automatic reset."""

    def __init__(self):
        self.tasks = {}

    def add_task(self, name: str) -> None:
        self.tasks[name] = False

    def complete(self, name: str) -> None:
        if name in self.tasks:
            self.tasks[name] = True

    def reset(self) -> None:
        for k in self.tasks:
            self.tasks[k] = False
