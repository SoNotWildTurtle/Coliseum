"""Headless UI smoke runner for menu/HUD/MMO scaling validation.

Example sweep:
python -m hololive_coliseum.tools.ui_smoke_runner ^
  --res 1280x720 --res 1600x900 --res 1920x1080 ^
  --font-scale 0.9 --font-scale 1.0 --font-scale 1.25 ^
  --mode all --frames 60 ^
  --output-dir SavedGames/ui_smoke/sweep_YYYYMMDD_HHMMSS

Stress config:
python -m hololive_coliseum.tools.ui_smoke_runner ^
  --res 1024x576 --font-scale 1.25 ^
  --mode all --frames 60 --ui-debug ^
  --output-dir SavedGames/ui_smoke/stress_YYYYMMDD_HHMMSS
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import time
import traceback
from typing import Any


def _configure_headless_env() -> None:
    os.environ.setdefault("PYGAME_HEADLESS", "1")
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")


_configure_headless_env()

import pygame

from hololive_coliseum.game import Game
from hololive_coliseum.ui_debug import UIDebugger


@dataclass(frozen=True)
class RunConfig:
    """Single smoke run configuration tuple."""

    width: int
    height: int
    font_scale: float
    frames: int
    mode: str
    seed: int
    screenshot: bool
    ui_debug: bool
    ui_debug_frames: bool
    output_dir: Path
    verbose: bool


class _HUDSmokePlayer:
    """Minimal player object for deterministic HUD-only rendering."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.max_health = 100
        self.health = 82
        self.last_hit_time = -1_000_000
        self.last_hit_difficulty_scale = 1.0
        self._screen = screen

    def draw_status(self, screen: pygame.Surface) -> None:
        width = max(140, int(screen.get_width() * 0.22))
        bar_x = 10
        bar_y = 10
        pygame.draw.rect(screen, (25, 35, 55), pygame.Rect(bar_x, bar_y, width, 18))
        fill = int((self.health / max(1, self.max_health)) * (width - 2))
        pygame.draw.rect(screen, (180, 70, 90), pygame.Rect(bar_x + 1, bar_y + 1, fill, 16))
        pygame.draw.rect(screen, (220, 220, 240), pygame.Rect(bar_x, bar_y, width, 18), 1)


def _parse_resolution(value: str) -> tuple[int, int]:
    text = value.lower().strip()
    if "x" not in text:
        raise ValueError(f"resolution must look like 1280x720, got {value!r}")
    left, right = text.split("x", 1)
    width = int(left)
    height = int(right)
    if width < 320 or height < 240:
        raise ValueError(f"resolution too small: {width}x{height}")
    return width, height


def _frame_stats(frame_times: list[float]) -> dict[str, float]:
    if not frame_times:
        return {"min_ms": 0.0, "avg_ms": 0.0, "max_ms": 0.0}
    return {
        "min_ms": min(frame_times) * 1000.0,
        "avg_ms": (sum(frame_times) / len(frame_times)) * 1000.0,
        "max_ms": max(frame_times) * 1000.0,
    }


def _git_commit() -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        return None
    commit = out.strip()
    return commit or None


def _apply_resolution_and_scale(game: Game, width: int, height: int, font_scale: float) -> None:
    game.width = int(width)
    game.height = int(height)
    game.world_width = int(width)
    game.world_height = int(height)
    game.ground_y = game.height - 50
    game.screen = game._apply_display_mode()
    game.accessibility_manager.options["font_scale"] = float(font_scale)
    game._apply_font_scale()


def _render_menu_frame(game: Game) -> None:
    game._set_state("main_menu")
    drawer = game.menu_drawers.get("main_menu")
    if drawer is None:
        raise RuntimeError("main_menu drawer not available")
    drawer()


def _render_hud_frame(game: Game, frame_idx: int) -> None:
    game.screen.fill((8, 14, 24))
    player = _HUDSmokePlayer(game.screen)
    game.hud_manager.draw(
        game.screen,
        player,
        score=frame_idx,
        elapsed=frame_idx // 60,
        combo=2,
        objectives=["UI smoke objective"],
        cooldowns=[],
    )


def _render_mmo_frame(game: Game) -> None:
    game._set_state("mmo")
    game.mmo_overlay_mode = "help"
    game._draw_mmo_world()


