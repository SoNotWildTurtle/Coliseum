"""Score tracking and leaderboard helpers."""

class ScoreManager:
    """Track the current and best score for a run."""

    def __init__(self, best_score: int = 0, combo_window: float = 2.0) -> None:
        self.best_score = best_score
        self.score = 0
        self.combo = 0
        self.combo_window = combo_window
        self._last_kill = 0.0

    def reset(self) -> None:
        """Reset the score at the start of a level."""
        self.score = 0

    def add(self, points: int) -> None:
        """Increase the score by ``points``."""
        self.score += points

    def record_kill(self, now: float) -> None:
        """Register an enemy defeat and award combo points."""
        if now - self._last_kill <= self.combo_window:
            self.combo += 1
        else:
            self.combo = 1
        self._last_kill = now
        self.add(10 * self.combo)

    def update(self, now: float) -> None:
        """Reset combo if no kill occurred recently."""
        if now - self._last_kill > self.combo_window:
            self.combo = 0

    def finalize(self) -> int:
        """Update and return the best score if the current score is higher."""
        if self.score > self.best_score:
            self.best_score = self.score
        return self.best_score
