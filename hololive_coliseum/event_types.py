"""Canonical event type constants and minimal payload requirements."""

from __future__ import annotations

from typing import Final

DAMAGE: Final[str] = "damage"
HAZARD_DAMAGE: Final[str] = "hazard_damage"
HEAL: Final[str] = "heal"
STATUS_TICK: Final[str] = "status_tick"

CURRENCY_DELTA: Final[str] = "currency_delta"
XP_DELTA: Final[str] = "xp_delta"
REPUTATION_DELTA: Final[str] = "reputation_delta"

ACHIEVEMENT_UNLOCKED: Final[str] = "achievement_unlocked"
OBJECTIVE_PROGRESS: Final[str] = "objective_progress"
OBJECTIVE_COMPLETED: Final[str] = "objective_completed"
OBJECTIVE_REWARD: Final[str] = "objective_reward"

EVENT_TYPES: Final[set[str]] = {
    DAMAGE,
    HAZARD_DAMAGE,
    HEAL,
    STATUS_TICK,
    CURRENCY_DELTA,
    XP_DELTA,
    REPUTATION_DELTA,
    ACHIEVEMENT_UNLOCKED,
    OBJECTIVE_PROGRESS,
    OBJECTIVE_COMPLETED,
    OBJECTIVE_REWARD,
}

REQUIRED_PAYLOAD_KEYS: Final[dict[str, tuple[str, ...]]] = {
    DAMAGE: ("target_id", "amount"),
    HAZARD_DAMAGE: ("target_id", "amount"),
    HEAL: ("target_id", "amount"),
    STATUS_TICK: ("target_id", "amount"),
    CURRENCY_DELTA: ("delta",),
    XP_DELTA: ("delta",),
    REPUTATION_DELTA: ("faction", "delta"),
    ACHIEVEMENT_UNLOCKED: ("id",),
    OBJECTIVE_PROGRESS: ("objective", "progress", "target"),
    OBJECTIVE_COMPLETED: ("objective",),
    OBJECTIVE_REWARD: ("objective", "reward"),
}

OPTIONAL_PAYLOAD_KEYS: Final[dict[str, tuple[str, ...]]] = {
    DAMAGE: ("attacker_id", "source", "hp_before", "hp_after", "kind", "critical"),
    HAZARD_DAMAGE: ("attacker_id", "source", "hp_before", "hp_after", "kind"),
    HEAL: ("attacker_id", "source", "hp_before", "hp_after", "kind"),
    STATUS_TICK: ("attacker_id", "source", "hp_before", "hp_after", "kind"),
    CURRENCY_DELTA: ("balance", "source", "reason"),
    XP_DELTA: ("level", "xp", "source", "reason", "leveled"),
    REPUTATION_DELTA: ("value", "source", "reason"),
    ACHIEVEMENT_UNLOCKED: ("source", "at"),
    OBJECTIVE_PROGRESS: ("event", "rewarded", "source", "objective_id", "period", "delta"),
    OBJECTIVE_COMPLETED: ("source", "at", "objective_id", "period", "completed_utc"),
    OBJECTIVE_REWARD: ("source", "objective_id", "period", "daily_streak"),
}
