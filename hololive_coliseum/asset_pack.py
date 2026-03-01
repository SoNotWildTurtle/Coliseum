"""Resolve asset pack paths and folders for sprite loading."""
from __future__ import annotations

import os


def resolve_asset_dir() -> str:
    """Pick the asset pack directory from env or default locations."""
    env_path = os.environ.get("HOLO_ASSET_PACK", "").strip()
    if env_path:
        return env_path
    base_dir = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(base_dir, ".."))
    candidate = os.path.join(repo_root, "asset_pack")
    if os.path.isdir(candidate):
        return candidate
    return os.path.join(repo_root, "Images")


def ensure_asset_dirs(asset_dir: str) -> None:
    """Ensure expected asset pack subfolders exist."""
    for name in ("characters", "enemies", "specials", "effects"):
        os.makedirs(os.path.join(asset_dir, name), exist_ok=True)


def asset_path(
    asset_dir: str,
    category: str,
    base: str,
    direction: str | None = None,
) -> str:
    """Return a preferred asset path for the category and base name."""
    filename = base
    if direction:
        filename = f"{base}_{direction}.png"
    if not filename.endswith(".png"):
        filename = f"{filename}.png"
    candidates = [
        os.path.join(asset_dir, category, filename),
        os.path.join(asset_dir, filename),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return candidates[0]
