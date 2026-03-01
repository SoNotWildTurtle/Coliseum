"""Damage calculation and mitigation helpers."""

import random


class DamageManager:
    """Compute final damage values and apply them to targets."""

    def calculate(
        self,
        base: int,
        defense: int = 0,
        multiplier: float = 1.0,
        crit_chance: int = 0,
        crit_multiplier: float = 2.0,
        return_crit: bool = False,
    ) -> int | tuple[int, bool]:
        amount = max(base - defense, 0)
        dmg = int(amount * multiplier)
        critical = False
        if crit_chance > 0 and random.random() < crit_chance / 100:
            dmg = int(dmg * crit_multiplier)
            critical = True
        if return_crit:
            return dmg, critical
        return dmg

    def apply(self, target, base: int, **kwargs) -> int:
        """Apply damage to ``target`` and return the amount dealt."""
        dmg = self.calculate(base, **kwargs)
        if isinstance(dmg, tuple):
            dmg = dmg[0]
        if hasattr(target, "take_damage"):
            target.take_damage(dmg)
        return dmg
