"""Replay and analyze telemetry JSONL event logs."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from hololive_coliseum.event_schema import normalize_event, validate_event


def _iter_jsonl_paths(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    return sorted(path for path in input_path.glob("*.jsonl") if path.is_file())


def _write_csv(summary_path: Path, counts: dict[str, int]) -> None:
    csv_path = summary_path.with_suffix(".csv")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["event_type", "count"])
        for key, value in sorted(counts.items()):
            writer.writerow([key, value])


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Replay telemetry JSONL and summarize stats.")
    parser.add_argument("--input", required=True, help="JSONL file or directory")
    parser.add_argument("--output", default=None, help="Summary output JSON path")
    parser.add_argument("--csv", action="store_true", help="Write summary CSV")
    parser.add_argument("--anomaly-threshold-damage", type=float, default=9999.0)
    parser.add_argument("--strict", action="store_true", help="Exit 2 on schema/anomalies")
    parser.add_argument("--filter", default=None, help="Comma-separated event type filter")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    input_path = Path(args.input)
    paths = _iter_jsonl_paths(input_path)
    if not paths:
        raise SystemExit(f"no telemetry JSONL files found under {input_path}")

    if args.output:
        summary_path = Path(args.output)
    else:
        if input_path.is_dir():
            summary_path = input_path / "telemetry_summary.json"
        else:
            summary_path = input_path.with_name("telemetry_summary.json")
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    filter_types = set()
    if args.filter:
        filter_types = {item.strip() for item in args.filter.split(",") if item.strip()}

    event_counts: Counter[str] = Counter()
    totals = {
        "damage": 0.0,
        "hazard_damage": 0.0,
        "heal": 0.0,
        "status_tick": 0.0,
        "currency_delta": 0.0,
        "xp_delta": 0.0,
    }
    top_targets: defaultdict[str, float] = defaultdict(float)
    top_sources: defaultdict[str, float] = defaultdict(float)
    objective_count = 0
    achievement_count = 0
    anomalies: list[dict[str, Any]] = []
    processed = 0

    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, raw in enumerate(handle, start=1):
                raw = raw.strip()
                if not raw:
                    continue
                processed += 1
                try:
                    event = json.loads(raw)
                except json.JSONDecodeError as exc:
                    anomalies.append(
                        {
                            "kind": "json_decode_error",
                            "file": str(path),
                            "line": line_number,
                            "detail": str(exc),
                        }
                    )
                    continue

                envelope = normalize_event(event)
                event_type = str(envelope.get("type", "unknown"))
                if filter_types and event_type not in filter_types:
                    continue
                event_counts[event_type] += 1

                ok, errors = validate_event(envelope, strict=False)
                if not ok:
                    anomalies.append(
                        {
                            "kind": "schema_error",
                            "file": str(path),
                            "line": line_number,
                            "event_type": event_type,
                            "errors": errors,
                        }
                    )

                payload = envelope.get("payload", {})
                if not isinstance(payload, dict):
                    payload = {}

                if event_type in {"damage", "hazard_damage", "heal", "status_tick"}:
                    amount = float(payload.get("amount", 0.0) or 0.0)
                    if not math.isfinite(amount):
                        anomalies.append(
                            {
                                "kind": "invalid_amount",
                                "file": str(path),
                                "line": line_number,
                                "event_type": event_type,
                                "value": payload.get("amount"),
                            }
                        )
                        amount = 0.0
                    totals[event_type] += amount
                    target_id = str(payload.get("target_id", "unknown"))
                    top_targets[target_id] += amount
                    source_id = str(payload.get("attacker_id") or payload.get("source") or "unknown")
                    top_sources[source_id] += amount
                    if event_type in {"damage", "hazard_damage"} and amount > float(
                        args.anomaly_threshold_damage
                    ):
                        anomalies.append(
                            {
                                "kind": "damage_spike",
                                "file": str(path),
                                "line": line_number,
                                "event_type": event_type,
                                "amount": amount,
                            }
                        )
                elif event_type == "currency_delta":
                    delta = float(payload.get("delta", 0.0) or 0.0)
                    totals["currency_delta"] += delta
                    reason = str(payload.get("reason", payload.get("source", "")))
                    if delta < 0 and "spend" not in reason.lower():
                        anomalies.append(
                            {
                                "kind": "unexpected_negative_currency_delta",
                                "file": str(path),
                                "line": line_number,
                                "delta": delta,
                                "reason": reason,
                            }
                        )
                elif event_type == "xp_delta":
                    delta = float(payload.get("delta", 0.0) or 0.0)
                    totals["xp_delta"] += delta
                    if delta < 0:
                        anomalies.append(
                            {
                                "kind": "negative_xp_delta",
                                "file": str(path),
                                "line": line_number,
                                "delta": delta,
                            }
                        )
                elif event_type == "objective_progress":
                    objective_count += 1
                elif event_type == "achievement_unlocked":
                    achievement_count += 1

    summary = {
        "files_processed": [str(path) for path in paths],
        "events_processed": int(processed),
        "event_counts": dict(event_counts),
        "aggregates": {
            "damage_total": float(totals["damage"]),
            "hazard_damage_total": float(totals["hazard_damage"]),
            "heal_total": float(totals["heal"]),
            "status_tick_total": float(totals["status_tick"]),
            "currency_delta_total": float(totals["currency_delta"]),
            "xp_delta_total": float(totals["xp_delta"]),
        },
        "top_targets": [
            {"target_id": key, "amount": float(value)}
            for key, value in sorted(
                top_targets.items(),
                key=lambda item: item[1],
                reverse=True,
            )[:10]
        ],
        "top_sources": [
            {"source": key, "amount": float(value)}
            for key, value in sorted(
                top_sources.items(),
                key=lambda item: item[1],
                reverse=True,
            )[:10]
        ],
        "objective_event_count": int(objective_count),
        "achievement_event_count": int(achievement_count),
        "anomaly_count": len(anomalies),
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    if anomalies:
        anomaly_path = summary_path.with_name("telemetry_anomalies.json")
        anomaly_path.write_text(json.dumps(anomalies, indent=2, sort_keys=True), encoding="utf-8")
    if args.csv:
        _write_csv(summary_path, dict(event_counts))
    print(summary_path)

    if args.strict and anomalies:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
