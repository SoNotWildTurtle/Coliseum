"""Craft weapons and armor from trade skill blueprints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Sequence

from .item_manager import Armor, Bow, ItemManager, Wand, Weapon
from .trade_skill_generator import TradeSkillGenerator


@dataclass(frozen=True)
class CraftedItem:
    """Record linking a crafted item to the trade skill that produced it."""

    name: str
    trade_skill: str
    product_type: str
    stats: dict[str, int]
    recipe_materials: tuple[str, ...]
    quality: str

    def as_dict(self) -> dict[str, object]:
        """Return the crafted item record as a serialisable mapping."""

        return {
            "name": self.name,
            "trade_skill": self.trade_skill,
            "product_type": self.product_type,
            "stats": dict(self.stats),
            "recipe_materials": self.recipe_materials,
            "quality": self.quality,
        }


class TradeSkillCraftingManager:
    """Produce gear blueprints based on available trade skills."""

    def __init__(
        self,
        item_manager: ItemManager | None = None,
        generator: TradeSkillGenerator | None = None,
    ) -> None:
        self.item_manager = item_manager or ItemManager()
        self.generator = generator or TradeSkillGenerator()

    def craft_items(self, trade_skills: Sequence[str]) -> tuple[CraftedItem, ...]:
        """Craft gear for ``trade_skills`` and return the resulting records."""

        crafted: list[CraftedItem] = []
        if not trade_skills:
            trade_skills = self.generator.list_core_skills()
        gathering_modifiers = self.generator.collect_gathering_bonuses(trade_skills)
        for index, (skill, recipe) in enumerate(
            self.generator.iter_recipe_sources(trade_skills)
        ):
            product_type = str(recipe.get("product", "weapon")).lower()
            item_name = str(recipe.get("name", f"{skill} Prototype"))
            level_band = self.generator.level_band(skill)
            stats = self._derive_stats(skill, product_type, index, level_band)
            stats = self._apply_gathering_modifiers(
                stats, product_type, gathering_modifiers
            )
            materials = tuple(str(m) for m in recipe.get("materials", ()))
            item, product_type = self._create_item(item_name, product_type, stats)
            stored_name = item.name if item is not None else item_name
            if item is not None and self.item_manager.get(item.name) is None:
                self.item_manager.add_item(item)
            crafted.append(
                CraftedItem(
                    name=stored_name,
                    trade_skill=skill,
                    product_type=product_type,
                    stats=dict(stats),
                    recipe_materials=materials,
                    quality=self._quality_from_skill(skill, index),
                )
            )
        return tuple(crafted)

    def craft_summary(self, trade_skills: Sequence[str]) -> list[dict[str, object]]:
        """Return :class:`CraftedItem` records as dictionaries for convenience."""

        return [record.as_dict() for record in self.craft_items(trade_skills)]

    @staticmethod
    def _derive_stats(
        skill: str,
        product_type: str,
        index: int,
        level_band: tuple[int, int],
    ) -> dict[str, int]:
        """Return deterministic stats for ``skill`` and ``product_type``."""

        minimum, maximum = level_band
        midpoint = (minimum + maximum) // 2
        spread = max(1, maximum - minimum)
        base = max(6, min(24, 6 + midpoint // 3 + (len(skill) + index * 2) % spread))
        if product_type == "armor":
            return {
                "attack": base // 4,
                "defense": base + 8,
                "health": 85 + base * 6,
            }
        if product_type == "bow":
            return {
                "attack": base + 10,
                "defense": base // 3 + 2,
                "health": 58 + base * 3,
            }
        if product_type == "wand":
            return {
                "attack": base + 7,
                "defense": base // 2 + 5,
                "health": 62 + base * 4,
            }
        if product_type == "material":
            return {
                "yield": 12 + base,
                "purity": min(10, 3 + base // 4),
            }
        return {
            "attack": base + 9,
            "defense": base // 2 + 4,
            "health": 64 + base * 4,
        }

    @staticmethod
    def _apply_gathering_modifiers(
        stats: dict[str, int],
        product_type: str,
        modifiers: dict[str, dict[str, int]],
    ) -> dict[str, int]:
        """Return ``stats`` with gathering bonuses applied."""

        if product_type not in modifiers:
            return stats
        adjusted = dict(stats)
        for stat, bonus in modifiers[product_type].items():
            adjusted[stat] = adjusted.get(stat, 0) + bonus
        return adjusted

    @staticmethod
    def _create_item(
        item_name: str, product_type: str, stats: dict[str, int]
    ) -> tuple[Optional[Weapon | Armor | Bow | Wand], str]:
        """Instantiate an item for ``product_type`` and return it with the type label."""

        builders = {
            "armor": Armor,
            "weapon": Weapon,
            "bow": Bow,
            "wand": Wand,
        }
        builder = builders.get(product_type)
        if builder is None:
            return None, product_type
        item = builder(item_name, stats)
        return item, product_type

    @staticmethod
    def _quality_from_skill(skill: str, index: int) -> str:
        """Return a flavour quality descriptor based on ``skill``."""

        tiers = ("apprentice", "artisan", "masterwork", "legendary")
        anchor = sum(ord(char) for char in skill) + index * 7
        return tiers[anchor % len(tiers)]

    def iter_crafted_items(
        self, trade_skills: Sequence[str]
    ) -> Iterable[CraftedItem]:
        """Yield crafted item records without storing them in a list."""

        for record in self.craft_items(trade_skills):
            yield record
