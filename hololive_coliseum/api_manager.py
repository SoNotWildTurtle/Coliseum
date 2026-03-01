"""API integration helpers for external services."""

class APIManager:
    """Store webhook endpoints for third-party integrations."""

    def __init__(self) -> None:
        self.endpoints: dict[str, str] = {}

    def add_endpoint(self, name: str, url: str) -> None:
        self.endpoints[name] = url

    def get(self, name: str) -> str | None:
        return self.endpoints.get(name)
