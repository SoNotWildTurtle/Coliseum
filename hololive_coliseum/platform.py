"""Moving platform sprite and behavior."""

import random
import pygame

class Platform(pygame.sprite.Sprite):
    """Static platform that players and enemies can stand on."""

    def __init__(
        self,
        rect: pygame.Rect | tuple[int, int, int, int],
        theme: str = "stone",
    ):
        super().__init__()
        if not isinstance(rect, pygame.Rect):
            rect = pygame.Rect(rect)
        self.image = self._build_surface(rect.size, theme)
        self.rect = rect
        self.velocity = pygame.math.Vector2(0, 0)

    def _build_surface(self, size: tuple[int, int], theme: str) -> pygame.Surface:
        width, height = size
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        base, accent, trim = self._theme_colors(theme)
        for y in range(height):
            ratio = y / max(1, height - 1)
            shade = (
                int(base[0] * (0.75 + ratio * 0.25)),
                int(base[1] * (0.75 + ratio * 0.25)),
                int(base[2] * (0.75 + ratio * 0.25)),
            )
            pygame.draw.line(surface, shade, (0, y), (width, y))
        pygame.draw.rect(surface, trim, pygame.Rect(0, 0, width, 4))
        pygame.draw.rect(surface, trim, pygame.Rect(0, height - 3, width, 3))
        rng = random.Random(width * 37 + height * 91 + len(theme) * 13)
        for _ in range(max(2, width // 40)):
            bx = rng.randint(6, max(6, width - 14))
            by = rng.randint(6, max(6, height - 10))
            pygame.draw.rect(
                surface,
                accent,
                pygame.Rect(bx, by, 6, 3),
                border_radius=1,
            )
        return surface

    def _theme_colors(
        self, theme: str
    ) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
        if theme == "metal":
            return (140, 150, 160), (180, 200, 210), (90, 100, 110)
        if theme == "crumble":
            return (170, 130, 110), (210, 170, 140), (110, 80, 70)
        return (150, 150, 160), (190, 190, 200), (90, 90, 100)


class MovingPlatform(Platform):
    """Platform that moves back and forth along a vector."""

    def __init__(
        self,
        rect: pygame.Rect | tuple[int, int, int, int],
        offset: tuple[int, int],
        speed: int,
    ) -> None:
        super().__init__(rect, theme="metal")
        self.start = pygame.math.Vector2(self.rect.topleft)
        self.offset = pygame.math.Vector2(offset)
        self.speed = speed
        self.direction = 1
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self) -> None:
        target = self.start + self.offset if self.direction > 0 else self.start
        move = target - pygame.math.Vector2(self.rect.topleft)
        if move.length() <= self.speed:
            self.rect.topleft = target
            self.direction *= -1
            self.velocity.update(0, 0)
        else:
            move.scale_to_length(self.speed)
            self.rect.move_ip(move)
            self.velocity.update(move.x, move.y)


class CrumblingPlatform(Platform):
    """Platform that disappears shortly after being stepped on."""

    def __init__(self, rect: pygame.Rect | tuple[int, int, int, int], delay: int = 60) -> None:
        super().__init__(rect, theme="crumble")
        self.delay = delay
        self.timer = -1

    def start_crumble(self) -> None:
        """Begin the crumble timer if not already running."""
        if self.timer < 0:
            self.timer = self.delay

    def update(self) -> None:  # pragma: no cover - simple countdown
        if self.timer > 0:
            self.timer -= 1
            if self.timer == 0:
                self.kill()
