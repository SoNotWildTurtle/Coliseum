"""Name generation and validation helpers."""

class NameManager:
    """Handle naming conventions and renames."""

    def __init__(self, name: str) -> None:
        self.name = name

    def rename(self, new_name: str) -> None:
        self.name = new_name
