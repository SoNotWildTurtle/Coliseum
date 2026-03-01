"""Status effect classes used for temporary sprite modifiers."""

import pygame


class StatusEffect:
    """Base status effect applied to a sprite."""

    def __init__(self, duration_ms: int, start_time: int | None = None) -> None:
        start_time = start_time if start_time is not None else pygame.time.get_ticks()
        self.start_time = start_time
        self.end_time = self.start_time + duration_ms

    def apply(self, target):
        pass

    def update(self, target, now: int) -> None:
        """Update the effect each frame."""
        pass

    def remove(self, target):
        pass


class FreezeEffect(StatusEffect):
    """Halve target speed for a short duration."""

    def __init__(
        self,
        duration_ms: int = 1000,
        factor: float = 0.5,
        start_time: int | None = None,
    ) -> None:
        super().__init__(duration_ms, start_time)
        self.factor = factor

    def apply(self, target):
        if hasattr(target, "speed_factor"):
            target.speed_factor *= self.factor
        target.velocity.x *= self.factor
        target.velocity.y *= self.factor

    def remove(self, target) -> None:
        if hasattr(target, "speed_factor"):
            target.speed_factor /= self.factor


class SlowEffect(StatusEffect):
    """Reduce horizontal speed of the target."""

    def __init__(self, duration_ms: int = 1000, factor: float = 0.5) -> None:
        super().__init__(duration_ms)
        self.factor = factor

    def apply(self, target):
        if hasattr(target, "speed_factor"):
            target.speed_factor *= self.factor
        target.velocity.x *= self.factor

    def remove(self, target) -> None:
        if hasattr(target, "speed_factor"):
            target.speed_factor /= self.factor


class SpeedEffect(StatusEffect):
    """Temporarily increase target speed."""

    def __init__(self, duration_ms: int = 1000, factor: float = 2.0) -> None:
        super().__init__(duration_ms)
        self.factor = factor

    def apply(self, target) -> None:
        if hasattr(target, "speed_factor"):
            target.speed_factor *= self.factor

    def remove(self, target) -> None:
        if hasattr(target, "speed_factor"):
            target.speed_factor /= self.factor


class ShieldEffect(StatusEffect):
    """Make target temporarily invincible."""

    def __init__(self, duration_ms: int = 1000) -> None:
        super().__init__(duration_ms)

    def apply(self, target) -> None:
        setattr(target, "invincible", True)

    def remove(self, target) -> None:
        setattr(target, "invincible", False)


class AttackEffect(StatusEffect):
    """Temporarily increase the target's attack stat."""

    def __init__(self, duration_ms: int = 1000, amount: int = 5) -> None:
        super().__init__(duration_ms)
        self.amount = amount

    def apply(self, target) -> None:
        if hasattr(target, "stats"):
            target.stats.apply_modifier("attack", self.amount)

    def remove(self, target) -> None:
        if hasattr(target, "stats"):
            target.stats.remove_modifier("attack", self.amount)


class DefenseEffect(StatusEffect):
    """Temporarily increase the target's defense stat."""

    def __init__(self, duration_ms: int = 1000, amount: int = 5) -> None:
        super().__init__(duration_ms)
        self.amount = amount

    def apply(self, target) -> None:
        if hasattr(target, "stats"):
            target.stats.apply_modifier("defense", self.amount)

    def remove(self, target) -> None:
        if hasattr(target, "stats"):
            target.stats.remove_modifier("defense", self.amount)


class PoisonEffect(StatusEffect):
    """Inflict periodic damage on the target."""

    def __init__(
        self,
        duration_ms: int = 1000,
        damage: int = 1,
        interval_ms: int = 250,
    ) -> None:
        super().__init__(duration_ms)
        self.damage = damage
        self.interval_ms = interval_ms
        self._last_tick = self.start_time

    def update(self, target, now: int) -> None:
        if now - self._last_tick >= self.interval_ms:
            if hasattr(target, "take_damage"):
                target.take_damage(self.damage)
            self._last_tick = now


class BurnEffect(StatusEffect):
    """Apply periodic burn damage to the target."""

    def __init__(
        self,
        duration_ms: int = 1000,
        damage: int = 1,
        interval_ms: int = 200,
    ) -> None:
        super().__init__(duration_ms)
        self.damage = damage
        self.interval_ms = interval_ms
        self._last_tick = self.start_time

    def update(self, target, now: int) -> None:
        if now - self._last_tick >= self.interval_ms:
            if hasattr(target, "take_damage"):
                target.take_damage(self.damage)
            self._last_tick = now


class StunEffect(StatusEffect):
    """Temporarily prevent the target from moving."""

    def __init__(self, duration_ms: int = 500) -> None:
        super().__init__(duration_ms)

    def apply(self, target) -> None:
        setattr(target, "stunned", True)
        if hasattr(target, "velocity"):
            target.velocity.update(0, 0)

    def remove(self, target) -> None:
        setattr(target, "stunned", False)


class SilenceEffect(StatusEffect):
    """Temporarily prevent the target from using special attacks."""

    def __init__(self, duration_ms: int = 1000) -> None:
        super().__init__(duration_ms)

    def apply(self, target) -> None:
        setattr(target, "silenced", True)

    def remove(self, target) -> None:
        setattr(target, "silenced", False)



class StatusEffectManager:
    """Keep track of active status effects on sprites."""

    def __init__(self) -> None:
        self._effects: list[tuple[object, StatusEffect]] = []

    def add_effect(self, target, effect: StatusEffect) -> None:
        effect.apply(target)
        self._effects.append((target, effect))

    def update(self, now: int | None = None) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        for target, effect in list(self._effects):
            if now >= effect.end_time:
                effect.remove(target)
                self._effects.remove((target, effect))
            else:
                effect.update(target, now)

    def active_effects(
        self,
        target: object | None = None,
        now: int | None = None,
    ) -> list[dict[str, object]]:
        """Return summaries of currently active effects.

        Parameters
        ----------
        target:
            When provided, only effects applied to the given target are
            returned. Otherwise all tracked effects are included.
        now:
            Optional timestamp used to compute the remaining duration for each
            effect. Defaults to :func:`pygame.time.get_ticks`.

        Returns
        -------
        list of dict
            Each entry contains the original ``target`` reference, the
            ``effect`` instance, a user-facing ``name`` suitable for the HUD,
            and ``remaining_ms`` describing how long the effect will last.
        """

        if now is None:
            now = pygame.time.get_ticks()
        summaries: list[dict[str, object]] = []
        for current_target, effect in self._effects:
            if target is not None and current_target is not target:
                continue
            remaining = max(0, effect.end_time - now)
            name = getattr(effect, "ui_name", effect.__class__.__name__)
            if isinstance(name, str) and name.endswith("Effect"):
                name = name[:-6]
            summaries.append(
                {
                    "target": current_target,
                    "effect": effect,
                    "name": name,
                    "remaining_ms": remaining,
                }
            )
        return summaries
