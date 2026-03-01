"""Key binding configuration and persistence."""

class KeybindManager:
    """Store and modify input bindings."""

    def __init__(self, defaults: dict[str, int]):
        self.defaults = defaults.copy()
        self.bindings = defaults.copy()

    def get(self, action: str) -> int | None:
        return self.bindings.get(action, self.defaults.get(action))

    def set(self, action: str, key: int) -> None:
        self.bindings[action] = key

    def reset(self) -> None:
        self.bindings = self.defaults.copy()

    def to_dict(self) -> dict[str, int]:
        return dict(self.bindings)

    def load_from_dict(self, data: dict[str, int]) -> None:
        self.bindings = self.defaults.copy()
        for action, key in data.items():
            self.bindings[action] = key

