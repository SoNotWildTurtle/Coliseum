"""Generate deterministic special-attack VFX sprites for local use."""
from __future__ import annotations

import os
import math

import pygame


def _save(surface: pygame.Surface, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pygame.image.save(surface, path)


def _draw_circle(surface: pygame.Surface, color: tuple[int, int, int]) -> None:
    radius = min(surface.get_width(), surface.get_height()) // 2
    pygame.draw.circle(
        surface, color, (surface.get_width() // 2, surface.get_height() // 2), radius
    )


def _draw_vfx() -> dict[str, tuple[tuple[int, int], callable]]:
    return {
        "special_gura_trident": ((20, 8), _draw_trident),
        "special_watson_dash": ((32, 32), _draw_dash_ring),
        "special_ina_tentacle": ((18, 6), _draw_tentacle),
        "special_kiara_blast": ((84, 84), _draw_blast),
        "special_calliope_scythe": ((18, 18), _draw_scythe),
        "special_fauna_grove": ((140, 120), _draw_grove),
        "special_kronii_guard": ((36, 36), _draw_guard),
        "special_irys_shield": ((40, 40), _draw_shield),
        "special_mumei_flock": ((16, 10), _draw_flock),
        "special_baelz_glitch": ((30, 30), _draw_glitch),
        "special_baelz_burst": ((12, 12), _draw_burst),
        "special_fubuki_shard": ((16, 6), _draw_shard),
        "special_matsuri_firework": ((10, 10), _draw_firework),
        "special_miko_beam": ((18, 4), _draw_beam),
        "special_aqua_bubble": ((16, 10), _draw_bubble),
        "special_pekora_carrot": ((12, 12), _draw_carrot),
        "special_marine_anchor": ((18, 18), _draw_anchor),
        "special_suisei_star": ((14, 14), _draw_star),
        "special_ayame_slash": ((30, 30), _draw_slash),
        "special_noel_shock": ((28, 8), _draw_shockwave),
        "special_flare_fireball": ((14, 10), _draw_fireball),
        "special_subaru_blast": ((14, 8), _draw_blast_small),
        "special_sora_melody": ((14, 14), _draw_melody),
        "special_enemy_pulse": ((16, 6), _draw_enemy_pulse),
    }


def _render_frame(
    size: tuple[int, int],
    draw_fn,
    idx: int,
    total: int,
) -> pygame.Surface:
    base = pygame.Surface(size, pygame.SRCALPHA)
    draw_fn(base)
    if total <= 1:
        return base
    phase = (idx / total) * math.tau
    angle = math.sin(phase) * 8
    scale = 0.9 + 0.1 * math.sin(phase + 0.5)
    warped = pygame.transform.rotozoom(base, angle, scale)
    frame = pygame.Surface(size, pygame.SRCALPHA)
    frame.blit(warped, warped.get_rect(center=(size[0] // 2, size[1] // 2)))
    return frame


def _draw_trident(surface: pygame.Surface) -> None:
    pygame.draw.line(surface, (0, 235, 235), (0, 4), (20, 4), 3)
    pygame.draw.line(surface, (0, 235, 235), (14, 1), (20, 4), 2)
    pygame.draw.line(surface, (0, 235, 235), (14, 7), (20, 4), 2)


def _draw_dash_ring(surface: pygame.Surface) -> None:
    pygame.draw.circle(surface, (120, 200, 255), (16, 16), 12, 2)
    pygame.draw.line(surface, (120, 200, 255), (6, 16), (26, 16), 2)


def _draw_tentacle(surface: pygame.Surface) -> None:
    pygame.draw.line(surface, (150, 90, 210), (0, 3), (18, 3), 3)


def _draw_blast(surface: pygame.Surface) -> None:
    _draw_circle(surface, (255, 130, 50))
    pygame.draw.circle(
        surface,
        (255, 200, 140),
        (surface.get_width() // 2, surface.get_height() // 2),
        surface.get_width() // 2 - 6,
        3,
    )


def _draw_scythe(surface: pygame.Surface) -> None:
    pygame.draw.arc(
        surface,
        (200, 200, 220),
        pygame.Rect(2, 2, 14, 14),
        0.6,
        2.6,
        3,
    )


def _draw_grove(surface: pygame.Surface) -> None:
    surface.fill((0, 0, 0, 0))
    pygame.draw.ellipse(surface, (90, 220, 140, 110), surface.get_rect(), 0)
    pygame.draw.ellipse(
        surface, (140, 255, 190, 120), surface.get_rect().inflate(-20, -14), 2
    )


def _draw_guard(surface: pygame.Surface) -> None:
    pygame.draw.circle(surface, (170, 200, 255), (18, 18), 14, 2)
    pygame.draw.circle(surface, (80, 110, 160), (18, 18), 6, 2)


def _draw_shield(surface: pygame.Surface) -> None:
    pygame.draw.circle(surface, (210, 170, 255), (20, 20), 16, 2)
    pygame.draw.circle(surface, (240, 220, 255), (20, 20), 8, 2)


def _draw_flock(surface: pygame.Surface) -> None:
    pygame.draw.polygon(
        surface,
        (180, 180, 240),
        [(0, 5), (8, 0), (15, 5), (8, 9)],
    )


def _draw_glitch(surface: pygame.Surface) -> None:
    pygame.draw.circle(surface, (200, 120, 255), (15, 15), 11, 2)
    pygame.draw.circle(surface, (80, 40, 120), (15, 15), 5, 2)
    pygame.draw.line(surface, (255, 160, 210), (4, 15), (26, 15), 2)


def _draw_burst(surface: pygame.Surface) -> None:
    pygame.draw.circle(surface, (255, 120, 200), (6, 6), 6)


def _draw_shard(surface: pygame.Surface) -> None:
    pygame.draw.polygon(
        surface,
        (200, 240, 255),
        [(0, 3), (10, 0), (15, 3), (10, 6)],
    )


def _draw_firework(surface: pygame.Surface) -> None:
    pygame.draw.circle(surface, (255, 210, 120), (5, 5), 5)


def _draw_beam(surface: pygame.Surface) -> None:
    pygame.draw.line(surface, (255, 90, 120), (0, 2), (18, 2), 3)


def _draw_bubble(surface: pygame.Surface) -> None:
    pygame.draw.circle(surface, (80, 150, 255), (8, 5), 5)


def _draw_carrot(surface: pygame.Surface) -> None:
    pygame.draw.polygon(
        surface,
        (250, 150, 70),
        [(6, 0), (0, 12), (12, 12)],
    )
    pygame.draw.line(surface, (90, 170, 90), (6, 0), (6, 1), 2)


def _draw_anchor(surface: pygame.Surface) -> None:
    pygame.draw.circle(surface, (210, 120, 160), (9, 9), 7, 2)
    pygame.draw.line(surface, (210, 120, 160), (9, 2), (9, 14), 2)


def _draw_star(surface: pygame.Surface) -> None:
    pygame.draw.polygon(
        surface,
        (120, 210, 255),
        [(7, 0), (9, 5), (14, 7), (9, 9), (7, 14), (5, 9), (0, 7), (5, 5)],
    )


def _draw_slash(surface: pygame.Surface) -> None:
    pygame.draw.polygon(
        surface,
        (200, 90, 90),
        [(2, 15), (15, 2), (28, 15), (15, 28)],
        2,
    )


def _draw_shockwave(surface: pygame.Surface) -> None:
    surface.fill((190, 190, 210))
    pygame.draw.rect(surface, (90, 90, 120), surface.get_rect(), 2)


def _draw_fireball(surface: pygame.Surface) -> None:
    pygame.draw.circle(surface, (255, 140, 60), (7, 5), 5)


def _draw_blast_small(surface: pygame.Surface) -> None:
    pygame.draw.circle(surface, (255, 230, 120), (7, 4), 4)


def _draw_melody(surface: pygame.Surface) -> None:
    pygame.draw.circle(surface, (160, 210, 255), (6, 10), 4)
    pygame.draw.line(surface, (160, 210, 255), (6, 2), (6, 10), 2)
    pygame.draw.line(surface, (160, 210, 255), (6, 2), (12, 0), 2)


def _draw_enemy_pulse(surface: pygame.Surface) -> None:
    pygame.draw.rect(surface, (255, 170, 120), surface.get_rect(), 0)
    pygame.draw.rect(surface, (255, 210, 170), surface.get_rect(), 2)


def main() -> None:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    vfx_dir = os.path.join(base_dir, "Images", "vfx")
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    frame_count = 6
    for name, (size, draw_fn) in _draw_vfx().items():
        first_frame: pygame.Surface | None = None
        for idx in range(frame_count):
            frame = _render_frame(size, draw_fn, idx, frame_count)
            if idx == 0:
                first_frame = frame
            _save(frame, os.path.join(vfx_dir, f"{name}_{idx}.png"))
        if first_frame is not None:
            _save(first_frame, os.path.join(vfx_dir, f"{name}.png"))
    pygame.quit()
    print(f"Special VFX sprites generated in {vfx_dir}")


if __name__ == "__main__":
    main()
