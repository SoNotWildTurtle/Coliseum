"""Loot table selection and drop generation."""

import random

class LootManager:
    """Generate loot drops using simple tables."""

    def __init__(self, tables: dict | None = None) -> None:
        self.tables = tables or {}

    def add_table(self, enemy_type: str, drops: list[str]) -> None:
        self.tables[enemy_type] = drops

    def roll_loot(self, enemy_type: str):
        drops = self.tables.get(enemy_type, [])
        return random.choice(drops) if drops else None
