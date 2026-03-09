"""Snapshot emitter format and atomic write smoke tests."""

from __future__ import annotations

import json
from types import SimpleNamespace

from hololive_coliseum.playtest_snapshot import SnapshotEmitter


class _Rect:
    def __init__(self, x: int, y: int) -> None:
        self.centerx = x
        self.centery = y


class _FakePlayer:
    def __init__(self) -> None:
        self.health = 80
        self.max_health = 100
        self.rect = _Rect(120, 240)
        self.vx = 2.5
        self.vy = -1.0
        self.currency_manager = SimpleNamespace(get_balance=lambda: 42)
        self.experience_manager = SimpleNamespace(xp=15, level=3)

    def cooldown_status(self, now: int) -> list[dict[str, object]]:
        return [{"name": "Shoot", "remaining_ms": 100, "total_ms": 400}]


def test_snapshot_emitter_writes_required_fields(tmp_path) -> None:
    game = SimpleNamespace(
        state="playing",
        player=_FakePlayer(),
        enemies=[SimpleNamespace(rect=_Rect(150, 250)), SimpleNamespace(rect=_Rect(900, 400))],
        status_manager=SimpleNamespace(
            active_effects=lambda player, now: [{"name": "Burn", "remaining_ms": 500}]
        ),
        reputation_manager=SimpleNamespace(to_dict=lambda: {"Arena": 7}),
        objective_manager=SimpleNamespace(
            objectives={
                "defeat_enemies": SimpleNamespace(progress=2, target=5, rewarded=False)
            }
        ),
    )
    emitter = SnapshotEmitter(game, tmp_path / "session", interval_sec=0.1, max_files=10)
    emitter.tick(frame=12, ticks=5000)
    files = sorted((tmp_path / "session" / "snapshots").glob("snap_*.json"))
    assert files
    payload = json.loads(files[0].read_text(encoding="utf-8"))
    assert payload["frame"] == 12
    assert payload["state"] == "playing"
    assert "player" in payload
    assert "world" in payload
    assert "economy" in payload
    assert "objectives" in payload
    assert "events_summary" in payload
