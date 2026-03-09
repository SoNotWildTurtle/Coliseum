"""Periodic playtest snapshot emitter for opt-in dev diagnostics."""

from __future__ import annotations

import json
import os
from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .save_manager import SAVE_DIR


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class SnapshotEmitter:
    """Emit periodic JSON snapshots from a live game instance."""

    def __init__(
        self,
        game_ref: Any,
        output_dir: str | os.PathLike[str],
        interval_sec: float = 2.0,
        max_files: int = 200,
    ) -> None:
        self.game_ref = game_ref
        self.output_dir = Path(output_dir)
        self.snapshots_dir = self.output_dir / "snapshots"
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        self.interval_sec = max(0.2, float(interval_sec))
        self.max_files = max(10, int(max_files))
        self._last_emit_ticks = -1_000_000_000
        self._event_types: deque[str] = deque(maxlen=256)
        self._event_bus = None

    @classmethod
    def from_env(cls, game_ref: Any) -> "SnapshotEmitter | None":
        if os.environ.get("HOLO_PLAYTEST", "0") != "1":
            return None
        root = os.environ.get("HOLO_PLAYTEST_DIR", str(Path(SAVE_DIR) / "playtest"))
        interval = float(os.environ.get("HOLO_PLAYTEST_INTERVAL", "2.0") or 2.0)
        max_files = int(os.environ.get("HOLO_PLAYTEST_MAX_FILES", "200") or 200)
        session_id = os.environ.get("HOLO_PLAYTEST_SESSION")
        if not session_id:
            session_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        return cls(
            game_ref,
            Path(root) / str(session_id),
            interval_sec=interval,
            max_files=max_files,
        )

    def bind_event_bus(self, event_bus: Any) -> None:
        self._event_bus = event_bus
        if event_bus is not None:
            event_bus.subscribe("*", self._on_event)

    def close(self) -> None:
        if self._event_bus is not None:
            self._event_bus.unsubscribe("*", self._on_event)
            self._event_bus = None

    def tick(self, frame: int, ticks: int) -> None:
        if ticks - self._last_emit_ticks < int(self.interval_sec * 1000):
            return
        self._last_emit_ticks = int(ticks)
        snapshot = self._build_snapshot(frame=frame, ticks=ticks)
        markers = self._issue_markers(snapshot)
        if markers:
            snapshot["issue_markers"] = markers
        name = f"snap_{int(frame):08d}.json"
        target = self.snapshots_dir / name
        tmp_path = target.with_suffix(".json.tmp")
        tmp_path.write_text(json.dumps(snapshot, indent=2, sort_keys=True), encoding="utf-8")
        os.replace(tmp_path, target)
        if markers and self._event_bus is not None:
            for marker in markers:
                self._event_bus.publish(
                    {
                        "type": "playtest_issue",
                        "t": int(ticks),
                        "frame": int(frame),
                        "payload": marker,
                    }
                )
        self._prune()

    def _on_event(self, event: dict[str, Any]) -> None:
        event_type = str(event.get("type", "unknown"))
        self._event_types.append(event_type)

    def _prune(self) -> None:
        files = sorted(self.snapshots_dir.glob("snap_*.json"))
        if len(files) <= self.max_files:
            return
        for path in files[: len(files) - self.max_files]:
            try:
                path.unlink()
            except OSError:
                pass

    def _build_snapshot(self, *, frame: int, ticks: int) -> dict[str, Any]:
        game = self.game_ref
        missing: list[str] = []
        state_name = str(getattr(game, "state", "unknown"))
        player = getattr(game, "player", None)
        if player is None:
            missing.append("player")

        player_snapshot: dict[str, Any] = {
            "hp": None,
            "max_hp": None,
            "position": None,
            "velocity": None,
            "status_effects": [],
            "cooldowns": [],
        }
        if player is not None:
            hp = _safe_float(getattr(player, "health", 0.0), 0.0)
            max_hp = _safe_float(getattr(player, "max_health", 0.0), 0.0)
            player_snapshot["hp"] = round(hp, 2)
            player_snapshot["max_hp"] = round(max_hp, 2)
            rect = getattr(player, "rect", None)
            if rect is not None and hasattr(rect, "centerx"):
                player_snapshot["position"] = [int(rect.centerx), int(rect.centery)]
            else:
                missing.append("player.rect")
            vx = None
            vy = None
            for key in ("velocity_x", "vel_x", "vx"):
                if hasattr(player, key):
                    vx = _safe_float(getattr(player, key), 0.0)
                    break
            for key in ("velocity_y", "vel_y", "vy"):
                if hasattr(player, key):
                    vy = _safe_float(getattr(player, key), 0.0)
                    break
            if vx is not None or vy is not None:
                player_snapshot["velocity"] = [round(vx or 0.0, 2), round(vy or 0.0, 2)]
            status_manager = getattr(game, "status_manager", None)
            if status_manager is not None and hasattr(status_manager, "active_effects"):
                effects = status_manager.active_effects(player, int(ticks))
                cleaned_effects = []
                for effect in effects:
                    if isinstance(effect, dict):
                        cleaned_effects.append(
                            {
                                "name": str(effect.get("name", "")),
                                "remaining_ms": _safe_int(effect.get("remaining_ms"), 0),
                            }
                        )
                player_snapshot["status_effects"] = cleaned_effects
            cooldown_status = getattr(player, "cooldown_status", None)
            if callable(cooldown_status):
                cooldowns = cooldown_status(int(ticks))
                cleaned_cd = []
                for entry in cooldowns:
                    if isinstance(entry, dict):
                        cleaned_cd.append(
                            {
                                "name": str(entry.get("name", "")),
                                "remaining_ms": _safe_int(entry.get("remaining_ms"), 0),
                                "total_ms": _safe_int(entry.get("total_ms"), 0),
                            }
                        )
                player_snapshot["cooldowns"] = cleaned_cd

        enemies = getattr(game, "enemies", []) or []
        enemy_count = len(enemies)
        nearest_enemy_distance = None
        if player is not None and getattr(player, "rect", None) is not None:
            px = float(player.rect.centerx)
            py = float(player.rect.centery)
            best = None
            for enemy in enemies:
                rect = getattr(enemy, "rect", None)
                if rect is None:
                    continue
                dx = float(rect.centerx) - px
                dy = float(rect.centery) - py
                dist = (dx * dx + dy * dy) ** 0.5
                if best is None or dist < best:
                    best = dist
            nearest_enemy_distance = None if best is None else round(float(best), 2)

        economy = {
            "coins": 0,
            "xp": 0,
            "level": 1,
            "reputation_total": 0,
            "reputation": {},
        }
        if player is not None:
            currency_manager = getattr(player, "currency_manager", None)
            if currency_manager is not None and hasattr(currency_manager, "get_balance"):
                economy["coins"] = _safe_int(currency_manager.get_balance(), 0)
            xp_manager = getattr(player, "experience_manager", None)
            if xp_manager is not None:
                economy["xp"] = _safe_int(getattr(xp_manager, "xp", 0), 0)
                economy["level"] = _safe_int(getattr(xp_manager, "level", 1), 1)
        reputation_manager = getattr(game, "reputation_manager", None)
        if reputation_manager is not None and hasattr(reputation_manager, "to_dict"):
            rep = reputation_manager.to_dict()
            if isinstance(rep, dict):
                economy["reputation"] = {str(k): _safe_int(v, 0) for k, v in rep.items()}
                economy["reputation_total"] = int(sum(economy["reputation"].values()))

        objectives: dict[str, Any] = {"active_ids": [], "progress": {}}
        objective_manager = getattr(game, "objective_manager", None)
        if objective_manager is not None and hasattr(objective_manager, "objectives"):
            active_ids = []
            progress: dict[str, Any] = {}
            for key, obj in objective_manager.objectives.items():
                active_ids.append(str(key))
                progress[str(key)] = {
                    "progress": _safe_int(getattr(obj, "progress", 0), 0),
                    "target": _safe_int(getattr(obj, "target", 0), 0),
                    "rewarded": bool(getattr(obj, "rewarded", False)),
                }
            objectives["active_ids"] = active_ids
            objectives["progress"] = progress
        else:
            missing.append("objective_manager.objectives")

        event_counts = Counter(self._event_types)
        event_summary = {
            "window_size": len(self._event_types),
            "counts": dict(sorted(event_counts.items())),
        }

        return {
            "timestamp_utc": _utc_now(),
            "frame": int(frame),
            "ticks": int(ticks),
            "state": state_name,
            "player": player_snapshot,
            "world": {
                "enemy_count": int(enemy_count),
                "nearest_enemy_distance": nearest_enemy_distance,
            },
            "economy": economy,
            "objectives": objectives,
            "events_summary": event_summary,
            "missing": sorted(set(missing)),
        }

    def _issue_markers(self, snapshot: dict[str, Any]) -> list[dict[str, Any]]:
        markers: list[dict[str, Any]] = []
        player = snapshot.get("player", {})
        hp = _safe_float(player.get("hp"), 0.0)
        max_hp = _safe_float(player.get("max_hp"), 0.0)
        if max_hp > 0:
            ratio = hp / max_hp
            if ratio <= 0.1:
                markers.append(
                    {
                        "kind": "near_death",
                        "severity": "high",
                        "message": "Player HP below 10%",
                    }
                )
            elif ratio <= 0.25:
                markers.append(
                    {
                        "kind": "low_hp",
                        "severity": "medium",
                        "message": "Player HP below 25%",
                    }
                )
        nearest = snapshot.get("world", {}).get("nearest_enemy_distance")
        if nearest is not None and _safe_float(nearest, 0.0) < 40.0:
            markers.append(
                {
                    "kind": "enemy_pressure",
                    "severity": "medium",
                    "message": "Enemy pressure very close to player",
                }
            )
        return markers
