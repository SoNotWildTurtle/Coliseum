"""Lightweight UI diagnostics for overlay rendering and layout logging."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from typing import Any

import pygame


@dataclass(frozen=True, slots=True)
class RectRecord:
    """Small immutable record describing a collected UI rectangle."""

    name: str
    kind: str
    rect: pygame.Rect
    meta: dict[str, Any]


def _rect_payload(rect: pygame.Rect) -> dict[str, int]:
    return {"x": int(rect.x), "y": int(rect.y), "w": int(rect.width), "h": int(rect.height)}


class UIDebugger:
    """Collect, check, and optionally draw UI layout diagnostics."""

    def __init__(
        self,
        enabled: bool = False,
        output_dir: str | Path | None = None,
        *,
        log_enabled: bool = False,
        log_frames: bool = False,
        headless: bool | None = None,
    ) -> None:
        self.overlay_enabled = bool(enabled)
        self.log_enabled = bool(log_enabled)
        self.log_frames = bool(log_frames)
        env_headless = str(os.environ.get("PYGAME_HEADLESS", "0")) == "1"
        self.headless = env_headless if headless is None else bool(headless)
        self.output_dir = Path(output_dir) if output_dir else Path("SavedGames") / "ui_debug"
        self._font: pygame.font.Font | None = None
        self._reset_runtime()

    @property
    def is_active(self) -> bool:
        return self.overlay_enabled or self.log_enabled

    def _reset_runtime(self) -> None:
        self.frame_index = 0
        self.current_mode = "unknown"
        self.current_state = "unknown"
        self.current_fps = 0.0
        self.current_resolution = (0, 0)
        self.current_ui_scale = 1.0
        self.current_effective_scale = 1.0
        self.current_records: list[RectRecord] = []
        self.current_overflows: list[dict[str, Any]] = []
        self.current_collisions: list[dict[str, Any]] = []
        self.current_clip_risks: list[dict[str, Any]] = []
        self.summary: dict[str, Any] = {
            "schema_version": "1.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "metadata": {},
            "counts": {
                "overflow_count": 0,
                "collision_count": 0,
                "clip_risk_count": 0,
            },
            "modes": {},
            "top_offenders": [],
        }
        self._offenders: dict[tuple[str, str], dict[str, Any]] = {}
        self._frame_logs: list[dict[str, Any]] = []

    def toggle(self) -> bool:
        """Toggle overlay visibility and return its new value."""
        self.overlay_enabled = not self.overlay_enabled
        return self.overlay_enabled

    def begin_frame(
        self,
        *,
        mode: str,
        state_name: str,
        resolution: tuple[int, int],
        ui_scale: float,
        effective_font_scale: float,
        fps: float,
    ) -> None:
        """Initialize frame-local debug collection."""
        if not self.is_active:
            return
        self.current_mode = str(mode)
        self.current_state = str(state_name)
        self.current_resolution = (int(resolution[0]), int(resolution[1]))
        self.current_ui_scale = float(ui_scale)
        self.current_effective_scale = float(effective_font_scale)
        self.current_fps = float(fps)
        self.current_records.clear()
        self.current_overflows.clear()
        self.current_collisions.clear()
        self.current_clip_risks.clear()

    def collect_rect(
        self,
        name: str,
        rect: pygame.Rect,
        kind: str,
        meta: dict[str, Any] | None = None,
    ) -> None:
        """Collect a top-level UI rectangle and optional bounds checks."""
        if not self.is_active:
            return
        payload = dict(meta or {})
        safe_rect = pygame.Rect(rect)
        record = RectRecord(str(name), str(kind), safe_rect, payload)
        self.current_records.append(record)
        bounds_value = payload.get("bounds")
        if isinstance(bounds_value, pygame.Rect):
            self.check_overflow(record.name, safe_rect, bounds_value, kind=record.kind)
        clip_size = payload.get("text_size")
        if isinstance(clip_size, (tuple, list)) and len(clip_size) == 2:
            self.record_clip_risk(record.name, tuple(clip_size), safe_rect)

    def check_overflow(
        self,
        name: str,
        rect: pygame.Rect,
        bounds_rect: pygame.Rect,
        *,
        tolerance: int = 12,
        kind: str = "rect",
    ) -> None:
        """Record overflow details when ``rect`` exceeds ``bounds_rect``."""
        if not self.is_active:
            return
        edges: dict[str, int] = {}
        if rect.left < bounds_rect.left - tolerance:
            edges["left"] = int(bounds_rect.left - rect.left)
        if rect.top < bounds_rect.top - tolerance:
            edges["top"] = int(bounds_rect.top - rect.top)
        if rect.right > bounds_rect.right + tolerance:
            edges["right"] = int(rect.right - bounds_rect.right)
        if rect.bottom > bounds_rect.bottom + tolerance:
            edges["bottom"] = int(rect.bottom - bounds_rect.bottom)
        if not edges:
            return
        self.current_overflows.append(
            {
                "name": str(name),
                "kind": str(kind),
                "rect": _rect_payload(rect),
                "bounds": _rect_payload(bounds_rect),
                "overflow_edges": edges,
            }
        )

    def check_collisions(
        self,
        group_name: str,
        rects: list[tuple[str, pygame.Rect]],
    ) -> None:
        """Record collisions among rect pairs within a logical group."""
        if not self.is_active or len(rects) < 2:
            return
        for left in range(len(rects)):
            a_name, a_rect = rects[left]
            for right in range(left + 1, len(rects)):
                b_name, b_rect = rects[right]
                overlap = a_rect.clip(b_rect)
                if overlap.width <= 0 or overlap.height <= 0:
                    continue
                self.current_collisions.append(
                    {
                        "group": str(group_name),
                        "a": str(a_name),
                        "b": str(b_name),
                        "intersection_area": int(overlap.width * overlap.height),
                        "intersection": _rect_payload(overlap),
                    }
                )

    def record_clip_risk(
        self,
        name: str,
        text_size: tuple[int, int],
        container_rect: pygame.Rect,
    ) -> None:
        """Record possible text clipping when text exceeds its container."""
        if not self.is_active:
            return
        tw, th = int(text_size[0]), int(text_size[1])
        if tw <= container_rect.width and th <= container_rect.height:
            return
        self.current_clip_risks.append(
            {
                "name": str(name),
                "text_size": {"w": tw, "h": th},
                "container": _rect_payload(container_rect),
            }
        )

    def _ensure_font(self) -> pygame.font.Font | None:
        if self._font is not None:
            return self._font
        try:
            self._font = pygame.font.SysFont(None, 16)
        except Exception:
            self._font = None
        return self._font

    def render_overlay(
        self,
        surface: pygame.Surface,
        ui_metrics,
        fps: float,
        state_name: str,
    ) -> None:
        """Draw overlay boxes and summary text when enabled."""
        if not self.overlay_enabled or self.headless:
            return
        font = self._ensure_font()
        if font is None:
            return
        width, height = surface.get_size()
        gutter = 12
        if ui_metrics is not None and hasattr(ui_metrics, "gutter"):
            gutter = max(0, int(ui_metrics.gutter))
        safe_rect = pygame.Rect(gutter, gutter, max(0, width - 2 * gutter), max(0, height - 2 * gutter))
        pygame.draw.rect(surface, (80, 180, 240), safe_rect, 1)
        colors = {
            "bounds": (120, 190, 240),
            "panel": (120, 220, 180),
            "title": (220, 220, 120),
            "option": (240, 180, 120),
            "highlight": (255, 120, 120),
            "label": (190, 170, 240),
        }
        for item in self.current_records:
            color = colors.get(item.kind, (180, 180, 180))
            pygame.draw.rect(surface, color, item.rect, 1)
        for issue in self.current_overflows:
            rect_data = issue["rect"]
            rect = pygame.Rect(rect_data["x"], rect_data["y"], rect_data["w"], rect_data["h"])
            pygame.draw.rect(surface, (255, 70, 70), rect, 2)
        for issue in self.current_collisions:
            rect_data = issue["intersection"]
            rect = pygame.Rect(rect_data["x"], rect_data["y"], rect_data["w"], rect_data["h"])
            pygame.draw.rect(surface, (255, 80, 140), rect, 2)
        lines = [
            f"UI Debug  {width}x{height}  fps:{fps:.1f}",
            f"state:{state_name} mode:{self.current_mode}",
            f"scale:{self.current_effective_scale:.3f} ui:{self.current_ui_scale:.3f}",
            f"overflow:{len(self.current_overflows)} collisions:{len(self.current_collisions)} clip:{len(self.current_clip_risks)}",
        ]
        y = 8
        for line in lines:
            label = font.render(line, True, (230, 240, 250))
            shadow = font.render(line, True, (10, 12, 16))
            surface.blit(shadow, (9, y + 1))
            surface.blit(label, (8, y))
            y += label.get_height() + 2

    def _mode_bucket(self, mode: str) -> dict[str, Any]:
        modes = self.summary.setdefault("modes", {})
        bucket = modes.get(mode)
        if bucket is None:
            bucket = {
                "frames": 0,
                "overflow_count": 0,
                "collision_count": 0,
                "clip_risk_count": 0,
                "sample_overflows": [],
                "sample_collisions": [],
                "sample_clip_risks": [],
            }
            modes[mode] = bucket
        return bucket

    def _record_offender(self, issue_type: str, name: str, payload: dict[str, Any]) -> None:
        key = (issue_type, name)
        existing = self._offenders.get(key)
        if existing is None:
            self._offenders[key] = {
                "type": issue_type,
                "name": name,
                "count": 1,
                "sample": payload,
            }
            return
        existing["count"] = int(existing["count"]) + 1

    def flush_frame(self, frame_index: int) -> None:
        """Finalize frame metrics and aggregate summary counters."""
        if not self.is_active:
            return
        self.frame_index = int(frame_index)
        bucket = self._mode_bucket(self.current_mode)
        bucket["frames"] += 1
        overflow_count = len(self.current_overflows)
        collision_count = len(self.current_collisions)
        clip_count = len(self.current_clip_risks)
        self.summary["counts"]["overflow_count"] += overflow_count
        self.summary["counts"]["collision_count"] += collision_count
        self.summary["counts"]["clip_risk_count"] += clip_count
        bucket["overflow_count"] += overflow_count
        bucket["collision_count"] += collision_count
        bucket["clip_risk_count"] += clip_count
        if overflow_count and len(bucket["sample_overflows"]) < 8:
            bucket["sample_overflows"].extend(self.current_overflows[: 8 - len(bucket["sample_overflows"])])
        if collision_count and len(bucket["sample_collisions"]) < 8:
            bucket["sample_collisions"].extend(self.current_collisions[: 8 - len(bucket["sample_collisions"])])
        if clip_count and len(bucket["sample_clip_risks"]) < 8:
            bucket["sample_clip_risks"].extend(self.current_clip_risks[: 8 - len(bucket["sample_clip_risks"])])
        for issue in self.current_overflows:
            self._record_offender("overflow", issue["name"], issue)
        for issue in self.current_collisions:
            self._record_offender("collision", f"{issue['a']}::{issue['b']}", issue)
        for issue in self.current_clip_risks:
            self._record_offender("clip_risk", issue["name"], issue)
        if self.log_enabled and self.log_frames:
            self._frame_logs.append(
                {
                    "frame_index": int(frame_index),
                    "mode": self.current_mode,
                    "state": self.current_state,
                    "fps": self.current_fps,
                    "overflow_count": overflow_count,
                    "collision_count": collision_count,
                    "clip_risk_count": clip_count,
                }
            )

    def set_metadata(self, **kwargs: Any) -> None:
        """Merge metadata entries into the summary header."""
        if not self.is_active:
            return
        metadata = self.summary.setdefault("metadata", {})
        metadata.update(kwargs)

    def finalize_run(self, summary_path: str | Path | None = None) -> Path | None:
        """Write summary JSON artifacts and return the primary path."""
        if not self.log_enabled:
            return None
        offenders = sorted(
            self._offenders.values(),
            key=lambda item: int(item.get("count", 0)),
            reverse=True,
        )
        self.summary["top_offenders"] = offenders[:25]
        output_path = Path(summary_path) if summary_path else self.output_dir / "ui_layout_summary.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(self.summary, indent=2), encoding="utf-8")
        alias_path = self.output_dir / "ui_layout_summary.json"
        if alias_path.resolve() != output_path.resolve():
            alias_path.parent.mkdir(parents=True, exist_ok=True)
            alias_path.write_text(json.dumps(self.summary, indent=2), encoding="utf-8")
        if self.log_frames:
            frames_path = output_path.parent / "ui_layout_frames.json"
            frames_path.write_text(json.dumps(self._frame_logs, indent=2), encoding="utf-8")
        return output_path
