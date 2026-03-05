"""Tests for UI layout helper primitives."""

from __future__ import annotations

import pytest
pygame = pytest.importorskip("pygame")

from hololive_coliseum.ui_layout import (
    align_rect,
    clamp_rect,
    hstack,
    inset_rect,
    place,
    truncate_text,
    vstack,
)


def test_inset_and_clamp_rect() -> None:
    bounds = pygame.Rect(0, 0, 200, 100)
    inset = inset_rect(bounds, 10, 12, 14, 16)
    assert inset == pygame.Rect(10, 12, 176, 72)
    rect = pygame.Rect(-30, -20, 300, 150)
    clamped = clamp_rect(rect, bounds)
    assert clamped.width == 200
    assert clamped.height == 100
    assert clamped.topleft == (0, 0)


def test_align_and_place() -> None:
    bounds = pygame.Rect(10, 20, 300, 200)
    rect = pygame.Rect(0, 0, 50, 30)
    aligned = align_rect(rect, bounds, h="right", v="bottom")
    assert aligned.right == bounds.right
    assert aligned.bottom == bounds.bottom
    center = place(bounds, 40, 20, anchor="c")
    assert center.center == bounds.center


def test_vstack_hstack_count_and_bounds() -> None:
    bounds = pygame.Rect(0, 0, 120, 80)
    rows, overflow_rows = vstack(bounds, [20, 20, 20, 20], 4, with_overflow=True)
    assert len(rows) == 4
    assert isinstance(overflow_rows, bool)
    for rect in rows:
        assert bounds.contains(rect)
    cols, overflow_cols = hstack(bounds, [40, 40, 40], 4, with_overflow=True)
    assert len(cols) == 3
    assert isinstance(overflow_cols, bool)
    for rect in cols:
        assert bounds.contains(rect)


def test_truncate_text_fits_width() -> None:
    if not pygame.get_init():
        pygame.init()
    try:
        if not pygame.font.get_init():
            pygame.font.init()
    except pygame.error:
        pytest.skip("pygame font unavailable in this environment")
    font = pygame.font.SysFont(None, 24)
    text = "This is a long diagnostic label"
    out = truncate_text(font, text, 100)
    assert isinstance(out, str)
    assert font.size(out)[0] <= 100
