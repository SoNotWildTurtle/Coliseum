"""Draw the heads-up display showing player status, timer, score and overlays."""

from __future__ import annotations

from collections.abc import Sequence
import math

import pygame

from .ui_metrics import UIMetrics


FLASH_DURATION = 150  # milliseconds


class HUDManager:
    """Render status bars, combos and the arena overlay panels."""

    def __init__(
        self,
        font: pygame.font.Font | None = None,
        metrics: UIMetrics | None = None,
    ) -> None:
        self.font = font or pygame.font.SysFont(None, 24)
        self.metrics = metrics

    def _draw_text(
        self,
        screen: pygame.Surface,
        text: str,
        color: tuple[int, int, int],
        pos: tuple[int, int],
        *,
        shadow: tuple[int, int, int] = (10, 10, 15),
        offset: tuple[int, int] = (2, 2),
    ) -> None:
        shadow_render = self.font.render(text, True, shadow)
        screen.blit(shadow_render, (pos[0] + offset[0], pos[1] + offset[1]))
        render = self.font.render(text, True, color)
        screen.blit(render, pos)

    def _draw_panel(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        *,
        top: tuple[int, int, int],
        bottom: tuple[int, int, int],
        border: tuple[int, int, int],
        accent: tuple[int, int, int],
        pulse: float = 0.0,
    ) -> None:
        metrics = self.metrics
        border_w = metrics.border_thickness if metrics else 2
        panel_pad = metrics.panel_pad if metrics else 8
        title_gap = metrics.pad(4) if metrics else 4
        panel = pygame.Surface(rect.size, pygame.SRCALPHA)
        height = rect.height
        for y in range(height):
            ratio = y / max(1, height - 1)
            r = int(top[0] + (bottom[0] - top[0]) * ratio)
            g = int(top[1] + (bottom[1] - top[1]) * ratio)
            b = int(top[2] + (bottom[2] - top[2]) * ratio)
            panel.fill((r, g, b, 235), pygame.Rect(0, y, rect.width, 1))
        screen.blit(panel, rect.topleft)
        glow = pygame.Surface(rect.size, pygame.SRCALPHA)
        glow.fill((*accent, int(40 + 60 * pulse)))
        screen.blit(glow, rect.topleft)
        pygame.draw.rect(screen, border, rect, border_w)
        pygame.draw.line(
            screen,
            accent,
            (rect.x + panel_pad, rect.y + title_gap),
            (rect.right - panel_pad, rect.y + title_gap),
            border_w,
        )

    def draw(
        self,
        screen: pygame.Surface,
        player,
        score: int,
        elapsed: int,
        combo: int = 0,
        allies: Sequence[object] | None = None,
        objectives: list[str] | None = None,
        resource_summary: Sequence[tuple[str, object]] | None = None,
        status_effects: Sequence[dict[str, object]] | None = None,
        insights: Sequence[str] | None = None,
        auto_dev_summary: Sequence[tuple[str, object]] | None = None,
        world_activity: Sequence[str] | None = None,
        cooldowns: Sequence[dict[str, object]] | None = None,
        minimap: dict[str, object] | None = None,
        hype_meter: float | None = None,
        hype_label: str | None = None,
        threat_rating: float | None = None,
        threat_label: str | None = None,
        sfx_debug: str | None = None,
        sfx_profile: str | None = None,
        impact_scale: float | None = None,
    ) -> None:
        """Draw status bars, timers, combo text and optional objectives."""     
        metrics = self.metrics
        hud_pad = metrics.panel_pad if metrics else 10
        top_gap = metrics.pad(80) if metrics else 80
        player.draw_status(screen)
        if allies:
            self._draw_allies_panel(screen, allies)
        now = pygame.time.get_ticks()
        if now - getattr(player, "last_hit_time", -FLASH_DURATION) < FLASH_DURATION:
            scale = float(getattr(player, "last_hit_difficulty_scale", 1.0) or 1.0)
            alpha = int(min(180, max(60, 100 * scale)))
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, alpha))
            screen.blit(overlay, (0, 0))
        health_ratio = 1.0
        if getattr(player, "max_health", 0):
            health_ratio = player.health / player.max_health
        if health_ratio <= 0.25 and (now // 250) % 2 == 0:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 60))
            screen.blit(overlay, (0, 0))
        timer_label = f"Time: {elapsed}"
        timer_x = screen.get_width() - (metrics.pad(120) if metrics else 120)
        timer_y = hud_pad
        self._draw_text(screen, timer_label, (255, 255, 255), (timer_x, timer_y))
        score_label = f"Score: {score}"
        self._draw_text(screen, score_label, (255, 255, 255), (hud_pad, top_gap))
        if combo > 1:
            self._draw_text(
                screen,
                f"Combo: {combo}",
                (255, 255, 255),
                (hud_pad, top_gap + (metrics.pad(15) if metrics else 15)),
            )
            self._draw_combo_meter(screen, combo)
        if hype_meter is not None:
            self._draw_hype_panel(screen, hype_meter, hype_label or "Crowd")    
        if threat_rating is not None:
            self._draw_threat_chip(
                screen,
                threat_rating,
                threat_label,
            )
        if objectives:
            y = top_gap + (metrics.pad(30) if metrics else 30)
            height = len(objectives) * 15 + 10
            obj_rect = pygame.Rect(0, y - 5, screen.get_width(), height)
            pulse = (math.sin(now / 700) + 1) * 0.5
            self._draw_panel(
                screen,
                obj_rect,
                top=(18, 28, 44),
                bottom=(10, 16, 28),
                border=(70, 110, 150),
                accent=(120, 190, 220),
                pulse=pulse,
            )
            for line in objectives:
                self._draw_text(
                    screen,
                    line,
                    (200, 230, 255),
                    (hud_pad, y),
                    shadow=(10, 16, 24),
                )
                y += 15
        resource_rect = None
        if resource_summary:
            resource_rect = self._draw_resource_panel(screen, resource_summary)
        if auto_dev_summary:
            self._draw_auto_dev_panel(screen, auto_dev_summary, resource_rect)
        if insights:
            self._draw_insight_banner(screen, insights)
        if status_effects:
            self._draw_status_panel(screen, status_effects)
        if world_activity:
            self._draw_world_ticker(screen, world_activity)
        if cooldowns is None and hasattr(player, "cooldown_status"):
            cooldowns = player.cooldown_status(now)
        minimap_rect = None
        if minimap:
            minimap_rect = self._draw_minimap(screen, minimap)
        if cooldowns:
            self._draw_cooldown_panel(screen, cooldowns, minimap_rect)
        if sfx_debug or sfx_profile or impact_scale is not None:
            self._draw_sfx_debug(screen, sfx_debug, sfx_profile, impact_scale)

    def _draw_sfx_debug(
        self,
        screen: pygame.Surface,
        label: str | None,
        profile: str | None,
        impact_scale: float | None = None,
    ) -> None:
        """Render last-played SFX cue for debugging."""
        metrics = self.metrics
        pad = metrics.panel_pad if metrics else 10
        rect = pygame.Rect(
            pad,
            screen.get_height() - (metrics.pad(42) if metrics else 42),
            metrics.pad(260) if metrics else 260,
            metrics.pad(28) if metrics else 28,
        )
        pulse = (math.sin(pygame.time.get_ticks() / 600) + 1) * 0.5
        self._draw_panel(
            screen,
            rect,
            top=(16, 22, 30),
            bottom=(8, 12, 18),
            border=(90, 140, 170),
            accent=(120, 200, 220),
            pulse=pulse,
        )
        text = self._sfx_debug_text(label, profile, impact_scale)
        self._draw_text(
            screen,
            text,
            (220, 235, 245),
            (
                rect.x + (metrics.panel_pad if metrics else 8),
                rect.y + (metrics.pad(6) if metrics else 6),
            ),
            shadow=(8, 12, 18),
        )

    @staticmethod
    def _sfx_debug_text(
        label: str | None,
        profile: str | None,
        impact_scale: float | None,
    ) -> str:
        text = "SFX:"
        if label:
            text = f"SFX: {label}"
        if profile:
            text = f"{text} ({profile})"
        if impact_scale is not None:
            text = f"{text} Impact x{impact_scale:.2f}"
        return text

    def _draw_allies_panel(
        self,
        screen: pygame.Surface,
        allies: Sequence[object],
    ) -> None:
        """Render ally health bars beneath the player status panel."""
        if not allies:
            return
        now = pygame.time.get_ticks()
        width = 190
        height = 22 + 18 * len(allies)
        rect = pygame.Rect(10, 110, width, height)
        pulse = (math.sin(now / 800) + 1) * 0.5
        self._draw_panel(
            screen,
            rect,
            top=(18, 26, 36),
            bottom=(10, 16, 26),
            border=(80, 120, 160),
            accent=(130, 190, 220),
            pulse=pulse,
        )
        for idx, ally in enumerate(allies):
            name = getattr(ally, "display_name", None)
            if not name:
                name = f"Ally {idx + 1}"
            health = getattr(ally, "health", 0)
            max_health = max(1, int(getattr(ally, "max_health", 1)))
            lives = int(getattr(ally, "lives", 0))
            ratio = max(0.0, min(1.0, health / max_health))
            label = f"{name}  {health}/{max_health}  L{lives}"
            self._draw_text(
                screen,
                label,
                (210, 235, 255),
                (rect.x + 8, rect.y + 6 + idx * 18),
                shadow=(10, 14, 22),
            )
            bar_x = rect.right - 54
            bar_y = rect.y + 10 + idx * 18
            pygame.draw.rect(screen, (30, 50, 70), pygame.Rect(bar_x, bar_y, 40, 6))
            pygame.draw.rect(
                screen,
                (120, 210, 180),
                pygame.Rect(bar_x, bar_y, int(40 * ratio), 6),
            )
            pygame.draw.rect(
                screen,
                (120, 160, 190),
                pygame.Rect(bar_x, bar_y, 40, 6),
                1,
            )

    def _draw_resource_panel(
        self, screen: pygame.Surface, summary: Sequence[tuple[str, object]]     
    ) -> pygame.Rect:
        """Render a compact panel with resource values in the top-right corner."""

        now = pygame.time.get_ticks()
        width = 190
        height = 20 + 18 * len(summary)
        rect = pygame.Rect(
            screen.get_width() - width - 10,
            40,
            width,
            height,
        )
        pulse = (math.sin(now / 900) + 1) * 0.5
        self._draw_panel(
            screen,
            rect,
            top=(18, 26, 40),
            bottom=(10, 16, 28),
            border=(60, 90, 120),
            accent=(110, 180, 210),
            pulse=pulse,
        )
        for idx, (label, value) in enumerate(summary):
            self._draw_text(
                screen,
                f"{label}: {value}",
                (210, 235, 255),
                (rect.x + 8, rect.y + 6 + idx * 18),
                shadow=(10, 14, 22),
            )
        return rect

    def _draw_threat_chip(
        self,
        screen: pygame.Surface,
        threat: float,
        label: str | None,
    ) -> None:
        """Render a compact stage threat indicator near the timer."""

        threat = max(0.0, threat)
        ratio = min(1.0, threat / 10.0)
        base_r = int(80 + 160 * ratio)
        base_g = int(200 - 120 * ratio)
        accent = (base_r, base_g, 90)
        border = (min(255, base_r + 30), min(255, base_g + 30), 120)
        rect = pygame.Rect(screen.get_width() - 210, 38, 200, 36)
        pulse = (math.sin(pygame.time.get_ticks() / 700) + 1) * 0.5
        self._draw_panel(
            screen,
            rect,
            top=(18, 26, 38),
            bottom=(12, 18, 28),
            border=border,
            accent=accent,
            pulse=pulse,
        )
        label_text = label or "Stage"
        self._draw_text(
            screen,
            f"{label_text}",
            (220, 230, 240),
            (rect.x + 8, rect.y + 6),
            shadow=(8, 12, 18),
        )
        rating_text = f"Threat {round(threat, 1)}"
        rating_size = self.font.size(rating_text)
        self._draw_text(
            screen,
            rating_text,
            (240, 220, 160),
            (rect.right - rating_size[0] - 10, rect.y + 6),
            shadow=(8, 12, 18),
        )
        bar_rect = pygame.Rect(rect.x + 10, rect.y + 26, rect.width - 20, 6)
        pygame.draw.rect(screen, (25, 30, 40), bar_rect)
        pygame.draw.rect(
            screen,
            accent,
            pygame.Rect(bar_rect.x, bar_rect.y, int(bar_rect.width * ratio), 6),
        )

    def _draw_status_panel(
        self, screen: pygame.Surface, effects: Sequence[dict[str, object]]      
    ) -> None:
        """Render current status effects and durations above the bottom-right."""

        if not effects:
            return
        lines: list[str] = []
        for effect in effects:
            name = str(effect.get("name", "Effect"))
            remaining_ms = int(effect.get("remaining_ms", 0))
            remaining = max(0, round(remaining_ms / 1000))
            lines.append(f"{name}: {remaining}s")
        now = pygame.time.get_ticks()
        width = 200
        height = 20 + 18 * len(lines)
        rect = pygame.Rect(
            screen.get_width() - width - 10,
            max(0, screen.get_height() - height - 10),
            width,
            height,
        )
        pulse = (math.sin(now / 850) + 1) * 0.5
        self._draw_panel(
            screen,
            rect,
            top=(20, 32, 44),
            bottom=(12, 20, 30),
            border=(90, 120, 150),
            accent=(120, 200, 160),
            pulse=pulse,
        )
        for idx, line in enumerate(lines):
            self._draw_text(
                screen,
                line,
                (200, 255, 200),
                (rect.x + 8, rect.y + 6 + idx * 18),
                shadow=(10, 20, 10),
            )

    def _draw_insight_banner(
        self, screen: pygame.Surface, insights: Sequence[str]
    ) -> None:
        """Render a banner near the timer summarising match insights."""

        lines = [line for line in insights if line]
        if not lines:
            return
        width = 260
        height = 18 * len(lines) + 12
        rect = pygame.Rect((screen.get_width() - width) // 2, 36, width, height)
        now = pygame.time.get_ticks()
        pulse = (math.sin(now / 1100) + 1) * 0.5
        self._draw_panel(
            screen,
            rect,
            top=(15, 35, 60),
            bottom=(10, 20, 34),
            border=(80, 150, 200),
            accent=(150, 210, 240),
            pulse=pulse,
        )
        for idx, line in enumerate(lines):
            self._draw_text(
                screen,
                str(line),
                (235, 245, 255),
                (rect.x + 8, rect.y + 6 + idx * 18),
                shadow=(10, 16, 24),
            )

    def _draw_auto_dev_panel(
        self,
        screen: pygame.Surface,
        summary: Sequence[tuple[str, object]],
        anchor: pygame.Rect | None,
    ) -> None:
        """Render auto-dev telemetry stacked beneath the resource panel."""

        if not summary:
            return
        width = 210
        height = 20 + 18 * len(summary)
        top = 40
        if anchor is not None:
            top = anchor.bottom + 10
        rect = pygame.Rect(
            screen.get_width() - width - 10,
            top,
            width,
            height,
        )
        now = pygame.time.get_ticks()
        pulse = (math.sin(now / 1000) + 1) * 0.5
        self._draw_panel(
            screen,
            rect,
            top=(22, 34, 52),
            bottom=(12, 20, 32),
            border=(90, 140, 190),
            accent=(140, 200, 240),
            pulse=pulse,
        )
        for idx, (label, value) in enumerate(summary):
            self._draw_text(
                screen,
                f"{label}: {value}",
                (225, 240, 255),
                (rect.x + 8, rect.y + 6 + idx * 18),
                shadow=(12, 16, 24),
            )

    def _draw_world_ticker(
        self, screen: pygame.Surface, events: Sequence[str]
    ) -> None:
        """Render a world activity ticker near the bottom of the screen."""

        lines = [line for line in events if line]
        if not lines:
            return
        text = "  |  ".join(str(line) for line in lines)
        render = self.font.render(text, True, (240, 245, 255))
        padding = 8
        width = render.get_width() + padding * 2
        height = render.get_height() + padding * 2
        x = max(10, (screen.get_width() - width) // 2)
        y = max(0, screen.get_height() - height - 70)
        rect = pygame.Rect(x, y, width, height)
        now = pygame.time.get_ticks()
        pulse = (math.sin(now / 950) + 1) * 0.5
        self._draw_panel(
            screen,
            rect,
            top=(18, 28, 46),
            bottom=(10, 16, 28),
            border=(80, 120, 180),
            accent=(140, 200, 255),
            pulse=pulse,
        )
        shadow = self.font.render(text, True, (10, 14, 22))
        screen.blit(shadow, (rect.x + padding + 2, rect.y + padding + 2))
        screen.blit(render, (rect.x + padding, rect.y + padding))

    def _draw_combo_meter(self, screen: pygame.Surface, combo: int) -> None:
        bar_width = 110
        bar_height = 8
        x = 10
        y = 105
        ratio = min(1.0, combo / 10)
        pygame.draw.rect(screen, (30, 50, 70), pygame.Rect(x, y, bar_width, bar_height))
        pygame.draw.rect(
            screen,
            (240, 200, 80),
            pygame.Rect(x, y, int(bar_width * ratio), bar_height),
        )
        pygame.draw.rect(screen, (140, 180, 210), pygame.Rect(x, y, bar_width, bar_height), 1)

    def _draw_hype_panel(
        self, screen: pygame.Surface, meter: float, label: str
    ) -> None:
        meter = max(0.0, min(1.0, meter))
        x = 10
        y = 38
        width = 120
        height = 34
        rect = pygame.Rect(x, y, width, height)
        now = pygame.time.get_ticks()
        pulse = (math.sin(now / 600) + 1) * 0.5
        self._draw_panel(
            screen,
            rect,
            top=(22, 34, 50),
            bottom=(12, 20, 32),
            border=(120, 170, 210),
            accent=(180, 220, 250),
            pulse=pulse,
        )
        label_text = self.font.render(label, True, (230, 240, 250))
        screen.blit(label_text, (rect.x + 8, rect.y + 4))
        bar_rect = pygame.Rect(rect.x + 8, rect.y + 20, rect.width - 16, 8)
        pygame.draw.rect(screen, (30, 50, 70), bar_rect)
        pygame.draw.rect(
            screen,
            (255, 200, 120),
            pygame.Rect(bar_rect.x, bar_rect.y, int(bar_rect.width * meter), 8),
        )
        pygame.draw.rect(screen, (120, 160, 190), bar_rect, 1)

    def _draw_cooldown_panel(
        self,
        screen: pygame.Surface,
        cooldowns: Sequence[dict[str, object]],
        anchor: pygame.Rect | None,
    ) -> None:
        """Render cooldown timers above the minimap."""
        items = [c for c in cooldowns if c.get("total_ms")]
        if not items:
            return
        width = 210
        height = 24 + 18 * len(items)
        x = 12
        y = screen.get_height() - height - 18
        if anchor is not None:
            y = anchor.top - height - 12
        rect = pygame.Rect(x, max(10, y), width, height)
        now = pygame.time.get_ticks()
        pulse = (math.sin(now / 900) + 1) * 0.5
        self._draw_panel(
            screen,
            rect,
            top=(18, 30, 42),
            bottom=(10, 16, 26),
            border=(90, 130, 160),
            accent=(130, 190, 230),
            pulse=pulse,
        )
        for idx, entry in enumerate(items):
            name = str(entry.get("name", "Skill"))
            remaining = max(0, int(entry.get("remaining_ms", 0)))
            total = max(1, int(entry.get("total_ms", 1)))
            ratio = max(0.0, min(1.0, remaining / total))
            label = f"{name}: {round(remaining / 1000, 1)}s"
            self._draw_text(
                screen,
                label,
                (220, 235, 245),
                (rect.x + 8, rect.y + 6 + idx * 18),
                shadow=(10, 14, 22),
            )
            bar_x = rect.right - 70
            bar_y = rect.y + 8 + idx * 18
            pygame.draw.rect(screen, (30, 50, 70), pygame.Rect(bar_x, bar_y, 50, 6))
            pygame.draw.rect(
                screen,
                (80, 200, 140),
                pygame.Rect(bar_x, bar_y, int(50 * (1 - ratio)), 6),
            )
            pygame.draw.rect(
                screen,
                (120, 160, 190),
                pygame.Rect(bar_x, bar_y, 50, 6),
                1,
            )

    def _draw_minimap(
        self, screen: pygame.Surface, data: dict[str, object]
    ) -> pygame.Rect:
        """Render a compact arena minimap in the lower-left corner."""
        size = 120
        margin = 12
        rect = pygame.Rect(margin, screen.get_height() - size - margin, size, size)
        now = pygame.time.get_ticks()
        pulse = (math.sin(now / 800) + 1) * 0.5
        self._draw_panel(
            screen,
            rect,
            top=(12, 22, 34),
            bottom=(8, 12, 20),
            border=(70, 110, 150),
            accent=(120, 190, 220),
            pulse=pulse,
        )
        bounds = data.get("bounds") or (0.0, 1.0, 0.0, 1.0)
        min_x, max_x, min_y, max_y = bounds
        span_x = max(1.0, max_x - min_x)
        span_y = max(1.0, max_y - min_y)
        player_pos = data.get("player")
        enemies = data.get("enemies") or []
        allies = data.get("allies") or []
        for enemy in enemies:
            pos = enemy.get("pos") if isinstance(enemy, dict) else None
            if not pos:
                continue
            ex = int(rect.x + 6 + ((pos[0] - min_x) / span_x) * (rect.width - 12))
            ey = int(rect.y + 6 + ((pos[1] - min_y) / span_y) * (rect.height - 12))
            color = (255, 120, 120) if enemy.get("boss") else (255, 200, 120)
            pygame.draw.circle(screen, color, (ex, ey), 3)
        for ally in allies:
            pos = ally.get("pos") if isinstance(ally, dict) else None
            if not pos:
                continue
            ax = int(rect.x + 6 + ((pos[0] - min_x) / span_x) * (rect.width - 12))
            ay = int(rect.y + 6 + ((pos[1] - min_y) / span_y) * (rect.height - 12))
            pygame.draw.circle(screen, (120, 220, 180), (ax, ay), 3)
        if player_pos:
            px = int(rect.x + 6 + ((player_pos[0] - min_x) / span_x) * (rect.width - 12))
            py = int(rect.y + 6 + ((player_pos[1] - min_y) / span_y) * (rect.height - 12))
            pygame.draw.circle(screen, (120, 240, 220), (px, py), 4)
        return rect
