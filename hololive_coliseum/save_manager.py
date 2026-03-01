"""Utility functions for reading and writing settings files."""

import json
import os
import shutil
from typing import Any

SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'SavedGames')
os.makedirs(SAVE_DIR, exist_ok=True)


def _settings_file() -> str:
    return os.path.join(SAVE_DIR, 'settings.json')


def _inventory_file() -> str:
    return os.path.join(SAVE_DIR, 'inventory.json')


def load_settings() -> dict[str, Any]:
    path = _settings_file()
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_settings(data: dict[str, Any]) -> None:
    """Save settings to the `SavedGames` directory, creating it if missing."""
    path = _settings_file()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def wipe_saves() -> None:
    """Delete all files in the save directory if it exists."""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR, exist_ok=True)
        return
    for fname in os.listdir(SAVE_DIR):
        path = os.path.join(SAVE_DIR, fname)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except OSError:
            pass


def merge_records(data: dict[str, Any]) -> dict[str, Any]:
    """Merge ``best_time`` and ``best_score`` from ``data`` into settings."""
    settings = load_settings()
    best_time = data.get("best_time")
    if best_time is not None:
        current = settings.get("best_time")
        if current is None or best_time > current:
            settings["best_time"] = best_time
    best_score = data.get("best_score")
    if best_score is not None:
        current = settings.get("best_score")
        if current is None or best_score > current:
            settings["best_score"] = best_score
    save_settings(settings)
    return settings


def load_inventory() -> dict[str, int]:
    """Read inventory items from disk."""

    path = _inventory_file()
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_inventory(items: dict[str, int]) -> None:
    """Persist ``items`` to the save directory."""

    path = _inventory_file()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(items, f)
