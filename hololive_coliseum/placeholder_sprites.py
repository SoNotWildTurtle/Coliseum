"""Create placeholder sprite files at runtime when assets are missing."""

from __future__ import annotations

import os
import math
from typing import Iterable

import pygame

DEFAULT_SIZE = (64, 64)
MAP_SIZE = (96, 64)


def ensure_placeholder_sprites(
    image_dir: str,
    character_names: list[str],
    chapter_count: int = 20,
    enemy_names: Iterable[str] | None = None,
    map_names: Iterable[str] | None = None,
    force: bool = False,
) -> None:
    """Generate themed placeholder PNGs for characters, enemies, and menus."""

    os.makedirs(image_dir, exist_ok=True)
    char_dir = os.path.join(image_dir, "characters")
    enemy_dir = os.path.join(image_dir, "enemies")
    os.makedirs(char_dir, exist_ok=True)
    os.makedirs(enemy_dir, exist_ok=True)
    names = list(dict.fromkeys(character_names))
    for name in names:
        base = _filename_base(name)
        label = _short_label(name)
        _create_sprite_pair(
            char_dir, base, label, theme_name=name, force=force
        )
    enemies = list(dict.fromkeys(list(enemy_names or [])))
    for name in enemies:
        base = _filename_base(name)
        label = _short_label(name)
        _create_sprite_pair(
            enemy_dir, base, label, theme_name=name, force=force
        )
    if map_names:
        for name in map_names:
            filename = _map_filename(name)
            label = _short_label(name, limit=8)
            _create_single(
                image_dir,
                filename,
                label,
                MAP_SIZE,
                _color_from_name(name),
                theme_name=name,
                force=force,
            )
    else:
        map_entries = [
            ("map_default.png", "Map"),
            ("map_sky_spires.png", "Sky"),
            ("map_canyon_run.png", "Canyon"),
            ("map_forge_pit.png", "Forge"),
            ("map_crystal_rift.png", "Rift"),
            ("map_verdant_ruins.png", "Ruins"),
        ]
        for filename, label in map_entries:
            _create_single(
                image_dir,
                filename,
                label,
                MAP_SIZE,
                _color_from_name(filename),
                force=force,
            )
    for index in range(1, chapter_count + 1):
        _create_single(
            image_dir,
            f"chapter{index}.png",
            f"Ch {index}",
            DEFAULT_SIZE,
            _color_from_name(f"chapter{index}"),
            force=force,
        )


def _filename_base(name: str) -> str:
    return name.replace(" ", "_").replace("'", "").replace(".", "")


def _short_label(name: str, limit: int = 10) -> str:
    label = name.strip() or "Sprite"
    return label if len(label) <= limit else f"{label[:limit - 1]}."


def _map_filename(name: str) -> str:
    base = _filename_base(name).lower()
    return f"map_{base}.png"


def _create_sprite_pair(
    image_dir: str,
    base: str,
    label: str,
    theme_name: str | None = None,
    force: bool = False,
) -> None:
    right = os.path.join(image_dir, f"{base}_right.png")
    left = os.path.join(image_dir, f"{base}_left.png")
    color = _color_from_name(theme_name or base)
    _create_single(
        image_dir,
        os.path.basename(right),
        label,
        DEFAULT_SIZE,
        color,
        direction="right",
        theme_name=theme_name,
        force=force,
    )
    _create_single(
        image_dir,
        os.path.basename(left),
        label,
        DEFAULT_SIZE,
        color,
        direction="left",
        theme_name=theme_name,
        force=force,
    )


def _create_single(
    image_dir: str,
    filename: str,
    label: str,
    size: tuple[int, int],
    color: tuple[int, int, int],
    direction: str | None = None,
    theme_name: str | None = None,
    force: bool = False,
) -> None:
    path = os.path.join(image_dir, filename)
    if os.path.exists(path) and not force:
        return
    surface = pygame.Surface(size, pygame.SRCALPHA)
    accent, shade = _accent_palette(color)
    _paint_gradient(surface, color)
    _paint_panels(surface, accent, shade)
    _paint_highlights(surface)
    _paint_badge_stripes(surface, accent)
    motif = _motif_for_name(theme_name or label)
    _paint_emblem(surface, direction, accent, motif)
    _paint_frame(surface, shade)
    _render_label(surface, label)
    pygame.image.save(surface, path)


