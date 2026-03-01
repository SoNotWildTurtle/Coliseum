"""Interactable station that crafts items using a recipe."""

from __future__ import annotations


class CraftingStation:
    """Craft items when the player interacts with the station."""

    def __init__(self, crafting_manager, recipe: str) -> None:
        self.crafting_manager = crafting_manager
        self.recipe = recipe

    def interact(self, inventory) -> str | None:
        """Craft the configured recipe using ``inventory``.

        Returns the crafted item or ``None`` if the recipe requirements are not
        met.
        """
        return self.crafting_manager.craft(self.recipe, inventory)
