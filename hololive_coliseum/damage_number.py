"""Sprites for floating damage indicators."""

from __future__ import annotations

import pygame


class DamageNumber(pygame.sprite.Sprite):
    """Display a floating number for recent damage.

    Critical hits render in yellow to stand out from normal red numbers.
    """

    def __init__(self, value: int, pos: tuple[int, int], critical: bool = False) -> None:
        super().__init__()
        if not pygame.font.get_init():
            pygame.font.init()
        font = pygame.font.Font(None, 24 if critical else 20)
        color = (255, 255, 0) if critical else (255, 0, 0)
        self.image = font.render(str(value), True, color)
        self.rect = self.image.get_rect(center=pos)
        self.start = pygame.time.get_ticks()

    def update(self, now: int) -> None:
        """Rise upward and expire after half a second."""
        self.rect.y -= 1
        if now - self.start > 500:
            self.kill()


class CheerText(pygame.sprite.Sprite):
    """Floating cheer text for hype moments."""

    def __init__(
        self,
        text: str,
        pos: tuple[int, int],
        *,
        color: tuple[int, int, int] = (255, 220, 120),
    ) -> None:
        super().__init__()
        if not pygame.font.get_init():
            pygame.font.init()
        font = pygame.font.Font(None, 26)
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(center=pos)
        self.start = pygame.time.get_ticks()

    def update(self, now: int) -> None:
        self.rect.y -= 1
        if now - self.start > 700:
            self.kill()
