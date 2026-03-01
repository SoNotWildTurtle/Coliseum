"""Tests for trade skill crafting manager."""

from hololive_coliseum import (
    CraftedItem,
    ItemManager,
    TradeSkillCraftingManager,
)


def test_trade_skill_crafting_manager_creates_items() -> None:
    item_manager = ItemManager()
    crafting_manager = TradeSkillCraftingManager(item_manager)
    crafted = crafting_manager.craft_items(["Smithing", "Alchemy"])
    assert crafted
    assert any(record.product_type == "armor" for record in crafted)
    assert any(record.product_type in {"weapon", "wand", "bow"} for record in crafted)
    for record in crafted:
        stored = item_manager.get(record.name)
        assert stored is not None
        assert record.trade_skill in {"Smithing", "Alchemy"}


def test_trade_skill_crafting_manager_summary_matches_items() -> None:
    crafting_manager = TradeSkillCraftingManager(ItemManager())
    summary = crafting_manager.craft_summary(["Mining"])
    assert summary
    entry = summary[0]
    assert entry["product_type"] in {"weapon", "armor", "bow", "wand"}
    assert entry["recipe_materials"]


def test_trade_skill_crafting_manager_supports_bows_and_wands() -> None:
    crafting_manager = TradeSkillCraftingManager(ItemManager())
    crafted = crafting_manager.craft_items(["Fletching", "Enchanting"])
    product_types = {record.product_type for record in crafted}
    assert "bow" in product_types
    assert "wand" in product_types


def test_gathering_skills_amplify_crafted_items() -> None:
    baseline_manager = TradeSkillCraftingManager(ItemManager())
    baseline_items = baseline_manager.craft_items(["Smithing"])
    boosted_manager = TradeSkillCraftingManager(ItemManager())
    boosted_items = boosted_manager.craft_items(
        ["Smithing", "Herbalism", "Prospecting"]
    )

    def _find(records: tuple[CraftedItem, ...], name: str) -> CraftedItem:
        for record in records:
            if record.name == name:
                return record
        raise AssertionError(f"missing {name}")

    baseline = _find(baseline_items, "Bulwark Vanguard")
    boosted = _find(boosted_items, "Bulwark Vanguard")
    assert boosted.stats["defense"] > baseline.stats["defense"]
    assert any(record.product_type == "material" for record in boosted_items)
