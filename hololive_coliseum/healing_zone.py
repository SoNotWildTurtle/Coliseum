"""Healing zone sprite and recovery effects."""

import math
import pygame

class HealingZone(pygame.sprite.Sprite):
    """Zone that heals players standing inside it."""

    def __init__(
        self,
        rect: pygame.Rect,
        heal_rate: int = 1,
        duration: int = 60,
        *,
        base_color: tuple[int, int, int] = (0, 255, 0),
        pulse_style: str = "grove",
    ) -> None:
        super().__init__()
        self.rect = rect
        self.heal_rate = heal_rate
        self.timer = duration
        self.base_color = base_color
        self.pulse_style = pulse_style
        self.phase = (rect.x + rect.y) % 360
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((*self.base_color, 80))

    def update(self) -> None:
        style = self.pulse_style
        if style == "bloom":
            speed = 220
            alpha_min, alpha_max = 90, 200
        elif style == "calm":
            speed = 380
            alpha_min, alpha_max = 50, 140
        else:
            speed = 300
            alpha_min, alpha_max = 70, 150
        pulse = (math.sin((pygame.time.get_ticks() + self.phase) / speed) + 1) * 0.5
        alpha = alpha_min + int((alpha_max - alpha_min) * pulse)
        self.image.fill((*self.base_color, alpha))
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
