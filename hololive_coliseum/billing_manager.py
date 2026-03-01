"""Billing and subscription helpers."""

class BillingManager:
    """Track player purchases and subscriptions."""

    def __init__(self) -> None:
        self.records: dict[str, list[str]] = {}

    def add_purchase(self, user_id: str, item: str) -> None:
        self.records.setdefault(user_id, []).append(item)

    def get_purchases(self, user_id: str) -> list[str]:
        return self.records.get(user_id, [])