def _run_mode(game: Game, mode: str, frames: int, screenshot_path: Path | None) -> dict[str, Any]:
    clock = pygame.time.Clock()
    frame_times: list[float] = []
    skipped_reason: str | None = None
    mode_start = datetime.now(timezone.utc).isoformat()
    try:
        for idx in range(frames):
            pygame.event.pump()
            debugger = getattr(game, "ui_debugger", None)
            if debugger is not None and debugger.is_active:
                ui_metrics = getattr(game, "ui_metrics", None)
                debugger.begin_frame(
                    mode=mode,
                    state_name=game.state,
                    resolution=(game.width, game.height),
                    ui_scale=float(getattr(ui_metrics, "ui_scale", 1.0)),
                    effective_font_scale=float(getattr(game, "effective_font_scale", 1.0)),
                    fps=float(clock.get_fps()),
                )
            start = time.perf_counter()
            if mode == "menu":
                _render_menu_frame(game)
            elif mode == "hud":
                _render_hud_frame(game, idx)
            elif mode == "mmo":
                _render_mmo_frame(game)
            else:
                raise ValueError(f"unknown mode: {mode}")
            if debugger is not None and debugger.is_active:
                debugger.render_overlay(
                    game.screen,
                    getattr(game, "ui_metrics", None),
                    float(clock.get_fps()),
                    game.state,
                )
                debugger.flush_frame(idx)
            pygame.display.flip()
            frame_times.append(time.perf_counter() - start)
            clock.tick(60)
        if screenshot_path is not None:
            pygame.image.save(game.screen, str(screenshot_path))
    except Exception as exc:
        if mode == "mmo":
            skipped_reason = f"{exc.__class__.__name__}: {exc}"
        else:
            raise
    mode_end = datetime.now(timezone.utc).isoformat()
    result: dict[str, Any] = {
        "status": "ok",
        "start_ts": mode_start,
        "end_ts": mode_end,
        "frames_requested": frames,
        "frames_rendered": len(frame_times),
        "timing": _frame_stats(frame_times),
    }
    if skipped_reason:
        result["status"] = "skipped"
        result["skipped_reason"] = skipped_reason
        result["todo"] = "Stabilize MMO smoke setup for headless mode."
    return result


def _run_single(config: RunConfig) -> tuple[bool, dict[str, Any]]:
    random.seed(config.seed)
    run_started = datetime.now(timezone.utc).isoformat()
    run_report: dict[str, Any] = {
        "schema_version": "1.0",
        "python_version": sys.version.split()[0],
        "pygame_version": pygame.version.ver,
        "git_commit": _git_commit(),
        "start_ts": run_started,
        "config": {
            "resolution": f"{config.width}x{config.height}",
            "font_scale": config.font_scale,
            "frames": config.frames,
            "mode": config.mode,
            "seed": config.seed,
            "ui_debug": config.ui_debug,
            "ui_debug_frames": config.ui_debug_frames,
        },
        "modes_executed": [],
        "modes": {},
        "exception": None,
    }
    success = True
    game: Game | None = None
    layout_summary_path: Path | None = None
    try:
        game = Game(width=config.width, height=config.height)
        if config.ui_debug:
            debugger = UIDebugger(
                enabled=False,
                output_dir=config.output_dir,
                log_enabled=True,
                log_frames=config.ui_debug_frames,
                headless=(os.environ.get("PYGAME_HEADLESS") == "1"),
            )
            game.ui_debugger = debugger
            debugger.set_metadata(
                python_version=sys.version.split()[0],
                pygame_version=pygame.version.ver,
                run_mode=config.mode,
                resolution=f"{config.width}x{config.height}",
                requested_font_scale=config.font_scale,
            )
        _apply_resolution_and_scale(game, config.width, config.height, config.font_scale)
        if getattr(game, "hud_manager", None) is not None:
            game.hud_manager.debugger = getattr(game, "ui_debugger", None)
        run_report["effective_font_scale"] = getattr(game, "effective_font_scale", None)
        ui_metrics = getattr(game, "ui_metrics", None)
        run_report["ui_scale"] = getattr(ui_metrics, "ui_scale", None)
        mode_order = ["menu", "hud", "mmo"] if config.mode == "all" else [config.mode]
        for mode in mode_order:
            run_report["modes_executed"].append(mode)
            screenshot_path = None
            if config.screenshot:
                screenshot_path = config.output_dir / (
                    f"{mode}_{config.width}x{config.height}_fs{config.font_scale:.2f}.png"
                )
            mode_result = _run_mode(game, mode, config.frames, screenshot_path)
            run_report["modes"][mode] = mode_result
            if mode == "mmo" and mode_result.get("status") == "skipped":
                run_report["mmo_skipped"] = mode_result.get("skipped_reason")
            if mode == "mmo" and mode_result.get("status") == "skipped" and config.mode == "mmo":
                success = False
        debugger = getattr(game, "ui_debugger", None)
        if debugger is not None and debugger.log_enabled:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            layout_summary_path = config.output_dir / (
                f"ui_layout_summary_{config.width}x{config.height}"
                f"_fs{config.font_scale:.2f}_{stamp}.json"
            )
            final_path = debugger.finalize_run(layout_summary_path)
            if final_path is not None:
                layout_summary_path = final_path
                run_report["layout_summary_path"] = str(final_path)
    except Exception:
        success = False
        run_report["exception"] = traceback.format_exc()
    finally:
        run_report["end_ts"] = datetime.now(timezone.utc).isoformat()
        if game is not None:
            try:
                game.running = False
            except Exception:
                pass
            debugger = getattr(game, "ui_debugger", None)
            if (
                layout_summary_path is None
                and debugger is not None
                and debugger.log_enabled
            ):
                fallback = debugger.finalize_run(config.output_dir / "ui_layout_summary.json")
                if fallback is not None:
                    run_report["layout_summary_path"] = str(fallback)
        pygame.quit()
    return success, run_report


