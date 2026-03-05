"""Central UI scaling metrics and layout token helpers."""

from __future__ import annotations

from dataclasses import dataclass


UI_SCALE_MIN = 0.72
UI_SCALE_MAX = 1.85
USER_FONT_SCALE_MIN = 0.8
USER_FONT_SCALE_MAX = 1.6


def clamp_ui_scale(scale: float) -> float:
    """Clamp UI scale to the supported visual range."""
    return max(UI_SCALE_MIN, min(UI_SCALE_MAX, float(scale)))


def normalize_user_font_scale(scale: float) -> float:
    """Clamp user font preference to the supported accessibility range."""
    return max(USER_FONT_SCALE_MIN, min(USER_FONT_SCALE_MAX, float(scale)))


def compute_effective_font_scale(
    user_scale: float,
    screen_w: int,
    screen_h: int,
) -> float:
    """Return the effective font/UI scale from user preference and resolution."""
    clamped_user = normalize_user_font_scale(user_scale)
    baseline = min(screen_w / 1280, screen_h / 720)
    resolution_scale = max(0.78, min(1.22, baseline ** 0.35))
    return clamp_ui_scale(clamped_user * resolution_scale)


@dataclass(frozen=True, slots=True)
class UIMetrics:
    """Immutable UI metrics object exposing scale-aware layout helpers."""

    screen_w: int
    screen_h: int
    effective_font_scale: float
    ui_scale: float
    gutter_base: int = 16
    panel_pad_base: int = 16
    title_gap_base: int = 18
    corner_radius_base: int = 8
    border_base: int = 2
    shadow_base: int = 2
    button_height_base: int = 42

    def px(self, value: float) -> int:
        return max(0, int(round(float(value) * self.ui_scale)))

    def pad(self, value: float) -> int:
        return self.px(value)

    def radius(self, value: float) -> int:
        return self.px(value)

    def border(self, value: float) -> int:
        scaled = int(round(float(value) * self.ui_scale))
        if value > 0:
            return max(1, scaled)
        return max(0, scaled)

    def shadow(self, value: float) -> int:
        return self.px(value)

    def font_px(self, base_size: float) -> int:
        return max(10, int(round(float(base_size) * self.ui_scale)))

    @property
    def gutter(self) -> int:
        return self.pad(self.gutter_base)

    @property
    def panel_pad(self) -> int:
        return self.pad(self.panel_pad_base)

    @property
    def title_gap(self) -> int:
        return self.pad(self.title_gap_base)

    @property
    def corner_radius(self) -> int:
        return self.radius(self.corner_radius_base)

    @property
    def border_thickness(self) -> int:
        return self.border(self.border_base)

    @property
    def shadow_size(self) -> int:
        return self.shadow(self.shadow_base)

    @property
    def button_height(self) -> int:
        return self.pad(self.button_height_base)


def build_ui_metrics(
    effective_font_scale: float,
    screen_w: int,
    screen_h: int,
) -> UIMetrics:
    """Build immutable metrics using an already-computed effective scale."""
    ui_scale = clamp_ui_scale(effective_font_scale)
    return UIMetrics(
        screen_w=int(screen_w),
        screen_h=int(screen_h),
        effective_font_scale=ui_scale,
        ui_scale=ui_scale,
    )


def build_ui_metrics_from_user_scale(
    user_scale: float,
    screen_w: int,
    screen_h: int,
) -> UIMetrics:
    """Build immutable metrics from user font scale and resolution."""
    effective = compute_effective_font_scale(user_scale, int(screen_w), int(screen_h))
    return build_ui_metrics(effective, int(screen_w), int(screen_h))
