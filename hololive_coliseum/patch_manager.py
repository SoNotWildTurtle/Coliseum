"""Patch notes and version update helpers."""

class PatchManager:
    """Store the current client version and hotfix level."""

    def __init__(self, version: str = "0.0.1") -> None:
        self.version = version

    def update_version(self, version: str) -> None:
        self.version = version
