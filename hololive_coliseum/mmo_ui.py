"""MMO hub UI helpers for consistent professional presentation."""

from __future__ import annotations

from typing import Iterable

import pygame
import math

from .ui_layout import inset_rect, place, truncate_text


def mmo_palette() -> dict[str, tuple[int, int, int]]:
    """Return the shared MMO hub palette."""
    return {
        "bg_top": (4, 10, 18),
        "bg_bottom": (12, 24, 44),
        "panel": (12, 18, 32),
        "panel_alt": (16, 24, 40),
        "border": (90, 140, 190),
        "accent": (120, 220, 255),
        "accent_warm": (245, 190, 90),
        "accent_hot": (255, 120, 140),
        "neon": (120, 255, 230),
        "idol_pink": (255, 160, 210),
        "text": (230, 245, 255),
        "text_dim": (150, 180, 210),
    }


def draw_mmo_backdrop(game) -> None:
    """Draw the MMO hub background with gradient and subtle grid."""
    palette = mmo_palette()
    width, height = game.width, game.height
    metrics = getattr(game, "ui_metrics", None)
    gutter = int(getattr(metrics, "gutter", 12))
    screen_bounds = pygame.Rect(0, 0, width, height)
    safe_bounds = inset_rect(screen_bounds, gutter, gutter, gutter, gutter)
    debugger = getattr(game, "ui_debugger", None)
    if debugger is not None and debugger.is_active:
        debugger.collect_rect("mmo.screen_bounds", screen_bounds, "bounds")
        debugger.collect_rect("mmo.safe_bounds", safe_bounds, "bounds", meta={"bounds": screen_bounds})
        debugger.collect_rect("mmo.content_bounds", safe_bounds, "bounds", meta={"bounds": screen_bounds})
    top = palette["bg_top"]
    bottom = palette["bg_bottom"]
    for y in range(height):
        ratio = y / max(1, height - 1)
        r = int(top[0] + (bottom[0] - top[0]) * ratio)
        g = int(top[1] + (bottom[1] - top[1]) * ratio)
        b = int(top[2] + (bottom[2] - top[2]) * ratio)
        pygame.draw.line(game.screen, (r, g, b), (0, y), (width, y))
    game._mmo_draw_starfield()
    grid = pygame.Surface((width, height), pygame.SRCALPHA)
    for x in range(0, width, 90):
        pygame.draw.line(grid, (*palette["accent"], 16), (x, 0), (x, height))
    for y in range(0, height, 90):
        pygame.draw.line(grid, (*palette["accent"], 16), (0, y), (width, y))
    game.screen.blit(grid, (0, 0))
    sweep = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(0, width, 220):
        pygame.draw.line(
            sweep,
            (*palette["neon"], 14),
            (i, 0),
            (i + 120, height),
            2,
        )
    game.screen.blit(sweep, (0, 0))
    vignette = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(vignette, (0, 0, 0, 90), vignette.get_rect(), 24)
    game.screen.blit(vignette, (0, 0))


