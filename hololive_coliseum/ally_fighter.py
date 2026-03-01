"""AI-driven ally fighters that assist the player during matches."""

from __future__ import annotations

import pygame

from .player import Enemy, PlayerCharacter


class AllyFighter(Enemy):
    """Ally variant that reuses enemy AI but uses player-aligned attacks."""

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str | None = None,
        difficulty: str = "Normal",
        faction: str = "Allies",
    ) -> None:
        super().__init__(x, y, image_path, difficulty, faction=faction, reputation_reward=0)
        self.stats = self.stats.__class__({"attack": 7, "defense": 4, "max_health": 80})
        self.max_health = self.stats.get("max_health")
        self.health_manager.max_health = self.max_health
        self.health_manager.health = self.max_health
        self.health = self.health_manager.health
        self.lives = 3
        self.support_cooldown_ms = 6000
        self.support_last_time = -self.support_cooldown_ms
        self.support_heal_threshold = 0.55
        self.support_shield_threshold = 0.3
        self.focus_low_health = True
        self.focus_threshold = 0.45
        self.focus_range = 280
        self.protect_player = True
        self.protect_player_threshold = 0.6
        self.avoid_hazards = True
        self.role = "intercept"
        self.stance = "balanced"
        self.role_locked = False
        self.stance_locked = False
        self.role_last_switch = -99999
        self.role_switch_cooldown_ms = 4000
        self.stance_last_switch = -99999
        self.stance_switch_cooldown_ms = 2500

    def take_damage(self, amount: int) -> None:
        """Use the player-style revive flow for allies."""
        PlayerCharacter.take_damage(self, amount)

    def shoot(self, now: int, target: tuple[int, int] | None = None):
        """Fire a projectile that damages enemies (not the player team)."""
        proj = PlayerCharacter.shoot(self, now, target)
        if proj:
            proj.owner = self
        return proj

    def melee_attack(self, now: int):
        """Perform a melee strike that damages enemies."""
        attack = PlayerCharacter.melee_attack(self, now)
        if attack:
            attack.owner = self
        return attack

    def revive_at(self, point: tuple[int, int], now: int) -> None:
        """Revive the ally at a spawn point."""
        self.begin_revive(point, now)
