"""Snapshot-style hooks for VFX regression coverage."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame = pytest.importorskip("pygame")

from hololive_coliseum.player import (
    GuraPlayer,
    WatsonPlayer,
    FaunaPlayer,
    MikoPlayer,
    Enemy,
)


def _hash_surface(surface: pygame.Surface) -> str:
    data = pygame.image.tobytes(surface, "RGBA")
    return hashlib.sha256(data).hexdigest()


def _capture_hash(effect, monkeypatch, ticks: int = 1000) -> str:
    monkeypatch.setattr("pygame.time.get_ticks", lambda: ticks)
    effect.update()
    return _hash_surface(effect.image)


def _compute_snapshots(monkeypatch) -> dict[str, str]:
    pygame.init()
    pygame.display.set_mode((1, 1))

    snapshots: dict[str, str] = {}

    gura = GuraPlayer(0, 0)
    gura.mana = gura.max_mana
    proj = gura.special_attack(0)
    snapshots["gura_trident"] = _capture_hash(proj, monkeypatch)

    watson = WatsonPlayer(0, 0)
    watson.mana = watson.max_mana
    effect = watson.special_attack(0)
    snapshots["watson_dash"] = _capture_hash(effect, monkeypatch)

    fauna = FaunaPlayer(0, 0)
    fauna.mana = fauna.max_mana
    zone = fauna.special_attack(0)
    snapshots["fauna_grove"] = _capture_hash(zone, monkeypatch)

    miko = MikoPlayer(0, 0)
    miko.mana = miko.max_mana
    beam = miko.special_attack(0)
    snapshots["miko_beam"] = _capture_hash(beam, monkeypatch)

    enemy = Enemy(0, 0)
    enemy.mana = enemy.max_mana
    pulse = enemy.special_attack(0)
    snapshots["enemy_pulse"] = _capture_hash(pulse, monkeypatch)

    pygame.quit()
    return snapshots


def test_vfx_snapshot_hashes(monkeypatch):
    snapshots = _compute_snapshots(monkeypatch)
    assert snapshots

    path = Path(__file__).with_name("vfx_snapshots.json")
    if os.environ.get("VFX_SNAPSHOT_WRITE") == "1":
        path.write_text(json.dumps(snapshots, indent=2, sort_keys=True))

    if not path.exists():
        pytest.skip("No snapshot file present; set VFX_SNAPSHOT_WRITE=1 to create.")

    stored = json.loads(path.read_text())
    for key, value in snapshots.items():
        assert stored.get(key) == value
