"""Screenshot manager for saving captured images to disk."""

from __future__ import annotations

import os
import time
from typing import List

from .save_manager import SAVE_DIR


class ScreenshotManager:
    """Manage in-game screenshots stored under ``SavedGames/screenshots``."""

    def __init__(self) -> None:
        self.directory = os.path.join(SAVE_DIR, "screenshots")
        os.makedirs(self.directory, exist_ok=True)
        self.shots: List[str] = []

    def capture(self, surface, name: str | None = None) -> str:
        """Save ``surface`` as a PNG and record the filename.

        A timestamped name is generated when ``name`` is ``None``. The saved
        filename is appended to the internal shot list and returned.
        """

        import pygame  # Local import so tests can skip if pygame is missing

        if name is None:
            name = f"shot_{int(time.time() * 1000)}.png"
        path = os.path.join(self.directory, name)
        pygame.image.save(surface, path)
        self.shots.append(name)
        return path

    def list_shots(self) -> List[str]:
        """Return the list of filenames for captured screenshots."""

        return list(self.shots)
