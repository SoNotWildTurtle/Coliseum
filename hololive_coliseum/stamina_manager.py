"""Track and spend a character's stamina resource."""


class StaminaManager:
    """Track and spend a character's stamina resource."""

    def __init__(self, max_stamina: int) -> None:
        self.max_stamina = max_stamina
        self.stamina = max_stamina
        self.regen_step = 1.0
        self._regen_buffer = 0.0

    def use(self, amount: int) -> bool:
        """Attempt to spend stamina, returning True if enough was available."""
        if self.stamina >= amount:
            self.stamina -= amount
            return True
        return False

    def set_regen_step(self, step: float) -> None:
        """Adjust how much stamina is restored each regeneration tick."""

        self.regen_step = max(0.0, step)

    def regen(self, amount: int) -> int:
        """Regenerate stamina and return the new value."""

        if self.regen_step == 0:
            return self.stamina
        self._regen_buffer += amount * self.regen_step
        gain = int(self._regen_buffer)
        if gain > 0:
            self._regen_buffer -= gain
            self.stamina = min(self.max_stamina, self.stamina + gain)
        return self.stamina

