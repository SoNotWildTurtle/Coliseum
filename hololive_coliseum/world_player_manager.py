"""Track MMO player positions and limit them to existing regions."""

from __future__ import annotations

import math
from typing import Dict, Tuple

from .world_generation_manager import WorldGenerationManager
from .world_region_manager import WorldRegionManager


class WorldPlayerManager:
    """Record positions and block movement beyond generated regions."""

    def __init__(
        self,
        world_manager: WorldGenerationManager | None = None,
        region_manager: WorldRegionManager | None = None,
    ) -> None:
        self.world_manager = world_manager or WorldGenerationManager()
        self.region_manager = region_manager or self.world_manager.region_manager
        self.positions: Dict[str, Tuple[float, float]] = {}

    def set_position(self, player_id: str, pos: Tuple[float, float]) -> None:
        """Set ``player_id``'s global position to ``pos``."""
        self.positions[player_id] = (float(pos[0]), float(pos[1]))

    def get_position(self, player_id: str) -> Tuple[float, float]:
        """Return the stored position for ``player_id`` or the origin."""
        return self.positions.get(player_id, (0.0, 0.0))

    def move_player(self, player_id: str, dx: float, dy: float) -> Tuple[float, float]:
        """Move a player but stop at the outermost region.

        Attempted movement past the largest region radius is clamped so players
        cannot wander outside the generated world.
        """
        x, y = self.get_position(player_id)
        x += dx
        y += dy
        max_radius = max(
            (r.get("radius", 0) for r in self.region_manager.get_regions()),
            default=0,
        )
        distance = math.hypot(x, y)
        if distance > max_radius and distance:
            scale = max_radius / distance
            x *= scale
            y *= scale
        self.positions[player_id] = (x, y)
        return x, y

    def move_player_relative(
        self, player_id: str, forward: float, strafe: float, yaw: float
    ) -> Tuple[float, float]:
        """Move a player using forward/strafe input relative to ``yaw``.

        ``yaw`` is measured in radians. The values are rotated into world
        coordinates and passed to :meth:`move_player` so movement still obeys
        region boundaries.
        """
        dx = forward * math.cos(yaw) - strafe * math.sin(yaw)
        dy = forward * math.sin(yaw) + strafe * math.cos(yaw)
        return self.move_player(player_id, dx, dy)
