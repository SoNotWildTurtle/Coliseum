"""Helpers to assemble core MMO managers automatically.

`MMOBuilder` instantiates a set of managers that power the self-building MMO
systems. It wires together world seed, generation, region, player and voting
managers so games can start with minimal setup code.
"""

from __future__ import annotations

from dataclasses import dataclass

from .world_seed_manager import WorldSeedManager
from .world_generation_manager import WorldGenerationManager
from .world_region_manager import WorldRegionManager
from .world_player_manager import WorldPlayerManager
from .voting_manager import VotingManager


@dataclass
class MMOBuilder:
    """Constructs the core managers for the MMO subsystems."""

    def build(self) -> dict[str, object]:
        """Return freshly constructed managers keyed by role."""
        return {
            "world_seed": WorldSeedManager(),
            "world_gen": WorldGenerationManager(),
            "world_region": WorldRegionManager(),
            "world_player": WorldPlayerManager(),
            "voting": VotingManager(),
        }
