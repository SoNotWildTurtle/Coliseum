"""Reusable UI layout primitives for alignment, stacking, and text fitting."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import pygame


def _to_rect(value: pygame.Rect | tuple[int, int, int, int]) -> pygame.Rect:
    if isinstance(value, pygame.Rect):
        return pygame.Rect(value)
    return pygame.Rect(int(value[0]), int(value[1]), int(value[2]), int(value[3]))


def clamp_rect(
    rect: pygame.Rect | tuple[int, int, int, int],
    bounds: pygame.Rect | tuple[int, int, int, int],
) -> pygame.Rect:
    """Clamp a rect to bounds while keeping as much area as possible."""
    out = _to_rect(rect)
    limit = _to_rect(bounds)
    out.width = min(max(0, out.width), max(0, limit.width))
    out.height = min(max(0, out.height), max(0, limit.height))
    out.left = max(limit.left, min(out.left, limit.right - out.width))
    out.top = max(limit.top, min(out.top, limit.bottom - out.height))
    return out


def inset_rect(
    bounds: pygame.Rect | tuple[int, int, int, int],
    left: int,
    top: int,
    right: int,
    bottom: int,
) -> pygame.Rect:
    """Inset a bounds rect and clamp to non-negative dimensions."""
    src = _to_rect(bounds)
    x = src.x + int(left)
    y = src.y + int(top)
    w = max(0, src.width - int(left) - int(right))
    h = max(0, src.height - int(top) - int(bottom))
    return pygame.Rect(x, y, w, h)


def align_rect(
    rect: pygame.Rect | tuple[int, int, int, int],
    bounds: pygame.Rect | tuple[int, int, int, int],
    h: str = "left",
    v: str = "top",
) -> pygame.Rect:
    """Align rect inside bounds on horizontal/vertical anchors."""
    out = _to_rect(rect)
    limit = _to_rect(bounds)
    if h == "center":
        out.centerx = limit.centerx
    elif h == "right":
        out.right = limit.right
    else:
        out.left = limit.left
    if v in {"middle", "center"}:
        out.centery = limit.centery
    elif v == "bottom":
        out.bottom = limit.bottom
    else:
        out.top = limit.top
    return out


def place(
    bounds: pygame.Rect | tuple[int, int, int, int],
    w: int,
    h: int,
    *,
    anchor: str = "tl",
    dx: int = 0,
    dy: int = 0,
) -> pygame.Rect:
    """Place a rectangle of size (w,h) within bounds using shorthand anchor."""
    limit = _to_rect(bounds)
    rect = pygame.Rect(0, 0, max(0, int(w)), max(0, int(h)))
    anchor_key = str(anchor).lower()
    if anchor_key == "tr":
        rect = align_rect(rect, limit, h="right", v="top")
    elif anchor_key == "bl":
        rect = align_rect(rect, limit, h="left", v="bottom")
    elif anchor_key == "br":
        rect = align_rect(rect, limit, h="right", v="bottom")
    elif anchor_key in {"c", "mc"}:
        rect = align_rect(rect, limit, h="center", v="middle")
    elif anchor_key == "tc":
        rect = align_rect(rect, limit, h="center", v="top")
    elif anchor_key == "bc":
        rect = align_rect(rect, limit, h="center", v="bottom")
    elif anchor_key == "ml":
        rect = align_rect(rect, limit, h="left", v="middle")
    elif anchor_key == "mr":
        rect = align_rect(rect, limit, h="right", v="middle")
    else:
        rect = align_rect(rect, limit, h="left", v="top")
    rect.move_ip(int(dx), int(dy))
    return clamp_rect(rect, limit)


def _resolve_size_item(item: int | Callable[..., int], idx: int, bounds: pygame.Rect) -> int:
    if callable(item):
        try:
            value = item(idx, bounds)
        except TypeError:
            value = item(idx)
    else:
        value = item
    return max(0, int(value))


def _debug_collect(
    debugger: Any | None,
    name: str,
    rect: pygame.Rect,
    kind: str,
    *,
    bounds: pygame.Rect,
) -> None:
    if debugger is None or not getattr(debugger, "is_active", False):
        return
    debugger.collect_rect(name, rect, kind, meta={"bounds": bounds})


def vstack(
    bounds: pygame.Rect | tuple[int, int, int, int],
    heights: Sequence[int | Callable[..., int]],
    gap: int,
    *,
    align: str = "left",
    pad: int = 0,
    with_overflow: bool = False,
    debugger: Any | None = None,
    name_prefix: str | None = None,
    kind: str = "panel",
) -> list[pygame.Rect] | tuple[list[pygame.Rect], bool]:
    """Lay out rects vertically inside bounds with optional overflow reporting."""
    limit = inset_rect(bounds, pad, pad, pad, pad)
    rects: list[pygame.Rect] = []
    y = limit.top
    overflow = False
    for idx, item in enumerate(heights):
        height = _resolve_size_item(item, idx, limit)
        rect = pygame.Rect(limit.x, y, limit.width, height)
        if align == "center":
            rect = align_rect(rect, limit, h="center", v="top")
        elif align == "right":
            rect = align_rect(rect, limit, h="right", v="top")
        else:
            rect = align_rect(rect, limit, h="left", v="top")
        clamped = clamp_rect(rect, limit)
        if clamped != rect or rect.bottom > limit.bottom:
            overflow = True
        rects.append(clamped)
        if name_prefix:
            _debug_collect(debugger, f"{name_prefix}.{idx}", clamped, kind, bounds=limit)
        y += height + int(gap)
    if with_overflow:
        return rects, overflow
    return rects


def hstack(
    bounds: pygame.Rect | tuple[int, int, int, int],
    widths: Sequence[int | Callable[..., int]],
    gap: int,
    *,
    align: str = "top",
    pad: int = 0,
    with_overflow: bool = False,
    debugger: Any | None = None,
    name_prefix: str | None = None,
    kind: str = "panel",
) -> list[pygame.Rect] | tuple[list[pygame.Rect], bool]:
    """Lay out rects horizontally inside bounds with optional overflow reporting."""
    limit = inset_rect(bounds, pad, pad, pad, pad)
    rects: list[pygame.Rect] = []
    x = limit.left
    overflow = False
    for idx, item in enumerate(widths):
        width = _resolve_size_item(item, idx, limit)
        rect = pygame.Rect(x, limit.y, width, limit.height)
        if align in {"middle", "center"}:
            rect = align_rect(rect, limit, h="left", v="middle")
        elif align == "bottom":
            rect = align_rect(rect, limit, h="left", v="bottom")
        else:
            rect = align_rect(rect, limit, h="left", v="top")
        clamped = clamp_rect(rect, limit)
        if clamped != rect or rect.right > limit.right:
            overflow = True
        rects.append(clamped)
        if name_prefix:
            _debug_collect(debugger, f"{name_prefix}.{idx}", clamped, kind, bounds=limit)
        x += width + int(gap)
    if with_overflow:
        return rects, overflow
    return rects


def truncate_text(font: pygame.font.Font, text: str, max_width: int) -> str:
    """Return text truncated with ellipsis so it fits max_width."""
    if max_width <= 0:
        return ""
    raw = str(text)
    if font.size(raw)[0] <= max_width:
        return raw
    ellipsis = "..."
    if font.size(ellipsis)[0] > max_width:
        return ""
    available = max_width - font.size(ellipsis)[0]
    out = raw
    while out and font.size(out)[0] > available:
        out = out[:-1]
    return f"{out}{ellipsis}"

