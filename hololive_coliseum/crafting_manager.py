"""Crafting recipes and crafting flow management."""

class CraftingManager:
    """Manage crafting recipes and craft items from an inventory."""

    def __init__(self) -> None:
        self._recipes: dict[str, dict[str, int]] = {}
        self._results: dict[str, str] = {}

    def add_recipe(self, name: str, ingredients: dict[str, int], result: str) -> None:
        """Register a recipe by name."""
        self._recipes[name] = dict(ingredients)
        self._results[name] = result

    def craft(self, name: str, inventory) -> str | None:
        """Craft the recipe if all ingredients are present.
        The ``inventory`` object must provide ``count`` and ``remove`` methods
        and ``add`` to receive the crafted item.
        Returns the crafted item or ``None`` if requirements are not met."""
        req = self._recipes.get(name)
        if not req:
            return None
        for item, cnt in req.items():
            if getattr(inventory, "count")(item) < cnt:
                return None
        for item, cnt in req.items():
            getattr(inventory, "remove")(item, cnt)
        result = self._results[name]
        getattr(inventory, "add")(result)
        return result
