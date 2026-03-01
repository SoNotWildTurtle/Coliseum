"""Power-up sprites that grant health, mana, stamina, speed, shield, attack,
defense, experience or extra lives."""

import math
import pygame


class PowerUp(pygame.sprite.Sprite):
    """Simple powerup that restores health, mana, stamina, speed, attack,
    defense, experience or grants a shield or extra life."""

    def __init__(self, x: int, y: int, effect: str) -> None:
        super().__init__()
        self.effect = effect
        self.base_center = (x, y)
        self.phase = (x + y) % 360
        self.image = self._build_sprite(effect)
        self.rect = self.image.get_rect(center=self.base_center)

    def _build_sprite(self, effect: str) -> pygame.Surface:
        size = 28
        image = pygame.Surface((size, size), pygame.SRCALPHA)
        inner = pygame.Surface((size, size), pygame.SRCALPHA)
        color, accent = self._colors_for_effect(effect)
        for i in range(size // 2, 0, -1):
            alpha = 40 + int(140 * (i / (size / 2)))
            pygame.draw.circle(
                inner,
                (*color, alpha),
                (size // 2, size // 2),
                i,
            )
        image.blit(inner, (0, 0))
        pygame.draw.circle(image, (*accent, 210), (size // 2, size // 2), 11, 2)
        pygame.draw.circle(image, (15, 20, 25, 160), (size // 2, size // 2), 12, 1)
        self._draw_icon(image, effect, accent)
        return image

    def _colors_for_effect(self, effect: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        if effect == "heal":
            return (80, 220, 120), (120, 255, 170)
        if effect == "mana":
            return (70, 120, 255), (140, 180, 255)
        if effect == "stamina":
            return (90, 230, 210), (160, 255, 240)
        if effect == "speed":
            return (255, 210, 90), (255, 240, 140)
        if effect == "shield":
            return (170, 140, 255), (210, 190, 255)
        if effect == "attack":
            return (255, 100, 90), (255, 170, 160)
        if effect == "defense":
            return (90, 150, 255), (140, 200, 255)
        if effect == "xp":
            return (210, 220, 255), (240, 245, 255)
        return (255, 160, 90), (255, 210, 150)

    def _draw_icon(self, surface: pygame.Surface, effect: str, color: tuple[int, int, int]) -> None:
        cx, cy = surface.get_width() // 2, surface.get_height() // 2
        if effect == "heal":
            pygame.draw.rect(surface, color, pygame.Rect(cx - 2, cy - 8, 4, 16))
            pygame.draw.rect(surface, color, pygame.Rect(cx - 8, cy - 2, 16, 4))
        elif effect == "mana":
            pygame.draw.polygon(
                surface,
                color,
                [(cx, cy - 9), (cx - 6, cy + 2), (cx, cy + 9), (cx + 6, cy + 2)],
            )
        elif effect == "stamina":
            pygame.draw.polygon(
                surface,
                color,
                [(cx - 4, cy - 8), (cx + 2, cy - 2), (cx - 1, cy - 2),
                 (cx + 4, cy + 8), (cx - 2, cy + 2), (cx + 1, cy + 2)],
            )
        elif effect == "speed":
            pygame.draw.polygon(
                surface,
                color,
                [(cx - 8, cy - 6), (cx - 1, cy - 2), (cx - 6, cy - 2),
                 (cx + 8, cy + 6), (cx + 1, cy + 2), (cx + 6, cy + 2)],
            )
        elif effect == "shield":
            pygame.draw.polygon(
                surface,
                color,
                [(cx - 7, cy - 7), (cx + 7, cy - 7), (cx + 4, cy + 7),
                 (cx, cy + 9), (cx - 4, cy + 7)],
            )
        elif effect == "attack":
            pygame.draw.line(surface, color, (cx - 6, cy + 6), (cx + 6, cy - 6), 3)
            pygame.draw.line(surface, color, (cx - 2, cy + 7), (cx + 7, cy - 2), 2)
        elif effect == "defense":
            pygame.draw.circle(surface, color, (cx, cy), 6, 2)
            pygame.draw.circle(surface, color, (cx, cy), 2)
        elif effect == "xp":
            points = []
            for i in range(5):
                angle = i * (2 * math.pi / 5) - math.pi / 2
                outer = (cx + int(math.cos(angle) * 8), cy + int(math.sin(angle) * 8))
                inner = (
                    cx + int(math.cos(angle + math.pi / 5) * 4),
                    cy + int(math.sin(angle + math.pi / 5) * 4),
                )
                points.extend([outer, inner])
            pygame.draw.polygon(surface, color, points)
        else:  # extra life
            pygame.draw.circle(surface, color, (cx - 4, cy - 2), 4)
            pygame.draw.circle(surface, color, (cx + 4, cy - 2), 4)
            pygame.draw.polygon(
                surface,
                color,
                [(cx - 8, cy), (cx + 8, cy), (cx, cy + 10)],
            )

    def update(self) -> None:
        now = pygame.time.get_ticks()
        bob = int(3 * math.sin((now + self.phase) / 300))
        self.rect.center = (self.base_center[0], self.base_center[1] + bob)
