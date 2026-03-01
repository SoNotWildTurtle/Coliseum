"""Melee attack sprite behavior and collision."""

import math
import pygame

MELEE_LIFETIME = 10  # frames
MELEE_SIZE = (30, 20)


class MeleeAttack(pygame.sprite.Sprite):
    """Temporary hitbox representing a melee swing."""

    def __init__(
        self,
        x: int,
        y: int,
        facing: int,
        owner: object | None = None,
        from_enemy: bool = False,
    ) -> None:
        super().__init__()
        self.image = pygame.Surface(MELEE_SIZE, pygame.SRCALPHA)
        self.image.fill((255, 255, 0))  # yellow
        self.base_image = self.image.copy()
        self.vfx_style = "slash_arc"
        self.vfx_color = (255, 220, 120)
        self.vfx_intensity = 1.0
        self._phase = 0.0
        # Position attack in front of the player
        if facing >= 0:
            self.rect = self.image.get_rect(midleft=(x, y))
        else:
            self.rect = self.image.get_rect(midright=(x, y))
        self.lifetime = MELEE_LIFETIME
        self.from_enemy = from_enemy
        self.owner = owner
        self.knockback = 2.5

    def update(self) -> None:
        self._animate()
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

    def _animate(self) -> None:
        width, height = self.base_image.get_size()
        self._phase += 0.4
        pulse = (math.sin(self._phase) + 1) * 0.5
        alpha = int(min(220, max(40, 80 + 120 * pulse * self.vfx_intensity)))
        image = self.base_image.copy()
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        color = (*self.vfx_color, alpha)
        if self.vfx_style == "slash_thrust":
            pygame.draw.line(
                overlay,
                color,
                (0, height // 2),
                (width, height // 2),
                3,
            )
        elif self.vfx_style == "slash_cross":
            pygame.draw.line(overlay, color, (0, 0), (width, height), 2)
            pygame.draw.line(overlay, color, (width, 0), (0, height), 2)
        elif self.vfx_style == "slash_wave":
            points = []
            for x in range(0, width + 1, 4):
                y = int(height / 2 + math.sin(self._phase + x / 6) * 4)
                points.append((x, y))
            if len(points) >= 2:
                pygame.draw.lines(overlay, color, False, points, 2)
        elif self.vfx_style == "slash_spike":
            for x in range(0, width, 6):
                pygame.draw.line(overlay, color, (x, height), (x + 3, 0), 2)
        else:
            pygame.draw.arc(
                overlay,
                color,
                pygame.Rect(0, 0, width, height),
                0.6,
                2.6,
                2,
            )
        image.blit(overlay, (0, 0))
        center = self.rect.center
        self.image = image
        self.rect = self.image.get_rect(center=center)
