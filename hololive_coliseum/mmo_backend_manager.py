"""SQLite-backed storage for MMO hub state, players, and regions."""
from __future__ import annotations

import json
import os
import sqlite3
import time
from typing import Any, Iterable

from . import save_manager


class MMOBackendManager:
    """Persist MMO hub data and snapshots in a lightweight SQLite database."""

    def __init__(self, path: str | None = None) -> None:
        save_dir = save_manager.SAVE_DIR
        os.makedirs(save_dir, exist_ok=True)
        self.path = path or os.path.join(save_dir, "mmo_state.db")
        self._conn = sqlite3.connect(self.path)
        self._conn.row_factory = sqlite3.Row
        self._configure()
        self._migrate()

    def _configure(self) -> None:
        cur = self._conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL")
        cur.execute("PRAGMA synchronous=NORMAL")
        cur.execute("PRAGMA temp_store=MEMORY")
        cur.execute("PRAGMA cache_size=-20000")
        self._conn.commit()

    def _migrate(self) -> None:
        cur = self._conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS players (
                player_id TEXT PRIMARY KEY,
                pos_x REAL,
                pos_y REAL,
                updated_at REAL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS regions (
                name TEXT PRIMARY KEY,
                seed TEXT,
                biome TEXT,
                payload TEXT,
                updated_at REAL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS snapshots (
                seq INTEGER PRIMARY KEY,
                state TEXT,
                crc32 TEXT,
                sha256 TEXT,
                created_at REAL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS plans (
                plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                summary TEXT,
                payload TEXT,
                created_at REAL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS outposts (
                region TEXT PRIMARY KEY,
                level INTEGER,
                status TEXT,
                payload TEXT,
                updated_at REAL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS routes (
                route_id INTEGER PRIMARY KEY AUTOINCREMENT,
                origin TEXT,
                destination TEXT,
                status TEXT,
                payload TEXT,
                updated_at REAL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS operations (
                op_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                region TEXT,
                status TEXT,
                payload TEXT,
                updated_at REAL
            )
            """
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS snapshots_created_at ON snapshots(created_at)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS plans_created_at ON plans(created_at)"  
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS outposts_updated_at ON outposts(updated_at)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS routes_updated_at ON routes(updated_at)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS operations_updated_at ON operations(updated_at)"
        )
        self._conn.commit()

    def upsert_player(self, player_id: str, pos: tuple[float, float]) -> None:
        """Persist a player position snapshot."""
        self._conn.execute(
            """
            INSERT INTO players (player_id, pos_x, pos_y, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(player_id) DO UPDATE SET
                pos_x=excluded.pos_x,
                pos_y=excluded.pos_y,
                updated_at=excluded.updated_at
            """,
            (player_id, float(pos[0]), float(pos[1]), time.time()),
        )
        self._conn.commit()

    def upsert_regions(self, regions: Iterable[dict[str, Any]]) -> None:
        """Store region metadata for MMO previews."""
        cur = self._conn.cursor()
        timestamp = time.time()
        for region in regions:
            name = str(region.get("name", "region"))
            payload = json.dumps(region, separators=(",", ":"))
            cur.execute(
                """
                INSERT INTO regions (name, seed, biome, payload, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    seed=excluded.seed,
                    biome=excluded.biome,
                    payload=excluded.payload,
                    updated_at=excluded.updated_at
                """,
                (
                    name,
                    str(region.get("seed", "")),
                    str(region.get("biome", "")),
                    payload,
                    timestamp,
                ),
            )
        self._conn.commit()

    def record_snapshot(
        self, sequence: int, state: dict[str, Any], digests: dict[str, str]
    ) -> None:
        """Persist a verified shared-state snapshot."""
        payload = json.dumps(state, separators=(",", ":"))
        self._conn.execute(
            """
            INSERT OR REPLACE INTO snapshots (seq, state, crc32, sha256, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                int(sequence),
                payload,
                str(digests.get("crc32", "")),
                str(digests.get("sha256", "")),
                time.time(),
            ),
        )
        self._conn.commit()

    def prune_snapshots(self, keep: int = 200) -> None:
        """Keep only the newest ``keep`` snapshot rows."""
        keep = max(0, int(keep))
        if keep <= 0:
            return
        cur = self._conn.cursor()
        cur.execute(
            """
            DELETE FROM snapshots
            WHERE seq NOT IN (
                SELECT seq FROM snapshots
                ORDER BY created_at DESC
                LIMIT ?
            )
            """,
            (keep,),
        )
        self._conn.commit()

    def latest_snapshot(self) -> dict[str, Any] | None:
        """Return the most recent snapshot payload."""
        row = self._conn.execute(
            "SELECT seq, state, crc32, sha256 FROM snapshots ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
        if row is None:
            return None
        try:
            state = json.loads(row["state"])
        except (json.JSONDecodeError, TypeError):
            state = {}
        return {
            "seq": row["seq"],
            "state": state,
            "crc32": row["crc32"],
            "sha256": row["sha256"],
        }

    def record_plan(self, summary: dict[str, Any], plan: dict[str, Any]) -> None:
        """Persist an auto-dev plan snapshot."""
        payload = json.dumps(plan, separators=(",", ":"))
        summary_payload = json.dumps(summary, separators=(",", ":"))
        self._conn.execute(
            """
            INSERT INTO plans (summary, payload, created_at)
            VALUES (?, ?, ?)
            """,
            (summary_payload, payload, time.time()),
        )
        self._conn.commit()

    def latest_plan(self) -> dict[str, Any] | None:
        """Return the most recent auto-dev plan summary."""
        row = self._conn.execute(
            "SELECT summary, payload FROM plans ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
        if row is None:
            return None
        try:
            summary = json.loads(row["summary"])
        except (json.JSONDecodeError, TypeError):
            summary = {}
        try:
            payload = json.loads(row["payload"])
        except (json.JSONDecodeError, TypeError):
            payload = {}
        return {"summary": summary, "payload": payload}

    def upsert_outpost(self, outpost: dict[str, Any]) -> None:
        """Persist or update an MMO outpost entry."""
        region = str(outpost.get("region", "region"))
        payload = json.dumps(outpost, separators=(",", ":"))
        self._conn.execute(
            """
            INSERT INTO outposts (region, level, status, payload, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(region) DO UPDATE SET
                level=excluded.level,
                status=excluded.status,
                payload=excluded.payload,
                updated_at=excluded.updated_at
            """,
            (
                region,
                int(outpost.get("level", 1)),
                str(outpost.get("status", "operational")),
                payload,
                time.time(),
            ),
        )
        self._conn.commit()

    def record_route(self, route: dict[str, Any]) -> None:
        """Persist a new trade route entry."""
        payload = json.dumps(route, separators=(",", ":"))
        self._conn.execute(
            """
            INSERT INTO routes (origin, destination, status, payload, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(route.get("origin", "")),
                str(route.get("destination", "")),
                str(route.get("status", "active")),
                payload,
                time.time(),
            ),
        )
        self._conn.commit()

    def record_operation(self, operation: dict[str, Any]) -> None:
        """Persist a new operation entry."""
        payload = json.dumps(operation, separators=(",", ":"))
        self._conn.execute(
            """
            INSERT INTO operations (name, region, status, payload, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(operation.get("name", "operation")),
                str(operation.get("region", "")),
                str(operation.get("status", "active")),
                payload,
                time.time(),
            ),
        )
        self._conn.commit()

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()
