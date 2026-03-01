"""Mob enemy variants for ambient wave spawning."""

from __future__ import annotations

from .player import Enemy


class MobEnemy(Enemy):
    """Lightweight mob that swarms the arena with aggressive bias."""

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str | None = None,
        difficulty: str = "Normal",
        faction: str = "Mob",
    ) -> None:
        super().__init__(x, y, image_path, difficulty, faction=faction, reputation_reward=2)
        self.stats = self.stats.__class__({"attack": 6, "defense": 1, "max_health": 35})
        self.max_health = self.stats.get("max_health")
        self.health_manager.max_health = self.max_health
        self.health_manager.health = self.max_health
        self.health = self.health_manager.health
        self.ai_bias = {
            "react_ms": max(80, self.AI_LEVELS[difficulty]["react_ms"] - 40),
            "speed": min(1.4, self.AI_LEVELS[difficulty]["speed"] + 0.2),
            "shoot_prob": 0.7,
            "melee_prob": 1.0,
            "jump_prob": min(0.6, self.AI_LEVELS[difficulty]["jump_prob"] + 0.1),
            "dodge_prob": min(0.7, self.AI_LEVELS[difficulty]["dodge_prob"] + 0.1),
            "block_prob": 0.1,
            "special_prob": 0.04,
            "dash_prob": min(0.22, self.AI_LEVELS[difficulty]["dash_prob"] + 0.05),
            "feint_prob": 0.02,
            "strafe_prob": 0.12,
            "hold_distance": 70,
            "lead_frames": max(0, self.AI_LEVELS[difficulty]["lead_frames"] - 2),
            "retreat_threshold": 0.2,
        }
