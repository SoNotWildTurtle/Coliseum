"""Deterministic rotating objective system for arena progression."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Callable, Dict, Iterable, List, Mapping, Sequence

from .time_provider import TimeProvider


def _utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, int(value)))


def _day_distance(day_a: str | None, day_b: str | None) -> int | None:
    if not day_a or not day_b:
        return None
    try:
        left = datetime.strptime(day_a, "%Y-%m-%d").date()
        right = datetime.strptime(day_b, "%Y-%m-%d").date()
    except ValueError:
        return None
    return (left - right).days


def _humanize_key(value: str) -> str:
    return value.replace("_", " ").title()


@dataclass
class ObjectiveUpdate:
    """Delta returned from objective progress recording."""

    objective_id: str
    objective_type: str
    period: str
    progress_delta: int
    progress: int
    target: int
    completed: bool
    rewarded: bool

    @property
    def kind(self) -> str:
        return self.objective_type

    @property
    def delta(self) -> int:
        return self.progress_delta

    @property
    def completed_now(self) -> bool:
        return self.completed

    def to_dict(self) -> Dict[str, object]:
        """Return a JSON-safe update payload."""

        return {
            "objective_id": self.objective_id,
            "period": self.period,
            "kind": self.objective_type,
            "delta": int(self.progress_delta),
            "progress": int(self.progress),
            "target": int(self.target),
            "completed_now": bool(self.completed),
            "rewarded": bool(self.rewarded),
        }


@dataclass
class Objective:
    """Runtime objective state persisted through profiles and settings."""

    objective_id: str
    objective_type: str
    period: str
    name: str
    description: str
    target: int
    progress: int = 0
    reward: Dict[str, int] = field(default_factory=dict)
    created_utc: str = ""
    expires_utc: str = ""
    created_day_key: str | None = None
    created_week_key: str | None = None
    expires_day_key: str | None = None
    expires_week_key: str | None = None
    completed: bool = False
    completed_utc: str | None = None
    completed_day_key: str | None = None
    rewarded: bool = False
    metadata: Dict[str, object] = field(default_factory=dict)

    @property
    def key(self) -> str:
        return self.objective_type

    @property
    def scope(self) -> str:
        return self.period

    @property
    def rewards(self) -> Dict[str, int]:
        return self.reward

    @property
    def kind(self) -> str:
        return self.objective_type

    @property
    def reward_claimed(self) -> bool:
        return self.rewarded

    @reward_claimed.setter
    def reward_claimed(self, value: bool) -> None:
        self.rewarded = bool(value)

    @property
    def meta(self) -> Dict[str, object]:
        return self.metadata

    def to_dict(self) -> Dict[str, object]:
        """Return a JSON-serialisable representation of the objective."""

        return {
            "objective_id": self.objective_id,
            "objective_type": self.objective_type,
            "kind": self.objective_type,
            "period": self.period,
            "scope": self.period,
            "name": self.name,
            "description": self.description,
            "target": int(self.target),
            "progress": int(self.progress),
            "reward": dict(self.reward),
            "rewards": dict(self.reward),
            "created_utc": self.created_utc,
            "expires_utc": self.expires_utc,
            "created_day_key": self.created_day_key,
            "created_week_key": self.created_week_key,
            "expires_day_key": self.expires_day_key,
            "expires_week_key": self.expires_week_key,
            "completed": bool(self.completed),
            "completed_utc": self.completed_utc,
            "completed_day_key": self.completed_day_key,
            "rewarded": bool(self.rewarded),
            "reward_claimed": bool(self.rewarded),
            "metadata": dict(self.metadata),
            "meta": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, key: str, data: Mapping[str, object]) -> "Objective":
        """Build an objective from persisted state."""

        reward = data.get("reward", data.get("rewards", {}))
        if not isinstance(reward, Mapping):
            reward = {}
        metadata = data.get("metadata", data.get("meta", {}))
        if not isinstance(metadata, Mapping):
            metadata = {}
        objective_type = str(
            data.get("objective_type")
            or data.get("kind")
            or data.get("key")
            or data.get("objective")
            or key
        )
        objective_type = ObjectiveManager.normalize_objective_type(objective_type)
        period = str(data.get("period") or data.get("scope") or "daily")
        target = max(0, _safe_int(data.get("target"), 0))
        progress = _clamp(_safe_int(data.get("progress"), 0), 0, max(0, target))
        completed = bool(data.get("completed", progress >= target and target > 0))
        created_day_key = data.get("created_day_key")
        created_week_key = data.get("created_week_key")
        expires_day_key = data.get("expires_day_key")
        expires_week_key = data.get("expires_week_key")
        completed_day_key = data.get("completed_day_key")
        if created_day_key in {None, ""} and period == "daily":
            created_day_key = metadata.get("period_key")
        if created_week_key in {None, ""} and period == "weekly":
            created_week_key = metadata.get("period_key")
        if expires_day_key in {None, ""} and period == "daily":
            expires_day_key = metadata.get("period_key")
        if expires_week_key in {None, ""} and period == "weekly":
            expires_week_key = metadata.get("period_key")
        period_key = (
            str(created_day_key)
            if period == "daily" and created_day_key not in {None, ""}
            else str(created_week_key)
            if period == "weekly" and created_week_key not in {None, ""}
            else ""
        )
        fallback_objective_id = (
            f"{period}:{period_key}:{objective_type}"
            if period_key
            else f"{period}:{objective_type}"
        )
        objective_id = str(data.get("objective_id") or fallback_objective_id)
        return cls(
            objective_id=objective_id,
            objective_type=objective_type,
            period=period,
            name=str(data.get("name") or _humanize_key(objective_type)),
            description=str(data.get("description", "")),
            target=target,
            progress=progress,
            reward={
                str(reward_key): max(0, _safe_int(reward_value, 0))
                for reward_key, reward_value in reward.items()
                if isinstance(reward_key, str)
            },
            created_utc=str(data.get("created_utc", "")),
            expires_utc=str(data.get("expires_utc", "")),
            created_day_key=(
                None if created_day_key in {None, ""} else str(created_day_key)
            ),
            created_week_key=(
                None if created_week_key in {None, ""} else str(created_week_key)
            ),
            expires_day_key=(
                None if expires_day_key in {None, ""} else str(expires_day_key)
            ),
            expires_week_key=(
                None if expires_week_key in {None, ""} else str(expires_week_key)
            ),
            completed=completed,
            completed_utc=(
                None
                if data.get("completed_utc") in {None, ""}
                else str(data.get("completed_utc"))
            ),
            completed_day_key=(
                None if completed_day_key in {None, ""} else str(completed_day_key)
            ),
            rewarded=bool(data.get("rewarded", data.get("reward_claimed", False))),
            metadata={str(meta_key): meta_value for meta_key, meta_value in metadata.items()},
        )

    def record(
        self,
        amount: int = 1,
        *,
        completed_utc: str | None = None,
        completed_day_key: str | None = None,
    ) -> int:
        """Increment progress toward the target and return the applied delta."""

        if amount <= 0 or self.completed:
            return 0
        before = int(self.progress)
        self.progress = min(int(self.target), int(self.progress) + int(amount))
        delta = self.progress - before
        if self.progress >= self.target and self.target > 0:
            self.completed = True
            if completed_utc:
                self.completed_utc = completed_utc
            if completed_day_key:
                self.completed_day_key = completed_day_key
        return delta


@dataclass(frozen=True)
class ObjectiveTemplate:
    """Static rule set used to build objective instances."""

    objective_type: str
    event_types: tuple[str, ...]
    periods: tuple[str, ...]
    base_daily: int
    base_weekly: int
    tier_step: int
    radius_step: int
    recommended_step: int
    minimum: int
    maximum: int
    reward_base_coins: int
    reward_base_xp: int
    reward_step_coins: int
    reward_step_xp: int


class ObjectiveManager:
    """Coordinate deterministic daily and weekly objectives."""

    EVENT_MAP: Dict[str, Iterable[str]] = {
        "enemy_defeated": ("defeat_enemies",),
        "coin_collected": ("earn_coins",),
        "coins_earned": ("earn_coins",),
        "powerup_collected": ("collect_powerups",),
        "match_victory": ("win_matches",),
        "match_won": ("win_matches",),
        "hazard_logged": ("hazard_mastery",),
        "damage_dealt": ("deal_damage",),
    }

    ORDER: List[str] = [
        "defeat_enemies",
        "collect_powerups",
        "earn_coins",
        "hazard_mastery",
        "win_matches",
        "deal_damage",
    ]

    PERIOD_SLOTS: Dict[str, int] = {"daily": 2, "weekly": 2}

    TEMPLATES: Dict[str, ObjectiveTemplate] = {
        "defeat_enemies": ObjectiveTemplate(
            objective_type="defeat_enemies",
            event_types=("enemy_defeated",),
            periods=("daily", "weekly"),
            base_daily=6,
            base_weekly=24,
            tier_step=2,
            radius_step=1,
            recommended_step=2,
            minimum=5,
            maximum=60,
            reward_base_coins=8,
            reward_base_xp=18,
            reward_step_coins=3,
            reward_step_xp=8,
        ),
        "collect_powerups": ObjectiveTemplate(
            objective_type="collect_powerups",
            event_types=("powerup_collected",),
            periods=("daily", "weekly"),
            base_daily=3,
            base_weekly=10,
            tier_step=1,
            radius_step=1,
            recommended_step=1,
            minimum=2,
            maximum=18,
            reward_base_coins=6,
            reward_base_xp=16,
            reward_step_coins=2,
            reward_step_xp=6,
        ),
        "earn_coins": ObjectiveTemplate(
            objective_type="earn_coins",
            event_types=("coin_collected", "coins_earned"),
            periods=("daily", "weekly"),
            base_daily=18,
            base_weekly=80,
            tier_step=10,
            radius_step=4,
            recommended_step=6,
            minimum=15,
            maximum=300,
            reward_base_coins=10,
            reward_base_xp=20,
            reward_step_coins=3,
            reward_step_xp=8,
        ),
        "win_matches": ObjectiveTemplate(
            objective_type="win_matches",
            event_types=("match_victory", "match_won"),
            periods=("weekly",),
            base_daily=0,
            base_weekly=2,
            tier_step=1,
            radius_step=0,
            recommended_step=1,
            minimum=1,
            maximum=8,
            reward_base_coins=22,
            reward_base_xp=55,
            reward_step_coins=5,
            reward_step_xp=12,
        ),
        "deal_damage": ObjectiveTemplate(
            objective_type="deal_damage",
            event_types=("damage_dealt",),
            periods=("daily", "weekly"),
            base_daily=140,
            base_weekly=700,
            tier_step=90,
            radius_step=30,
            recommended_step=40,
            minimum=100,
            maximum=4000,
            reward_base_coins=10,
            reward_base_xp=24,
            reward_step_coins=2,
            reward_step_xp=10,
        ),
        "hazard_mastery": ObjectiveTemplate(
            objective_type="hazard_mastery",
            event_types=("hazard_logged",),
            periods=("weekly",),
            base_daily=0,
            base_weekly=4,
            tier_step=1,
            radius_step=0,
            recommended_step=1,
            minimum=3,
            maximum=20,
            reward_base_coins=12,
            reward_base_xp=32,
            reward_step_coins=3,
            reward_step_xp=10,
        ),
    }

    LEGACY_OBJECTIVE_KEY_MAP: Dict[str, str] = {"collect_coins": "earn_coins"}

    def __init__(
        self,
        *,
        profile_id: str = "default",
        time_provider: TimeProvider | None = None,
        reward_sink: Callable[[dict[str, int], Objective], None] | None = None,
        event_emitter: Callable[[dict[str, object]], None] | None = None,
        progression_level_provider: Callable[[], int] | None = None,
    ) -> None:
        self.profile_id = str(profile_id or "default")
        self.time_provider = time_provider or TimeProvider()
        self.reward_sink = reward_sink
        self.event_emitter = event_emitter
        self.progression_level_provider = progression_level_provider
        self.region_key: str | None = None
        self.region_name: str = "Arena"
        self.region_biome: str = "arena"
        self.region_context: Dict[str, object] = {}
        self.objectives: Dict[str, Objective] = {}
        self.last_reset_day_key: str | None = None
        self.last_reset_week_key: str | None = None
        self.daily_streak: int = 0
        self.last_daily_completion_day_key: str | None = None
        self.last_assigned_types: Dict[str, List[str]] = {"daily": [], "weekly": []}
        self.assignment_history: Dict[str, Dict[str, List[str]]] = {
            "daily": {},
            "weekly": {},
        }

    @staticmethod
    def normalize_objective_type(objective_type: str) -> str:
        """Normalize legacy objective identifiers to the current set."""

        key = str(objective_type or "").strip() or "defeat_enemies"
        return ObjectiveManager.LEGACY_OBJECTIVE_KEY_MAP.get(key, key)

    def set_reward_sink(
        self,
        reward_sink: Callable[[dict[str, int], Objective], None] | None,
    ) -> None:
        self.reward_sink = reward_sink

    def set_event_emitter(
        self,
        event_emitter: Callable[[dict[str, object]], None] | None,
    ) -> None:
        self.event_emitter = event_emitter

    def set_progression_level_provider(
        self,
        provider: Callable[[], int] | None,
    ) -> None:
        self.progression_level_provider = provider

    def load_from_dict(self, data: Dict[str, object]) -> None:
        """Restore objective state from persisted settings/profile data."""

        self.import_state(data)

    def to_dict(self) -> Dict[str, object]:
        """Return the persisted representation of the manager."""

        return self.export_state()

    def export_state(self) -> Dict[str, object]:
        """Return a JSON-safe export of the current objective state."""

        daily_objectives = [
            objective.to_dict()
            for objective in self.objectives.values()
            if objective.period == "daily"
        ]
        weekly_objectives = [
            objective.to_dict()
            for objective in self.objectives.values()
            if objective.period == "weekly"
        ]
        recent_daily_kinds: list[str] = []
        daily_history = self.assignment_history.get("daily", {})
        for history_key in sorted(daily_history)[-3:]:
            recent_daily_kinds.extend(list(daily_history.get(history_key, [])))
        return {
            "schema_version": 1,
            "profile_id": self.profile_id,
            "region_key": self.region_key,
            "region_name": self.region_name,
            "region_biome": self.region_biome,
            "region_context": dict(self.region_context),
            "objectives": {
                key: objective.to_dict() for key, objective in self.objectives.items()
            },
            "daily_objectives": daily_objectives,
            "weekly_objectives": weekly_objectives,
            "last_reset_day_key": self.last_reset_day_key,
            "last_reset_week_key": self.last_reset_week_key,
            "last_daily_key": self.last_reset_day_key,
            "last_weekly_key": self.last_reset_week_key,
            "daily_streak": int(self.daily_streak),
            "daily_streak_count": int(self.daily_streak),
            "last_daily_completion_day_key": self.last_daily_completion_day_key,
            "last_daily_completion_key": self.last_daily_completion_day_key,
            "last_assigned_types": {
                period: list(values)
                for period, values in self.last_assigned_types.items()
            },
            "last_daily_kinds": recent_daily_kinds[-6:],
            "last_weekly_kinds": list(self.last_assigned_types.get("weekly", [])),
            "assignment_history": {
                period: {
                    history_key: list(values)
                    for history_key, values in history.items()
                }
                for period, history in self.assignment_history.items()
            },
        }

    def import_state(self, state: Dict[str, object] | None) -> None:
        """Import objective state from persisted settings/profile data."""

        data = state if isinstance(state, Mapping) else {}
        self.profile_id = str(data.get("profile_id") or self.profile_id or "default")
        self.region_key = data.get("region_key") or None
        self.region_name = str(data.get("region_name", self.region_name) or self.region_name)
        self.region_biome = str(
            data.get("region_biome", self.region_biome) or self.region_biome
        )
        region_context = data.get("region_context", {})
        if isinstance(region_context, Mapping):
            self.region_context = {str(key): value for key, value in region_context.items()}
        else:
            self.region_context = {}
        raw_objectives = data.get("objectives", {})
        if not isinstance(raw_objectives, Mapping):
            raw_objectives = {}
        imported: Dict[str, Objective] = {}
        for list_key in ("daily_objectives", "weekly_objectives"):
            values = data.get(list_key, [])
            if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
                continue
            for value in values:
                if not isinstance(value, Mapping):
                    continue
                objective = Objective.from_dict(
                    str(value.get("objective_id") or value.get("objective_type") or value.get("kind") or ""),
                    value,
                )
                imported[objective.objective_type] = objective
        for key, value in raw_objectives.items():
            if not isinstance(key, str) or not isinstance(value, Mapping):
                continue
            objective = Objective.from_dict(key, value)
            imported[objective.objective_type] = objective
        self.objectives = imported
        self.last_reset_day_key = (
            None
            if data.get("last_reset_day_key", data.get("last_daily_key")) in {None, ""}
            else str(data.get("last_reset_day_key", data.get("last_daily_key")))
        )
        self.last_reset_week_key = (
            None
            if data.get("last_reset_week_key", data.get("last_weekly_key")) in {None, ""}
            else str(data.get("last_reset_week_key", data.get("last_weekly_key")))
        )
        self.daily_streak = max(
            0,
            _safe_int(data.get("daily_streak", data.get("daily_streak_count")), 0),
        )
        self.last_daily_completion_day_key = (
            None
            if data.get(
                "last_daily_completion_day_key",
                data.get("last_daily_completion_key"),
            ) in {None, ""}
            else str(
                data.get(
                    "last_daily_completion_day_key",
                    data.get("last_daily_completion_key"),
                )
            )
        )
        self.last_assigned_types = {"daily": [], "weekly": []}
        raw_assigned = data.get("last_assigned_types", {})
        if isinstance(raw_assigned, Mapping):
            for period in ("daily", "weekly"):
                values = raw_assigned.get(period, [])
                if isinstance(values, Sequence) and not isinstance(values, (str, bytes)):
                    self.last_assigned_types[period] = [
                        self.normalize_objective_type(str(item))
                        for item in values
                        if str(item).strip()
                    ]
        for period, alias_key in (("daily", "last_daily_kinds"), ("weekly", "last_weekly_kinds")):
            if self.last_assigned_types[period]:
                continue
            values = data.get(alias_key, [])
            if isinstance(values, Sequence) and not isinstance(values, (str, bytes)):
                self.last_assigned_types[period] = [
                    self.normalize_objective_type(str(item))
                    for item in values
                    if str(item).strip()
                ]
        self.assignment_history = {"daily": {}, "weekly": {}}
        raw_history = data.get("assignment_history", {})
        if isinstance(raw_history, Mapping):
            for period in ("daily", "weekly"):
                history = raw_history.get(period, {})
                if not isinstance(history, Mapping):
                    continue
                self.assignment_history[period] = {
                    str(history_key): [
                        self.normalize_objective_type(str(item))
                        for item in values
                        if str(item).strip()
                    ]
                    for history_key, values in history.items()
                    if isinstance(history_key, str)
                    and isinstance(values, Sequence)
                    and not isinstance(values, (str, bytes))
                }
        if self.objectives and self.last_reset_day_key is None:
            self.last_reset_day_key = self.time_provider.day_key()
        if self.objectives and self.last_reset_week_key is None:
            self.last_reset_week_key = self.time_provider.week_key()
        self.refresh()

    def ensure_region_objectives(
        self,
        region: Dict[str, object] | None,
        fallback_name: str = "Arena",
    ) -> None:
        """Generate or refresh objectives for the active region."""

        context = self._normalize_region(region, fallback_name=fallback_name)
        previous_region_key = self.region_key
        self.region_context = context
        self.region_key = str(context["region_key"])
        self.region_name = str(context["region_name"])
        self.region_biome = str(context["region_biome"])
        force = previous_region_key not in {None, self.region_key}
        self.refresh(force=force)

    def refresh(self, *, force: bool = False) -> None:
        """Refresh daily/weekly objectives if the active reset keys changed."""

        now = self.time_provider.now_utc()
        day_key = self.time_provider.day_key(now)
        week_key = self.time_provider.week_key(now)
        self._sync_streak(day_key)
        self._prune_history(day_key, week_key)
        if not self.region_context:
            self.region_context = self._normalize_region(None, fallback_name=self.region_name)
            self.region_key = str(self.region_context["region_key"])
            self.region_name = str(self.region_context["region_name"])
            self.region_biome = str(self.region_context["region_biome"])
        should_reset_weekly = force or (self.last_reset_week_key != week_key)
        should_reset_daily = force or (self.last_reset_day_key != day_key)
        if should_reset_weekly:
            self._generate_period("weekly", week_key, now)
            self.last_reset_week_key = week_key
        if should_reset_daily:
            self._generate_period("daily", day_key, now)
            self.last_reset_day_key = day_key
        if should_reset_weekly and not should_reset_daily:
            self._remove_period_duplicates("daily")

    def record_event(
        self,
        event_type: str,
        amount: int = 1,
        meta: dict | None = None,
    ) -> list[ObjectiveUpdate]:
        """Record progress via a centralized event entry point."""

        self.refresh()
        amount = max(0, int(amount))
        if amount <= 0:
            return []
        tracked_types = {
            self.normalize_objective_type(objective_type)
            for objective_type in self.EVENT_MAP.get(str(event_type), ())
        }
        if not tracked_types:
            return []
        now_iso = _utc_iso(self.time_provider.now_utc())
        current_day_key = self.time_provider.day_key()
        source = ""
        if isinstance(meta, Mapping):
            source = str(meta.get("source", "")).strip()
        updates: list[ObjectiveUpdate] = []
        for objective in self.objectives.values():
            if objective.objective_type not in tracked_types:
                continue
            was_completed = objective.completed
            delta = objective.record(
                amount,
                completed_utc=now_iso,
                completed_day_key=current_day_key,
            )
            if delta <= 0:
                continue
            update = ObjectiveUpdate(
                objective_id=objective.objective_id,
                objective_type=objective.objective_type,
                period=objective.period,
                progress_delta=delta,
                progress=int(objective.progress),
                target=int(objective.target),
                completed=bool(objective.completed),
                rewarded=bool(objective.rewarded),
            )
            updates.append(update)
            self._emit_event(
                "objective_progress",
                {
                    "objective_id": objective.objective_id,
                    "objective": objective.objective_type,
                    "kind": objective.objective_type,
                    "period": objective.period,
                    "event": str(event_type),
                    "progress": int(objective.progress),
                    "target": int(objective.target),
                    "delta": int(delta),
                    "rewarded": bool(objective.rewarded),
                    "source": source,
                },
            )
            if objective.completed and not was_completed:
                if objective.period == "daily":
                    self._record_daily_completion()
                self._emit_event(
                    "objective_completed",
                    {
                        "objective_id": objective.objective_id,
                        "objective": objective.objective_type,
                        "kind": objective.objective_type,
                        "period": objective.period,
                        "completed_utc": objective.completed_utc or now_iso,
                        "completed_day_key": objective.completed_day_key,
                        "source": source,
                    },
                )
        if self.reward_sink is not None:
            self.claim_completed_rewards(meta=meta)
        return updates

    def claim_completed_rewards(
        self,
        *,
        meta: dict | None = None,
    ) -> list[dict[str, int]]:
        """Apply pending objective rewards once and return what was awarded."""

        self.refresh()
        source = ""
        if isinstance(meta, Mapping):
            source = str(meta.get("source", "")).strip()
        awarded: list[dict[str, int]] = []
        for objective in self.objectives.values():
            if not objective.completed or objective.rewarded:
                continue
            reward = self._reward_with_streak_bonus(objective)
            if self.reward_sink is not None:
                self.reward_sink(dict(reward), objective)
            objective.rewarded = True
            awarded.append(dict(reward))
            payload: dict[str, object] = {
                "objective_id": objective.objective_id,
                "objective": objective.objective_type,
                "kind": objective.objective_type,
                "period": objective.period,
                "reward": dict(reward),
                "source": source,
            }
            if objective.period == "daily":
                payload["daily_streak"] = int(self.daily_streak)
            self._emit_event("objective_reward", payload)
        return awarded

    def summary(self, limit: int = 3) -> List[str]:
        """Return human-readable progress lines suitable for the HUD."""

        self.refresh()
        lines: List[str] = []
        for key in self.ORDER:
            objective = self.objectives.get(key)
            if objective is None:
                continue
            prefix = "[x]" if objective.completed else "[ ]"
            lines.append(
                f"{prefix} {objective.name}: {objective.progress}/{objective.target}"
            )
            if len(lines) >= limit:
                break
        return lines

    @property
    def daily_objectives(self) -> List[Objective]:
        return [objective for objective in self.objectives.values() if objective.period == "daily"]

    @property
    def weekly_objectives(self) -> List[Objective]:
        return [objective for objective in self.objectives.values() if objective.period == "weekly"]

    def _emit_event(self, event_type: str, payload: dict[str, object]) -> None:
        emitter = self.event_emitter
        if emitter is None:
            return
        emitter({"type": str(event_type), "payload": dict(payload)})

    def _normalize_region(
        self,
        region: Dict[str, object] | None,
        *,
        fallback_name: str,
    ) -> Dict[str, object]:
        info = region if isinstance(region, Mapping) else {}
        region_name = str(info.get("name") or fallback_name or "Arena")
        region_key = str(info.get("seed") or region_name)
        recommended_level = max(1, _safe_int(info.get("recommended_level"), 1))
        radius = max(1, _safe_int(info.get("radius"), 1))
        quest = str(info.get("quest", "ongoing operations") or "ongoing operations")
        biome = str(info.get("biome") or self.region_biome or "arena")
        hazard_name = ""
        hazard_target = 0
        auto_dev = info.get("auto_dev", {})
        if isinstance(auto_dev, Mapping):
            hazard = auto_dev.get("hazard_challenge", {})
            if isinstance(hazard, Mapping):
                hazard_name = str(hazard.get("hazard", "")).strip()
                hazard_target = max(0, _safe_int(hazard.get("target"), 0))
        return {
            "region_name": region_name,
            "region_key": region_key,
            "region_biome": biome,
            "recommended_level": recommended_level,
            "radius": radius,
            "quest": quest,
            "hazard_name": hazard_name,
            "hazard_target": hazard_target,
        }

    def _progression_tier(self) -> int:
        level = 1
        provider = self.progression_level_provider
        if provider is not None:
            try:
                level = _safe_int(provider(), 1)
            except Exception:
                level = 1
        region_level = max(1, _safe_int(self.region_context.get("recommended_level"), 1))
        effective_level = max(level, region_level)
        return _clamp(((effective_level - 1) // 5) + 1, 1, 5)

    def _remove_period_duplicates(self, protected_period: str) -> None:
        protected_types = {
            objective.objective_type
            for objective in self.objectives.values()
            if objective.period == protected_period
        }
        for key in list(self.objectives):
            objective = self.objectives.get(key)
            if objective is None or objective.period == protected_period:
                continue
            if objective.objective_type in protected_types:
                self.objectives.pop(key, None)

    def _candidate_types(self, period: str) -> list[str]:
        candidates: list[str] = []
        for objective_type, template in self.TEMPLATES.items():
            if period not in template.periods:
                continue
            if objective_type == "hazard_mastery" and not self.region_context.get("hazard_name"):
                continue
            candidates.append(objective_type)
        return candidates

    def _generate_period(self, period: str, period_key: str, now: datetime) -> None:
        for key in [
            objective_key
            for objective_key, objective in self.objectives.items()
            if objective.period == period
        ]:
            self.objectives.pop(key, None)
        selected = self._select_types(period, period_key)
        for objective_type in selected:
            objective = self._build_objective(objective_type, period, period_key, now)
            self.objectives[objective.objective_type] = objective
        self.last_assigned_types[period] = list(selected)
        history = self.assignment_history.setdefault(period, {})
        values = list(history.get(period_key, []))
        values.extend(selected)
        history[period_key] = values[-21:]

    def _select_types(self, period: str, period_key: str) -> list[str]:
        count = int(self.PERIOD_SLOTS.get(period, 1))
        candidates = self._candidate_types(period)
        forced: list[str] = []
        if period == "weekly" and "hazard_mastery" in candidates:
            forced.append("hazard_mastery")
            candidates = [item for item in candidates if item != "hazard_mastery"]
        if period == "weekly":
            current_daily = {
                objective.objective_type
                for objective in self.objectives.values()
                if objective.period == "daily"
            }
            candidates = [item for item in candidates if item not in current_daily] or candidates
        if period == "daily":
            weekly_types = {
                objective.objective_type
                for objective in self.objectives.values()
                if objective.period == "weekly"
            }
            candidates = [item for item in candidates if item not in weekly_types] or candidates
        history = self.assignment_history.get(period, {})
        history_values: list[str] = []
        if period == "daily":
            for history_key in sorted(history)[-3:]:
                history_values.extend(list(history.get(history_key, [])))
        else:
            history_values.extend(list(history.get(period_key, [])))
        repeat_block = set(self.last_assigned_types.get(period, []))
        region_token = str(self.region_key or self.region_name)
        seed_prefix = f"{self.profile_id}:{region_token}:{period}:{period_key}"
        ranked = sorted(
            candidates,
            key=lambda objective_type: (
                history_values.count(objective_type),
                1 if objective_type in repeat_block else 0,
                self._stable_score(f"{seed_prefix}:{objective_type}"),
            ),
        )
        remaining = max(0, count - len(forced))
        return forced + ranked[: max(0, min(remaining, len(ranked)))]

    @staticmethod
    def _stable_score(token: str) -> int:
        digest = sha256(token.encode("utf-8")).hexdigest()
        return int(digest[:12], 16)

    def _build_objective(
        self,
        objective_type: str,
        period: str,
        period_key: str,
        now: datetime,
    ) -> Objective:
        template = self.TEMPLATES[objective_type]
        tier = self._progression_tier()
        recommended = max(1, _safe_int(self.region_context.get("recommended_level"), 1))
        radius = max(1, _safe_int(self.region_context.get("radius"), 1))
        if objective_type == "hazard_mastery":
            base = max(
                template.minimum,
                _safe_int(self.region_context.get("hazard_target"), template.base_weekly),
            )
        elif period == "weekly":
            base = template.base_weekly
        else:
            base = template.base_daily
        target = base + (tier * template.tier_step)
        target += radius * template.radius_step
        target += recommended * template.recommended_step
        if period == "weekly" and objective_type != "hazard_mastery":
            target = max(target, template.base_weekly)
        target = _clamp(target, template.minimum, template.maximum)
        if period == "weekly" and objective_type in {"defeat_enemies", "earn_coins", "collect_powerups"}:
            target = _clamp(
                max(target, self._weekly_floor(objective_type)),
                template.minimum,
                template.maximum,
            )
        reward = self._build_reward(template, period, tier, target)
        created_utc = _utc_iso(now)
        expires_utc = _utc_iso(self._expiry_for_period(period, now))
        objective_id = f"{period}:{period_key}:{objective_type}"
        name = self._objective_name(objective_type, period)
        description = self._objective_description(objective_type, target)
        created_day_key = period_key if period == "daily" else None
        created_week_key = period_key if period == "weekly" else None
        expires_day_key = (
            self.time_provider.day_key(self._expiry_for_period(period, now))
            if period == "daily"
            else None
        )
        expires_week_key = (
            self.time_provider.week_key(self._expiry_for_period(period, now))
            if period == "weekly"
            else None
        )
        return Objective(
            objective_id=objective_id,
            objective_type=objective_type,
            period=period,
            name=name,
            description=description,
            target=target,
            reward=reward,
            created_utc=created_utc,
            expires_utc=expires_utc,
            created_day_key=created_day_key,
            created_week_key=created_week_key,
            expires_day_key=expires_day_key,
            expires_week_key=expires_week_key,
            metadata={"period_key": period_key, "region_key": self.region_key},
        )

    def _weekly_floor(self, objective_type: str) -> int:
        if objective_type == "defeat_enemies":
            return 20
        if objective_type == "earn_coins":
            return 80
        if objective_type == "collect_powerups":
            return 8
        return 1

    def _build_reward(
        self,
        template: ObjectiveTemplate,
        period: str,
        tier: int,
        target: int,
    ) -> dict[str, int]:
        period_mult = 2 if period == "weekly" else 1
        scale = max(1, target // max(1, template.minimum))
        coins = template.reward_base_coins
        xp = template.reward_base_xp
        coins += tier * template.reward_step_coins
        xp += tier * template.reward_step_xp
        coins += max(0, scale - 1) * max(1, template.reward_step_coins // 2)
        xp += max(0, scale - 1) * max(1, template.reward_step_xp // 2)
        coins *= period_mult
        xp *= period_mult
        return {"coins": _clamp(coins, 1, 500), "xp": _clamp(xp, 1, 2000)}

    def _objective_name(self, objective_type: str, period: str) -> str:
        prefix = "Daily" if period == "daily" else "Weekly"
        names = {
            "defeat_enemies": "Frontline Sweep",
            "collect_powerups": "Support Drop Run",
            "earn_coins": "Funding Drive",
            "win_matches": "Arena Closer",
            "deal_damage": "Pressure Test",
            "hazard_mastery": "Hazard Mastery",
        }
        return f"{prefix} {names.get(objective_type, _humanize_key(objective_type))}"

    def _objective_description(self, objective_type: str, target: int) -> str:
        region_name = str(self.region_context.get("region_name", self.region_name))
        quest = str(self.region_context.get("quest", "ongoing operations"))
        hazard_name = str(self.region_context.get("hazard_name", "")).strip() or "regional"
        descriptions = {
            "defeat_enemies": f"Defeat {target} foes while securing {region_name}.",
            "collect_powerups": (
                f"Collect {target} power-ups while advancing {quest}."
            ),
            "earn_coins": f"Earn {target} coins to fund {region_name} operations.",
            "win_matches": f"Win {target} arena matches for {region_name}.",
            "deal_damage": f"Deal {target} total damage on the {region_name} front.",
            "hazard_mastery": (
                f"Endure {target} {hazard_name} hazard events around {region_name}."
            ),
        }
        return descriptions.get(objective_type, f"Complete {target} {objective_type}.")

    def _expiry_for_period(self, period: str, now: datetime) -> datetime:
        start = now.astimezone(timezone.utc).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        if period == "daily":
            return start + timedelta(days=1)
        weekday = start.weekday()
        week_start = start - timedelta(days=weekday)
        return week_start + timedelta(days=7)

    def _reward_with_streak_bonus(self, objective: Objective) -> dict[str, int]:
        reward = dict(objective.reward)
        if objective.period != "daily" or self.daily_streak <= 1:
            return reward
        bonus_steps = min(self.daily_streak - 1, 4)
        if bonus_steps <= 0:
            return reward
        multiplier = 1.0 + (0.1 * bonus_steps)
        for key in ("coins", "xp"):
            if key in reward:
                reward[key] = max(reward[key], int(round(reward[key] * multiplier)))
        return reward

    def _record_daily_completion(self) -> None:
        current_day = self.time_provider.day_key()
        if self.last_daily_completion_day_key == current_day:
            return
        distance = _day_distance(current_day, self.last_daily_completion_day_key)
        if distance == 1:
            self.daily_streak += 1
        elif distance in {0, None}:
            self.daily_streak = max(1, self.daily_streak)
        else:
            self.daily_streak = 1
        self.last_daily_completion_day_key = current_day

    def _sync_streak(self, current_day: str) -> None:
        distance = _day_distance(current_day, self.last_daily_completion_day_key)
        if distance is not None and distance > 1:
            self.daily_streak = 0

    def _prune_history(self, current_day_key: str, current_week_key: str) -> None:
        daily_history = self.assignment_history.setdefault("daily", {})
        keep_daily = set(sorted(daily_history)[-7:])
        keep_daily.add(current_day_key)
        for key in list(daily_history):
            if key not in keep_daily:
                daily_history.pop(key, None)
        weekly_history = self.assignment_history.setdefault("weekly", {})
        for key in list(weekly_history):
            if key != current_week_key:
                weekly_history.pop(key, None)
