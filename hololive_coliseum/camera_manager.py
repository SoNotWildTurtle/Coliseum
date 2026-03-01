"""Camera manager tracking viewport offset."""
from __future__ import annotations

from typing import Tuple
import random
import pygame


class CameraManager:
    """Store a camera offset that follows a target rect and can shake."""

    def __init__(self) -> None:
        self.offset = pygame.Vector2(0, 0)
        self.shake_end = 0
        self.shake_mag = 0
        self._shake_offset = pygame.Vector2(0, 0)

    def shake(self, duration: int, magnitude: int) -> None:
        """Trigger a screen shake for ``duration`` milliseconds."""
        self.shake_end = pygame.time.get_ticks() + duration
        self.shake_mag = magnitude

    def update(self) -> None:
        """Update the current shake offset based on time."""
        if pygame.time.get_ticks() < self.shake_end:
            self._shake_offset.x = random.randint(-self.shake_mag, self.shake_mag)
            self._shake_offset.y = random.randint(-self.shake_mag, self.shake_mag)
            if self.shake_mag and not self._shake_offset.length_squared():
                self._shake_offset.x = self.shake_mag
        else:
            self._shake_offset.update(0, 0)

    def follow(self, rect: pygame.Rect, screen_size: Tuple[int, int]) -> None:
        """Center the camera on *rect* within *screen_size*."""
        self.offset.x = rect.centerx - screen_size[0] // 2
        self.offset.y = rect.centery - screen_size[1] // 2

    def follow_bounds(
        self,
        rect: pygame.Rect,
        screen_size: Tuple[int, int],
        world_size: Tuple[int, int],
        *,
        smoothing: float = 0.18,
        lock_y: bool = True,
    ) -> None:
        """Center the camera on *rect* within the world bounds."""
        target_x = rect.centerx - screen_size[0] // 2
        target_y = rect.centery - screen_size[1] // 2
        max_x = max(0, world_size[0] - screen_size[0])
        max_y = max(0, world_size[1] - screen_size[1])
        target_x = max(0, min(target_x, max_x))
        target_y = 0 if lock_y else max(0, min(target_y, max_y))
        if smoothing:
            self.offset.x += (target_x - self.offset.x) * smoothing
            self.offset.y += (target_y - self.offset.y) * smoothing
        else:
            self.offset.x = target_x
            self.offset.y = target_y

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        """Return a rectangle moved by the current camera offset."""
        return rect.move(
            -self.offset.x + self._shake_offset.x,
            -self.offset.y + self._shake_offset.y,
        )


class ThirdPersonCamera(CameraManager):
    """Camera that keeps the target lower on screen for a 3rd-person view."""

    def follow(self, rect: pygame.Rect, screen_size: Tuple[int, int]) -> None:
        super().follow(rect, screen_size)
        self.offset.y += screen_size[1] // 4
