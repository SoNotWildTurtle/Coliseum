"""Validation helpers for character, move, and item content definitions."""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import Any

from .item_manager import ItemManager
from .player import (
    CHARACTER_CLASSES,
    MELEE_COOLDOWN,
    MOVE_SPEED,
    PROJECTILE_COOLDOWN,
    SPECIAL_COOLDOWN,
)
from .trade_skill_crafting_manager import TradeSkillCraftingManager
from .trade_skill_generator import TradeSkillGenerator


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str]


def _item_id(name: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", name.strip().lower())
    return cleaned.strip("_") or "item"


def _character_image_path(name: str) -> str:
    base = name.replace(" ", "_").replace("'", "").replace(".", "")
    return os.path.join(
        os.path.dirname(__file__),
        "..",
        "Images",
        "characters",
        f"{base}_right.png",
    )


def _build_character_catalog() -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    try:
        import pygame
    except Exception as exc:  # pragma: no cover - guarded by tests
        return [], [f"pygame unavailable for character validation: {exc}"]

    if os.environ.get("SDL_VIDEODRIVER") is None:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    try:
        if pygame.display.get_surface() is None:
            pygame.display.set_mode((1, 1))
    except Exception as exc:
        return [], [f"failed to initialize dummy display for validation: {exc}"]

    catalog: list[dict[str, Any]] = []
    for name, cls in sorted(CHARACTER_CLASSES.items()):
        try:
            actor = cls(0, 0, _character_image_path(name))
            attacks = {
                "projectile": {
                    "damage": int(actor.stats.get("attack")),
                    "cooldown": int(PROJECTILE_COOLDOWN),
                    "range": 1200,
                    "cost": 0,
                },
                "melee": {
                    "damage": int(actor.stats.get("attack")) + 5,
                    "cooldown": int(MELEE_COOLDOWN),
                    "range": 64,
                    "cost": 10,
                },
                "special": {
                    "damage": int(actor.stats.get("attack")),
                    "cooldown": int(SPECIAL_COOLDOWN),
                    "range": 900,
                    "cost": 25,
                },
            }
            catalog.append(
                {
                    "id": _item_id(name),
                    "name": name,
                    "hp": int(actor.max_health),
                    "speed": float(getattr(actor, "speed", MOVE_SPEED)),
                    "attacks": attacks,
                }
            )
        except Exception as exc:
            errors.append(f"character '{name}' failed to initialize: {exc}")
    return catalog, errors


def _build_item_catalog() -> list[dict[str, Any]]:
    manager = ItemManager()
    crafter = TradeSkillCraftingManager(item_manager=manager)
    records = crafter.craft_summary(TradeSkillGenerator().list_core_skills())
    catalog: list[dict[str, Any]] = []
    for record in records:
        stats = record.get("stats", {})
        value = 0
        if isinstance(stats, dict):
            value = sum(max(0, int(v)) for v in stats.values() if isinstance(v, int))
        product_type = str(record.get("product_type", "unknown"))
        catalog.append(
            {
                "id": _item_id(str(record.get("name", ""))),
                "type": product_type,
                "value": int(value),
                "stackable": product_type == "material",
            }
        )
    return catalog


def _validate_characters(entries: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for entry in entries:
        name = str(entry.get("name", "<unknown>"))
        for key in ("id", "name", "hp", "speed", "attacks"):
            if key not in entry:
                errors.append(f"character '{name}' missing field '{key}'")
        if int(entry.get("hp", 0)) <= 0:
            errors.append(f"character '{name}' has invalid hp")
        if float(entry.get("speed", 0)) <= 0:
            errors.append(f"character '{name}' has invalid speed")
        attacks = entry.get("attacks", {})
        if not isinstance(attacks, dict):
            errors.append(f"character '{name}' attacks payload is not a mapping")
            continue
        for attack_name, payload in attacks.items():
            if not isinstance(payload, dict):
                errors.append(f"character '{name}' attack '{attack_name}' invalid")
                continue
            for field in ("damage", "cooldown", "range", "cost"):
                if field not in payload:
                    errors.append(
                        f"character '{name}' attack '{attack_name}' missing '{field}'"
                    )
            if int(payload.get("cooldown", -1)) < 0:
                errors.append(
                    f"character '{name}' attack '{attack_name}' has negative cooldown"
                )
    return errors


def _validate_items(entries: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    allowed_types = {"weapon", "armor", "bow", "wand", "material"}
    for item in entries:
        item_id = str(item.get("id", "<unknown>"))
        for key in ("id", "type", "value", "stackable"):
            if key not in item:
                errors.append(f"item '{item_id}' missing field '{key}'")
        if str(item.get("type", "")) not in allowed_types:
            errors.append(f"item '{item_id}' has unknown type '{item.get('type')}'")
        if int(item.get("value", -1)) < 0:
            errors.append(f"item '{item_id}' has negative value")
        if not isinstance(item.get("stackable"), bool):
            errors.append(f"item '{item_id}' stackable must be bool")
    return errors


def validate_all() -> tuple[bool, list[str]]:
    """Validate character, moveset, and item content schemas."""

    characters, character_init_errors = _build_character_catalog()
    errors = list(character_init_errors)
    errors.extend(_validate_characters(characters))
    errors.extend(_validate_items(_build_item_catalog()))
    return (len(errors) == 0), errors


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate content definitions.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on errors")
    return parser


def _cli_main(argv: list[str]) -> int:
    args = _build_parser().parse_args(argv)
    ok, errors = validate_all()
    if ok:
        print("[OK] content validation passed")
        return 0
    for error in errors:
        print(f"[ERROR] {error}")
    if args.strict:
        return 1
    return 0


def main() -> int:
    return _cli_main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
