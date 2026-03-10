"""Deterministic UTC time helpers for gameplay systems."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone


class TimeProvider:
    """Provide UTC timestamps and reset keys for daily/weekly systems."""

    def now_utc(self) -> datetime:
        return datetime.now(timezone.utc)

    def day_key(self, now: datetime | None = None) -> str:
        current = now or self.now_utc()
        return current.astimezone(timezone.utc).strftime("%Y-%m-%d")

    def week_key(self, now: datetime | None = None) -> str:
        current = now or self.now_utc()
        year, week, _ = current.astimezone(timezone.utc).isocalendar()
        return f"{year}-W{week:02d}"


class FixedTimeProvider(TimeProvider):
    """Mutable fixed clock used by tests and deterministic tools."""

    def __init__(self, now: datetime | None = None) -> None:
        self._now = (now or datetime(2026, 1, 1, tzinfo=timezone.utc)).astimezone(
            timezone.utc
        )

    def now_utc(self) -> datetime:
        return self._now

    def set(self, now: datetime) -> None:
        self._now = now.astimezone(timezone.utc)

    def advance(
        self,
        *,
        days: int = 0,
        weeks: int = 0,
        hours: int = 0,
    ) -> None:
        self._now = self._now + timedelta(days=days, weeks=weeks, hours=hours)
