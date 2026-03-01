"""Profession tracking and progression helpers."""

from collections import defaultdict

class ProfessionManager:
    """Track profession experience and provide levels."""

    def __init__(self) -> None:
        self._xp: defaultdict[str, int] = defaultdict(int)

    def gain_xp(self, profession: str, amount: int) -> None:
        self._xp[profession] += amount

    def level_of(self, profession: str) -> int:
        return self._xp[profession] // 100