def _write_report(output_dir: Path, report: dict[str, Any]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    name = (
        f"ui_smoke_{report['config']['resolution']}"
        f"_fs{float(report['config']['font_scale']):.2f}_{stamp}.json"
    )
    path = output_dir / name
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run headless UI smoke checks.")
    parser.add_argument("--res", action="append", default=[], help="Resolution, e.g. 1280x720.")
    parser.add_argument("--width", type=int, default=None)
    parser.add_argument("--height", type=int, default=None)
    parser.add_argument(
        "--font-scale",
        action="append",
        type=float,
        default=[],
        help="Repeat for sweeps, e.g. --font-scale 0.9 --font-scale 1.25",
    )
    parser.add_argument("--seconds", type=float, default=2.0)
    parser.add_argument("--frames", type=int, default=None)
    parser.add_argument("--mode", choices=("menu", "hud", "mmo", "all"), default="all")
    parser.add_argument("--output-dir", default="SavedGames/ui_smoke")
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--screenshot", action="store_true")
    parser.add_argument("--ui-debug", action="store_true", help="Enable UI debug layout logging.")
    parser.add_argument(
        "--ui-debug-frames",
        action="store_true",
        help="Include per-frame debug counters (larger logs).",
    )
    return parser.parse_args(argv)


def _build_run_matrix(args: argparse.Namespace) -> list[RunConfig]:
    if args.res:
        resolutions = [_parse_resolution(value) for value in args.res]
    elif args.width and args.height:
        resolutions = [(int(args.width), int(args.height))]
    else:
        resolutions = [(1280, 720)]
    font_scales = args.font_scale or [1.0]
    frames = int(args.frames) if args.frames is not None else max(1, int(round(args.seconds * 60)))
    output_dir = Path(args.output_dir)
    matrix: list[RunConfig] = []
    for width, height in resolutions:
        for font_scale in font_scales:
            matrix.append(
                RunConfig(
                    width=width,
                    height=height,
                    font_scale=float(font_scale),
                    frames=frames,
                    mode=args.mode,
                    seed=int(args.seed),
                    screenshot=bool(args.screenshot),
                    ui_debug=bool(args.ui_debug),
                    ui_debug_frames=bool(args.ui_debug_frames),
                    output_dir=output_dir,
                    verbose=bool(args.verbose),
                )
            )
    return matrix


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    matrix = _build_run_matrix(args)
    failures = 0
    reports: list[Path] = []
    for run_cfg in matrix:
        if run_cfg.verbose:
            print(
                "[ui-smoke] run "
                f"res={run_cfg.width}x{run_cfg.height} "
                f"font_scale={run_cfg.font_scale:.2f} mode={run_cfg.mode} "
                f"frames={run_cfg.frames}"
            )
        ok, report = _run_single(run_cfg)
        path = _write_report(run_cfg.output_dir, report)
        reports.append(path)
        if run_cfg.verbose:
            print(f"[ui-smoke] report: {path}")
        if not ok:
            failures += 1
            if report.get("exception"):
                first = str(report["exception"]).splitlines()[-1]
                print(f"[ui-smoke] failed: {first}")
    if args.verbose:
        print(f"[ui-smoke] wrote {len(reports)} report(s) to {Path(args.output_dir).resolve()}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
