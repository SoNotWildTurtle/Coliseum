"""Background proof-of-work mining used to grow future MMORPG features."""

from __future__ import annotations

import threading
import time
from typing import Optional

from .blockchain import mine_dummy_block, add_seed
from .world_seed_manager import WorldSeedManager
from .world_generation_manager import WorldGenerationManager


class MiningManager:
    """Run a lightweight mining loop in a background thread.

    When enabled, the manager repeatedly performs proof-of-work on dummy blocks
    to generate hashes for the expanding game world. The workload is extremely
    small but demonstrates how clients could volunteer spare resources for
    world generation in later iterations of the project. When supplied with a
    :class:`WorldGenerationManager`, each mined hash immediately spawns a new
    region so the MMO can grow on its own.
    """

    def __init__(
        self,
        seed_manager: Optional[WorldSeedManager] = None,
        world_gen: Optional[WorldGenerationManager] = None,
        player_id: Optional[str] = None,
    ) -> None:
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self.mined = 0
        self._world_gen = world_gen
        self.player_id = player_id
        if seed_manager is not None:
            self._seed_manager = seed_manager
        elif world_gen is not None:
            self._seed_manager = world_gen.seed_manager
        else:
            self._seed_manager = None

    def start(self, intensity: float = 0.2) -> None:
        """Begin mining with a rough ``intensity`` of CPU usage.

        ``intensity`` is a value between 0 and 1 and influences how quickly the
        miner loops. Values at or below ``0`` disable mining. The default of
        ``0.2`` targets about twenty percent CPU usage so the MMO world can
        evolve while leaving resources for gameplay.
        """
        if self._running or intensity <= 0:
            return
        self._running = True
        delay = max(0.0, 0.1 * (1 - intensity))
        # mine once immediately so callers see progress even if the thread
        # hasn't scheduled before ``stop`` is called
        header = mine_dummy_block()
        if self._seed_manager is not None:
            self._seed_manager.add_seed(header["hash"])
        add_seed(header["hash"])
        if self._world_gen is not None:
            self._world_gen.generate_region_from_seed(header["hash"], self.player_id)
        self.mined += 1
        self._thread = threading.Thread(
            target=self._mine_loop, args=(delay,), daemon=True
        )
        self._thread.start()

    def _mine_loop(self, delay: float) -> None:
        while self._running:
            header = mine_dummy_block()
            if self._seed_manager is not None:
                self._seed_manager.add_seed(header["hash"])
            add_seed(header["hash"])
            if self._world_gen is not None:
                self._world_gen.generate_region_from_seed(header["hash"], self.player_id)
            self.mined += 1
            time.sleep(delay)

    def stop(self) -> None:
        """Stop the mining loop if it is running."""
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=0.1)
            self._thread = None
