"""Gravity zone sprite and physics behavior."""

import pygame

class GravityZone(pygame.sprite.Sprite):
    """Rectangular zone that modifies gravity for sprites inside it."""

    def __init__(self, rect: pygame.Rect, multiplier: float) -> None:
        super().__init__()
        self.rect = rect
        self.multiplier = multiplier
        # For visualization (optional), we can make a semi-transparent surface
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        color = (0, 0, 255, 50) if multiplier > 1 else (255, 0, 0, 50)
        self.image.fill(color)

