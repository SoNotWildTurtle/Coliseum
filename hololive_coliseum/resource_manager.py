"""Resource loading and caching utilities."""

class ResourceManager:
    """Cache loaded assets so files are only read once."""

    def __init__(self) -> None:
        self.cache: dict[str, object] = {}

    def load(self, path: str, loader) -> object:
        if path not in self.cache:
            self.cache[path] = loader(path)
        return self.cache[path]

    def unload(self, path: str) -> None:
        self.cache.pop(path, None)
