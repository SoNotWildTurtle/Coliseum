"""In-game ad placement and rotation helpers."""

class AdManager:
    """Manage in-game advertisements and promotions."""

    def __init__(self) -> None:
        self.ads: list[str] = []

    def add_ad(self, text: str) -> None:
        self.ads.append(text)

    def current_ads(self) -> list[str]:
        return self.ads
