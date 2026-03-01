"""Item catalog, lookup, and usage helpers."""

from dataclasses import dataclass


@dataclass
class Item:
    """Base item carrying a name, slot type and stat modifiers."""

    name: str
    slot: str
    stats: dict[str, int]


@dataclass
class Weapon(Item):
    """Weapon automatically assigned to the ``weapon`` slot."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, "weapon", stats)


@dataclass
class Sword(Weapon):
    """Classic melee blade."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, stats)


@dataclass
class Bow(Weapon):
    """Ranged weapon using arrows."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, stats)


@dataclass
class Wand(Weapon):
    """Mystic focus for spellcasters."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, stats)


@dataclass
class Axe(Weapon):
    """Heavy chopping weapon."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, stats)


@dataclass
class Spear(Weapon):
    """Long thrusting weapon."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, stats)


@dataclass
class Helmet(Item):
    """Head gear that equips to the ``head`` slot."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, "head", stats)


@dataclass
class Armor(Item):
    """Body armor that equips to the ``chest`` slot."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, "chest", stats)


@dataclass
class Boots(Item):
    """Footwear for the ``boots`` slot."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, "boots", stats)


@dataclass
class Shield(Item):
    """Offhand equipment stored in the ``offhand`` slot."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, "offhand", stats)


@dataclass
class Tome(Item):
    """Magic book for the ``offhand`` slot."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, "offhand", stats)


@dataclass
class Orb(Item):
    """Mystic orb held in the ``offhand`` slot."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, "offhand", stats)


@dataclass
class Quiver(Item):
    """Arrow container for the ``offhand`` slot."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, "offhand", stats)


@dataclass
class Ring(Item):
    """Accessory occupying the ``ring`` slot."""

    def __init__(self, name: str, stats: dict[str, int]):
        super().__init__(name, "ring", stats)


class ItemManager:
    """Register and look up items by name."""

    def __init__(self) -> None:
        self.items: dict[str, Item] = {}

    def add_item(self, item: Item) -> None:
        """Store ``item`` so it can be equipped later."""
        self.items[item.name] = item

    def get(self, name: str) -> Item | None:
        """Return the item with ``name`` if present."""
        return self.items.get(name)

    def list_items(self) -> list[Item]:
        """Return all registered items."""
        return list(self.items.values())
