"""Hazard orchestration and lifecycle management."""

class HazardManager:
    """Manage hazard sprites, apply effects, and log interactions."""

    def __init__(self, status_manager=None, analytics=None, objective_manager=None):
        import pygame

        self.hazards = pygame.sprite.Group()
        self.last_damage = 0
        self.status_manager = status_manager
        self.damage_multiplier = 1.0
        self.analytics = analytics
        self.objective_manager = objective_manager

    def set_damage_multiplier(self, multiplier: float) -> None:
        """Scale hazard damage to match global event modifiers."""

        self.damage_multiplier = max(0.0, multiplier)

    def set_analytics(self, analytics) -> None:
        """Attach an analytics manager to record hazard interactions."""

        self.analytics = analytics

    def set_objective_manager(self, objective_manager) -> None:
        """Attach an objective manager to advance hazard-related goals."""

        self.objective_manager = objective_manager

    def _record_hazard(self, hazard, label: str | None = None) -> None:
        """Forward hazard interactions to the analytics manager if present."""

        name = label or getattr(hazard, "hazard_label", hazard.__class__.__name__.lower())
        if self.analytics:
            record = getattr(self.analytics, "record_hazard", None)
            if callable(record):
                record(name)
        if self.objective_manager:
            recorder = getattr(self.objective_manager, "record_event", None)
            if callable(recorder):
                recorder("hazard_logged")

    def _scaled_damage(self, base: int) -> int:
        """Return hazard ``base`` damage adjusted by the multiplier."""

        if base <= 0:
            return 0
        scaled = int(round(base * self.damage_multiplier))
        return max(1, scaled)

    def load_from_data(self, hazard_data):
        """Create hazard sprites from map metadata."""
        import pygame
        from .hazards import (
            SpikeTrap,
            IceZone,
            LavaZone,
            AcidPool,
            PoisonZone,
            SilenceZone,
            FireZone,
            FrostZone,
            QuicksandZone,
            LightningZone,
            BouncePad,
            TeleportPad,
            WindZone,
            RegenZone,
        )
        self.hazards.empty()
        hazard_map = {
            "spike": SpikeTrap,
            "ice": IceZone,
            "lava": LavaZone,
            "acid": AcidPool,
            "poison": PoisonZone,
            "silence": SilenceZone,
            "fire": FireZone,
            "frost": FrostZone,
            "quicksand": QuicksandZone,
            "lightning": LightningZone,
            "bounce": BouncePad,
            "teleport": TeleportPad,
            "wind": WindZone,
            "regen": RegenZone,
        }
        for hd in hazard_data:
            rect = pygame.Rect(*hd["rect"])
            label = hd.get("type", "spike")
            cls = hazard_map.get(label, SpikeTrap)
            if cls is TeleportPad:
                hz = cls(rect, tuple(hd.get("target", (0, 0))))
            elif cls is WindZone:
                hz = cls(rect, hd.get("force", 2.0))
            elif cls is LightningZone:
                hz = cls(
                    rect,
                    hd.get("damage", 4),
                    hd.get("interval", 400),
                    hd.get("force", -8),
                )
            else:
                hz = cls(rect)
            setattr(hz, "hazard_label", label)
            self.hazards.add(hz)

    def apply_to_player(self, player, now):
        import pygame
        from .hazards import (
            SpikeTrap,
            IceZone,
            LavaZone,
            AcidPool,
            PoisonZone,
            SilenceZone,
            FireZone,
            FrostZone,
            QuicksandZone,
            LightningZone,
            BouncePad,
            TeleportPad,
            WindZone,
            RegenZone,
        )
        hz = pygame.sprite.spritecollideany(player, self.hazards)
        if hz:
            if isinstance(hz, SpikeTrap) and now - self.last_damage >= 500:
                self._record_hazard(hz, "spike")
                player.take_damage(self._scaled_damage(hz.damage))
                self.last_damage = now
            elif isinstance(hz, LavaZone) and now - self.last_damage >= hz.interval:
                self._record_hazard(hz, "lava")
                player.take_damage(self._scaled_damage(hz.damage))
                self.last_damage = now
            elif isinstance(hz, AcidPool) and now - self.last_damage >= hz.interval:
                self._record_hazard(hz, "acid")
                player.take_damage(self._scaled_damage(hz.damage))
                player.set_friction_multiplier(hz.friction)
                self.last_damage = now
                return
            elif isinstance(hz, LightningZone) and now - self.last_damage >= hz.interval:
                self._record_hazard(hz, "lightning")
                player.take_damage(self._scaled_damage(hz.damage))
                player.velocity.y = hz.force
                player.on_ground = False
                self.last_damage = now
            elif (
                isinstance(hz, FrostZone)
                and self.status_manager
                and now - self.last_damage >= 500
            ):
                from .status_effects import FreezeEffect
                self._record_hazard(hz, "frost")
                self.status_manager.add_effect(
                    player, FreezeEffect(hz.duration, start_time=now)
                )
                self.last_damage = now
            elif isinstance(hz, FireZone) and self.status_manager and now - self.last_damage >= 500:
                from .status_effects import BurnEffect
                self._record_hazard(hz, "fire")
                self.status_manager.add_effect(player, BurnEffect())
                self.last_damage = now
            elif isinstance(hz, PoisonZone) and self.status_manager and now - self.last_damage >= 500:
                from .status_effects import PoisonEffect
                self._record_hazard(hz, "poison")
                self.status_manager.add_effect(player, PoisonEffect())
                self.last_damage = now
            elif isinstance(hz, SilenceZone) and self.status_manager and now - self.last_damage >= 500:
                from .status_effects import SilenceEffect
                self._record_hazard(hz, "silence")
                self.status_manager.add_effect(player, SilenceEffect(hz.duration))
                self.last_damage = now
            elif isinstance(hz, QuicksandZone):
                self._record_hazard(hz, "quicksand")
                player.velocity.y += hz.pull
                player.set_friction_multiplier(hz.friction)
                return
            elif isinstance(hz, BouncePad):
                self._record_hazard(hz, "bounce")
                player.velocity.y = hz.force
                player.on_ground = False
            elif isinstance(hz, TeleportPad):
                self._record_hazard(hz, "teleport")
                player.rect.topleft = hz.target
                player.velocity.xy = (0, 0)
                player.on_ground = False
            elif isinstance(hz, WindZone):
                self._record_hazard(hz, "wind")
                player.velocity.x += hz.force
            elif isinstance(hz, RegenZone) and now - self.last_damage >= hz.interval:
                self._record_hazard(hz, "regen")
                player.health = player.health_manager.heal(hz.heal)
                self.last_damage = now
            elif isinstance(hz, IceZone):
                self._record_hazard(hz, "ice")
                player.set_friction_multiplier(hz.friction)
                return
        player.set_friction_multiplier(1.0)

    def apply_to_enemy(self, enemy, now):
        import pygame
        from .hazards import (
            SpikeTrap,
            LavaZone,
            AcidPool,
            PoisonZone,
            SilenceZone,
            FireZone,
            FrostZone,
            QuicksandZone,
            LightningZone,
            BouncePad,
            TeleportPad,
            WindZone,
            RegenZone,
        )
        hz = pygame.sprite.spritecollideany(enemy, self.hazards)
        if isinstance(hz, SpikeTrap):
            self._record_hazard(hz, "spike")
            enemy.take_damage(self._scaled_damage(hz.damage))
            if enemy.health == 0:
                enemy.kill()
                return True
        elif isinstance(hz, LavaZone) and now - self.last_damage >= hz.interval:
            self._record_hazard(hz, "lava")
            enemy.take_damage(self._scaled_damage(hz.damage))
            self.last_damage = now
        elif isinstance(hz, AcidPool) and now - self.last_damage >= hz.interval:
            self._record_hazard(hz, "acid")
            enemy.take_damage(self._scaled_damage(hz.damage))
            self.last_damage = now
        elif isinstance(hz, LightningZone) and now - self.last_damage >= hz.interval:
            self._record_hazard(hz, "lightning")
            enemy.take_damage(self._scaled_damage(hz.damage))
            enemy.velocity.y = hz.force
            enemy.on_ground = False
            self.last_damage = now
        elif isinstance(hz, FrostZone) and self.status_manager and now - self.last_damage >= 500:
            from .status_effects import FreezeEffect
            self._record_hazard(hz, "frost")
            self.status_manager.add_effect(enemy, FreezeEffect(hz.duration))
            self.last_damage = now
        elif isinstance(hz, FireZone) and self.status_manager and now - self.last_damage >= 500:
            from .status_effects import BurnEffect
            self._record_hazard(hz, "fire")
            self.status_manager.add_effect(enemy, BurnEffect())
            self.last_damage = now
        elif isinstance(hz, PoisonZone) and self.status_manager and now - self.last_damage >= 500:
            from .status_effects import PoisonEffect
            self._record_hazard(hz, "poison")
            self.status_manager.add_effect(enemy, PoisonEffect())
            self.last_damage = now
        elif isinstance(hz, SilenceZone) and self.status_manager and now - self.last_damage >= 500:
            from .status_effects import SilenceEffect
            self._record_hazard(hz, "silence")
            self.status_manager.add_effect(enemy, SilenceEffect(hz.duration))
            self.last_damage = now
        elif isinstance(hz, QuicksandZone):
            self._record_hazard(hz, "quicksand")
            enemy.velocity.y += hz.pull
        elif isinstance(hz, BouncePad):
            self._record_hazard(hz, "bounce")
            enemy.velocity.y = hz.force
            enemy.on_ground = False
        elif isinstance(hz, TeleportPad):
            self._record_hazard(hz, "teleport")
            enemy.rect.topleft = hz.target
            enemy.velocity.xy = (0, 0)
            enemy.on_ground = False
        elif isinstance(hz, WindZone):
            self._record_hazard(hz, "wind")
            enemy.velocity.x += hz.force
        elif isinstance(hz, RegenZone) and now - self.last_damage >= hz.interval:
            self._record_hazard(hz, "regen")
            enemy.health = enemy.health_manager.heal(hz.heal)
            self.last_damage = now
        return False

    def clear(self):
        self.hazards.empty()
        self.last_damage = 0
