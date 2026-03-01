"""Store generated regions and sync them through the blockchain."""

from __future__ import annotations

import json
import os
from typing import Dict, List

from .blockchain import load_chain, hash_region
from . import save_manager

DEFAULT_SAVE_DIR = save_manager.SAVE_DIR
SAVE_DIR = DEFAULT_SAVE_DIR
DEFAULT_REGION_FILE = os.path.join(SAVE_DIR, 'regions.json')
REGION_FILE = DEFAULT_REGION_FILE


def _region_file() -> str:
    global SAVE_DIR, REGION_FILE
    if SAVE_DIR == DEFAULT_SAVE_DIR and save_manager.SAVE_DIR != SAVE_DIR:
        SAVE_DIR = save_manager.SAVE_DIR
    if REGION_FILE == DEFAULT_REGION_FILE and SAVE_DIR != DEFAULT_SAVE_DIR:
        REGION_FILE = os.path.join(SAVE_DIR, 'regions.json')
    return REGION_FILE


def load_regions() -> List[Dict[str, object]]:
    """Return the saved list of world regions."""
    path = _region_file()
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_regions(regions: List[Dict[str, object]]) -> None:
    """Persist ``regions`` to disk."""
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(_region_file(), 'w', encoding='utf-8') as f:
        json.dump(regions, f)


class WorldRegionManager:
    """Collect generated regions and merge them from the blockchain."""

    def __init__(self) -> None:
        self.regions: List[Dict[str, object]] = load_regions()

    def add_region(self, region: Dict[str, object]) -> None:
        """Store ``region`` and persist it."""
        self.regions.append(region)
        save_regions(self.regions)

    def get_regions(self) -> List[Dict[str, object]]:
        """Return a copy of stored regions."""
        return [dict(r) for r in self.regions]

    def set_regions(self, regions: List[Dict[str, object]]) -> None:
        """Replace stored regions and persist them."""
        self.regions = [dict(r) for r in regions]
        save_regions(self.regions)

    def sync_with_blockchain(self) -> None:
        """Merge region blocks from the blockchain into local storage."""
        for block in load_chain():
            if block.get('type') == 'region':
                region = block.get('region')
                if (
                    region
                    and hash_region(region) == block.get('region_hash')
                    and all(r.get('name') != region.get('name') for r in self.regions)
                ):
                    self.regions.append(region)
        save_regions(self.regions)
