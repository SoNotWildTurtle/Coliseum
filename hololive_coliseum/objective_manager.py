"""Track rotating arena objectives linked to MMO world regions."""

"""Manage rotating objectives shared between arenas and MMO regions."""

from dataclasses import dataclass, field
from typing import Dict, Iterable, List


@dataclass
class Objective:
    """Store progress for a single arena objective."""

    key: str
    description: str
    target: int
    progress: int = 0
    scope: str = "daily"
    rewards: Dict[str, int] = field(default_factory=dict)
    rewarded: bool = False

    def to_dict(self) -> Dict[str, object]:
        """Return a JSON-serialisable representation of the objective."""

        return {
            "description": self.description,
            "target": self.target,
            "progress": self.progress,
            "scope": self.scope,
            "rewards": dict(self.rewards),
            "rewarded": self.rewarded,
        }

    @classmethod
    def from_dict(cls, key: str, data: Dict[str, object]) -> "Objective":
        """Build an :class:`Objective` from saved data."""

        return cls(
            key=key,
            description=str(data.get("description", "")),
            target=int(data.get("target", 0)),
            progress=int(data.get("progress", 0)),
            scope=str(data.get("scope", "daily")),
            rewards=dict(data.get("rewards", {})),
            rewarded=bool(data.get("rewarded", False)),
        )

    def record(self, amount: int = 1) -> None:
        """Increment ``progress`` towards ``target`` by ``amount``."""

        if amount <= 0:
            return
        self.progress = min(self.target, self.progress + amount)

    def completed(self) -> bool:
        """Return ``True`` when the objective has been fulfilled."""

        return self.progress >= self.target


class ObjectiveManager:
    """Coordinate rotating objectives for the arena and MMO."""

    EVENT_MAP: Dict[str, Iterable[str]] = {
        "enemy_defeated": ("defeat_enemies",),
        "coin_collected": ("collect_coins",),
        "powerup_collected": ("collect_powerups",),
        "match_victory": ("win_matches",),
        "hazard_logged": ("hazard_mastery",),
    }

    ORDER: List[str] = [
        "defeat_enemies",
        "collect_coins",
        "collect_powerups",
        "hazard_mastery",
        "win_matches",
    ]

    def __init__(self) -> None:
        self.region_key: str | None = None
        self.region_name: str = "Arena"
        self.region_biome: str = "arena"
        self.objectives: Dict[str, Objective] = {}

    def load_from_dict(self, data: Dict[str, object]) -> None:
        """Restore objectives from saved settings."""

        self.region_key = data.get("region_key") or None
        self.region_name = str(data.get("region_name", self.region_name))
        self.region_biome = str(data.get("region_biome", self.region_biome))
        raw = data.get("objectives") or {}
        self.objectives = {
            key: Objective.from_dict(key, value)
            for key, value in raw.items()
        }

    def to_dict(self) -> Dict[str, object]:
        """Return the persisted representation of the manager."""

        return {
            "region_key": self.region_key,
            "region_name": self.region_name,
            "region_biome": self.region_biome,
            "objectives": {k: obj.to_dict() for k, obj in self.objectives.items()},
        }

    def ensure_region_objectives(
        self, region: Dict[str, object] | None, fallback_name: str = "Arena"
    ) -> None:
        """Create objectives for ``region`` if they do not already exist."""

        region = region or {}
        region_name = str(region.get("name") or fallback_name)
        region_key = str(region.get("seed") or region_name)
        biome = str(region.get("biome") or self.region_biome)
        if self.objectives and self.region_key == region_key:
            # Region unchanged; keep existing progress but refresh labels.
            self.region_name = region_name
            self.region_biome = biome
            return
        recommended = max(1, int(region.get("recommended_level", 1)))
        radius = max(1, int(region.get("radius", 1)))
        kill_target = max(5, recommended * 3)
        coin_target = max(10, 10 + radius * 4)
        drop_target = max(3, radius + 1)
        quest = str(region.get("quest", "ongoing operations"))
        self.region_key = region_key
        self.region_name = region_name
        self.region_biome = biome
        self.objectives = {
            "defeat_enemies": Objective(
                key="defeat_enemies",
                description=(
                    f"Defeat {kill_target} foes supporting the {region_name} front"
                ),
                target=kill_target,
                rewards={"coins": max(5, kill_target // 2)},
            ),
            "collect_coins": Objective(
                key="collect_coins",
                description=(
                    f"Gather {coin_target} coins to fund {region_name} upgrades"
                ),
                target=coin_target,
                scope="weekly",
                rewards={"xp": coin_target * 2},
            ),
            "collect_powerups": Objective(
                key="collect_powerups",
                description=(
                    f"Claim {drop_target} support drops while tackling {quest}"
                ),
                target=drop_target,
                rewards={"coins": drop_target, "xp": drop_target * 3},
            ),
            "win_matches": Objective(
                key="win_matches",
                description=f"Win an arena match for {region_name}",
                target=1,
                scope="weekly",
                rewards={"coins": 15, "xp": 50},
            ),
        }
        insight = {}
        raw_insight = region.get("auto_dev")
        if isinstance(raw_insight, dict):
            insight = raw_insight
        hazard_info = insight.get("hazard_challenge")
        if isinstance(hazard_info, dict):
            hazard_name = str(hazard_info.get("hazard", "")).strip()
            hazard_target = int(hazard_info.get("target", 0))
            if hazard_name:
                hazard_target = max(3, hazard_target)
                description = (
                    f"Withstand {hazard_target} {hazard_name} hazards around {region_name}"
                )
                self.objectives["hazard_mastery"] = Objective(
                    key="hazard_mastery",
                    description=description,
                    target=hazard_target,
                    scope="weekly",
                    rewards={"xp": hazard_target * 4},
                )

    def record_event(self, event: str, amount: int = 1) -> List[Dict[str, int]]:
        """Record ``event`` progress and return newly earned rewards."""

        rewards: List[Dict[str, int]] = []
        for key in self.EVENT_MAP.get(event, ()):
            objective = self.objectives.get(key)
            if not objective:
                continue
            objective.record(amount)
            if objective.completed() and not objective.rewarded:
                objective.rewarded = True
                if objective.rewards:
                    rewards.append(dict(objective.rewards))
        return rewards

    def summary(self, limit: int = 3) -> List[str]:
        """Return human-readable progress lines for the HUD."""

        lines: List[str] = []
        for key in self.ORDER:
            obj = self.objectives.get(key)
            if not obj:
                continue
            prefix = "✓" if obj.completed() else "•"
            lines.append(
                f"{prefix} {obj.description}: {obj.progress}/{obj.target}"
            )
            if len(lines) >= limit:
                break
        return lines