def draw_mmo_header(
    game,
    *,
    title: str,
    subtitle: str,
    status_lines: Iterable[str],
) -> None:
    """Render the MMO hub top bar with title and status."""
    palette = mmo_palette()
    metrics = getattr(game, "ui_metrics", None)
    pad = int(getattr(metrics, "panel_pad", 16))
    line_gap = int(getattr(metrics, "title_gap", 18))
    now = pygame.time.get_ticks()
    bar_height = metrics.pad(64) if metrics else 64
    bar = pygame.Surface((game.width, bar_height), pygame.SRCALPHA)
    debugger = getattr(game, "ui_debugger", None)
    if debugger is not None and debugger.is_active:
        header_rect = pygame.Rect(0, 0, game.width, bar_height)
        debugger.collect_rect(
            "mmo.header",
            header_rect,
            "panel",
            meta={"bounds": pygame.Rect(0, 0, game.width, game.height)},
        )
    bar.fill((*palette["panel"], 232))
    pygame.draw.line(
        bar,
        palette["accent"],
        (0, bar_height - 3),
        (game.width, bar_height - 3),
        2,
    )
    pulse = 0
    if getattr(game, "mmo_match_status", "") in {"ready", "launching"}:
        pulse = int((math.sin(now / 180) + 1) * 40)
    neon_color = (
        min(255, palette["neon"][0] + pulse),
        min(255, palette["neon"][1] + pulse),
        min(255, palette["neon"][2] + pulse),
    )
    pygame.draw.line(
        bar,
        neon_color,
        (0, bar_height - 1),
        (game.width, bar_height - 1),
        1,
    )
    game.screen.blit(bar, (0, 0))
    title_render = game.menu_font.render(title, True, palette["text"])
    title_pos = place(
        pygame.Rect(0, 0, game.width, bar_height),
        title_render.get_width(),
        title_render.get_height(),
        anchor="tl",
        dx=pad,
        dy=metrics.pad(12) if metrics else 12,
    )
    game.screen.blit(title_render, title_pos.topleft)
    subtitle_render = game.small_font.render(subtitle, True, palette["text_dim"])
    subtitle_pos = place(
        pygame.Rect(0, 0, game.width, bar_height),
        subtitle_render.get_width(),
        subtitle_render.get_height(),
        anchor="tl",
        dx=pad,
        dy=bar_height - subtitle_render.get_height() - max(4, line_gap // 2),
    )
    game.screen.blit(subtitle_render, subtitle_pos.topleft)
    x = game.width - pad
    max_line_width = max(40, game.width // 4)
    for line in status_lines:
        clipped = truncate_text(game.small_font, str(line), max_line_width)
        render = game.small_font.render(clipped, True, palette["text"])
        rect = render.get_rect()
        x -= rect.width
        game.screen.blit(render, (x, 18))
        x -= pad


def draw_mmo_command_panel(
    game,
    *,
    rect: pygame.Rect,
    sections: Iterable[tuple[str, Iterable[str]]],
) -> None:
    """Draw a structured command guide panel."""
    palette = mmo_palette()
    debugger = getattr(game, "ui_debugger", None)
    if debugger is not None and debugger.is_active:
        debugger.collect_rect(
            "mmo.command_panel",
            rect,
            "panel",
            meta={"bounds": pygame.Rect(0, 0, game.width, game.height)},
        )
    metrics = getattr(game, "ui_metrics", None)
    pad = int(getattr(metrics, "panel_pad", 16))
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    panel.fill((*palette["panel"], 220))
    pygame.draw.rect(panel, palette["border"], panel.get_rect(), metrics.border_thickness if metrics else 2)
    x = pad
    y = metrics.pad(12) if metrics else 12
    for title, lines in sections:
        if y > rect.height - (metrics.pad(28) if metrics else 28):
            break
        heading = game.small_font.render(title, True, palette["accent"])
        panel.blit(heading, (x, y))
        y += metrics.pad(20) if metrics else 20
        for line in lines:
            label = game.small_font.render(line, True, palette["text"])
            panel.blit(label, (x, y))
            y += metrics.pad(18) if metrics else 18
        y += max(4, (metrics.pad(8) if metrics else 8))
    game.screen.blit(panel, rect.topleft)


def draw_mmo_status_panel(
    game,
    *,
    rect: pygame.Rect,
    title: str,
    rows: Iterable[tuple[str, str]],
) -> None:
    """Draw a right-side status card for MMO telemetry."""
    palette = mmo_palette()
    debugger = getattr(game, "ui_debugger", None)
    if debugger is not None and debugger.is_active:
        debugger.collect_rect(
            "mmo.status_panel",
            rect,
            "panel",
            meta={"bounds": pygame.Rect(0, 0, game.width, game.height)},
        )
    metrics = getattr(game, "ui_metrics", None)
    pad = int(getattr(metrics, "panel_pad", 16))
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    panel.fill((*palette["panel_alt"], 230))
    pygame.draw.rect(panel, palette["border"], panel.get_rect(), metrics.border_thickness if metrics else 2)
    header = game.small_font.render(title, True, palette["accent"])
    panel.blit(header, (pad, metrics.pad(10) if metrics else 10))
    pygame.draw.line(
        panel,
        palette["idol_pink"],
        (pad, metrics.pad(28) if metrics else 28),
        (rect.width - pad, metrics.pad(28) if metrics else 28),
        1,
    )
    y = metrics.pad(32) if metrics else 32
    for label, value in rows:
        if y > rect.height - (metrics.pad(24) if metrics else 24):
            break
        label_render = game.small_font.render(label, True, palette["text_dim"])
        value_render = game.small_font.render(value, True, palette["text"])
        panel.blit(label_render, (pad, y))
        panel.blit(value_render, (rect.width - value_render.get_width() - pad, y))
        y += metrics.pad(20) if metrics else 20
    game.screen.blit(panel, rect.topleft)


def draw_mmo_footer(game, text: str) -> None:
    """Draw a footer strip for system status messaging."""
    palette = mmo_palette()
    metrics = getattr(game, "ui_metrics", None)
    pad = int(getattr(metrics, "panel_pad", 16))
    height = metrics.pad(34) if metrics else 34
    rect = place(
        pygame.Rect(0, 0, game.width, game.height),
        game.width,
        height,
        anchor="bl",
    )
    debugger = getattr(game, "ui_debugger", None)
    if debugger is not None and debugger.is_active:
        debugger.collect_rect(
            "mmo.footer",
            rect,
            "panel",
            meta={"bounds": pygame.Rect(0, 0, game.width, game.height)},
        )
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    panel.fill((*palette["panel"], 224))
    pygame.draw.line(panel, palette["border"], (0, 0), (rect.width, 0), metrics.border_thickness if metrics else 2)
    pygame.draw.line(panel, palette["neon"], (0, 2), (rect.width, 2), 1)
    clipped = truncate_text(game.small_font, str(text), max(40, rect.width - pad * 2))
    label = game.small_font.render(clipped, True, palette["text_dim"])
    panel.blit(label, (pad, max(0, (rect.height - label.get_height()) // 2)))
    game.screen.blit(panel, rect.topleft)
