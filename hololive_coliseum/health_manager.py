"""Health tracking and regeneration utilities."""

import pygame


class HealthManager:
    """Track, modify and regenerate a character's health."""

    def __init__(self, max_health: int) -> None:
        self.max_health = max_health
        self.health = max_health
        now = pygame.time.get_ticks()
        self.last_damage_time = now
        self.last_regen_tick = now

    def take_damage(
        self,
        amount: int,
        blocking: bool = False,
        parrying: bool = False,
        now: int | None = None,
    ) -> int:
        """Apply damage and return the new health value."""
        if parrying:
            return self.health
        if blocking:
            amount //= 2
        self.health = max(0, self.health - amount)
        if now is None:
            now = pygame.time.get_ticks()
        self.last_damage_time = now
        self.last_regen_tick = now
        return self.health

    def heal(self, amount: int) -> int:
        """Restore health and return the new value."""
        self.health = min(self.max_health, self.health + amount)
        return self.health

    def update(self, now: int | None = None) -> int:
        """Regenerate health after a delay and return the new value."""
        if now is None:
            now = pygame.time.get_ticks()
        if self.health < self.max_health and now - self.last_damage_time >= 3000:
            if now - self.last_regen_tick >= 1000:
                self.health = min(self.max_health, self.health + 1)
                self.last_regen_tick = now
        return self.health
