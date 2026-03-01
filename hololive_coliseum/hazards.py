"""Hazard sprite definitions for arenas."""

import pygame

class SpikeTrap(pygame.sprite.Sprite):
    """Rectangular hazard that damages sprites on contact."""

    def __init__(self, rect: pygame.Rect, damage: int = 10) -> None:
        super().__init__()
        self.rect = rect
        self.damage = damage
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((200, 0, 0))
        self.avoid = True

class IceZone(pygame.sprite.Sprite):
    """Zone with slippery surface reducing friction."""

    def __init__(self, rect: pygame.Rect, friction: float = 0.5) -> None:
        super().__init__()
        self.rect = rect
        self.friction = friction
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((0, 200, 255, 80))
        self.avoid = False

class LavaZone(pygame.sprite.Sprite):
    """Hazard zone that deals periodic damage while touched."""

    def __init__(self, rect: pygame.Rect, damage: int = 5, interval: int = 300) -> None:
        super().__init__()
        self.rect = rect
        self.damage = damage
        self.interval = interval
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((255, 100, 0, 120))
        self.avoid = True

class AcidPool(pygame.sprite.Sprite):
    """Hazard zone that damages and slows sprites."""

    def __init__(self, rect: pygame.Rect, damage: int = 4, interval: int = 300, friction: float = 0.7) -> None:
        super().__init__()
        self.rect = rect
        self.damage = damage
        self.interval = interval
        self.friction = friction
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((0, 255, 0, 120))
        self.avoid = True


class PoisonZone(pygame.sprite.Sprite):
    """Hazard zone that poisons sprites for damage over time."""

    def __init__(self, rect: pygame.Rect) -> None:
        super().__init__()
        self.rect = rect
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((160, 32, 240, 150))
        self.avoid = True


class FireZone(pygame.sprite.Sprite):
    """Hazard zone that ignites sprites causing burn damage."""

    def __init__(self, rect: pygame.Rect) -> None:
        super().__init__()
        self.rect = rect
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((255, 50, 0, 150))
        self.avoid = True


class FrostZone(pygame.sprite.Sprite):
    """Hazard zone that freezes sprites temporarily."""

    def __init__(self, rect: pygame.Rect, duration: int = 1000) -> None:
        super().__init__()
        self.rect = rect
        self.duration = duration
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((150, 220, 255, 160))
        self.avoid = True


class QuicksandZone(pygame.sprite.Sprite):
    """Hazard zone that drags sprites downward and slows movement."""

    def __init__(
        self, rect: pygame.Rect, pull: float = 1.0, friction: float = 0.5
    ) -> None:
        super().__init__()
        self.rect = rect
        self.pull = pull
        self.friction = friction
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((194, 178, 128, 120))
        self.avoid = True


class LightningZone(pygame.sprite.Sprite):
    """Hazard zone that periodically zaps and knocks sprites upward."""

    def __init__(
        self,
        rect: pygame.Rect,
        damage: int = 4,
        interval: int = 400,
        force: int = -8,
    ) -> None:
        super().__init__()
        self.rect = rect
        self.damage = damage
        self.interval = interval
        self.force = force
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((255, 255, 0, 150))
        self.avoid = True

class BouncePad(pygame.sprite.Sprite):
    """Pad that launches sprites upward when touched."""

    def __init__(self, rect: pygame.Rect, force: int = -12) -> None:
        super().__init__()
        self.rect = rect
        self.force = force
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((255, 255, 0))
        self.avoid = False


class TeleportPad(pygame.sprite.Sprite):
    """Pad that relocates sprites to a target position."""

    def __init__(self, rect: pygame.Rect, target: tuple[int, int]) -> None:
        super().__init__()
        self.rect = rect
        self.target = target
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((0, 200, 255))
        self.avoid = False


class WindZone(pygame.sprite.Sprite):
    """Zone that pushes sprites horizontally."""

    def __init__(self, rect: pygame.Rect, force: float = 2.0) -> None:
        super().__init__()
        self.rect = rect
        self.force = force
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((200, 200, 255, 120))
        self.avoid = False


class SilenceZone(pygame.sprite.Sprite):
    """Hazard zone that temporarily blocks special attacks."""

    def __init__(self, rect: pygame.Rect, duration: int = 1000) -> None:
        super().__init__()
        self.rect = rect
        self.duration = duration
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((128, 128, 128, 150))
        self.avoid = True


class RegenZone(pygame.sprite.Sprite):
    """Area that restores health to sprites standing inside."""

    def __init__(
        self,
        rect: pygame.Rect,
        heal: int = 1,
        interval: int = 500,
    ) -> None:
        super().__init__()
        self.rect = rect
        self.heal = heal
        self.interval = interval
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((0, 255, 0, 120))
        self.avoid = False

