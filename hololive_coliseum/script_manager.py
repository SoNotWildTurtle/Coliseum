"""Scripted event execution helpers."""

class ScriptManager:
    """Load and execute simple scripts for events and modding."""

    def __init__(self) -> None:
        self.scripts: dict[str, str] = {}

    def add_script(self, name: str, code: str) -> None:
        self.scripts[name] = code

    def remove_script(self, name: str) -> None:
        self.scripts.pop(name, None)

    def get_script(self, name: str) -> str | None:
        return self.scripts.get(name)
