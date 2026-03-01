"""Adaptive autoplay agent that steers the local player during runs."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable

import pygame


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass
class AutoPlayerTuning:
    """Tune aggression and reactions for the autoplay agent."""

    aggression: float = 0.5
    caution: float = 0.5
    special_chance: float = 0.2
    dodge_bias: float = 0.5
    strafe_chance: float = 0.18
    melee_range: int = 55
    shoot_range: int = 240
    desired_range: int = 120

    @classmethod
    def from_dict(cls, data: dict | None) -> "AutoPlayerTuning":
        if not isinstance(data, dict):
            return cls()
        return cls(
            aggression=float(data.get("aggression", 0.5)),
            caution=float(data.get("caution", 0.5)),
            special_chance=float(data.get("special_chance", 0.2)),
            dodge_bias=float(data.get("dodge_bias", 0.5)),
            strafe_chance=float(data.get("strafe_chance", 0.18)),
            melee_range=int(data.get("melee_range", 55)),
            shoot_range=int(data.get("shoot_range", 240)),
            desired_range=int(data.get("desired_range", 120)),
        )

    def to_dict(self) -> dict[str, float | int]:
        return {
            "aggression": self.aggression,
            "caution": self.caution,
            "special_chance": self.special_chance,
            "dodge_bias": self.dodge_bias,
            "strafe_chance": self.strafe_chance,
            "melee_range": self.melee_range,
            "shoot_range": self.shoot_range,
            "desired_range": self.desired_range,
        }

    def clamp(self) -> None:
        self.aggression = _clamp(self.aggression, 0.1, 0.95)
        self.caution = _clamp(self.caution, 0.05, 0.95)
        self.special_chance = _clamp(self.special_chance, 0.05, 0.55)
        self.dodge_bias = _clamp(self.dodge_bias, 0.1, 0.95)
        self.strafe_chance = _clamp(self.strafe_chance, 0.05, 0.45)
        self.melee_range = max(30, min(90, self.melee_range))
        self.shoot_range = max(160, min(320, self.shoot_range))
        self.desired_range = max(70, min(220, self.desired_range))


class KeyState:
    """Lightweight key state wrapper for simulated input."""

    def __init__(self, pressed: set[int]) -> None:
        self._pressed = pressed

    def __getitem__(self, key: int) -> bool:
        return key in self._pressed


class _AutoTarget:
    """Tiny target wrapper for exploration goals."""

    def __init__(self, rect: pygame.Rect, name: str) -> None:
        self.rect = rect
        self.name = name


class AutoPlayer:
    """Generate basic input decisions for the local player."""

    def __init__(self, game, tuning: dict | None = None) -> None:
        self.game = game
        self.last_jump = 0
        self.last_special = 0
        self.last_dodge = 0
        self.last_block = 0
        self.last_item = 0
        self.last_mana = 0
        self.last_strafe = 0
        self.last_melee = 0
        self.last_shoot = 0
        self.last_sprint = 0
        self.last_feedback = 0
        self.last_difficulty_update = 0
        self.tuning = AutoPlayerTuning.from_dict(tuning)
        self.last_goal = "idle"
        self.last_target_name = "None"
        self.last_target_distance = 0
        self.explore_mode = "none"
        self.explore_until = 0
        self.explore_target: _AutoTarget | None = None

    def inputs(self, now: int) -> tuple[KeyState, Callable[[str], bool]]:
        pressed_keys: set[int] = set()
        actions: set[str] = set()
        player = getattr(self.game, "player", None)
        enemies = list(getattr(self.game, "enemies", []))
        projectiles = list(getattr(self.game, "projectiles", []))
        powerups = list(getattr(self.game, "powerups", []))
        hazards = list(getattr(self.game, "hazards", []))
        platforms = list(getattr(self.game, "platforms", []))

        threat_ratio = self._stage_threat_ratio(enemies, hazards)
        self._apply_difficulty_bias(now, threat_ratio)

        target = self._select_target(player, enemies)
        world_width = getattr(self.game, "world_width", getattr(self.game, "width", 0))
        self._maybe_set_explore_mode(now, player, hazards, platforms, world_width)
        target = self._select_goal_target(player, target, powerups, now, threat_ratio)

        if player and target:
            self._move_toward_target(player, target, pressed_keys, now)

            if target.rect.centery + 10 < player.rect.centery:
                self._maybe_jump(actions, now)

            distance = abs(target.rect.centerx - player.rect.centerx)
            melee_range = int(self.tuning.melee_range * (1 + 0.3 * self.tuning.aggression))
            shoot_range = int(self.tuning.shoot_range * (1 + 0.25 * self.tuning.aggression))
            if distance < melee_range:
                actions.add("melee")
            elif distance < shoot_range:
                actions.add("shoot")
            elif player.stamina > 20 and len(enemies) < 3:
                actions.add("sprint")

            if player.mana > 50 and now - self.last_special > 1200:
                chance = self.tuning.special_chance + 0.1 * self.tuning.aggression
                chance += 0.1 * threat_ratio
                if random.random() < chance:
                    actions.add("special")
                    self.last_special = now
            self._maybe_force_feature_tests(actions, now, player)

        if player:
            if self._incoming_projectile(player, projectiles):
                if now - self.last_dodge > 650:
                    actions.add("dodge")
                    self.last_dodge = now
            if self._near_enemy(player, target) and now - self.last_block > 900:
                block_bias = self.tuning.caution + 0.2 * threat_ratio
                if random.random() < min(0.95, block_bias):
                    actions.add("block")
                    if random.random() < 0.25 + 0.2 * threat_ratio:
                        actions.add("parry")
                    self.last_block = now
            self._maybe_use_item(actions, player, now, threat_ratio)
            self._maybe_use_mana(actions, player, now, threat_ratio)

        if player and self._hazard_ahead(player):
            self._maybe_jump(actions, now)
            if now - self.last_dodge > 700 and random.random() < self.tuning.dodge_bias:
                actions.add("dodge")
                self.last_dodge = now
        if player and self._gap_or_edge_risk(player, world_width):
            self._avoid_edges(player, pressed_keys, world_width)
            self._maybe_jump(actions, now)

        if player and not target and powerups:
            self._move_toward_powerup(player, powerups, pressed_keys)
            actions.add("sprint")

        def action_pressed(action: str) -> bool:
            return action in actions

        if hasattr(self.game, "_autoplay_trace_inputs"):
            self.game._autoplay_trace_inputs(pressed_keys, actions, now)

        return KeyState(pressed_keys), action_pressed

    def update_feedback(
        self,
        damage_taken: float,
        kills: int,
        health_ratio: float,
        elapsed_ms: int,
    ) -> None:
        if elapsed_ms <= 0:
            return
        damage_rate = damage_taken / max(1.0, elapsed_ms)
        if damage_taken > 0:
            self.tuning.caution += 0.08 + damage_rate * 160
            self.tuning.aggression -= 0.04
            self.tuning.dodge_bias += 0.05
        if kills > 0:
            self.tuning.aggression += 0.06 * kills
            self.tuning.caution -= 0.02 * kills
            self.tuning.special_chance += 0.01 * kills
        if health_ratio < 0.35:
            self.tuning.caution += 0.1
            self.tuning.aggression -= 0.05
        elif health_ratio > 0.8 and kills:
            self.tuning.aggression += 0.02
        self.tuning.clamp()

    def tuning_snapshot(self) -> dict[str, float | int]:
        return self.tuning.to_dict()

    def _nearest_enemy(self, player, enemies):
        if not player or not enemies:
            return None
        return min(enemies, key=lambda e: abs(e.rect.centerx - player.rect.centerx))

    def _apply_difficulty_bias(self, now: int, threat_ratio: float) -> None:
        if now - self.last_difficulty_update < 1000:
            return
        self.last_difficulty_update = now
        difficulty = getattr(self.game, "difficulty", "Normal")
        targets = {
            "Easy": (0.35, 0.6),
            "Normal": (0.5, 0.5),
            "Hard": (0.6, 0.45),
            "Elite": (0.7, 0.4),
            "Adaptive": (0.65, 0.45),
        }
        aggression, caution = targets.get(difficulty, (0.5, 0.5))
        if difficulty == "Adaptive":
            player = getattr(self.game, "player", None)
            if player:
                health_ratio = player.health / max(1, player.max_health)
                if health_ratio < 0.4:
                    caution = min(0.8, caution + 0.1)
                elif health_ratio > 0.8:
                    aggression = min(0.8, aggression + 0.05)
        if threat_ratio > 0:
            aggression = min(0.9, aggression + 0.08 * threat_ratio)
            caution = min(0.9, caution + 0.05 * threat_ratio)
        self.tuning.aggression = self._lerp(self.tuning.aggression, aggression, 0.1)
        self.tuning.caution = self._lerp(self.tuning.caution, caution, 0.1)
        if threat_ratio > 0:
            self.tuning.dodge_bias = self._lerp(
                self.tuning.dodge_bias,
                min(0.95, self.tuning.dodge_bias + 0.2 * threat_ratio),
                0.08,
            )
            self.tuning.special_chance = self._lerp(
                self.tuning.special_chance,
                min(0.55, self.tuning.special_chance + 0.12 * threat_ratio),
                0.08,
            )
        self.tuning.clamp()

    @staticmethod
    def _lerp(current: float, target: float, weight: float) -> float:
        return current + (target - current) * weight

    def _select_target(self, player, enemies):
        if not player or not enemies:
            return None
        boss = max(enemies, key=lambda e: getattr(e, "max_health", 0))
        if getattr(boss, "max_health", 0) >= 160:
            return boss
        if self.tuning.aggression > 0.65:
            return min(
                enemies,
                key=lambda e: (
                    getattr(e, "health", 0),
                    abs(e.rect.centerx - player.rect.centerx),
                ),
            )
        return self._nearest_enemy(player, enemies)

    def _select_goal_target(self, player, target, powerups, now: int, threat: float):
        if not player:
            self.last_goal = "idle"
            return None
        health_ratio = player.health / max(1, player.max_health)
        mana_ratio = player.mana / max(1, player.max_mana)
        if getattr(player, "revive_until", 0) > now:
            self.last_goal = "reviving"
            return target
        if powerups and (health_ratio < 0.45 or mana_ratio < 0.25):
            self.last_goal = "recover"
            pick = min(powerups, key=lambda p: abs(p.rect.centerx - player.rect.centerx))
            self._remember_target("PowerUp", abs(pick.rect.centerx - player.rect.centerx))
            return pick
        if self.explore_target and now < self.explore_until:
            if threat < 0.6 or random.random() < 0.35:
                self.last_goal = f"explore:{self.explore_mode}"
                self._remember_target(self.explore_target.name, 0)
                return self.explore_target
        if target:
            dist = abs(target.rect.centerx - player.rect.centerx)
            if health_ratio < 0.3 or threat > 0.6:
                self.last_goal = "kite"
            else:
                self.last_goal = "engage"
            self._remember_target(type(target).__name__, dist)
            return target
        self.last_goal = "explore"
        self._remember_target("None", 0)
        return target

    def _incoming_projectile(self, player, projectiles) -> bool:
        for proj in projectiles:
            if getattr(proj, "visual_only", False):
                continue
            dx = player.rect.centerx - proj.rect.centerx
            closing = (proj.velocity.x > 0 and dx < 0) or (
                proj.velocity.x < 0 and dx > 0
            )
            if proj.rect.colliderect(player.rect.inflate(60, 40)) or (
                closing
                and abs(dx) < 180
                and abs(proj.rect.centery - player.rect.centery) < 40
            ):
                return True
        return False

    def _hazard_ahead(self, player) -> bool:
        hazards = getattr(self.game, "hazards", [])
        if not player or not hazards:
            return False
        if self.explore_mode == "hazard_touch" and pygame.time.get_ticks() < self.explore_until:
            return False
        check_rect = player.rect.move(player.direction * 30, 0)
        for hz in hazards:
            if getattr(hz, "avoid", False) and hz.rect.colliderect(check_rect):
                return True
        return False

    def _maybe_jump(self, actions: set[str], now: int) -> None:
        if now - self.last_jump > 500:
            actions.add("jump")
            self.last_jump = now

    def _near_enemy(self, player, target) -> bool:
        if not player or not target:
            return False
        distance = abs(target.rect.centerx - player.rect.centerx)
        return distance < 70

    def _move_toward_target(
        self,
        player,
        target,
        pressed_keys: set[int],
        now: int,
    ) -> None:
        if not player or not target:
            return
        distance = abs(target.rect.centerx - player.rect.centerx)
        retreat_distance = 70 + int(60 * self.tuning.caution)
        close_enough = distance < retreat_distance
        chase = self.tuning.aggression >= self.tuning.caution
        desired_range = int(
            self.tuning.desired_range
            * (0.85 + 0.35 * (1 - self.tuning.caution))
        )
        if self.last_goal == "kite" and distance < desired_range:
            chase = False
        if close_enough and not chase:
            if target.rect.centerx < player.rect.centerx:
                pressed_keys.add(pygame.K_RIGHT)
            else:
                pressed_keys.add(pygame.K_LEFT)
            return
        if target.rect.centerx < player.rect.centerx - 10:
            pressed_keys.add(pygame.K_LEFT)
        elif target.rect.centerx > player.rect.centerx + 10:
            pressed_keys.add(pygame.K_RIGHT)
        if (
            distance < desired_range
            and now - self.last_strafe > 650
            and random.random() < self.tuning.strafe_chance
        ):
            if random.random() < 0.5:
                pressed_keys.add(pygame.K_LEFT)
            else:
                pressed_keys.add(pygame.K_RIGHT)
            self.last_strafe = now

    def _move_toward_powerup(self, player, powerups, pressed_keys: set[int]) -> None:
        if not powerups:
            return
        target = min(powerups, key=lambda p: abs(p.rect.centerx - player.rect.centerx))
        if target.rect.centerx < player.rect.centerx - 10:
            pressed_keys.add(pygame.K_LEFT)
        elif target.rect.centerx > player.rect.centerx + 10:
            pressed_keys.add(pygame.K_RIGHT)

    def _maybe_use_item(
        self, actions: set[str], player, now: int, threat_ratio: float
    ) -> None:
        threshold = 0.45 + 0.1 * threat_ratio
        if player.health / max(1, player.max_health) < threshold:
            if now - self.last_item > 2500:
                actions.add("use_item")
                self.last_item = now

    def _maybe_use_mana(
        self, actions: set[str], player, now: int, threat_ratio: float
    ) -> None:
        threshold = 0.3 + 0.08 * threat_ratio
        if player.mana / max(1, player.max_mana) < threshold:
            if now - self.last_mana > 3200:
                actions.add("use_mana")
                self.last_mana = now

    def _stage_threat_ratio(self, enemies, hazards) -> float:
        map_name = getattr(self.game, "selected_map", None)
        if hasattr(self.game, "map_manager") and self.game.map_manager.current:
            map_name = self.game.map_manager.current
        if map_name and hasattr(self.game, "_map_preview_data"):
            threat = float(self.game._map_preview_data(map_name).get("threat", 0))
            base = min(1.0, max(0.0, threat / 10.0))
        else:
            base = 0.0
        crowd = min(1.0, len(enemies) / 6) if enemies else 0.0
        hazard_factor = min(1.0, len(hazards) / 6) if hazards else 0.0
        return min(1.0, base + 0.25 * crowd + 0.15 * hazard_factor)

    def _gap_or_edge_risk(self, player, world_width: int) -> bool:
        if not player or world_width <= 0:
            return False
        if player.rect.left < 60 or player.rect.right > world_width - 60:
            return True
        gaps = getattr(player, "ground_gaps", [])
        for gap in gaps:
            if gap[0] <= player.rect.centerx <= gap[1]:
                return True
        return False

    def _avoid_edges(self, player, pressed_keys: set[int], world_width: int) -> None:
        if player.rect.centerx < world_width // 2:
            pressed_keys.add(pygame.K_RIGHT)
        else:
            pressed_keys.add(pygame.K_LEFT)

    def _remember_target(self, name: str, distance: int) -> None:
        self.last_target_name = name
        self.last_target_distance = distance

    def _maybe_set_explore_mode(
        self,
        now: int,
        player,
        hazards,
        platforms,
        world_width: int,
    ) -> None:
        if not getattr(self.game, "autoplay_explorer", False):
            self.explore_mode = "none"
            self.explore_until = 0
            self.explore_target = None
            return
        if now < self.explore_until:
            return
        modes = ["platform_high", "platform_low", "edge_left", "edge_right"]
        if hazards:
            modes.append("hazard_touch")
        if getattr(self.game, "powerups", []):
            modes.append("powerup")
        self.explore_mode = random.choice(modes)
        self.explore_until = now + random.randint(3500, 6500)
        self.explore_target = self._select_explore_target(
            player, hazards, platforms, world_width
        )
        if hasattr(self.game, "_autoplay_trace"):
            self.game._autoplay_trace(f"Explore -> {self.explore_mode}", now=now)

    def _select_explore_target(self, player, hazards, platforms, world_width: int):
        if not player:
            return None
        if self.explore_mode == "edge_left":
            rect = pygame.Rect(30, player.rect.centery, 10, 10)
            return _AutoTarget(rect, "EdgeL")
        if self.explore_mode == "edge_right" and world_width:
            rect = pygame.Rect(world_width - 30, player.rect.centery, 10, 10)
            return _AutoTarget(rect, "EdgeR")
        if self.explore_mode == "hazard_touch" and hazards:
            hazard = random.choice(hazards)
            return _AutoTarget(hazard.rect, "Hazard")
        if self.explore_mode == "powerup":
            powerups = getattr(self.game, "powerups", [])
            if powerups:
                pick = random.choice(list(powerups))
                return _AutoTarget(pick.rect, "PowerUp")
        if platforms:
            sorted_plats = sorted(platforms, key=lambda p: p.rect.centery)
            if self.explore_mode == "platform_high":
                plat = sorted_plats[0]
            else:
                plat = sorted_plats[-1]
            return _AutoTarget(plat.rect, "Platform")
        return None

    def _maybe_force_feature_tests(self, actions: set[str], now: int, player) -> None:
        force_audit = getattr(self.game, "autoplay_skill_audit_force", False)
        if not getattr(self.game, "autoplay_explorer", False) and not force_audit:
            return
        counts = getattr(self.game, "autoplay_feature_counts", {})
        if counts.get("action:special", 0) < 2 and player.mana > 25:
            actions.add("special")
        if counts.get("action:parry", 0) < 2 and now - self.last_block > 900:
            actions.add("parry")
        if counts.get("action:dodge", 0) < 2 and now - self.last_dodge > 650:
            actions.add("dodge")
            self.last_dodge = now
        if counts.get("action:block", 0) < 2 and now - self.last_block > 900:
            actions.add("block")
            self.last_block = now
        if counts.get("action:jump", 0) < 2 and now - self.last_jump > 600:
            actions.add("jump")
            self.last_jump = now
        if not force_audit:
            return
        missing: list[str] = []
        missing_fn = getattr(self.game, "_autoplay_character_missing_actions", None)
        if callable(missing_fn):
            missing = list(missing_fn())
        if "special" in missing and player.mana > 25 and now - self.last_special > 1200:
            actions.add("special")
            self.last_special = now
        if "parry" in missing and now - self.last_block > 900:
            actions.add("parry")
            self.last_block = now
        if "dodge" in missing and now - self.last_dodge > 650:
            actions.add("dodge")
            self.last_dodge = now
        if "block" in missing and now - self.last_block > 900:
            actions.add("block")
            self.last_block = now
        if "jump" in missing and now - self.last_jump > 600:
            actions.add("jump")
            self.last_jump = now
        if "sprint" in missing and now - self.last_sprint > 800:
            actions.add("sprint")
            self.last_sprint = now
        if "shoot" in missing and now - self.last_shoot > 400:
            actions.add("shoot")
            self.last_shoot = now
        if "melee" in missing and now - self.last_melee > 500:
            actions.add("melee")
            self.last_melee = now
        if "use_item" in missing and now - self.last_item > 2500:
            actions.add("use_item")
            self.last_item = now
        if "use_mana" in missing and now - self.last_mana > 3200:
            actions.add("use_mana")
            self.last_mana = now
        for action in missing:
            if action in {
                "special",
                "parry",
                "dodge",
                "block",
                "jump",
                "sprint",
                "shoot",
                "melee",
                "use_item",
                "use_mana",
            }:
                continue
            if now - self.last_special > 900:
                actions.add(action)
                self.last_special = now
