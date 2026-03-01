"""Inventory storage, capacity, and persistence."""

class InventoryManager:
    """Track items collected during play.

    An optional ``capacity`` limits how many total items may be stored. This
    mirrors inventory restrictions common in MMOs while keeping earlier levels
    lightweight.
    """

    def __init__(self, capacity: int | None = None) -> None:
        self.items: dict[str, int] = {}
        self.capacity = capacity

    def total_items(self) -> int:
        """Return the total count of items stored."""

        return sum(self.items.values())

    def add(self, item: str, count: int = 1) -> bool:
        """Add an item if capacity allows.

        Returns ``True`` when the items were added, or ``False`` if the
        inventory is full.
        """

        if self.capacity is not None and self.total_items() + count > self.capacity:
            return False
        self.items[item] = self.items.get(item, 0) + count
        return True

    def remove(self, item: str, count: int = 1) -> bool:
        current = self.items.get(item, 0)
        if current < count:
            return False
        new = current - count
        if new:
            self.items[item] = new
        else:
            self.items.pop(item, None)
        return True

    def has(self, item: str) -> bool:
        return item in self.items

    def count(self, item: str) -> int:
        return self.items.get(item, 0)

    def to_dict(self) -> dict[str, int]:
        return dict(self.items)

    def load_from_dict(self, data: dict[str, int]) -> None:
        self.items = dict(data)

