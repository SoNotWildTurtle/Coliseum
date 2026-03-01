"""Generate standardized placeholder sprites for local use."""
from __future__ import annotations

import os

import pygame

from hololive_coliseum.placeholder_sprites import ensure_placeholder_sprites
from hololive_coliseum.player import CHARACTER_CLASSES


def main() -> None:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    image_dir = os.path.join(base_dir, "Images")
    map_names = [
        "Default",
        "Sky Spires",
        "Canyon Run",
        "Forge Pit",
        "Crystal Rift",
        "Verdant Ruins",
    ] + [f"Chapter {i}" for i in range(1, 21)]
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    ensure_placeholder_sprites(
        image_dir,
        list(CHARACTER_CLASSES.keys()),
        chapter_count=20,
        map_names=map_names,
        force=True,
    )
    pygame.quit()
    print(f"Standardized sprites generated in {image_dir}")


if __name__ == "__main__":
    main()
