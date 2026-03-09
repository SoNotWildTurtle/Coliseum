"""JSONL event telemetry sink for opt-in dev and headless runs."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .event_schema import normalize_event, validate_event
from .save_manager import SAVE_DIR


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


class TelemetryLogger:
    """Subscribe to an event bus and write filtered events to JSONL."""

    def __init__(
        self,
        event_bus,
        *,
        output_dir: str | os.PathLike[str] | None = None,
        filter_types: set[str] | None = None,
        flush_every: int = 25,
        validate_schema: bool = False,
        strict_schema: bool = False,
    ) -> None:
        base = Path(output_dir) if output_dir else Path(SAVE_DIR) / "telemetry"
        base.mkdir(parents=True, exist_ok=True)
        self.path = base / f"events_{_utc_stamp()}.jsonl"
        self._handle = self.path.open("w", encoding="utf-8")
        self._event_bus = event_bus
        self._filter_types = set(filter_types or ())
        self._flush_every = max(1, int(flush_every))
        self._count = 0
        self._validate_schema = bool(validate_schema)
        self._strict_schema = bool(strict_schema)
        event_bus.subscribe("*", self.on_event)

    @classmethod
    def from_env(
        cls,
        event_bus,
        *,
        output_dir: str | os.PathLike[str] | None = None,
    ) -> "TelemetryLogger | None":
        if os.environ.get("HOLO_TELEMETRY", "0") != "1":
            return None
        raw = os.environ.get("HOLO_TELEMETRY_FILTER", "").strip()
        filter_types = {item.strip() for item in raw.split(",") if item.strip()}
        validate_schema = os.environ.get("HOLO_TELEMETRY_VALIDATE", "0") == "1"
        strict_schema = os.environ.get("HOLO_TELEMETRY_STRICT", "0") == "1"
        return cls(
            event_bus,
            output_dir=output_dir,
            filter_types=filter_types,
            validate_schema=validate_schema,
            strict_schema=strict_schema,
        )

    def on_event(self, event: dict[str, Any]) -> None:
        envelope = normalize_event(event)
        event_type = str(envelope.get("type", "unknown"))
        if self._filter_types and event_type not in self._filter_types:
            return
        if self._validate_schema:
            ok, errors = validate_event(envelope, strict=False)
            if not ok:
                if self._strict_schema:
                    raise RuntimeError(
                        f"telemetry schema validation failed for {event_type}: {errors}"
                    )
                payload = envelope.get("payload", {})
                if not isinstance(payload, dict):
                    payload = {}
                payload["_schema_errors"] = list(errors)
                envelope["payload"] = payload
        self._handle.write(json.dumps(envelope, sort_keys=True) + "\n")
        self._count += 1
        if self._count % self._flush_every == 0:
            self._handle.flush()

    def close(self) -> None:
        self._event_bus.unsubscribe("*", self.on_event)
        self._handle.flush()
        self._handle.close()
