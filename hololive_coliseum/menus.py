"""Menu rendering helpers used by :class:`~hololive_coliseum.game.Game`."""

from __future__ import annotations

from pathlib import Path
import math
import random

import pygame

from .mmo_ui import mmo_palette

MENU_BG_COLOR = (10, 17, 30)  # deep navy background
MENU_TEXT_COLOR = (240, 245, 255)  # soft white text
MENU_BORDER_COLOR = (70, 120, 160)  # steel border
MENU_HIGHLIGHT_COLOR = (235, 190, 90)  # warm gold highlight


class MenuMixin:
    """Provides drawing helpers for the game's various menus."""

    def _menu_pattern_surface(self) -> pygame.Surface:
        size = (self.width, self.height)
        cache = getattr(self, "_menu_pattern_cache", None)
        palette = self._menu_palette()
        key = (size, palette["highlight"])
        if cache and cache.get("key") == key:
            return cache["surface"]
        surface = pygame.Surface(size, pygame.SRCALPHA)
        stripe_color = (*palette["highlight"], 20)
        step = 52
        for x in range(-self.height, self.width, step):
            pygame.draw.line(surface, stripe_color, (x, 0), (x + self.height, self.height), 1)
        dot_color = (*palette["highlight"], 16)
        for x in range(0, self.width, 120):
            for y in range(0, self.height, 120):
                pygame.draw.circle(surface, dot_color, (x + 20, y + 20), 2)
        self._menu_pattern_cache = {"key": key, "surface": surface}
        return surface

    def _draw_menu_emblem(self) -> None:
        palette = self._menu_palette()
        center = (self.width // 2, int(self.height * 0.62))
        base = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        ring_colors = [
            (*palette["highlight"], 28),
            (*palette["highlight"], 18),
            (*palette["highlight"], 10),
        ]
        for idx, color in enumerate(ring_colors, start=1):
            radius = 140 + idx * 36
            pygame.draw.circle(base, color, center, radius, 2)
        now = pygame.time.get_ticks()
        angle = (now / 2000) % (2 * math.pi)
        tick_len = 40
        tick_x = int(center[0] + math.cos(angle) * (120 + tick_len))
        tick_y = int(center[1] + math.sin(angle) * (120 + tick_len))
        pygame.draw.line(
            base,
            (*palette["highlight"], 80),
            center,
            (tick_x, tick_y),
            2,
        )
        self._draw_menu_emblem_triangles(base, center, palette, now)
        self.screen.blit(base, (0, 0))

    def _draw_menu_emblem_triangles(
        self,
        surface: pygame.Surface,
        center: tuple[int, int],
        palette: dict[str, tuple[int, int, int]],
        now: int,
    ) -> None:
        pulse = (math.sin(now / 800) + 1) * 0.5
        alpha = 40 + int(40 * pulse)
        color = (*palette["highlight"], alpha)
        for idx in range(6):
            angle = idx * (math.pi / 3) + now / 2400
            outer = (
                int(center[0] + math.cos(angle) * 110),
                int(center[1] + math.sin(angle) * 110),
            )
            left = (
                int(center[0] + math.cos(angle + 0.2) * 90),
                int(center[1] + math.sin(angle + 0.2) * 90),
            )
            right = (
                int(center[0] + math.cos(angle - 0.2) * 90),
                int(center[1] + math.sin(angle - 0.2) * 90),
            )
            pygame.draw.polygon(surface, color, [outer, left, right])

    def _menu_contrast_enabled(self) -> bool:
        manager = getattr(self, "accessibility_manager", None)
        if manager is None:
            return False
        return bool(manager.options.get("high_contrast", False))

    def _menu_palette(self) -> dict[str, tuple[int, int, int]]:
        if self._menu_contrast_enabled():
            return {
                "top": (8, 12, 20),
                "bottom": (18, 22, 32),
                "border": (230, 230, 230),
                "highlight": (255, 210, 110),
                "text": (255, 255, 255),
                "text_dim": (200, 200, 200),
            }
        return {
            "top": MENU_BG_COLOR,
            "bottom": (20, 34, 58),
            "border": MENU_BORDER_COLOR,
            "highlight": MENU_HIGHLIGHT_COLOR,
            "text": MENU_TEXT_COLOR,
            "text_dim": (150, 170, 190),
        }

    def _draw_background(self) -> None:
        """Fill the screen with a premium gradient backdrop."""
        palette = self._menu_palette()
        top = pygame.Color(*palette["top"])
        bottom = pygame.Color(*palette["bottom"])
        for y in range(self.height):
            ratio = y / max(1, self.height - 1)
            r = int(top.r + (bottom.r - top.r) * ratio)
            g = int(top.g + (bottom.g - top.g) * ratio)
            b = int(top.b + (bottom.b - top.b) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))
        haze = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        haze_top = int(self.height * 0.7)
        haze_height = int(self.height * 0.3)
        pygame.draw.rect(
            haze,
            (0, 0, 0, 60),
            pygame.Rect(0, haze_top, self.width, haze_height),
        )
        self.screen.blit(haze, (0, 0))
        self.screen.blit(self._menu_pattern_surface(), (0, 0))
        self._draw_menu_parallax_bands()
        self._draw_menu_emblem()
        self._draw_menu_orbit_nodes()
        self._draw_ambient_glow()
        self._draw_menu_particles()
        self._draw_menu_vignette()
        # Keep a bright footer edge for legacy menu-gradient expectations.
        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            (0, self.height - 1),
            (self.width, self.height - 1),
        )
        self.screen.set_at((0, 0), palette["top"])

    def _draw_menu_parallax_bands(self) -> None:
        """Draw drifting translucent bands for depth and motion."""
        now = pygame.time.get_ticks()
        palette = self._menu_palette()
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        lanes = (
            (0.22, 1800.0, 220, 34),
            (0.46, 2600.0, 280, 28),
            (0.68, 3400.0, 340, 22),
            (0.84, 4300.0, 420, 18),
        )
        for idx, (y_ratio, period, seg_w, alpha) in enumerate(lanes):
            y = int(self.height * y_ratio)
            phase = (now / period + idx * 0.17) % 1.0
            x_offset = int(-seg_w + phase * (self.width + seg_w * 2))
            band_h = 28 + idx * 4
            rect = pygame.Rect(x_offset, y, seg_w, band_h)
            color = (*palette["highlight"], alpha)
            pygame.draw.rect(overlay, color, rect, border_radius=8)
            trail = rect.copy()
            trail.width = max(80, rect.width // 2)
            trail.x -= int(seg_w * 0.42)
            pygame.draw.rect(overlay, (*palette["highlight"], max(10, alpha - 10)),
                             trail, border_radius=6)
        self.screen.blit(overlay, (0, 0))

    def _draw_menu_orbit_nodes(self) -> None:
        """Draw orbiting nodes around the emblem to extend menu animation."""
        now = pygame.time.get_ticks()
        palette = self._menu_palette()
        center = (self.width // 2, int(self.height * 0.62))
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        nodes = (
            (166, 0.0009, 5, 95),
            (208, -0.0007, 4, 80),
            (248, 0.0005, 3, 68),
        )
        for idx, (radius, speed, size, alpha) in enumerate(nodes):
            angle = now * speed + idx * 2.1
            px = int(center[0] + math.cos(angle) * radius)
            py = int(center[1] + math.sin(angle) * (radius * 0.62))
            core = (*palette["highlight"], alpha)
            glow = (*palette["highlight"], max(20, alpha - 45))
            pygame.draw.circle(overlay, glow, (px, py), size + 7)
            pygame.draw.circle(overlay, core, (px, py), size)
            pygame.draw.line(
                overlay,
                (*palette["highlight"], max(18, alpha - 55)),
                center,
                (px, py),
                1,
            )
        self.screen.blit(overlay, (0, 0))

    def _draw_ambient_glow(self) -> None:
        now = pygame.time.get_ticks()
        inset = 24
        glow_width = max(0, self.width - inset * 2)
        glow_height = max(0, self.height - inset * 2)
        overlay = pygame.Surface((glow_width, glow_height), pygame.SRCALPHA)
        anchors = [
            (0.3, 0.22, 26, 90),
            (0.7, 0.38, 22, 70),
            (0.5, 0.68, 28, 85),
        ]
        for idx, (x_ratio, y_ratio, size, alpha) in enumerate(anchors):
            pulse = (math.sin(now / 800 + idx) + 1) * 0.5
            radius = int(size * (0.85 + 0.2 * pulse))
            color = (0, 160, 170, int(alpha * (0.6 + 0.4 * pulse)))
            cx = int(glow_width * x_ratio)
            cy = int(glow_height * y_ratio)
            pygame.draw.circle(overlay, color, (cx, cy), radius)
        self.screen.blit(overlay, (inset, inset))

    def _draw_menu_particles(self) -> None:
        width = self.width
        height = self.height
        if width <= 0 or height <= 0:
            return
        if getattr(self, "menu_particles_size", None) != (width, height):
            rng = random.Random(width + height + 19)
            count = max(24, (width * height) // 24000)
            particles = []
            for _ in range(count):
                particles.append(
                    {
                        "x": rng.random() * width,
                        "y": rng.random() * height,
                        "speed": rng.uniform(8.0, 18.0),
                        "size": rng.choice([1, 1, 2]),
                        "phase": rng.randint(0, 1000),
                    }
                )
            self.menu_particles = particles
            self.menu_particles_size = (width, height)
        now = pygame.time.get_ticks()
        inset = 18
        for particle in getattr(self, "menu_particles", []):
            y = (particle["y"] + now / particle["speed"]) % height
            x = particle["x"]
            if x < inset or x > width - inset or y < inset or y > height - inset:
                continue
            twinkle = (math.sin((now + particle["phase"]) / 500) + 1) * 0.5
            alpha = 70 + int(80 * twinkle)
            palette = self._menu_palette()
            color = (*palette["highlight"], alpha)
            pygame.draw.circle(
                self.screen,
                color,
                (int(x), int(y)),
                int(particle["size"]),
            )

    def _draw_menu_vignette(self) -> None:
        inset = 20
        if self.width <= inset * 2 or self.height <= inset * 2:
            return
        panel = pygame.Surface(
            (self.width - inset * 2, self.height - inset * 2), pygame.SRCALPHA
        )
        panel.fill((0, 0, 0, 32))
        border = pygame.Surface(panel.get_size(), pygame.SRCALPHA)
        palette = self._menu_palette()
        pygame.draw.rect(border, (*palette["highlight"], 50), border.get_rect(), 2)
        panel.blit(border, (0, 0))
        self.screen.blit(panel, (inset, inset))

    def _draw_option_label(
        self,
        label: str,
        idx: int,
        center: tuple[int, int],
        *,
        font: pygame.font.Font | None = None,
    ) -> None:
        """Render a menu option with a highlight if selected."""
        option_font = font or self.menu_font
        metrics = getattr(self, "ui_metrics", None)
        palette = self._menu_palette()
        color = (
            palette["text"]
            if idx == self.menu_index
            else palette["text_dim"]
        )
        text = option_font.render(label, True, color)
        rect = text.get_rect(center=center)
        panel_rect = rect.inflate(
            metrics.pad(90) if metrics else 90,
            metrics.pad(18) if metrics else 18,
        )
        panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        base_alpha = 160 if idx == self.menu_index else 120
        panel.fill((10, 18, 30, base_alpha))
        pygame.draw.rect(
            panel,
            (*palette["border"], 140 if idx == self.menu_index else 90),
            panel.get_rect(),
            metrics.border_thickness if metrics else 2,
        )
        self.screen.blit(panel, panel_rect)
        if idx == self.menu_index:
            now = pygame.time.get_ticks()
            pulse = (math.sin(now / 260) + 1) * 0.5
            glow = pygame.Surface(
                rect.inflate(
                    metrics.pad(36) if metrics else 36,
                    metrics.pad(16) if metrics else 16,
                ).size,
                pygame.SRCALPHA,
            )
            glow.fill((*palette["highlight"], 90 + int(80 * pulse)))
            glow_rect = glow.get_rect(center=rect.center)
            self.screen.blit(glow, glow_rect)
            pygame.draw.rect(
                self.screen,
                palette["highlight"],
                rect.inflate(
                    metrics.pad(20) if metrics else 20,
                    metrics.pad(10) if metrics else 10,
                ),
                metrics.border_thickness if metrics else 1,
            )
            underline_width = rect.width + (metrics.pad(40) if metrics else 40)
            underline_y = rect.bottom + (metrics.pad(6) if metrics else 6)
            pygame.draw.line(
                self.screen,
                palette["highlight"],
                (rect.centerx - underline_width // 2, underline_y),
                (rect.centerx + underline_width // 2, underline_y),
                metrics.border(3) if metrics else 3,
            )
            chevron_offset = (
                (metrics.pad(8) if metrics else 8)
                + int((metrics.pad(4) if metrics else 4) * pulse)
            )
            chevron_y = rect.centery
            left_x = rect.left - chevron_offset
            right_x = rect.right + chevron_offset
            chevron_color = palette["highlight"]
            pygame.draw.lines(
                self.screen,
                chevron_color,
                False,
                [
                    (left_x, chevron_y),
                    (left_x - 10, chevron_y - 6),
                    (left_x, chevron_y - 12),
                ],
                2,
            )
            pygame.draw.lines(
                self.screen,
                chevron_color,
                False,
                [
                    (right_x, chevron_y),
                    (right_x + 10, chevron_y - 6),
                    (right_x, chevron_y - 12),
                ],
                2,
            )
        shadow = option_font.render(label, True, (20, 20, 20))
        self.screen.blit(shadow, (rect.x + 2, rect.y + 2))
        self.screen.blit(text, rect)

    def _draw_mmo_option_label(
        self,
        label: str,
        idx: int,
        center: tuple[int, int],
        *,
        font: pygame.font.Font | None = None,
    ) -> None:
        """Render the MMO menu option with a distinct, neon identity."""
        option_font = font or self.menu_font
        palette = mmo_palette()
        selected = idx == self.menu_index
        color = palette["accent_warm"] if selected else palette["text_dim"]
        text = option_font.render(label, True, color)
        rect = text.get_rect(center=center)
        panel_rect = rect.inflate(100, 22)
        panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        panel.fill((*palette["panel_alt"], 210 if selected else 170))
        pygame.draw.rect(panel, palette["border"], panel.get_rect(), 2)
        self.screen.blit(panel, panel_rect)
        if selected:
            now = pygame.time.get_ticks()
            pulse = (math.sin(now / 260) + 1) * 0.5
            glow = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
            glow.fill((*palette["accent"], 60 + int(60 * pulse)))
            self.screen.blit(glow, panel_rect)
            pygame.draw.rect(
                self.screen,
                palette["accent"],
                rect.inflate(22, 12),
                2,
            )
        self.screen.blit(text, rect)
        pygame.draw.line(
            self.screen,
            palette["idol_pink"],
            (rect.centerx - rect.width // 2, rect.bottom + 6),
            (rect.centerx + rect.width // 2, rect.bottom + 6),
            2,
        )

    def _draw_icon_glow(self, rect: pygame.Rect) -> None:
        now = pygame.time.get_ticks()
        pulse = (math.sin(now / 220) + 1) * 0.5
        glow = pygame.Surface(rect.inflate(14, 14).size, pygame.SRCALPHA)
        glow.fill((255, 220, 140, 60 + int(80 * pulse)))
        glow_rect = glow.get_rect(center=rect.center)
        self.screen.blit(glow, glow_rect)
        pygame.draw.rect(self.screen, (255, 230, 160), rect.inflate(6, 6), 2)

    def _draw_title(
        self,
        text: str,
        center: tuple[int, int],
        *,
        color: tuple[int, int, int] = MENU_TEXT_COLOR,
        glow: tuple[int, int, int] = (0, 200, 200),
    ) -> None:
        render = self.title_font.render(text, True, color)
        glow_render = self.title_font.render(text, True, glow)
        glow_render.set_alpha(130)
        offsets = [(-3, 0), (3, 0), (0, -3), (0, 3)]
        for dx, dy in offsets:
            rect = glow_render.get_rect(center=(center[0] + dx, center[1] + dy))
            self.screen.blit(glow_render, rect)
        shadow = self.title_font.render(text, True, (15, 20, 25))
        shadow_rect = shadow.get_rect(center=(center[0] + 2, center[1] + 2))
        self.screen.blit(shadow, shadow_rect)
        render_rect = render.get_rect(center=center)
        self.screen.blit(render, render_rect)
        shimmer = pygame.Surface(render_rect.size, pygame.SRCALPHA)
        now = pygame.time.get_ticks()
        sweep = int((now / 6) % (render_rect.width + 40)) - 20
        pygame.draw.rect(
            shimmer,
            (255, 255, 255, 70),
            pygame.Rect(sweep, 0, 14, render_rect.height),
        )
        shimmer.set_alpha(140)
        self.screen.blit(shimmer, render_rect.topleft)

    def _draw_border(self) -> None:
        """Draw a teal border without covering the corners used by tests."""
        rect = self.screen.get_rect().inflate(-10, -10)
        palette = self._menu_palette()
        pygame.draw.rect(self.screen, palette["border"], rect, 4)
        now = pygame.time.get_ticks()
        pulse = (math.sin(now / 700) + 1) * 0.5
        inner = rect.inflate(-10, -10)
        pygame.draw.rect(self.screen, palette["highlight"], inner, 2)
        corner_alpha = 120 + int(80 * pulse)
        corner = pygame.Surface((20, 20), pygame.SRCALPHA)
        corner.fill((*palette["highlight"], corner_alpha))
        self.screen.blit(corner, rect.topleft)
        self.screen.blit(corner, (rect.right - 20, rect.top))
        self.screen.blit(corner, (rect.left, rect.bottom - 20))
        self.screen.blit(corner, (rect.right - 20, rect.bottom - 20))       

    def _draw_input_prompt(self, text: str) -> None:
        manager = getattr(self, "accessibility_manager", None)
        if manager is None or not manager.options.get("input_prompts", False):
            return
        hint = self.small_font.render(text, True, MENU_TEXT_COLOR)
        self.screen.blit(
            hint, hint.get_rect(center=(self.width // 2, self.height - 24))
        )

    def _draw_menu_header(self, title: str, *, subtitle: str | None = None) -> None:
        palette = self._menu_palette()
        banner_height = max(64, int(self.height * 0.12))
        shadow = pygame.Surface((self.width, banner_height + 10), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 90))
        self.screen.blit(shadow, (0, 6))
        banner = pygame.Surface((self.width, banner_height), pygame.SRCALPHA)
        for y in range(banner_height):
            ratio = y / max(1, banner_height - 1)
            r = int(palette["top"][0] + (palette["bottom"][0] - palette["top"][0]) * ratio)
            g = int(palette["top"][1] + (palette["bottom"][1] - palette["top"][1]) * ratio)
            b = int(palette["top"][2] + (palette["bottom"][2] - palette["top"][2]) * ratio)
            banner.fill((r, g, b, 210), pygame.Rect(0, y, self.width, 1))
        pygame.draw.line(
            banner,
            palette["highlight"],
            (0, banner_height - 2),
            (self.width, banner_height - 2),
            2,
        )
        pygame.draw.line(
            banner,
            palette["border"],
            (0, 2),
            (self.width, 2),
            2,
        )
        self.screen.blit(banner, (0, 0))
        self._draw_title(title, (self.width // 2, banner_height // 2 + 6))
        if subtitle:
            text = self.small_font.render(subtitle, True, palette["text"])
            self.screen.blit(text, (20, banner_height - 26))
        state = getattr(self, "state", "")
        if state:
            tag = self.small_font.render(
                state.replace("_", " ").title(), True, palette["text_dim"]
            )
            self.screen.blit(
                tag, (self.width - tag.get_width() - 20, banner_height - 26)
            )
        self._draw_menu_badges(banner_height, palette)

    def _draw_menu_badges(
        self, banner_height: int, palette: dict[str, tuple[int, int, int]]
    ) -> None:
        now = pygame.time.get_ticks()
        pulse = (math.sin(now / 600) + 1) * 0.5
        accent = palette["highlight"]
        left = (26, banner_height // 2 + 8)
        right = (self.width - 26, banner_height // 2 + 8)
        for center in (left, right):
            pygame.draw.circle(self.screen, accent, center, 10, 2)
            dot_alpha = 120 + int(80 * pulse)
            dot = pygame.Surface((6, 6), pygame.SRCALPHA)
            dot.fill((*accent, dot_alpha))
            self.screen.blit(dot, (center[0] - 3, center[1] - 3))
        tri = [
            (self.width // 2 - 40, banner_height - 10),
            (self.width // 2, banner_height - 4),
            (self.width // 2 + 40, banner_height - 10),
        ]
        pygame.draw.lines(self.screen, accent, False, tri, 2)

    def _draw_panel_sheen(self, rect: pygame.Rect) -> None:
        now = pygame.time.get_ticks()
        sweep = int((now / 5) % (rect.width + rect.height)) - rect.height
        sheen = pygame.Surface(rect.size, pygame.SRCALPHA)
        points = [
            (sweep, 0),
            (sweep + 60, 0),
            (sweep + rect.height + 60, rect.height),
            (sweep + rect.height, rect.height),
        ]
        pygame.draw.polygon(sheen, (255, 255, 255, 40), points)
        self.screen.blit(sheen, rect.topleft)

    def _draw_panel_shadow(self, rect: pygame.Rect) -> None:
        shadow = pygame.Surface(rect.inflate(10, 10).size, pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 70))
        self.screen.blit(shadow, (rect.x - 5, rect.y + 6))

    def _draw_end_flash(self, until: int, color: tuple[int, int, int]) -> None: 
        if until <= 0:
            return
        now = pygame.time.get_ticks()
        if now >= until:
            return
        remaining = until - now
        alpha = 180 if remaining > 800 else max(60, int(180 * remaining / 800))
        flash = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        flash.fill((*color, alpha))
        self.screen.blit(flash, (0, 0))

    def _draw_summary_cards(
        self, entries: list[tuple[str, str]], *, start_y: int
    ) -> None:
        """Render summary cards for victory and game over screens."""
        if not entries:
            return
        cols = 2
        card_width = int(self.width * 0.36)
        card_height = 70
        margin = 18
        total_width = cols * card_width + (cols - 1) * margin
        start_x = max(20, (self.width - total_width) // 2)
        for idx, (label, value) in enumerate(entries):
            row = idx // cols
            col = idx % cols
            x = start_x + col * (card_width + margin)
            y = start_y + row * (card_height + margin)
            rect = pygame.Rect(x, y, card_width, card_height)
            self._draw_panel_shadow(rect)
            palette = self._menu_palette()
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((12, 20, 34, 185))
            pygame.draw.rect(panel, palette["border"], panel.get_rect(), 2)
            self.screen.blit(panel, rect)
            title = self.small_font.render(label, True, (190, 210, 220))
            value_text = self.menu_font.render(value, True, MENU_TEXT_COLOR)
            self.screen.blit(title, (rect.x + 14, rect.y + 10))
            self.screen.blit(value_text, (rect.x + 14, rect.y + 30))

    def _draw_menu(self) -> None:
        """Render the splash menu screen."""
        self._draw_background()
        self._draw_title("Hololive Coliseum", (self.width // 2, self.height // 3))
        prompt = "Press any key to start"
        prompt_shadow = self.menu_font.render(prompt, True, (8, 12, 20))
        prompt_text = self.menu_font.render(prompt, True, MENU_TEXT_COLOR)
        prompt_rect = prompt_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(prompt_shadow, (prompt_rect.x + 2, prompt_rect.y + 2))
        self.screen.blit(prompt_text, prompt_rect)
        self._draw_border()

    def _draw_main_menu(self) -> None:
        """Render the main menu with a structured layout."""
        self._draw_background()
        palette = self._menu_palette()
        metrics = getattr(self, "ui_metrics", None)
        menu_scale = float(metrics.ui_scale if metrics else 1.0)
        panel_pad = metrics.panel_pad if metrics else 16
        title_gap = metrics.title_gap if metrics else 18
        border_w = metrics.border_thickness if metrics else 2
        outer_margin = max(20, int(self.width * 0.04))
        gutter = max(metrics.gutter if metrics else 14, int(self.width * 0.02))
        title_y = int(self.height * 0.18)
        title_text = "Hololive Coliseum"
        if getattr(self, "mmo_unlocked", False):
            title_text = "Hololive Coliseum: MMO Command"
        self._draw_title(title_text, (self.width // 2, title_y))
        subtitle = self.small_font.render(
            "Adaptive UI scales with your resolution",
            True,
            palette["text_dim"],
        )
        subtitle_y = min(
            self.height - metrics.pad(36) if metrics else self.height - 36,
            title_y + self.title_font.get_height() // 2 + title_gap,
        )
        self.screen.blit(subtitle, subtitle.get_rect(center=(self.width // 2, subtitle_y)))
        menu_top = int(self.height * 0.31)
        if getattr(self, "mmo_unlocked", False):
            mmo_palette_local = mmo_palette()
            ribbon_h = metrics.pad(54) if metrics else 54
            ribbon = pygame.Surface((self.width, ribbon_h), pygame.SRCALPHA)
            ribbon.fill((*mmo_palette_local["panel_alt"], 210))
            pygame.draw.line(
                ribbon,
                mmo_palette_local["accent"],
                (panel_pad, ribbon_h - metrics.pad(10) if metrics else 44),
                (self.width - panel_pad, ribbon_h - metrics.pad(10) if metrics else 44),
                border_w,
            )
            self.screen.blit(ribbon, (0, 0))
            badge = self.menu_font.render(
                "MMO HUB UNLOCKED",
                True,
                mmo_palette_local["accent_warm"],
            )
            self.screen.blit(
                badge,
                (
                    panel_pad,
                    metrics.pad(10) if metrics else 10,
                ),
            )
            hint = self.small_font.render(
                "Select MMO to enter the command hub",
                True,
                mmo_palette_local["text_dim"],
            )
            self.screen.blit(
                hint,
                (
                    panel_pad,
                    metrics.pad(34) if metrics else 34,
                ),
            )
            mmo_rect = pygame.Rect(
                outer_margin,
                max(int(self.height * 0.25), 70),
                self.width - outer_margin * 2,
                max(84, int(self.height * 0.11)),
            )
            mmo_panel = pygame.Surface(mmo_rect.size, pygame.SRCALPHA)
            mmo_panel.fill((*mmo_palette_local["panel"], 200))
            pygame.draw.rect(
                mmo_panel,
                mmo_palette_local["border"],
                mmo_panel.get_rect(),
                border_w,
            )
            self.screen.blit(mmo_panel, mmo_rect)
            title = self.menu_font.render(
                "MMO Network Overview",
                True,
                mmo_palette_local["text"],
            )
            self.screen.blit(
                title,
                (
                    mmo_rect.x + panel_pad,
                    mmo_rect.y + (metrics.pad(12) if metrics else 12),
                ),
            )
            regions = 0
            if hasattr(self, "world_generation_manager"):
                try:
                    regions = len(self.world_generation_manager.region_manager.get_regions())
                except Exception:
                    regions = 0
            overview = [
                f"Account: {getattr(self, 'account_id', 'player')}",
                f"Credits: {getattr(self, 'mmo_credits', 0)}",
                f"Regions: {regions}",
                f"Ops: {len(getattr(self, 'mmo_operations', []))}",
                f"Alerts: {len(getattr(self, 'mmo_alerts', []))}",
            ]
            ox = mmo_rect.x + panel_pad
            oy = mmo_rect.y + (metrics.pad(42) if metrics else 42)
            line_height = self.small_font.get_height() + (metrics.pad(4) if metrics else 4)
            for item in overview:
                text = self.small_font.render(
                    item,
                    True,
                    mmo_palette_local["text_dim"],
                )
                if ox + text.get_width() > mmo_rect.right - panel_pad:
                    ox = mmo_rect.x + panel_pad
                    oy += line_height
                if oy + text.get_height() > mmo_rect.bottom - (metrics.pad(10) if metrics else 10):
                    break
                self.screen.blit(text, (ox, oy))
                ox += text.get_width() + panel_pad + (metrics.pad(8) if metrics else 8)
            menu_top = max(menu_top, mmo_rect.bottom + title_gap)
        options = list(getattr(self, "main_menu_options", []))
        menu_bottom = self.height - max(20, int(self.height * 0.04))
        content_height = max(150, menu_bottom - menu_top)
        content_x = outer_margin
        content_width = max(320, self.width - outer_margin * 2)

        min_side_width = 170
        preferred_side = max(min_side_width, int(content_width * 0.23))
        center_width = content_width - preferred_side * 2 - gutter * 2
        three_column = center_width >= 300
        if not three_column:
            center_width = min(content_width, max(300, int(content_width * 0.68)))
            center_x = self.width // 2 - center_width // 2
            side_y = menu_top + int(content_height * 0.6)
            side_y = min(side_y, menu_bottom - 110)
            center_height = max(150, side_y - menu_top - 10)
            side_height = max(100, menu_bottom - side_y)
            half_width = (content_width - gutter) // 2
            if half_width >= 220:
                info_rect = pygame.Rect(content_x, side_y, half_width, side_height)
                setup_rect = pygame.Rect(
                    content_x + half_width + gutter, side_y, half_width, side_height
                )
            else:
                card_height = max(88, (side_height - 10) // 2)
                info_rect = pygame.Rect(content_x, side_y, content_width, card_height)
                setup_rect = pygame.Rect(
                    content_x,
                    side_y + card_height + 10,
                    content_width,
                    card_height,
                )
                center_height = max(130, info_rect.y - menu_top - 10)
        else:
            side_width = preferred_side
            center_x = content_x + side_width + gutter
            center_height = content_height
            info_rect = pygame.Rect(content_x, menu_top, side_width, content_height)
            setup_rect = pygame.Rect(
                center_x + center_width + gutter, menu_top, side_width, content_height
            )
        panel_rect = pygame.Rect(center_x, menu_top, center_width, center_height)
        panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        panel.fill((12, 20, 34, 190))
        pygame.draw.rect(panel, palette["border"], panel.get_rect(), border_w)
        pygame.draw.line(
            panel,
            palette["highlight"],
            (panel_pad, metrics.pad(8) if metrics else 8),
            (panel_rect.width - panel_pad, metrics.pad(8) if metrics else 8),
            border_w,
        )
        self.screen.blit(panel, panel_rect)

        base_option_size = max(15, int(31 * menu_scale))
        min_option_size = 12
        option_font = self.menu_font
        line_padding = max(metrics.pad(6) if metrics else 6, int(10 * menu_scale))
        line_height = option_font.get_height() + line_padding
        if options:
            for size in range(base_option_size, min_option_size - 1, -1):
                candidate = pygame.font.SysFont(None, size)
                candidate_padding = max(6, int(size * 0.32))
                candidate_line = candidate.get_height() + candidate_padding
                candidate_height = candidate_line * len(options) + panel_pad + (metrics.pad(8) if metrics else 8)
                widest = max(candidate.size(opt)[0] for opt in options)
                if (
                    candidate_height <= panel_rect.height - (metrics.pad(8) if metrics else 8)
                    and widest + (metrics.pad(120) if metrics else 120) <= panel_rect.width - (metrics.pad(12) if metrics else 12)
                ):
                    option_font = candidate
                    line_height = candidate_line
                    break

        visible_options = list(options)
        visible_start = 0
        max_visible = max(
            1,
            (panel_rect.height - panel_pad - (metrics.pad(8) if metrics else 8))
            // max(1, line_height),
        )
        if len(options) > max_visible:
            visible_start = max(0, self.menu_index - max_visible // 2)
            visible_start = min(visible_start, len(options) - max_visible)
            visible_options = options[visible_start:visible_start + max_visible]

        total_options_height = line_height * len(visible_options)
        start_y = panel_rect.y + max(
            metrics.pad(14) if metrics else 14,
            (panel_rect.height - total_options_height) // 2,
        )
        if visible_start > 0:
            up_hint = self.small_font.render("^", True, palette["text_dim"])
            self.screen.blit(
                up_hint,
                up_hint.get_rect(
                    center=(panel_rect.centerx, panel_rect.y + (metrics.pad(10) if metrics else 10))
                ),
            )
        if visible_start + len(visible_options) < len(options):
            down_hint = self.small_font.render("v", True, palette["text_dim"])
            self.screen.blit(
                down_hint,
                down_hint.get_rect(
                    center=(
                        panel_rect.centerx,
                        panel_rect.bottom - (metrics.pad(10) if metrics else 10),
                    )
                ),
            )
        for draw_idx, opt in enumerate(visible_options):
            i = visible_start + draw_idx
            center = (
                panel_rect.centerx,
                start_y + draw_idx * line_height + line_height // 2,
            )
            if opt == "MMO":
                self._draw_mmo_option_label(opt, i, center, font=option_font)
            else:
                self._draw_option_label(opt, i, center, font=option_font)

        lines = []
        difficulty = "n/a"
        if hasattr(self, "difficulty_levels"):
            idx = int(getattr(self, "difficulty_index", 0))
            difficulty = self.difficulty_levels[max(0, idx)]
        lines.append(f"Difficulty: {difficulty}")
        lines.append(f"Character: {getattr(self, 'selected_character', 'n/a')}")
        lines.append(f"Map: {getattr(self, 'selected_map', 'n/a')}")
        wins = int(getattr(self, "arena_wins", 0))
        lines.append(f"Arena Wins: {wins}")
        lives = int(getattr(self, "match_lives", 3))
        allies = int(getattr(self, "match_allies", 0))
        ai_players = int(getattr(self, "ai_players", 0))
        mobs = "On" if getattr(self, "match_mobs", False) else "Off"
        lines.append(f"Lives: {lives}")
        lines.append(f"Allies: {allies}  AI: {ai_players}")
        lines.append(f"Mob Waves: {mobs}")
        mmo_unlocked = bool(getattr(self, "mmo_unlocked", False))
        lines.append(f"MMO: {'Unlocked' if mmo_unlocked else 'Locked'}")
        if getattr(self, "mmo_plan_summary", ""):
            lines.append("Auto-Dev: Active")
        setup_lines = [
            f"Mode: {getattr(self, 'selected_mode', 'n/a')}",
            f"Map: {getattr(self, 'selected_map', 'n/a')}",
            f"Lives: {getattr(self, 'match_lives', 3)}",
            f"Allies: {getattr(self, 'match_allies', 0)}",
            f"AI Players: {getattr(self, 'ai_players', 0)}",
            f"Mob Waves: {'On' if getattr(self, 'match_mobs', False) else 'Off'}",
            f"Account: {getattr(self, 'account_id', 'player')}",
        ]

        def draw_side_panel(rect: pygame.Rect, heading: str, items: list[str]) -> None:
            panel_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel_surface.fill((14, 20, 32, 185))
            pygame.draw.rect(
                panel_surface, palette["border"], panel_surface.get_rect(), border_w
            )
            self.screen.blit(panel_surface, rect)
            heading_font = self.menu_font
            if heading_font.size(heading)[0] > rect.width - panel_pad * 2:
                heading_font = self.small_font
            heading_text = heading_font.render(heading, True, MENU_TEXT_COLOR)
            self.screen.blit(
                heading_text,
                (
                    rect.x + panel_pad,
                    rect.y + (metrics.pad(14) if metrics else 14),
                ),
            )

            line_font = self.small_font
            base_small_size = max(14, int(20 * menu_scale))
            for size in range(base_small_size, 13, -1):
                candidate = pygame.font.SysFont(None, size)
                gap = candidate.get_height() + (metrics.pad(4) if metrics else 4)
                needed_height = (metrics.pad(52) if metrics else 52) + gap * len(items)
                max_width = max((candidate.size(item)[0] for item in items), default=0)
                if (
                    needed_height <= rect.height - (metrics.pad(10) if metrics else 10)
                    and max_width <= rect.width - panel_pad * 2
                ):
                    line_font = candidate
                    break

            line_gap = line_font.get_height() + (metrics.pad(4) if metrics else 4)
            text_y = rect.y + (metrics.pad(48) if metrics else 48)
            visible_count = max(
                1,
                (rect.height - (metrics.pad(56) if metrics else 56)) // max(1, line_gap),
            )
            visible_lines = list(items[:visible_count])
            if len(items) > visible_count and visible_lines:
                visible_lines[-1] = "..."
            for line in visible_lines:
                text = line_font.render(line, True, (200, 215, 220))
                self.screen.blit(text, (rect.x + panel_pad, text_y))
                text_y += line_gap

        draw_side_panel(info_rect, "Arena Brief", lines)
        draw_side_panel(setup_rect, "Game Setup", setup_lines)
        status_label = self.small_font.render(
            f"{self.width}x{self.height}  Font {int(menu_scale * 100)}%",
            True,
            palette["text_dim"],
        )
        status_rect = status_label.get_rect(
            right=self.width - outer_margin,
            bottom=self.height - max(8, outer_margin // 2),
        )
        self.screen.blit(status_label, status_rect)
        self._draw_input_prompt("Use arrows + Enter/Space to select")
        self._draw_border()

    def _draw_option_menu(self, title: str, options: list[str]) -> None:
        """Generic menu drawing helper."""
        self._draw_background()
        self._draw_menu_header(title)
        if not options:
            self._draw_border()
            return
        labels = []
        for opt in options:
            label = opt
            if self.state == "settings_display":
                if opt == "Window Size":
                    label = f"Window Size: {self.width}x{self.height}"
                elif opt == "Display Mode":
                    label = f"Display Mode: {self.display_mode}"
                elif opt == "HUD Size":
                    label = f"HUD Size: {getattr(self, 'hud_font_size', 18)}px"
                elif opt == "Show FPS":
                    label = f"Show FPS: {'On' if self.show_fps else 'Off'}"
            elif self.state == "match_options":
                if opt == "Lives":
                    label = f"Lives: {getattr(self, 'match_lives', 3)}"
                elif opt == "Allies":
                    label = f"Allies: {getattr(self, 'match_allies', 0)}"
                elif opt == "AI Players":
                    label = f"AI Players: {getattr(self, 'ai_players', 0)}"
                elif opt == "Mob Waves":
                    enabled = getattr(self, "match_mobs", False)
                    label = f"Mob Waves: {'On' if enabled else 'Off'}"
                elif opt == "Mob Interval":
                    label = f"Mob Interval: {getattr(self, 'match_mob_interval', 3500)}ms"
                elif opt == "Mob Wave":
                    label = f"Mob Wave: {getattr(self, 'match_mob_wave', 2)}"
                elif opt == "Mob Cap":
                    label = f"Mob Cap: {getattr(self, 'match_mob_max', 8)}"
            labels.append(label)
        base_line_height = self.menu_font.get_height() + 16
        max_panel_height = int(self.height * 0.55)
        line_height = max(
            24,
            min(base_line_height, int(max_panel_height / max(1, len(labels)))),
        )
        total_height = line_height * len(labels)
        start_y = int(self.height * 0.5 - total_height / 2)
        start_y = max(start_y, int(self.height * 0.3))
        panel_height = total_height + 30
        panel_width = int(self.width * 0.46)
        panel_x = self.width // 2 - panel_width // 2
        panel_y = start_y - 18
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        self._draw_panel_shadow(panel_rect)
        palette = self._menu_palette()
        panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        panel.fill((14, 20, 32, 185))
        pygame.draw.rect(panel, palette["border"], panel.get_rect(), 2)
        pygame.draw.line(
            panel,
            palette["highlight"],
            (12, 8),
            (panel_rect.width - 12, 8),
            2,
        )
        self.screen.blit(panel, panel_rect)
        self._draw_panel_sheen(panel_rect)
        for i, label in enumerate(labels):
            self._draw_option_label(
                label,
                i,
                (self.width // 2, start_y + i * line_height),
            )
        self._draw_input_prompt("Use arrows + Enter/Space to select")
        self._draw_border()

    def _draw_character_menu(self) -> None:
        self._draw_background()
        self._draw_menu_header("Select Character", subtitle="Roster + Filters")
        if hasattr(self, "_character_filter_label"):
            filter_text = self.small_font.render(
                self._character_filter_label(), True, MENU_TEXT_COLOR
            )
            self.screen.blit(
                filter_text,
                (self.width - filter_text.get_width() - 20, 18),
            )
        if self.multiplayer and self.human_players > 1:
            picker = self.small_font.render(
                f"Picking: P{self.character_select_index + 1}",
                True,
                (200, 220, 230),
            )
            self.screen.blit(picker, (20, 18))
        characters = (
            self._paged_characters()
            if hasattr(self, "_paged_characters")
            else list(self.characters)
        )
        cols = 5
        size = 64
        margin = 18
        cols = min(6, max(3, self.width // (size + margin)))
        start_x = (self.width - (cols * size + (cols - 1) * margin)) // 2
        start_y = 100
        player_colors = [
            (0, 200, 255),
            (255, 170, 0),
            (130, 255, 170),
            (255, 120, 220),
        ]
        selections: list[str | None] = []
        if getattr(self, "multiplayer", False) and getattr(
            self, "human_players", 1
        ) > 1:
            selections = list(getattr(self, "character_selections", []))
        for idx, name in enumerate(characters):
            row = idx // cols
            col = idx % cols
            x = start_x + col * (size + margin)
            y = start_y + row * (size + margin)
            img = self.character_images[name]
            rect = img.get_rect(topleft=(x, y))
            frame_rect = pygame.Rect(x - 4, y - 4, size + 8, size + 8)
            pygame.draw.rect(self.screen, (12, 20, 28), frame_rect)
            pygame.draw.rect(self.screen, (0, 120, 150), frame_rect, 2)
            self.screen.blit(img, rect)
            if selections:
                picked = [
                    i for i, chosen in enumerate(selections) if chosen == name
                ]
                for tag_slot, player_idx in enumerate(picked):
                    color = player_colors[player_idx % len(player_colors)]
                    pygame.draw.rect(self.screen, color, rect, 3)
                    label = self.small_font.render(
                        f"P{player_idx + 1}", True, color
                    )
                    badge_x = rect.x + 4
                    badge_y = rect.y + 4 + tag_slot * 18
                    badge_rect = pygame.Rect(
                        badge_x - 2,
                        badge_y - 1,
                        label.get_width() + 6,
                        label.get_height() + 2,
                    )
                    pygame.draw.rect(self.screen, (8, 12, 16), badge_rect)
                    pygame.draw.rect(self.screen, color, badge_rect, 2)
                    self.screen.blit(label, (badge_x + 1, badge_y))
            if idx == self.menu_index:
                self._draw_icon_glow(rect)
        rows = max(1, (len(characters) + cols - 1) // cols)
        option_y = start_y + rows * (size + margin) + 16
        menu_options = (
            self._menu_options_for_state("char")
            if hasattr(self, "_menu_options_for_state")
            else []
        )
        if not menu_options:
            menu_options = ["Add AI Player", "Difficulty", "Continue", "Back"]
        extra_options = menu_options[len(characters):]
        option_spacing = self.menu_font.get_height() + 16
        available = self.height - option_y - 50
        if extra_options and option_spacing * len(extra_options) > available:
            option_spacing = max(22, int(available / len(extra_options)))
        for idx, opt in enumerate(extra_options, start=len(characters)):
            label = opt
            if opt == "Difficulty":
                label = f"Difficulty: {self.difficulty_levels[self.difficulty_index]}"
            elif opt == "Next Page":
                label = "Next Page >"
            elif opt == "Prev Page":
                label = "< Prev Page"
            elif opt.startswith("Filter:"):
                label = f"{opt} (Cycle)"
            offset = idx - len(characters)
            self._draw_option_label(
                label,
                idx,
                (self.width // 2, option_y + offset * option_spacing),
            )
        preview_name = None
        if characters and self.menu_index < len(characters):
            preview_name = characters[self.menu_index]
        else:
            preview_name = self.selected_character or (characters[0] if characters else None)
        preview_rect = None
        if preview_name and hasattr(self, "_character_preview_data"):
            info = self._character_preview_data(preview_name)
            grid_width = cols * size + (cols - 1) * margin
            panel_width = 260
            panel_height = 220
            panel_x = start_x + grid_width + 30
            if panel_x + panel_width > self.width - 20:
                panel_x = max(20, start_x - panel_width - 30)
            panel_y = start_y
            rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
            preview_rect = rect
            self._draw_panel_shadow(rect)
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((12, 22, 30, 180))
            pygame.draw.rect(panel, (0, 170, 170), panel.get_rect(), 2)
            self.screen.blit(panel, rect)
            title = self.menu_font.render(preview_name, True, MENU_TEXT_COLOR)
            self.screen.blit(title, (rect.x + 14, rect.y + 12))
            stats_lines = [
                f"Role: {info.get('role', 'n/a')}",
                f"ATK: {info.get('attack', 0)}",
                f"DEF: {info.get('defense', 0)}",
                f"HP: {info.get('health', 0)}",
                f"MANA: {info.get('mana', 0)}",
                f"SPD: {info.get('speed', 1.0)}x",
            ]
            text_y = rect.y + 50
            for line in stats_lines:
                text = self.small_font.render(line, True, (200, 220, 230))
                self.screen.blit(text, (rect.x + 14, text_y))
                text_y += 22
        guide_lines = [
            "Pick a fighter for each player.",
            "Enter confirms the highlighted tile.",
            "Continue moves to map selection.",
        ]
        if self.multiplayer and self.human_players > 1:
            guide_lines = [
                "Each player picks a fighter.",
                "Enter locks the current pick.",
                "Continue advances when ready.",
            ]
            for idx, chosen in enumerate(self.character_selections):
                guide_lines.append(f"P{idx + 1}: {chosen or '...'}")
        if guide_lines:
            grid_width = cols * size + (cols - 1) * margin
            panel_width = 260
            panel_height = 120 if len(guide_lines) <= 4 else 150
            panel_x = (
                preview_rect.x
                if preview_rect
                else start_x + grid_width + 30
            )
            if panel_x + panel_width > self.width - 20:
                panel_x = max(20, start_x - panel_width - 30)
            panel_y = (
                preview_rect.bottom + 16
                if preview_rect
                else start_y + 10
            )
            if panel_y + panel_height < self.height - 60:
                rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
                self._draw_panel_shadow(rect)
                panel = pygame.Surface(rect.size, pygame.SRCALPHA)
                panel.fill((12, 22, 30, 180))
                pygame.draw.rect(panel, (0, 170, 170), panel.get_rect(), 2)
                self.screen.blit(panel, rect)
                title = self.menu_font.render(
                    "Selection Guide", True, MENU_TEXT_COLOR
                )
                self.screen.blit(title, (rect.x + 14, rect.y + 10))
                text_y = rect.y + 42
                for line in guide_lines:
                    text = self.small_font.render(
                        line, True, (200, 220, 230)
                    )
                    self.screen.blit(text, (rect.x + 14, text_y))
                    text_y += 20
        if hasattr(self, "_page_count"):
            total_count = len(self.characters)
            if hasattr(self, "_filtered_characters"):
                total_count = len(self._filtered_characters())
            total = self._page_count(
                total_count, getattr(self, "character_page_size", 1)
            )
            if total > 1:
                page_label = self.menu_font.render(
                    f"Page {self.character_page + 1}/{total}", True, MENU_TEXT_COLOR
                )
                self.screen.blit(
                    page_label,
                    page_label.get_rect(center=(self.width // 2, 76)),
                )
        info = f"AI Players: {self.ai_players}"
        if self.multiplayer and not self.online_multiplayer:
            info += f" | Players Joined: {self.human_players}"
        selected = self.selected_character
        if self.menu_index < len(characters):
            selected = characters[self.menu_index]
        if selected:
            selected_text = self.menu_font.render(
                f"Selected: {selected}", True, MENU_TEXT_COLOR
            )
            self.screen.blit(
                selected_text,
                selected_text.get_rect(center=(self.width // 2, self.height - 70)),
            )
        if self.multiplayer and self.human_players > 1:
            status = []
            for idx, chosen in enumerate(self.character_selections):
                status.append(f"P{idx + 1}: {chosen or '...'}")
            status_text = self.small_font.render(
                " | ".join(status), True, (200, 220, 230)
            )
            self.screen.blit(
                status_text,
                status_text.get_rect(
                    center=(self.width // 2, self.height - 110)
                ),
            )
            pick_text = self.small_font.render(
                f"Picking: P{self.character_select_index + 1}",
                True,
                (190, 210, 220),
            )
            self.screen.blit(
                pick_text,
                pick_text.get_rect(
                    center=(self.width // 2, self.height - 90)
                ),
            )
        text = self.menu_font.render(info, True, MENU_TEXT_COLOR)
        self.screen.blit(
            text, text.get_rect(center=(self.width // 2, self.height - 40))
        )
        if self.multiplayer and not self.online_multiplayer:
            prompt = self.menu_font.render("Press J to join", True, MENU_TEXT_COLOR)
            self.screen.blit(
                prompt, prompt.get_rect(center=(self.width // 2, self.height - 20))
            )
        self._draw_input_prompt("Enter/Space selects - Filter option cycles list")
        self._draw_border()

    def _draw_map_menu(self) -> None:
        self._draw_background()
        self._draw_menu_header("Select Map", subtitle="Hazards + Layout")
        if hasattr(self, "_map_filter_label"):
            filter_text = self.small_font.render(
                self._map_filter_label(), True, MENU_TEXT_COLOR
            )
            self.screen.blit(
                filter_text,
                (self.width - filter_text.get_width() - 20, 18),
            )
        if self.multiplayer and self.human_players > 1:
            picker = self.small_font.render(
                f"Picking: P{self.map_select_index + 1}",
                True,
                (200, 220, 230),
            )
            self.screen.blit(picker, (20, 18))
        maps = self._paged_maps() if hasattr(self, "_paged_maps") else list(self.maps)
        cols = 5
        size = 64
        margin = 18
        cols = min(6, max(3, self.width // (size + margin)))
        start_x = (self.width - (cols * size + (cols - 1) * margin)) // 2
        start_y = 100
        player_colors = [
            (0, 200, 255),
            (255, 170, 0),
            (130, 255, 170),
            (255, 120, 220),
        ]
        selections: list[str | None] = []
        if getattr(self, "multiplayer", False) and getattr(
            self, "human_players", 1
        ) > 1:
            selections = list(getattr(self, "map_selections", []))
        for idx, name in enumerate(maps):
            row = idx // cols
            col = idx % cols
            x = start_x + col * (size + margin)
            y = start_y + row * (size + margin)
            img = self.map_images[name]
            rect = img.get_rect(topleft=(x, y))
            frame_rect = pygame.Rect(x - 4, y - 4, size + 8, size + 8)
            pygame.draw.rect(self.screen, (12, 20, 28), frame_rect)
            pygame.draw.rect(self.screen, (0, 120, 150), frame_rect, 2)
            self.screen.blit(img, rect)
            if selections:
                picked = [
                    i for i, chosen in enumerate(selections) if chosen == name
                ]
                for tag_slot, player_idx in enumerate(picked):
                    color = player_colors[player_idx % len(player_colors)]
                    pygame.draw.rect(self.screen, color, rect, 3)
                    label = self.small_font.render(
                        f"P{player_idx + 1}", True, color
                    )
                    badge_x = rect.x + 4
                    badge_y = rect.y + 4 + tag_slot * 18
                    badge_rect = pygame.Rect(
                        badge_x - 2,
                        badge_y - 1,
                        label.get_width() + 6,
                        label.get_height() + 2,
                    )
                    pygame.draw.rect(self.screen, (8, 12, 16), badge_rect)
                    pygame.draw.rect(self.screen, color, badge_rect, 2)
                    self.screen.blit(label, (badge_x + 1, badge_y))
            if idx == self.menu_index:
                self._draw_icon_glow(rect)
        rows = max(1, (len(maps) + cols - 1) // cols)
        option_y = start_y + rows * (size + margin) + 16
        menu_options = (
            self._menu_options_for_state("map")
            if hasattr(self, "_menu_options_for_state")
            else []
        )
        if not menu_options:
            menu_options = list(maps) + ["Back"]
        extra_options = menu_options[len(maps):]
        option_spacing = self.menu_font.get_height() + 16
        available = self.height - option_y - 50
        if extra_options and option_spacing * len(extra_options) > available:
            option_spacing = max(22, int(available / len(extra_options)))
        for idx, opt in enumerate(extra_options, start=len(maps)):
            label = opt
            if opt == "Next Page":
                label = "Next Page >"
            elif opt == "Prev Page":
                label = "< Prev Page"
            elif opt == "Random":
                label = "Random Map"
            elif opt.startswith("Filter:"):
                label = f"{opt} (Cycle)"
            offset = idx - len(maps)
            self._draw_option_label(
                label,
                idx,
                (self.width // 2, option_y + offset * option_spacing),
            )
        preview_name = None
        if maps and self.menu_index < len(maps):
            preview_name = maps[self.menu_index]
        else:
            preview_name = self.selected_map or (maps[0] if maps else None)
        preview_rect = None
        if preview_name and hasattr(self, "_map_preview_data"):
            info = self._map_preview_data(preview_name)
            grid_width = cols * size + (cols - 1) * margin
            panel_width = 280
            panel_height = 240
            panel_x = start_x + grid_width + 30
            if panel_x + panel_width > self.width - 20:
                panel_x = max(20, start_x - panel_width - 30)
            panel_y = start_y
            rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
            preview_rect = rect
            self._draw_panel_shadow(rect)
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((12, 22, 30, 180))
            pygame.draw.rect(panel, (0, 170, 170), panel.get_rect(), 2)
            self.screen.blit(panel, rect)
            title = self.menu_font.render(preview_name, True, MENU_TEXT_COLOR)
            self.screen.blit(title, (rect.x + 14, rect.y + 10))
            img = self.map_images.get(preview_name)
            if img:
                preview_img = pygame.transform.smoothscale(img, (110, 110))
                self.screen.blit(preview_img, (rect.x + 14, rect.y + 42))
            platform_total = (
                int(info.get("platforms", 0))
                + int(info.get("moving", 0))
                + int(info.get("crumbling", 0))
            )
            hazard_types = info.get("hazard_types") or []
            hazard_label = ", ".join(hazard_types) if hazard_types else "None"
            stats_lines = [
                f"Hazards: {info.get('hazards', 0)}",
                f"Types: {hazard_label}",
                f"Platforms: {platform_total}",
                f"Minions: {info.get('minions', 0)}",
                f"Boss: {'Yes' if info.get('boss') else 'No'}",
                f"Threat: {info.get('threat', 0)}",
            ]
            text_y = rect.y + 42
            text_x = rect.x + 140
            for line in stats_lines:
                text = self.small_font.render(line, True, (200, 220, 230))
                self.screen.blit(text, (text_x, text_y))
                text_y += 22
        guide_lines = [
            "Pick a stage or use Random.",
            "Filters narrow the map list.",
        ]
        if self.multiplayer and self.human_players > 1:
            guide_lines = [
                "Each player picks a stage.",
                "Final map is chosen randomly.",
            ]
            for idx, chosen in enumerate(self.map_selections):
                guide_lines.append(f"P{idx + 1}: {chosen or '...'}")
        if guide_lines:
            grid_width = cols * size + (cols - 1) * margin
            panel_width = 280
            panel_height = 110 if len(guide_lines) <= 4 else 140
            panel_x = (
                preview_rect.x
                if preview_rect
                else start_x + grid_width + 30
            )
            if panel_x + panel_width > self.width - 20:
                panel_x = max(20, start_x - panel_width - 30)
            panel_y = (
                preview_rect.bottom + 16
                if preview_rect
                else start_y + 10
            )
            if panel_y + panel_height < self.height - 60:
                rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
                self._draw_panel_shadow(rect)
                panel = pygame.Surface(rect.size, pygame.SRCALPHA)
                panel.fill((12, 22, 30, 180))
                pygame.draw.rect(panel, (0, 170, 170), panel.get_rect(), 2)
                self.screen.blit(panel, rect)
                title = self.menu_font.render(
                    "Map Ballot", True, MENU_TEXT_COLOR
                )
                self.screen.blit(title, (rect.x + 14, rect.y + 10))
                text_y = rect.y + 42
                for line in guide_lines:
                    text = self.small_font.render(
                        line, True, (200, 220, 230)
                    )
                    self.screen.blit(text, (rect.x + 14, text_y))
                    text_y += 20
        if hasattr(self, "_page_count"):
            total_count = len(self.maps)
            if hasattr(self, "_filtered_maps"):
                total_count = len(self._filtered_maps())
            total = self._page_count(total_count, getattr(self, "map_page_size", 1))
            if total > 1:
                page_label = self.menu_font.render(
                    f"Page {self.map_page + 1}/{total}", True, MENU_TEXT_COLOR
                )
                self.screen.blit(
                    page_label,
                    page_label.get_rect(center=(self.width // 2, 76)),
                )
        if not (self.multiplayer and self.human_players > 1) and preview_name:
            selected_text = self.menu_font.render(
                f"Selected: {preview_name}", True, MENU_TEXT_COLOR
            )
            self.screen.blit(
                selected_text,
                selected_text.get_rect(
                    center=(self.width // 2, self.height - 70)
                ),
            )
        if self.multiplayer and self.human_players > 1:
            status = []
            for idx, chosen in enumerate(self.map_selections):
                status.append(f"P{idx + 1}: {chosen or '...'}")
            status_text = self.small_font.render(
                " | ".join(status), True, (200, 220, 230)
            )
            self.screen.blit(
                status_text,
                status_text.get_rect(
                    center=(self.width // 2, self.height - 90)
                ),
            )
            message = getattr(self, "map_select_message", "")
            if message:
                msg_text = self.small_font.render(
                    message, True, (200, 220, 230)
                )
                self.screen.blit(
                    msg_text,
                    msg_text.get_rect(
                        center=(self.width // 2, self.height - 68)
                    ),
                )
        self._draw_input_prompt("Enter/Space selects - Filter option cycles list")
        self._draw_border()

    def _draw_chapter_menu(self) -> None:
        self._draw_background()
        self._draw_menu_header("Select Chapter", subtitle="Story Progression")
        cols = 5
        size = 64
        margin = 20
        start_x = (self.width - (cols * size + (cols - 1) * margin)) // 2
        start_y = 80
        for idx, name in enumerate(self.chapters):
            row = idx // cols
            col = idx % cols
            x = start_x + col * (size + margin)
            y = start_y + row * (size + margin)
            img = self.chapter_images[name]
            rect = img.get_rect(topleft=(x, y))
            frame_rect = pygame.Rect(x - 4, y - 4, size + 8, size + 8)
            pygame.draw.rect(self.screen, (12, 20, 28), frame_rect)
            pygame.draw.rect(self.screen, (0, 120, 150), frame_rect, 2)
            self.screen.blit(img, rect)
            if idx == self.menu_index:
                self._draw_icon_glow(rect)
        rows = max(1, (len(self.chapters) + cols - 1) // cols)
        option_y = start_y + rows * (size + margin) + 16
        back_idx = len(self.chapters)
        text = self.menu_font.render(
            "Back",
            True,
            MENU_TEXT_COLOR if self.menu_index == back_idx else (50, 50, 50),
        )
        rect = text.get_rect(center=(self.width // 2, option_y))
        self.screen.blit(text, rect)
        preview = None
        if self.chapters and self.menu_index < len(self.chapters):
            preview = self.chapters[self.menu_index]
        else:
            preview = self.selected_chapter
            if preview is None and self.chapters:
                preview = self.chapters[0]
        if preview:
            selected_text = self.menu_font.render(
                f"Selected: {preview}", True, MENU_TEXT_COLOR
            )
            self.screen.blit(
                selected_text,
                selected_text.get_rect(
                    center=(self.width // 2, self.height - 70)
                ),
            )
        preview_rect = None
        grid_width = cols * size + (cols - 1) * margin
        if preview and hasattr(self, "_chapter_preview_data"):
            info = self._chapter_preview_data(preview)
            panel_width = 280
            panel_height = 240
            panel_x = start_x + grid_width + 30
            if panel_x + panel_width > self.width - 20:
                panel_x = max(20, start_x - panel_width - 30)
            panel_y = start_y
            rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
            preview_rect = rect
            self._draw_panel_shadow(rect)
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((12, 22, 30, 180))
            pygame.draw.rect(panel, (0, 170, 170), panel.get_rect(), 2)
            self.screen.blit(panel, rect)
            title = self.menu_font.render(preview, True, MENU_TEXT_COLOR)
            self.screen.blit(title, (rect.x + 14, rect.y + 10))
            img = self.chapter_images.get(preview)
            if img:
                preview_img = pygame.transform.smoothscale(img, (110, 110))
                self.screen.blit(preview_img, (rect.x + 14, rect.y + 42))
            hazard_types = info.get("hazard_types") or []
            hazard_label = ", ".join(hazard_types) if hazard_types else "None"
            platform_total = (
                int(info.get("platforms", 0))
                + int(info.get("moving", 0))
                + int(info.get("crumbling", 0))
            )
            stats_lines = [
                f"Hazards: {info.get('hazards', 0)}",
                f"Types: {hazard_label}",
                f"Platforms: {platform_total}",
                f"Minions: {info.get('minions', 0)}",
                f"Boss: {'Yes' if info.get('boss') else 'No'}",
                f"Threat: {info.get('threat', 0)}",
            ]
            text_y = rect.y + 42
            text_x = rect.x + 140
            for line in stats_lines:
                text = self.small_font.render(line, True, (200, 220, 230))
                self.screen.blit(text, (text_x, text_y))
                text_y += 22
        portrait_name = self.selected_character
        if portrait_name is None and getattr(self, "characters", None):
            portrait_name = self.characters[0]
        if portrait_name and hasattr(self, "_character_preview_data"):
            info = self._character_preview_data(portrait_name)
            panel_width = 260
            panel_height = 220
            left_x = start_x - panel_width - 30
            panel_x = left_x if left_x >= 20 else start_x + grid_width + 30
            if panel_x + panel_width > self.width - 20:
                panel_x = max(20, self.width - panel_width - 20)
            panel_y = start_y
            if preview_rect and panel_x == preview_rect.x:
                panel_y = preview_rect.bottom + 16
            if panel_y + panel_height < self.height - 60:
                rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
                self._draw_panel_shadow(rect)
                panel = pygame.Surface(rect.size, pygame.SRCALPHA)
                panel.fill((12, 22, 30, 180))
                pygame.draw.rect(panel, (0, 170, 170), panel.get_rect(), 2)
                self.screen.blit(panel, rect)
                title = self.menu_font.render(
                    portrait_name, True, MENU_TEXT_COLOR
                )
                self.screen.blit(title, (rect.x + 14, rect.y + 10))
                portrait = self.character_images.get(portrait_name)
                if portrait:
                    portrait_img = pygame.transform.smoothscale(
                        portrait, (110, 110)
                    )
                    self.screen.blit(portrait_img, (rect.x + 14, rect.y + 42))
                stats_lines = [
                    f"Role: {info.get('role', 'n/a')}",
                    f"ATK: {info.get('attack', 0)}",
                    f"DEF: {info.get('defense', 0)}",
                    f"HP: {info.get('health', 0)}",
                ]
                text_y = rect.y + 42
                text_x = rect.x + 140
                for line in stats_lines:
                    text = self.small_font.render(line, True, (200, 220, 230))
                    self.screen.blit(text, (text_x, text_y))
                    text_y += 22
        guide_lines = [
            "Chapters unlock in order.",
            "Enter begins the highlighted chapter.",
        ]
        panel_width = 280
        panel_height = 110
        panel_x = preview_rect.x if preview_rect else start_x + grid_width + 30
        if panel_x + panel_width > self.width - 20:
            panel_x = max(20, start_x - panel_width - 30)
        panel_y = preview_rect.bottom + 16 if preview_rect else start_y
        if panel_y + panel_height < self.height - 60:
            rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
            self._draw_panel_shadow(rect)
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((12, 22, 30, 180))
            pygame.draw.rect(panel, (0, 170, 170), panel.get_rect(), 2)
            self.screen.blit(panel, rect)
            title = self.menu_font.render(
                "Chapter Guide", True, MENU_TEXT_COLOR
            )
            self.screen.blit(title, (rect.x + 14, rect.y + 10))
            text_y = rect.y + 42
            for line in guide_lines:
                text = self.small_font.render(line, True, (200, 220, 230))
                self.screen.blit(text, (rect.x + 14, text_y))
                text_y += 20
        self._draw_input_prompt("Use arrows + Enter/Space to select")
        self._draw_border()

    def _draw_settings_menu(self) -> None:
        """Display the settings options."""
        self._draw_background()
        self._draw_title("Settings", (self.width // 2, self.height // 4))
        labels = []
        for opt in self.settings_options:
            label = opt
            if opt == "Volume":
                label = f"Volume: {int(self.volume * 100)}%"
            elif opt == "Show FPS":
                label = f"Show FPS: {'On' if self.show_fps else 'Off'}"
            elif opt == "Input Method":
                label = f"Input Method: {self.input_method.title()}"
            elif opt == "Window Size":
                label = f"Window Size: {self.width}x{self.height}"
            elif opt == "HUD Size":
                label = f"HUD Size: {getattr(self, 'hud_font_size', 18)}px"
            labels.append(label)
        base_line_height = self.menu_font.get_height() + 16
        line_height = max(
            24,
            min(base_line_height, int(self.height * 0.5 / max(1, len(labels)))),
        )
        start_y = int(self.height * 0.5 - (line_height * len(labels)) / 2)
        for i, label in enumerate(labels):
            self._draw_option_label(
                label, i, (self.width // 2, start_y + i * line_height)
            )
        self._draw_border()
        self.screen.set_at((0, 0), MENU_BG_COLOR)
        self.screen.set_at((0, 0), MENU_BG_COLOR)
        self.screen.set_at((0, 0), MENU_BG_COLOR)

    def _draw_key_bindings_menu(self) -> None:
        """Show current key bindings and allow selection for rebinding."""
        self._draw_background()
        self._draw_title("Key Bindings", (self.width // 2, self.height // 4))
        labels = []
        for action in self.key_options:
            if action == "Back":
                label = "Back"
            else:
                key_name = pygame.key.name(self.key_bindings.get(action, 0))
                label = f"{action.title()}: {key_name}"
            labels.append(label)
        base_line_height = self.menu_font.get_height() + 14
        line_height = max(
            22,
            min(base_line_height, int(self.height * 0.55 / max(1, len(labels)))),
        )
        start_y = int(self.height * 0.5 - (line_height * len(labels)) / 2)
        for i, label in enumerate(labels):
            self._draw_option_label(
                label, i, (self.width // 2, start_y + i * line_height)
            )
        self._draw_border()
        self.screen.set_at((0, 0), MENU_BG_COLOR)

    def _draw_controller_bindings_menu(self) -> None:
        """Display controller button mappings."""
        self._draw_background()
        self._draw_title("Controller Bindings", (self.width // 2, self.height // 4))
        labels = []
        for action in self.controller_options:
            if action == "Back":
                label = "Back"
            else:
                label = f"{action.title()}: {self.controller_bindings.get(action, 0)}"
            labels.append(label)
        base_line_height = self.menu_font.get_height() + 14
        line_height = max(
            22,
            min(base_line_height, int(self.height * 0.55 / max(1, len(labels)))),
        )
        start_y = int(self.height * 0.5 - (line_height * len(labels)) / 2)
        for i, label in enumerate(labels):
            self._draw_option_label(
                label, i, (self.width // 2, start_y + i * line_height)
            )
        self._draw_border()

    def _draw_rebind_prompt(self) -> None:
        self._draw_background()
        prompt = self.menu_font.render(
            f"Press a key for {self.rebind_action.title()}", True, MENU_TEXT_COLOR
        )
        self.screen.blit(
            prompt, prompt.get_rect(center=(self.width // 2, self.height // 2))
        )
        self._draw_border()

    def _draw_rebind_controller_prompt(self) -> None:
        self._draw_background()
        prompt = self.menu_font.render(
            f"Press a button for {self.rebind_action.title()}", True, MENU_TEXT_COLOR
        )
        self.screen.blit(
            prompt, prompt.get_rect(center=(self.width // 2, self.height // 2))
        )
        self._draw_border()

    def _draw_node_menu(self) -> None:
        """Display node hosting options."""
        self._draw_background()
        self._draw_title("Node Settings", (self.width // 2, self.height // 4))
        for i, opt in enumerate(self.node_options):
            label = opt
            if opt == "Start Node" and self.node_hosting:
                label = "Start Node (running)"
            if opt == "Latency Helper" and self.latency_helper:
                label = "Latency Helper (on)"
            if opt == "Background Mining" and self.mining_enabled:
                label = "Background Mining (on)"
            self._draw_option_label(
                label, i, (self.width // 2, self.height // 2 + i * 40)
            )
        note = self.menu_font.render(
            "Mining uses ~20% CPU to build the MMO world.", True, MENU_TEXT_COLOR
        )
        self.screen.blit(
            note, note.get_rect(center=(self.width // 2, self.height - 40))
        )
        self._draw_border()

    def _draw_accessibility_menu(self) -> None:
        """Display accessibility toggles."""
        self._draw_background()
        self._draw_menu_header("Accessibility", subtitle="Comfort Settings")
        for i, opt in enumerate(self.accessibility_options):
            label = opt
            if opt == "Font Scale":
                scale = 1.0
                manager = getattr(self, "accessibility_manager", None)
                if manager:
                    scale = float(manager.options.get("font_scale", 1.0))
                label = f"Font Scale: {scale:.2f}x"
            if (
                opt == "High Contrast"
                and self.accessibility_manager.options.get("high_contrast")
            ):
                label = "High Contrast (on)"
            if (
                opt == "Input Prompts"
                and self.accessibility_manager.options.get("input_prompts")
            ):
                label = "Input Prompts (on)"
            if (
                opt == "Colorblind Mode"
                and self.accessibility_manager.options["colorblind"]
            ):
                label = "Colorblind Mode (on)"
            self._draw_option_label(
                label, i, (self.width // 2, self.height // 2 + i * 40)      
            )
        self._draw_input_prompt("Enter to toggle - Back to exit")
        self._draw_border()

    def _draw_accounts_menu(self) -> None:
        """Display simple account management options."""
        self._draw_background()
        palette = self._menu_palette()
        self._draw_menu_header("Accounts", subtitle="Identity + Access Keys")
        panel_width = int(self.width * 0.46)
        panel_height = int(self.height * 0.45)
        panel_x = int(self.width * 0.12)
        panel_y = int(self.height * 0.3)
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        self._draw_panel_shadow(panel_rect)
        panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        panel.fill((12, 20, 34, 190))
        pygame.draw.rect(panel, palette["border"], panel.get_rect(), 2)
        pygame.draw.line(
            panel,
            palette["highlight"],
            (16, 8),
            (panel_rect.width - 16, 8),
            2,
        )
        self.screen.blit(panel, panel_rect)
        for i, opt in enumerate(self.account_options):
            self._draw_option_label(
                opt,
                i,
                (panel_rect.centerx, panel_rect.y + 30 + i * 40),
            )
        summary_width = int(self.width * 0.28)
        summary_height = panel_height
        summary_x = panel_rect.right + int(self.width * 0.04)
        summary_y = panel_rect.y
        summary_rect = pygame.Rect(summary_x, summary_y, summary_width, summary_height)
        summary_panel = pygame.Surface(summary_rect.size, pygame.SRCALPHA)
        summary_panel.fill((14, 22, 36, 185))
        pygame.draw.rect(summary_panel, palette["border"], summary_panel.get_rect(), 2)
        self.screen.blit(summary_panel, summary_rect)
        title = self.menu_font.render("Account Profile", True, MENU_TEXT_COLOR)
        self.screen.blit(title, (summary_rect.x + 16, summary_rect.y + 16))
        account_id = getattr(self, "account_id", "player")
        accounts_manager = getattr(self, "accounts_manager", None)
        account_data = accounts_manager.get(account_id) if accounts_manager else None
        account_level = "guest"
        key_status = "None"
        if account_data:
            account_level = str(account_data.get("level", "user"))
            key_status = "On File" if account_data.get("public_key") else "None"
        lines = [
            f"Account: {account_id}",
            f"Tier: {account_level}",
            f"Key: {key_status}",
            f"Auto-Dev: {'Enabled' if getattr(self, 'auto_dev_manager', None) else 'Off'}",
            f"MMO Access: {'Unlocked' if getattr(self, 'mmo_unlocked', False) else 'Locked'}",
        ]
        y = summary_rect.y + 54
        for line in lines:
            text = self.small_font.render(line, True, (200, 215, 220))
            self.screen.blit(text, (summary_rect.x + 16, y))
            y += 24
        self._draw_input_prompt("Enter to manage account - Back to exit")
        self._draw_border()

    def _draw_lobby_menu(self) -> None:
        """Show current players before starting multiplayer."""
        self._draw_background()
        self._draw_menu_header("Lobby", subtitle="Ready Check")
        names = list(self.player_names)
        picks = list(getattr(self, "character_selections", []))
        cards = []
        for idx, name in enumerate(names):
            pick = None
            if idx < len(picks):
                pick = picks[idx]
            elif idx == 0 and self.selected_character:
                pick = self.selected_character
            if pick is None and name.lower().startswith("ai"):
                if getattr(self, "characters", None):
                    rng = random.Random(1200 + idx)
                    pick = rng.choice(self.characters)
            cards.append({"name": name, "pick": pick})
        maps = list(getattr(self, "maps", []))
        map_selection = self.selected_map
        selections = list(getattr(self, "map_selections", []))
        if selections:
            map_selection = next((item for item in selections if item), map_selection)
        if map_selection is None and maps:
            map_selection = maps[0]
        if maps:
            current_idx = maps.index(map_selection) if map_selection in maps else 0
            carousel = [
                maps[(current_idx - 1) % len(maps)],
                maps[current_idx],
                maps[(current_idx + 1) % len(maps)],
            ]
            size = 46
            margin = 12
            total_width = 3 * size + 2 * margin
            start_x = (self.width - total_width) // 2
            y = 68
            for i, name in enumerate(carousel):
                x = start_x + i * (size + margin)
                img = self.map_images.get(name)
                rect = pygame.Rect(x, y, size, size)
                self._draw_panel_shadow(rect)
                panel = pygame.Surface(rect.size, pygame.SRCALPHA)
                panel.fill((12, 22, 30, 160))
                pygame.draw.rect(panel, (0, 170, 170), panel.get_rect(), 2)
                self.screen.blit(panel, rect)
                if img:
                    thumb = pygame.transform.smoothscale(img, (size, size))
                    self.screen.blit(thumb, rect)
                if i == 1:
                    glow_rect = rect.inflate(8, 8)
                    pygame.draw.rect(self.screen, (240, 220, 120), glow_rect, 2)
            label = self.small_font.render(
                "Stage Preview", True, (200, 220, 230)
            )
            self.screen.blit(
                label, label.get_rect(center=(self.width // 2, 48))
            )
        cols = 2 if len(cards) > 1 else 1
        card_width = 260
        card_height = 72
        margin = 18
        grid_width = cols * card_width + (cols - 1) * margin
        start_x = (self.width - grid_width) // 2
        start_y = 120
        for idx, card in enumerate(cards):
            row = idx // cols
            col = idx % cols
            x = start_x + col * (card_width + margin)
            y = start_y + row * (card_height + margin)
            rect = pygame.Rect(x, y, card_width, card_height)
            self._draw_panel_shadow(rect)
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((12, 22, 30, 190))
            pygame.draw.rect(panel, (0, 170, 170), panel.get_rect(), 2)
            self.screen.blit(panel, rect)
            name_text = self.menu_font.render(
                card["name"], True, MENU_TEXT_COLOR
            )
            self.screen.blit(name_text, (rect.x + 14, rect.y + 8))
            pick_label = card["pick"] or "Pick: TBD"
            pick_text = self.small_font.render(
                f"Pick: {pick_label}", True, (200, 220, 230)
            )
            self.screen.blit(pick_text, (rect.x + 14, rect.y + 38))
            ready = bool(card["pick"])
            ready_text = self.small_font.render(
                "Ready" if ready else "Waiting",
                True,
                (120, 240, 160) if ready else (220, 180, 120),
            )
            self.screen.blit(
                ready_text,
                ready_text.get_rect(right=rect.right - 14, top=rect.y + 10),
            )
            if card["pick"] and card["pick"] in self.character_images:
                portrait = self.character_images[card["pick"]]
                portrait_img = pygame.transform.smoothscale(portrait, (48, 48))
                self.screen.blit(portrait_img, (rect.right - 62, rect.y + 12))
        rows = max(1, (len(cards) + cols - 1) // cols)
        grid_height = rows * card_height + (rows - 1) * margin
        summary_lines = [
            f"Mode: {self.selected_mode or 'Arena'}",
            f"Difficulty: {self.difficulty_levels[self.difficulty_index]}",
            f"AI Players: {self.ai_players}",
            f"Players: {self.human_players}",
        ]
        summary_width = 260
        summary_height = 140
        summary_x = start_x - summary_width - 30
        summary_y = start_y
        if summary_x < 20:
            summary_x = 20
            summary_y = start_y + grid_height + 24
        if summary_y + summary_height < self.height - 120:
            rect = pygame.Rect(summary_x, summary_y, summary_width, summary_height)
            self._draw_panel_shadow(rect)
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((12, 22, 30, 180))
            pygame.draw.rect(panel, (0, 170, 170), panel.get_rect(), 2)
            self.screen.blit(panel, rect)
            title = self.menu_font.render(
                "Match Summary", True, MENU_TEXT_COLOR
            )
            self.screen.blit(title, (rect.x + 14, rect.y + 10))
            text_y = rect.y + 42
            for line in summary_lines:
                text = self.small_font.render(line, True, (200, 220, 230))
                self.screen.blit(text, (rect.x + 14, text_y))
                text_y += 20
        map_name = None
        selections = list(getattr(self, "map_selections", []))
        if selections:
            map_name = next((item for item in selections if item), None)
        if map_name is None:
            map_name = self.selected_map
        preview_label = map_name or "Pending"
        if map_name is None and getattr(self, "maps", None):
            map_name = self.maps[0]
        map_rect = None
        if map_name and hasattr(self, "_map_preview_data"):
            info = self._map_preview_data(map_name)
            panel_width = 280
            panel_height = 240
            panel_x = start_x + grid_width + 30
            panel_y = start_y
            if panel_x + panel_width > self.width - 20:
                panel_x = max(20, start_x)
                panel_y = start_y + grid_height + 24
            if panel_y + panel_height < self.height - 100:
                rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
                map_rect = rect
                self._draw_panel_shadow(rect)
                panel = pygame.Surface(rect.size, pygame.SRCALPHA)
                panel.fill((12, 22, 30, 180))
                pygame.draw.rect(panel, (0, 170, 170), panel.get_rect(), 2)
                self.screen.blit(panel, rect)
                title = self.menu_font.render(
                    f"Stage: {preview_label}", True, MENU_TEXT_COLOR
                )
                self.screen.blit(title, (rect.x + 14, rect.y + 10))
                img = self.map_images.get(map_name)
                if img:
                    preview_img = pygame.transform.smoothscale(img, (110, 110))
                    self.screen.blit(preview_img, (rect.x + 14, rect.y + 42))
                hazard_types = info.get("hazard_types") or []
                hazard_label = ", ".join(hazard_types) if hazard_types else "None"
                platform_total = (
                    int(info.get("platforms", 0))
                    + int(info.get("moving", 0))
                    + int(info.get("crumbling", 0))
                )
                stats_lines = [
                    f"Hazards: {info.get('hazards', 0)}",
                    f"Types: {hazard_label}",
                    f"Platforms: {platform_total}",
                    f"Minions: {info.get('minions', 0)}",
                    f"Boss: {'Yes' if info.get('boss') else 'No'}",
                    f"Threat: {info.get('threat', 0)}",
                ]
                text_y = rect.y + 42
                text_x = rect.x + 140
                for line in stats_lines:
                    text = self.small_font.render(line, True, (200, 220, 230))
                    self.screen.blit(text, (text_x, text_y))
                    text_y += 22
        if self.selected_character and hasattr(self, "_character_preview_data"):
            info = self._character_preview_data(self.selected_character)
            panel_width = 260
            panel_height = 220
            panel_x = start_x - panel_width - 30
            panel_y = start_y
            if summary_y == start_y and summary_x == panel_x:
                panel_y = summary_y + summary_height + 16
            if panel_x < 20:
                panel_x = 20
                panel_y = start_y + grid_height + 24
            if map_rect and panel_x == map_rect.x:
                panel_y = map_rect.bottom + 16
            if panel_y + panel_height < self.height - 100:
                rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
                self._draw_panel_shadow(rect)
                panel = pygame.Surface(rect.size, pygame.SRCALPHA)
                panel.fill((12, 22, 30, 180))
                pygame.draw.rect(panel, (0, 170, 170), panel.get_rect(), 2)
                self.screen.blit(panel, rect)
                title = self.menu_font.render(
                    self.selected_character, True, MENU_TEXT_COLOR
                )
                self.screen.blit(title, (rect.x + 14, rect.y + 10))
                portrait = self.character_images.get(self.selected_character)
                if portrait:
                    portrait_img = pygame.transform.smoothscale(
                        portrait, (110, 110)
                    )
                    self.screen.blit(portrait_img, (rect.x + 14, rect.y + 42))
                stats_lines = [
                    f"Role: {info.get('role', 'n/a')}",
                    f"ATK: {info.get('attack', 0)}",
                    f"DEF: {info.get('defense', 0)}",
                    f"HP: {info.get('health', 0)}",
                ]
                text_y = rect.y + 42
                text_x = rect.x + 140
                for line in stats_lines:
                    text = self.small_font.render(line, True, (200, 220, 230))
                    self.screen.blit(text, (text_x, text_y))
                    text_y += 22
        option_start = max(start_y + grid_height + 30, self.height - 120)
        for i, opt in enumerate(self.lobby_options):
            idx = len(self.player_names) + i
            self._draw_option_label(
                opt, idx, (self.width // 2, option_start + i * 40)
            )
        self._draw_input_prompt("Enter to confirm - Back to adjust")
        self._draw_border()

    def _draw_pause_menu(self) -> None:
        """Display a simple pause menu."""
        self._draw_option_menu("Paused", self.pause_options)

    def _draw_game_over_menu(self) -> None:
        """Display results after the player loses all lives."""
        self._draw_background()
        self._draw_title("Game Over", (self.width // 2, int(self.height * 0.18)))
        combo = getattr(self.score_manager, "combo", 0)
        entries = [
            ("Time", f"{self.final_time}s"),
            ("Score", f"{self.score}"),
            ("High Score", f"{self.best_score}"),
            ("Combo", f"x{combo}"),
        ]
        self._draw_summary_cards(entries, start_y=int(self.height * 0.34))
        if self.show_end_options:
            panel_width = int(self.width * 0.4)
            panel_height = 30 + 36 * len(self.game_over_options)
            panel_x = self.width // 2 - panel_width // 2
            panel_y = int(self.height * 0.72)
            panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
            panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
            panel.fill((18, 20, 28, 170))
            pygame.draw.rect(panel, (140, 80, 80), panel.get_rect(), 2)
            self.screen.blit(panel, panel_rect)
            label = self.small_font.render("Next Actions", True, (220, 200, 200))
            self.screen.blit(label, (panel_rect.x + 12, panel_rect.y + 8))
            for i, opt in enumerate(self.game_over_options):
                self._draw_option_label(
                    opt,
                    i,
                    (panel_rect.centerx, panel_rect.y + 30 + i * 34),
                )
        self._draw_end_flash(getattr(self, "game_over_flash_until", 0), (180, 40, 40))
        self._draw_border()

    def _draw_victory_menu(self) -> None:
        """Display results after clearing the stage."""
        self._draw_background()
        self._draw_title("Victory!", (self.width // 2, int(self.height * 0.18)))
        combo = getattr(self.score_manager, "combo", 0)
        wins = getattr(self, "arena_wins", 0)
        entries = [
            ("Time", f"{self.final_time}s"),
            ("Best Time", f"{self.best_time}s"),
            ("Score", f"{self.score}"),
            ("High Score", f"{self.best_score}"),
            ("Combo", f"x{combo}"),
            ("Arena Wins", f"{wins}"),
        ]
        self._draw_summary_cards(entries, start_y=int(self.height * 0.32))
        if self.show_end_options:
            options = self.victory_options
            if hasattr(self, "_menu_options_for_state"):
                options = self._menu_options_for_state("victory") or options
            panel_width = int(self.width * 0.4)
            panel_height = 30 + 36 * len(options)
            panel_x = self.width // 2 - panel_width // 2
            panel_y = int(self.height * 0.72)
            panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
            panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
            panel.fill((12, 22, 30, 170))
            pygame.draw.rect(panel, (0, 170, 170), panel.get_rect(), 2)
            self.screen.blit(panel, panel_rect)
            label = self.small_font.render("Next Actions", True, (200, 220, 230))
            self.screen.blit(label, (panel_rect.x + 12, panel_rect.y + 8))
            for i, opt in enumerate(options):
                self._draw_option_label(
                    opt,
                    i,
                    (panel_rect.centerx, panel_rect.y + 30 + i * 34),
                )
        self._draw_end_flash(getattr(self, "victory_flash_until", 0), (220, 180, 80))
        self._draw_border()

    def _draw_inventory_menu(self) -> None:
        """Render the player's inventory list."""
        self._draw_background()
        items = list(self.player.inventory.items.items())
        for idx, (name, count) in enumerate(items):
            label = f"{name} x{count}"
            self._draw_option_label(label, idx, (self.width // 2, 80 + idx * 40))
        self._draw_option_label(
            "Back", len(items), (self.width // 2, 80 + len(items) * 40)
        )
        self._draw_border()

    def _draw_equipment_menu(self) -> None:
        """Render equipment slots in a Diablo-style grid."""
        self._draw_background()
        cx = self.width // 2
        layout = {
            "head": (cx, 80),
            "chest": (cx, 160),
            "legs": (cx, 240),
            "boots": (cx, 320),
            "weapon": (cx - 120, 160),
            "offhand": (cx + 120, 160),
            "ring": (cx + 120, 240),
        }
        slots = self.player.equipment.order
        for idx, slot in enumerate(slots):
            x, y = layout[slot]
            rect = pygame.Rect(0, 0, 80, 80)
            rect.center = (x, y)
            color = MENU_TEXT_COLOR if idx == self.menu_index else (50, 50, 50)
            pygame.draw.rect(self.screen, color, rect, 2)
            label = self.menu_font.render(
                self.player.equipment.get(slot) or slot, True, color
            )
            self.screen.blit(label, label.get_rect(center=rect.center))
        back_idx = len(slots)
        back_color = (
            MENU_TEXT_COLOR if self.menu_index == back_idx else (50, 50, 50)
        )
        back = self.menu_font.render("Back", True, back_color)
        self.screen.blit(back, back.get_rect(center=(cx, self.height - 60)))
        self._draw_border()

    def _draw_how_to_play(self) -> None:
        """Show basic controls and objective."""
        self._draw_background()
        self._draw_title("How To Play", (self.width // 2, 40))
        lines = [
            "Move: Arrow keys or WASD",
            "Jump: Space",
            "Shoot: Z",
            "Melee: X",
            "Block: Shift | Parry: C",
            "Special: V",
            "Back",
        ]
        for i, line in enumerate(lines):
            self._draw_option_label(line, i, (self.width // 2, 120 + i * 30))
        self._draw_border()

    def _draw_credits(self) -> None:
        """Display a simple credits screen."""
        self._draw_background()
        self._draw_title("Credits", (self.width // 2, 40))
        credits = [
            "Prototype by Hololive Fans",
            "Powered by Pygame",
            "Back",
        ]
        for i, line in enumerate(credits):
            self._draw_option_label(line, i, (self.width // 2, 120 + i * 30))
        self._draw_border()

    def _draw_goals_menu(self) -> None:
        """Show the first few project goals from documentation."""
        self._draw_background()
        self._draw_title("Goals", (self.width // 2, 40))
        goals: list[str] = []
        try:
            path = Path(__file__).resolve().parent.parent / "docs/GOALS.md"
            with path.open(encoding="utf-8") as fh:
                for line in fh:
                    if line.startswith("- "):
                        goals.append(line[2:].strip())
                    if len(goals) == 5:
                        break
        except OSError:
            pass
        goals.append("Back")
        for i, line in enumerate(goals):
            self._draw_option_label(line, i, (self.width // 2, 120 + i * 30))
        self._draw_border()

    def _draw_scoreboard_menu(self) -> None:
        """Show best time and high score."""
        self._draw_background()
        self._draw_title("Records", (self.width // 2, 40))
        lines = [
            f"Best Time: {self.best_time}s",
            f"High Score: {self.best_score}",
        ]
        if getattr(self, "reputation_manager", None):
            top = self.reputation_manager.top(3)
            if top:
                faction_summary = ", ".join(
                    f"{name} ({value})" for name, value in top
                )
                lines.append(f"Top Factions: {faction_summary}")
            else:
                lines.append("Top Factions: None yet")
        lines.append("Back")
        for i, line in enumerate(lines):
            self._draw_option_label(line, i, (self.width // 2, 120 + i * 30))
        self._draw_border()

    def _draw_achievements_menu(self) -> None:
        """List unlocked achievements."""
        self._draw_background()
        self._draw_title("Achievements", (self.width // 2, 40))
        if self.achievement_manager.unlocked:
            lines = sorted(self.achievement_manager.unlocked)
        else:
            lines = ["No achievements yet"]
        lines.append("Back")
        for i, line in enumerate(lines):
            self._draw_option_label(line, i, (self.width // 2, 120 + i * 30))
        self._draw_border()
