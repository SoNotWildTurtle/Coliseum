"""Combat related helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from .damage_manager import DamageManager
from .damage_number import DamageNumber
from .status_effects import (
    StatusEffectManager,
    FreezeEffect,
    SlowEffect,
    PoisonEffect,
    BurnEffect,
    StunEffect,
)

if TYPE_CHECKING:  # pragma: no cover
    from .team_manager import TeamManager


class CombatManager:
    """Manage combat turns and collision handling."""

    def __init__(
        self,
        status_manager: StatusEffectManager | None = None,
        team_manager: "TeamManager" | None = None,
        sound_manager: object | None = None,
    ) -> None:
        self.participants: list = []
        self.index = 0
        self.status_manager = status_manager or StatusEffectManager()
        self.team_manager = team_manager
        self.damage_manager = DamageManager()
        self.sound_manager = sound_manager
        self.last_enemy_damage = 0
        self.event_sink = None

    def add(self, actor) -> None:
        """Add a combatant to the turn list."""
        self.participants.append(actor)

    def _is_invincible(self, actor, now: int) -> bool:
        return (
            getattr(actor, "invincible", False)
            or getattr(actor, "dodging", False)
            or now < getattr(actor, "invincible_until", 0)
        )

    def remove(self, actor) -> None:
        if actor in self.participants:
            self.participants.remove(actor)

    def next_actor(self):
        """Return the next actor in the turn order."""
        if not self.participants:
            return None
        actor = self.participants[self.index % len(self.participants)]
        self.index += 1
        return actor

    def handle_collisions(
        self,
        player,
        enemies,
        projectiles,
        melee_attacks,
        now: int,
        allies: pygame.sprite.Group | None = None,
        damage_numbers: pygame.sprite.Group | None = None,
    ) -> list:
        """Process projectile and melee collisions.

        Returns a list of enemies killed so the caller can update score and
        roll for loot. If ``damage_numbers`` is provided floating indicators are
        spawned for each hit.
        """
        killed_enemies: list = []
        allies = allies or pygame.sprite.Group()
        for proj in list(projectiles):
            if getattr(proj, "visual_only", False):
                continue
            if getattr(proj, "from_enemy", False):
                targets = [player] + list(allies)
                for target in targets:
                    if target is None:
                        continue
                    if (
                        self.team_manager
                        and getattr(proj, "owner", None)
                        and self.team_manager.are_allies(proj.owner, target)
                    ):
                        proj.kill()
                        break
                    if target.rect.colliderect(proj.rect):
                        if (
                            getattr(target, "shield_active", False)
                            or self._is_invincible(target, now)
                        ):
                            proj.kill()
                        else:
                            base = getattr(proj, "attack", 10)
                            dmg, critical = self.damage_manager.calculate(
                                base,
                                target.stats.get("defense"),
                                crit_chance=getattr(proj, "crit_chance", 0),
                                crit_multiplier=getattr(proj, "crit_multiplier", 2),
                                return_crit=True,
                            )
                            target.last_hit_critical = critical
                            target.last_hit_difficulty_scale = self._impact_scale(
                                getattr(proj, "owner", None)
                            )
                            if hasattr(proj, "vfx_intensity"):
                                proj.vfx_intensity = self._vfx_intensity(
                                    getattr(proj, "owner", None)
                                )
                            self._apply_knockback(
                                getattr(proj, "owner", None) or player,
                                target,
                                getattr(proj, "knockback", 0.0),
                            )
                            self._apply_damage(
                                getattr(proj, "owner", None) or player,
                                target,
                                dmg,
                                kind="projectile",
                                critical=critical,
                            )
                            self._play_hit_sfx(dmg, critical)
                            if damage_numbers is not None:
                                damage_numbers.add(
                                    DamageNumber(dmg, target.rect.center, critical)
                                )
                            proj.kill()
                        break
                continue
            hits = pygame.sprite.spritecollide(proj, enemies, False)
            if hits:
                attacker = getattr(proj, "owner", None) or player
                for enemy in hits:
                    if (
                        self.team_manager
                        and getattr(proj, "owner", None)
                        and self.team_manager.are_allies(proj.owner, enemy)
                    ):
                        continue
                    if getattr(proj, "grapple", False):
                        enemy.rect.centerx = player.rect.centerx
                        enemy.pos.x = enemy.rect.x
                    else:
                        mult = 0.5 if (
                            getattr(proj, "freeze", False)
                            or getattr(proj, "slow", False)
                            or getattr(proj, "poison", False)
                            or getattr(proj, "burn", False)
                            or getattr(proj, "stun", False)
                        ) else 1.0
                        if getattr(proj, "freeze", False):
                            self.status_manager.add_effect(enemy, FreezeEffect())
                        elif getattr(proj, "slow", False):
                            self.status_manager.add_effect(enemy, SlowEffect())
                        elif getattr(proj, "poison", False):
                            self.status_manager.add_effect(enemy, PoisonEffect())
                        elif getattr(proj, "burn", False):
                            self.status_manager.add_effect(enemy, BurnEffect())
                        elif getattr(proj, "stun", False):
                            self.status_manager.add_effect(enemy, StunEffect())
                        base = attacker.stats.get("attack")
                        dmg, critical = self.damage_manager.calculate(
                            base,
                            enemy.stats.get("defense"),
                            multiplier=mult,
                            crit_chance=getattr(proj, "crit_chance", 0),
                            crit_multiplier=getattr(proj, "crit_multiplier", 2),
                            return_crit=True,
                        )
                        enemy.last_hit_critical = critical
                        enemy.last_hit_difficulty_scale = self._impact_scale(attacker)
                        if hasattr(proj, "vfx_intensity"):
                            proj.vfx_intensity = self._vfx_intensity(attacker)
                        self._apply_knockback(
                            attacker,
                            enemy,
                            getattr(proj, "knockback", 0.0),
                        )
                        self._apply_damage(
                            attacker,
                            enemy,
                            dmg,
                            kind="projectile",
                            critical=critical,
                        )
                        self._play_hit_sfx(dmg, critical)
                        if damage_numbers is not None:
                            damage_numbers.add(
                                DamageNumber(dmg, enemy.rect.center, critical)
                            )
                    if enemy.health == 0:
                        enemy.kill()
                        killed_enemies.append(enemy)
                if not getattr(proj, "pierce", False):
                    proj.kill()
        for attack in list(melee_attacks):
            if getattr(attack, "from_enemy", False):
                targets = [player] + list(allies)
                handled = False
                for target in targets:
                    if target is None:
                        continue
                    if (
                        self.team_manager
                        and getattr(attack, "owner", None)
                        and self.team_manager.are_allies(attack.owner, target)
                    ):
                        attack.kill()
                        handled = True
                        break
                    if attack.rect.colliderect(target.rect):
                        if not self._is_invincible(target, now):
                            base = getattr(attack, "attack", 0) or 5
                            dmg, critical = self.damage_manager.calculate(
                                base,
                                target.stats.get("defense"),
                                crit_chance=getattr(attack, "crit_chance", 0),
                                crit_multiplier=getattr(attack, "crit_multiplier", 2),
                                return_crit=True,
                            )
                            target.last_hit_critical = critical
                            target.last_hit_difficulty_scale = self._impact_scale(
                                getattr(attack, "owner", None)
                            )
                            self._apply_knockback(
                                getattr(attack, "owner", None) or player,
                                target,
                                getattr(attack, "knockback", 0.0),
                                stagger_ms=self._stagger_duration(
                                    dmg, critical, base_ms=80
                                ),
                            )
                            self._apply_damage(
                                getattr(attack, "owner", None) or player,
                                target,
                                dmg,
                                kind="melee",
                                critical=critical,
                            )
                            self._play_hit_sfx(dmg, critical)
                            if damage_numbers is not None:
                                damage_numbers.add(
                                    DamageNumber(dmg, target.rect.center, critical)
                                )
                        attack.kill()
                        handled = True
                        break
                if not handled:
                    attack.kill()
                continue
            hits = pygame.sprite.spritecollide(attack, enemies, False)
            if hits:
                attacker = getattr(attack, "owner", None) or player
                for enemy in hits:
                    if (
                        self.team_manager
                        and getattr(attack, "owner", None)
                        and self.team_manager.are_allies(attack.owner, enemy)
                    ):
                        continue
                    base = attacker.stats.get("attack") + 5
                    dmg, critical = self.damage_manager.calculate(
                        base,
                        enemy.stats.get("defense"),
                        crit_chance=getattr(attack, "crit_chance", 0),
                        crit_multiplier=getattr(attack, "crit_multiplier", 2),
                        return_crit=True,
                    )
                    enemy.last_hit_critical = critical
                    enemy.last_hit_difficulty_scale = self._impact_scale(attacker)
                    self._apply_knockback(
                        attacker,
                        enemy,
                        getattr(attack, "knockback", 0.0),
                        stagger_ms=self._stagger_duration(dmg, critical, base_ms=80),
                    )
                    self._apply_damage(
                        attacker,
                        enemy,
                        dmg,
                        kind="melee",
                        critical=critical,
                    )
                    self._play_hit_sfx(dmg, critical)
                    if damage_numbers is not None:
                        damage_numbers.add(
                            DamageNumber(dmg, enemy.rect.center, critical)
                        )
                    if enemy.health == 0:
                        enemy.kill()
                        killed_enemies.append(enemy)
            attack.kill()
        targets = [player] + list(allies)
        for target in targets:
            colliding = pygame.sprite.spritecollideany(target, enemies)
            if colliding and now - self.last_enemy_damage >= 500:
                if self.team_manager and self.team_manager.are_allies(colliding, target):
                    self.last_enemy_damage = now
                elif not self._is_invincible(target, now):
                    base = colliding.stats.get("attack")
                    dmg, critical = self.damage_manager.calculate(
                        base,
                        target.stats.get("defense"),
                        crit_chance=colliding.stats.get("crit_chance"),
                        crit_multiplier=colliding.stats.get("crit_multiplier"),
                        return_crit=True,
                    )
                    target.last_hit_critical = critical
                    target.last_hit_difficulty_scale = self._impact_scale(colliding)
                    self._apply_knockback(
                        colliding,
                        target,
                        getattr(colliding, "touch_knockback", 1.5),
                        stagger_ms=self._stagger_duration(dmg, critical, base_ms=50),
                    )
                    self._apply_damage(
                        colliding,
                        target,
                        dmg,
                        kind="contact",
                        critical=critical,
                    )
                    self._play_hit_sfx(dmg, critical)
                    if damage_numbers is not None:
                        damage_numbers.add(
                            DamageNumber(dmg, target.rect.center, critical)
                        )
                self.last_enemy_damage = now
        return killed_enemies

    def _play_hit_sfx(self, damage: int, critical: bool) -> None:
        if self.sound_manager is None:
            return
        event = "hit_light"
        if critical:
            event = "hit_crit"
        elif damage >= 18:
            event = "hit_heavy"
        if hasattr(self.sound_manager, "play_event"):
            self.sound_manager.play_event(event)

    def _apply_damage(
        self,
        attacker,
        target,
        damage: int,
        *,
        kind: str,
        critical: bool,
    ) -> None:
        hp_before = float(getattr(target, "health", 0))
        target.take_damage(damage)
        sink = self.event_sink
        if callable(sink):
            sink(
                {
                    "type": "damage",
                    "payload": {
                        "attacker_id": attacker.__class__.__name__
                        if attacker is not None
                        else "unknown",
                        "target_id": target.__class__.__name__,
                        "amount": float(damage),
                        "kind": kind,
                        "critical": bool(critical),
                        "hp_before": hp_before,
                        "hp_after": float(getattr(target, "health", 0)),
                    },
                }
            )

    @staticmethod
    def _apply_knockback(
        attacker,
        target,
        strength: float,
        *,
        stagger_ms: int = 0,
    ) -> None:
        if not strength:
            return
        if not hasattr(target, "velocity"):
            return
        scale = CombatManager._difficulty_scale(attacker)
        strength *= scale
        if attacker is None or not hasattr(attacker, "rect"):
            direction = 1
        else:
            direction = 1 if target.rect.centerx >= attacker.rect.centerx else -1
        target.velocity.x += strength * direction
        if hasattr(target.velocity, "x"):
            cap = 8.0
            if scale > 1.0:
                cap = min(10.0, 8.0 + (scale - 1.0) * 2.0)
            target.velocity.x = max(-cap, min(cap, target.velocity.x))
        if stagger_ms and hasattr(target, "stagger_until"):
            now = pygame.time.get_ticks()
            target.stagger_until = max(
                int(getattr(target, "stagger_until", 0)),
                now + int(stagger_ms * scale),
            )

    @staticmethod
    def _stagger_duration(damage: int, critical: bool, *, base_ms: int) -> int:
        bonus = min(70, int(max(0, damage) * 1.5))
        if critical:
            bonus += 30
        return min(140, base_ms + bonus)

    @staticmethod
    def _difficulty_scale(attacker) -> float:
        diff = str(getattr(attacker, "difficulty", "Normal"))
        return {
            "Easy": 0.85,
            "Normal": 1.0,
            "Hard": 1.1,
            "Elite": 1.2,
            "Adaptive": 1.15,
        }.get(diff, 1.0)

    @staticmethod
    def _weapon_impact_scale(attacker) -> float:
        weapon = str(getattr(attacker, "weapon_sfx_event", "") or "")
        return {
            "sword": 1.0,
            "axe": 1.15,
            "spear": 1.05,
            "bow": 0.9,
            "wand": 0.95,
            "weapon": 1.0,
        }.get(weapon, 1.0)

    @staticmethod
    def _impact_scale(attacker) -> float:
        scale = CombatManager._difficulty_scale(attacker)
        scale *= CombatManager._weapon_impact_scale(attacker)
        return max(0.75, min(1.5, scale))

    @staticmethod
    def _vfx_intensity(attacker) -> float:
        scale = CombatManager._difficulty_scale(attacker)
        return max(0.8, min(1.35, 0.9 + (scale - 1.0) * 1.4))
