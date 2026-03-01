"""Launch the game with autoplay enabled for a visible demo run."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hololive_coliseum.game import main


def _set_env(key: str, value: str) -> None:
    os.environ[key] = value


def configure_autoplay(
    *,
    mode: str,
    mmo: bool,
    duration: int | None,
    full: bool,
) -> None:
    """Apply environment flags for a visible autoplay session."""
    os.environ.pop("SDL_VIDEODRIVER", None)
    _set_env("HOLO_AUTOPLAY_VISIBLE", "1")
    _set_env("HOLO_AUTOPLAY", "1")
    _set_env("HOLO_AUTOPLAY_FLOW", "1" if mode == "flow" else "0")
    _set_env("HOLO_AUTOPLAY_EXTENDED", "1")
    _set_env("HOLO_AUTOPLAY_TRACE", "1")
    _set_env("HOLO_AUTOPLAY_TRACE_OVERLAY", "1")
    if full:
        _set_env("HOLO_AUTOPLAY_FULL", "1")
        _set_env("HOLO_AUTOPLAY_LEVELS", "20")
    if mmo:
        _set_env("HOLO_AUTOPLAY_FORCE_MMO", "1")
        _set_env("HOLO_AUTOPLAY_MMO_FAST", "0")
    if duration is not None:
        _set_env("HOLO_AUTOPLAY_DURATION", str(duration))


def main_cli() -> None:
    parser = argparse.ArgumentParser(description="Run a visible autoplay demo.")
    parser.add_argument(
        "--mode",
        choices=("flow", "agent"),
        default="flow",
        help="Autoplay mode to exercise.",
    )
    parser.add_argument(
        "--mmo",
        action="store_true",
        help="Start inside the MMO hub.",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=None,
        help="Optional autoplay duration in milliseconds.",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Play through every chapter for a full autoplay run.",
    )
    args = parser.parse_args()
    configure_autoplay(
        mode=args.mode,
        mmo=args.mmo,
        duration=args.duration,
        full=args.full,
    )
    main()


if __name__ == "__main__":
    main_cli()
