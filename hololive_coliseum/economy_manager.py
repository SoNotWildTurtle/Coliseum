"""Economy balance and pricing helpers."""

class EconomyManager:
    """Keep track of item prices."""

    def __init__(self) -> None:
        self._prices: dict[str, int] = {}

    def set_price(self, item: str, price: int) -> None:
        self._prices[item] = price

    def get_price(self, item: str) -> int:
        return self._prices.get(item, 0)

    def remove_price(self, item: str) -> None:
        self._prices.pop(item, None)
