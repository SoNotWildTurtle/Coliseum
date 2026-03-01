"""Experience tracking and award helpers."""

class ExperienceManager:
    """Handle experience gain and leveling."""

    def __init__(
        self,
        level: int = 1,
        xp: int = 0,
        threshold: int = 100,
        *,
        growth: float = 1.0,
        max_threshold: int | None = None,
    ) -> None:
        self.level = level
        self.xp = xp
        self.threshold = threshold
        self.growth = growth
        self.max_threshold = max_threshold

    def add_xp(self, amount: int) -> bool:
        """Add experience and return True if a level-up occurred."""
        self.xp += amount
        leveled = False
        while self.xp >= self.threshold:
            self.xp -= self.threshold
            self.level += 1
            if self.growth and self.growth > 1:
                next_threshold = max(
                    self.threshold + 1,
                    int(self.threshold * self.growth),
                )
                if self.max_threshold is not None:
                    next_threshold = min(self.max_threshold, next_threshold)
                self.threshold = next_threshold
            leveled = True
        return leveled
