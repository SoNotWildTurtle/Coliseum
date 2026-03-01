"""Manage ally entities and their behavior."""

from __future__ import annotations

from typing import Iterable

import pygame

from .healing_zone import HealingZone
from .status_effects import ShieldEffect, SpeedEffect, StatusEffectManager

class AllyManager:
    """Coordinate AI updates for friendly NPC allies."""

    def __init__(self, allies) -> None:
        self.allies = allies

    def update(
        self,
        player,
        enemies,
        hazards,
        projectiles,
        ground_y: int,
        now: int,
        *,
        status_manager: StatusEffectManager | None = None,
    ):
        new_projectiles = []
        new_melees = []
        support_zones: list[HealingZone] = []
        support_messages: list[tuple[str, tuple[int, int]]] = []
        self._assign_roles_and_stances(player, enemies, now)
        for ally in list(self.allies):
            if getattr(ally, "health", 1) <= 0 and getattr(ally, "lives", 0) == 0:
                ally.kill()
                continue
            ally.hazards = hazards
            target = self._select_target(ally, enemies, player)
            self._reposition_support(ally, player, target, now)
            if hasattr(ally, "handle_ai") and target is not None:
                proj, melee = ally.handle_ai(target, now, hazards, projectiles)
                if proj:
                    new_projectiles.append((ally, proj))
                if melee:
                    new_melees.append((ally, melee))
            else:
                if target is not None:
                    direction = 1 if target.rect.centerx > ally.rect.centerx else -1
                    ally.velocity.x = direction
            if status_manager is not None:
                zone, message = self._support_action(
                    ally, player, now, status_manager
                )
                if zone is not None:
                    support_zones.append(zone)
                if message is not None:
                    support_messages.append(message)
            ally.update(ground_y, now)
        return new_projectiles, new_melees, support_zones, support_messages

    @staticmethod
    def _select_target(ally, enemies, player):
        if enemies:
            if player is not None and getattr(ally, "protect_player", False):
                max_health = getattr(player, "max_health", 0) or 1
                ratio = getattr(player, "health", 0) / max_health
                threshold = float(getattr(ally, "protect_player_threshold", 0.5))
                if ratio <= threshold:
                    return min(
                        enemies,
                        key=lambda enemy: abs(
                            enemy.rect.centerx - player.rect.centerx
                        ),
                    )
            cc_targets = [
                enemy for enemy in enemies if AllyManager._crowd_control_score(enemy)
            ]
            if cc_targets:
                return min(
                    cc_targets,
                    key=lambda enemy: abs(enemy.rect.centerx - ally.rect.centerx),
                )
            focus_low = getattr(ally, "focus_low_health", False)
            if focus_low:
                threshold = float(getattr(ally, "focus_threshold", 0.4))
                focus_range = float(getattr(ally, "focus_range", 240))
                low_targets = []
                for enemy in enemies:
                    max_health = getattr(enemy, "max_health", 0)
                    if not max_health:
                        continue
                    ratio = getattr(enemy, "health", 0) / max_health
                    dist = abs(enemy.rect.centerx - ally.rect.centerx)
                    if ratio <= threshold and dist <= focus_range:
                        low_targets.append(enemy)
                if low_targets:
                    return min(
                        low_targets,
                        key=lambda enemy: abs(enemy.rect.centerx - ally.rect.centerx),
                    )
            return min(
                enemies,
                key=lambda enemy: abs(enemy.rect.centerx - ally.rect.centerx),
            )
        return player

    def _support_action(
        self,
        ally,
        player,
        now: int,
        status_manager: StatusEffectManager,
    ) -> tuple[HealingZone | None, tuple[str, tuple[int, int]] | None]:
        if player is None or not hasattr(player, "health"):
            return None, None
        last_time = int(getattr(ally, "support_last_time", -99999))
        cooldown = int(getattr(ally, "support_cooldown_ms", 6000))
        if now - last_time < cooldown:
            return None, None
        max_health = max(1, int(getattr(player, "max_health", 1)))
        health = int(getattr(player, "health", 0))
        ratio = health / max_health
        shield_threshold = float(getattr(ally, "support_shield_threshold", 0.3))
        heal_threshold = float(getattr(ally, "support_heal_threshold", 0.55))
        if ratio <= shield_threshold:
            status_manager.add_effect(player, ShieldEffect(duration_ms=1200))
            status_manager.add_effect(player, SpeedEffect(duration_ms=1200, factor=1.4))
            ally.support_last_time = now
            pos = (player.rect.centerx, player.rect.top - 26)
            return None, ("Ally Shield!", pos)
        if ratio <= heal_threshold:
            rect = pygame.Rect(
                player.rect.centerx - 40,
                player.rect.centery - 25,
                80,
                50,
            )
            zone = HealingZone(rect, heal_rate=2, duration=70)
            ally.support_last_time = now
            pos = (player.rect.centerx, player.rect.top - 26)
            return zone, ("Ally Heal!", pos)
        return None, None

    @staticmethod
    def _reposition_support(ally, player, target, now: int) -> None:
        if player is None or target is None:
            return
        if not getattr(ally, "protect_player", False):
            return
        hazards = getattr(ally, "hazards", None)
        avoid_hazards = bool(getattr(ally, "avoid_hazards", True))
        max_health = getattr(player, "max_health", 0) or 1
        ratio = getattr(player, "health", 0) / max_health
        threshold = float(getattr(ally, "protect_player_threshold", 0.6))
        if ratio > threshold:
            return
        ally_x = ally.rect.centerx
        player_x = player.rect.centerx
        target_x = target.rect.centerx
        desired = player_x + (target_x - player_x) * 0.35
        if avoid_hazards and hazards:
            for hz in hazards:
                if not getattr(hz, "avoid", False):
                    continue
                if hz.rect.colliderect(ally.rect.inflate(10, 10)):
                    desired = player_x
                    break
        delta = desired - ally_x
        if abs(delta) < 6:
            ally.velocity.x *= 0.5
            return
        ally.velocity.x = 1 if delta > 0 else -1
        ally.direction = 1 if delta > 0 else -1

    def _assign_roles_and_stances(self, player, enemies, now: int) -> None:
        allies = list(self.allies)
        if not allies:
            return
        role_plan = self._role_plan(len(allies))
        assignments: dict[object, str] = {}
        available = list(role_plan)
        for ally in allies:
            if getattr(ally, "role_locked", False):
                role = getattr(ally, "role", None)
                if role in available:
                    assignments[ally] = role
                    available.remove(role)
        for ally in allies:
            if ally in assignments:
                continue
            role = getattr(ally, "role", None)
            if role in available:
                assignments[ally] = role
                available.remove(role)
        for ally in allies:
            if ally in assignments:
                continue
            role = available.pop(0) if available else "intercept"
            assignments[ally] = role
        enemy_count = len(enemies or [])
        max_health = getattr(player, "max_health", 0) or 1
        health_ratio = (
            getattr(player, "health", max_health) / max_health
            if player
            else 1.0
        )
        for ally, role in assignments.items():
            if not getattr(ally, "role_locked", False):
                self._maybe_switch_role(ally, role, now)
            stance = self._select_stance(role, health_ratio, enemy_count)
            if not getattr(ally, "stance_locked", False):
                self._maybe_switch_stance(ally, stance, now)
            ally.protect_player = role in {"tank", "support"}
            self._apply_role_bias(ally, role, getattr(ally, "stance", "balanced"))

    @staticmethod
    def _role_plan(count: int) -> list[str]:
        if count <= 1:
            return ["intercept"]
        if count == 2:
            return ["tank", "intercept"]
        return ["tank", "support"] + ["intercept"] * (count - 2)

    @staticmethod
    def _select_stance(role: str, health_ratio: float, enemy_count: int) -> str:
        if health_ratio <= 0.35:
            return "defensive" if role in {"tank", "support"} else "intercept"
        if enemy_count >= 4:
            if role == "support":
                return "defensive"
            if role == "tank":
                return "balanced"
            return "aggressive"
        if health_ratio >= 0.7:
            if role == "tank":
                return "defensive"
            if role == "support":
                return "balanced"
            return "aggressive"
        return "balanced"

    @staticmethod
    def _maybe_switch_role(ally, role: str, now: int) -> None:
        last = int(getattr(ally, "role_last_switch", -99999))
        cooldown = int(getattr(ally, "role_switch_cooldown_ms", 3500))
        if role != getattr(ally, "role", None) and now - last >= cooldown:
            ally.role = role
            ally.role_last_switch = now

    @staticmethod
    def _maybe_switch_stance(ally, stance: str, now: int) -> None:
        last = int(getattr(ally, "stance_last_switch", -99999))
        cooldown = int(getattr(ally, "stance_switch_cooldown_ms", 2500))
        if stance != getattr(ally, "stance", None) and now - last >= cooldown:
            ally.stance = stance
            ally.stance_last_switch = now

    @staticmethod
    def _apply_role_bias(ally, role: str, stance: str) -> None:
        role_bias = {
            "tank": {
                "hold_distance": 70,
                "melee_prob": 1.0,
                "shoot_prob": 0.6,
                "block_prob": 0.35,
                "dodge_prob": 0.4,
                "retreat_threshold": 0.2,
            },
            "support": {
                "hold_distance": 170,
                "melee_prob": 0.6,
                "shoot_prob": 1.0,
                "block_prob": 0.2,
                "dodge_prob": 0.35,
                "retreat_threshold": 0.45,
                "special_prob": 0.12,
            },
            "intercept": {
                "hold_distance": 110,
                "melee_prob": 0.9,
                "shoot_prob": 0.9,
                "block_prob": 0.2,
                "dodge_prob": 0.35,
                "retreat_threshold": 0.3,
            },
        }
        stance_bias = {
            "aggressive": {
                "speed": 0.15,
                "melee_prob": 0.15,
                "shoot_prob": 0.1,
                "special_prob": 0.04,
            },
            "defensive": {
                "hold_distance": 25,
                "block_prob": 0.2,
                "dodge_prob": 0.1,
                "speed": -0.05,
                "retreat_threshold": 0.1,
            },
        }
        base = dict(role_bias.get(role, {}))
        for key, value in stance_bias.get(stance, {}).items():
            if key in base and isinstance(base[key], (int, float)):
                base[key] = base[key] + value
            else:
                base[key] = value
        ally.ai_bias = base

    @staticmethod
    def _crowd_control_score(target) -> float:
        if getattr(target, "stunned", False):
            return 1.0
        if getattr(target, "silenced", False):
            return 0.5
        speed_factor = float(getattr(target, "speed_factor", 1.0) or 1.0)
        if speed_factor < 0.75:
            return 0.4
        return 0.0