def _render_label(surface: pygame.Surface, label: str) -> None:
    try:
        font = pygame.font.SysFont(None, 16)
        shadow = font.render(label, True, (10, 10, 10))
        text = font.render(label, True, (245, 245, 245))
    except (pygame.error, RuntimeError):
        return
    rect = text.get_rect(center=surface.get_rect().center)
    surface.blit(shadow, (rect.x + 1, rect.y + 1))
    surface.blit(text, rect)


def _paint_gradient(surface: pygame.Surface, color: tuple[int, int, int]) -> None:
    width, height = surface.get_size()
    base_r, base_g, base_b = color
    for y in range(height):
        ratio = y / max(1, height - 1)
        r = int(base_r * (0.7 + ratio * 0.3))
        g = int(base_g * (0.7 + ratio * 0.3))
        b = int(base_b * (0.7 + ratio * 0.3))
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))


def _accent_palette(
    base: tuple[int, int, int]
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    accent = tuple(min(255, channel + 50) for channel in base)
    shade = tuple(max(0, channel - 45) for channel in base)
    return accent, shade


def _paint_panels(
    surface: pygame.Surface,
    accent: tuple[int, int, int],
    shade: tuple[int, int, int],
) -> None:
    width, height = surface.get_size()
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.polygon(
        overlay,
        (*shade, 120),
        [
            (0, int(height * 0.15)),
            (int(width * 0.4), 0),
            (int(width * 0.7), 0),
            (0, int(height * 0.55)),
        ],
    )
    pygame.draw.rect(
        overlay,
        (*accent, 90),
        pygame.Rect(
            int(width * 0.55),
            int(height * 0.15),
            int(width * 0.35),
            int(height * 0.18),
        ),
    )
    pygame.draw.rect(
        overlay,
        (*shade, 110),
        pygame.Rect(
            int(width * 0.1),
            int(height * 0.7),
            int(width * 0.8),
            int(height * 0.15),
        ),
        border_radius=4,
    )
    surface.blit(overlay, (0, 0))


def _paint_highlights(surface: pygame.Surface) -> None:
    width, height = surface.get_size()
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.polygon(
        overlay,
        (255, 255, 255, 70),
        [(0, 0), (int(width * 0.7), 0), (0, int(height * 0.6))],
    )
    pygame.draw.rect(
        overlay,
        (255, 255, 255, 40),
        pygame.Rect(
            int(width * 0.1),
            int(height * 0.65),
            int(width * 0.8),
            int(height * 0.18),
        ),
    )
    surface.blit(overlay, (0, 0))


def _paint_badge_stripes(
    surface: pygame.Surface, accent: tuple[int, int, int]
) -> None:
    width, height = surface.get_size()
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    for idx in range(3):
        offset = idx * 6
        pygame.draw.line(
            overlay,
            (*accent, 70),
            (width - 5 - offset, 4),
            (4, height - 5 - offset),
            2,
        )
    surface.blit(overlay, (0, 0))


def _paint_emblem(
    surface: pygame.Surface,
    direction: str | None,
    accent: tuple[int, int, int],
    motif: str,
) -> None:
    width, height = surface.get_size()
    center = (width // 2, height // 2)
    radius = min(width, height) // 3
    pygame.draw.circle(surface, (*accent, 200), center, radius)
    pygame.draw.circle(surface, (25, 25, 30), center, radius, 2)
    pygame.draw.circle(surface, (240, 240, 240, 160), center, radius - 6)       
    pygame.draw.circle(surface, (25, 25, 30), center, radius - 6, 2)
    _paint_motif(surface, motif, center, radius)
    eye_offset = radius // 2
    pygame.draw.circle(
        surface, (25, 25, 30), (center[0] - eye_offset, center[1] - 2), 3
    )
    pygame.draw.circle(
        surface, (25, 25, 30), (center[0] + eye_offset, center[1] - 2), 3
    )
    mouth = pygame.Rect(center[0] - 8, center[1] + 6, 16, 4)
    pygame.draw.rect(surface, (25, 25, 30), mouth)
    sparkle = [
        (center[0], center[1] - radius - 6),
        (center[0] + 4, center[1] - radius - 2),
        (center[0], center[1] + -radius + 2),
        (center[0] - 4, center[1] - radius - 2),
    ]
    pygame.draw.polygon(surface, (250, 250, 250), sparkle)
    if direction in {"left", "right"}:
        arrow_y = height - 12
        if direction == "left":
            points = [(10, arrow_y), (26, arrow_y - 6), (26, arrow_y + 6)]
        else:
            points = [(width - 10, arrow_y), (width - 26, arrow_y - 6), (width - 26, arrow_y + 6)]
        pygame.draw.polygon(surface, (25, 25, 30), points)


def _paint_motif(
    surface: pygame.Surface,
    motif: str,
    center: tuple[int, int],
    radius: int,
) -> None:
    if motif == "shark":
        fin = [
            (center[0] - 4, center[1] - radius + 6),
            (center[0] + 10, center[1] - radius + 2),
            (center[0] + 2, center[1] - radius + 18),
        ]
        pygame.draw.polygon(surface, (20, 40, 70), fin)
    elif motif == "phoenix":
        wing = [
            (center[0] - radius + 6, center[1] + 2),
            (center[0] - 4, center[1] - 6),
            (center[0] + radius - 8, center[1] + 4),
        ]
        pygame.draw.polygon(surface, (255, 120, 40), wing)
    elif motif == "reaper":
        pygame.draw.arc(
            surface,
            (180, 180, 200),
            pygame.Rect(center[0] - radius + 4, center[1] - radius + 4, radius, radius),
            0.8,
            2.6,
            3,
        )
    elif motif == "tentacle":
        for idx in range(3):
            offset = idx * 6 - 6
            pygame.draw.arc(
                surface,
                (120, 60, 180),
                pygame.Rect(
                    center[0] - 10 + offset,
                    center[1] - 4,
                    20,
                    20,
                ),
                3.6,
                5.9,
                3,
            )
    elif motif == "clock":
        pygame.draw.circle(surface, (30, 30, 40), center, radius - 10, 2)
        pygame.draw.line(
            surface,
            (30, 30, 40),
            center,
            (center[0], center[1] - radius + 12),
            2,
        )
        pygame.draw.line(
            surface,
            (30, 30, 40),
            center,
            (center[0] + 10, center[1] + 2),
            2,
        )
    elif motif == "shrimp":
        pygame.draw.arc(
            surface,
            (255, 170, 140),
            pygame.Rect(center[0] - 10, center[1] - 4, 20, 14),
            0.2,
            3.0,
            3,
        )
        pygame.draw.circle(surface, (60, 20, 20), (center[0] + 8, center[1]), 2)
    elif motif == "fan":
        pygame.draw.circle(surface, (230, 230, 255), center, radius - 12, 2)
        pygame.draw.line(
            surface,
            (230, 230, 255),
            (center[0] - 6, center[1] + 4),
            (center[0] + 8, center[1] - 6),
            2,
        )
    elif motif == "leaf":
        pygame.draw.ellipse(
            surface,
            (120, 200, 120),
            pygame.Rect(center[0] - 10, center[1] - 6, 20, 12),
        )
        pygame.draw.line(
            surface,
            (60, 120, 60),
            (center[0] - 8, center[1]),
            (center[0] + 8, center[1]),
            2,
        )
    elif motif == "magnifier":
        pygame.draw.circle(surface, (30, 30, 40), center, radius - 10, 2)
        pygame.draw.line(
            surface,
            (30, 30, 40),
            (center[0] + 6, center[1] + 6),
            (center[0] + 16, center[1] + 16),
            3,
        )
    elif motif == "heart":
        pygame.draw.circle(surface, (255, 110, 150), (center[0] - 6, center[1] - 4), 6)
        pygame.draw.circle(surface, (255, 110, 150), (center[0] + 6, center[1] - 4), 6)
        pygame.draw.polygon(
            surface,
            (255, 110, 150),
            [
                (center[0] - 14, center[1] - 2),
                (center[0] + 14, center[1] - 2),
                (center[0], center[1] + 14),
            ],
        )
    elif motif == "owl":
        pygame.draw.circle(surface, (120, 100, 70), center, radius - 8, 2)
        pygame.draw.circle(surface, (240, 230, 210), (center[0] - 6, center[1] - 2), 4)
        pygame.draw.circle(surface, (240, 230, 210), (center[0] + 6, center[1] - 2), 4)
        pygame.draw.circle(surface, (25, 25, 30), (center[0] - 6, center[1] - 2), 2)
        pygame.draw.circle(surface, (25, 25, 30), (center[0] + 6, center[1] - 2), 2)
    elif motif == "dice":
        dice = pygame.Rect(center[0] - 10, center[1] - 10, 20, 20)
        pygame.draw.rect(surface, (220, 220, 220), dice)
        pygame.draw.rect(surface, (30, 30, 40), dice, 2)
        pygame.draw.circle(surface, (30, 30, 40), dice.center, 2)
    elif motif == "fox":
        pygame.draw.polygon(
            surface,
            (255, 160, 90),
            [
                (center[0], center[1] + 6),
                (center[0] - 12, center[1] - 10),
                (center[0] + 12, center[1] - 10),
            ],
        )
    elif motif == "festival":
        points = []
        for i in range(5):
            angle = i * (2 * math.pi / 5) - math.pi / 2
            outer = (center[0] + int(math.cos(angle) * (radius - 6)),
                     center[1] + int(math.sin(angle) * (radius - 6)))
            inner = (center[0] + int(math.cos(angle + math.pi / 5) * (radius - 14)),
                     center[1] + int(math.sin(angle + math.pi / 5) * (radius - 14)))
            points.extend([outer, inner])
        pygame.draw.polygon(surface, (255, 230, 120), points)
    elif motif == "shrine":
        pygame.draw.rect(surface, (200, 40, 60), (center[0] - 12, center[1] - 8, 24, 4))
        pygame.draw.rect(surface, (200, 40, 60), (center[0] - 10, center[1] - 4, 4, 14))
        pygame.draw.rect(surface, (200, 40, 60), (center[0] + 6, center[1] - 4, 4, 14))
    elif motif == "water":
        pygame.draw.circle(surface, (80, 140, 220), (center[0], center[1] - 4), 6)
        pygame.draw.polygon(
            surface,
            (80, 140, 220),
            [
                (center[0] - 6, center[1] - 2),
                (center[0] + 6, center[1] - 2),
                (center[0], center[1] + 14),
            ],
        )
    elif motif == "carrot":
        pygame.draw.polygon(
            surface,
            (250, 140, 60),
            [
                (center[0], center[1] + 12),
                (center[0] - 6, center[1] - 6),
                (center[0] + 6, center[1] - 6),
            ],
        )
        pygame.draw.line(
            surface,
            (90, 170, 90),
            (center[0], center[1] - 10),
            (center[0], center[1] - 16),
            2,
        )
    elif motif == "anchor":
        pygame.draw.line(
            surface,
            (120, 120, 160),
            (center[0], center[1] - 10),
            (center[0], center[1] + 10),
            3,
        )
        pygame.draw.circle(surface, (120, 120, 160), (center[0], center[1] - 12), 4, 2)
        pygame.draw.arc(
            surface,
            (120, 120, 160),
            pygame.Rect(center[0] - 12, center[1], 24, 12),
            math.pi,
            2 * math.pi,
            3,
        )
    elif motif == "star":
        points = []
        for i in range(5):
            angle = i * (2 * math.pi / 5) - math.pi / 2
            outer = (center[0] + int(math.cos(angle) * (radius - 6)),
                     center[1] + int(math.sin(angle) * (radius - 6)))
            inner = (center[0] + int(math.cos(angle + math.pi / 5) * (radius - 14)),
                     center[1] + int(math.sin(angle + math.pi / 5) * (radius - 14)))
            points.extend([outer, inner])
        pygame.draw.polygon(surface, (180, 220, 255), points)
    elif motif == "oni":
        pygame.draw.polygon(
            surface,
            (180, 60, 60),
            [
                (center[0] - 10, center[1] - 6),
                (center[0] - 4, center[1] - 14),
                (center[0] + 2, center[1] - 6),
            ],
        )
        pygame.draw.polygon(
            surface,
            (180, 60, 60),
            [
                (center[0] + 10, center[1] - 6),
                (center[0] + 4, center[1] - 14),
                (center[0] - 2, center[1] - 6),
            ],
        )
    elif motif == "shield":
        pygame.draw.polygon(
            surface,
            (160, 200, 220),
            [
                (center[0] - 10, center[1] - 10),
                (center[0] + 10, center[1] - 10),
                (center[0] + 6, center[1] + 10),
                (center[0], center[1] + 14),
                (center[0] - 6, center[1] + 10),
            ],
        )
    elif motif == "flame":
        pygame.draw.circle(surface, (255, 140, 60), (center[0], center[1] + 4), 6)
        pygame.draw.polygon(
            surface,
            (255, 140, 60),
            [
                (center[0] - 6, center[1] + 2),
                (center[0] + 6, center[1] + 2),
                (center[0], center[1] - 12),
            ],
        )
    elif motif == "duck":
        pygame.draw.circle(surface, (250, 210, 90), center, 6)
        pygame.draw.rect(surface, (255, 150, 60), (center[0] + 4, center[1] + 2, 8, 4))
    elif motif == "music":
        pygame.draw.circle(surface, (150, 200, 255), (center[0] - 4, center[1] + 6), 4)
        pygame.draw.line(
            surface,
            (150, 200, 255),
            (center[0] - 4, center[1] - 8),
            (center[0] - 4, center[1] + 6),
            2,
        )
        pygame.draw.line(
            surface,
            (150, 200, 255),
            (center[0] - 4, center[1] - 8),
            (center[0] + 8, center[1] - 12),
            2,
        )
    elif motif == "book":
        pygame.draw.rect(
            surface,
            (210, 190, 150),
            pygame.Rect(center[0] - 12, center[1] - 10, 24, 18),
        )
        pygame.draw.line(
            surface,
            (120, 90, 60),
            (center[0], center[1] - 10),
            (center[0], center[1] + 8),
            2,
        )
    elif motif == "crystal":
        pygame.draw.polygon(
            surface,
            (140, 220, 255),
            [
                (center[0], center[1] - 12),
                (center[0] + 10, center[1] - 2),
                (center[0] + 6, center[1] + 12),
                (center[0] - 6, center[1] + 12),
                (center[0] - 10, center[1] - 2),
            ],
        )
    elif motif == "anvil":
        pygame.draw.rect(
            surface,
            (80, 90, 110),
            pygame.Rect(center[0] - 12, center[1] - 4, 24, 8),
        )
        pygame.draw.rect(
            surface,
            (60, 70, 90),
            pygame.Rect(center[0] - 6, center[1] + 4, 12, 6),
        )
    elif motif == "mountain":
        pygame.draw.polygon(
            surface,
            (120, 150, 170),
            [
                (center[0] - 12, center[1] + 12),
                (center[0], center[1] - 10),
                (center[0] + 12, center[1] + 12),
            ],
        )
    elif motif == "wind":
        pygame.draw.arc(
            surface,
            (170, 210, 230),
            pygame.Rect(center[0] - 12, center[1] - 6, 24, 12),
            0,
            math.pi,
            2,
        )
        pygame.draw.arc(
            surface,
            (170, 210, 230),
            pygame.Rect(center[0] - 10, center[1], 20, 10),
            0,
            math.pi,
            2,
        )
    elif motif == "arena":
        pygame.draw.rect(
            surface,
            (200, 170, 90),
            pygame.Rect(center[0] - 12, center[1] - 8, 24, 16),
            2,
        )


def _motif_for_name(name: str) -> str:
    low = name.lower()
    if "chapter" in low or "story" in low:
        return "book"
    if "crystal" in low or "rift" in low:
        return "crystal"
    if "forge" in low or "anvil" in low:
        return "anvil"
    if "canyon" in low or "ruins" in low:
        return "mountain"
    if "sky" in low or "wind" in low:
        return "wind"
    if "arena" in low or "coliseum" in low:
        return "arena"
    if "gura" in low or "shark" in low:
        return "shark"
    if "watson" in low or "amelia" in low:
        return "magnifier"
    if "ina" in low or "tentacle" in low:
        return "tentacle"
    if "kiara" in low or "phoenix" in low:
        return "phoenix"
    if "calliope" in low or "reaper" in low:
        return "reaper"
    if "fauna" in low or "nature" in low:
        return "leaf"
    if "kronii" in low or "time" in low:
        return "clock"
    if "irys" in low:
        return "heart"
    if "mumei" in low:
        return "owl"
    if "baelz" in low or "chaos" in low:
        return "dice"
    if "fubuki" in low or "fox" in low:
        return "fox"
    if "matsuri" in low or "festival" in low:
        return "festival"
    if "miko" in low or "shrine" in low:
        return "shrine"
    if "aqua" in low or "water" in low:
        return "water"
    if "pekora" in low or "carrot" in low:
        return "carrot"
    if "marine" in low or "anchor" in low:
        return "anchor"
    if "suisei" in low or "star" in low:
        return "star"
    if "ayame" in low or "oni" in low:
        return "oni"
    if "noel" in low or "shield" in low:
        return "shield"
    if "flare" in low or "flame" in low:
        return "flame"
    if "subaru" in low or "duck" in low:
        return "duck"
    if "sora" in low or "melody" in low:
        return "music"
    if "shrimp" in low:
        return "shrimp"
    if "fan" in low:
        return "fan"
    return "shark"


def _paint_frame(surface: pygame.Surface, shade: tuple[int, int, int]) -> None:
    rect = surface.get_rect()
    pygame.draw.rect(surface, (20, 20, 24), rect, 2)
    pygame.draw.rect(surface, shade, rect.inflate(-6, -6), 2)


def _color_from_name(name: str) -> tuple[int, int, int]:
    seed = sum(ord(ch) for ch in name)
    return (
        50 + seed % 180,
        50 + (seed * 2) % 180,
        50 + (seed * 3) % 180,
    )
