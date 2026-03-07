"""Tests for canonical event schema validation."""

from hololive_coliseum.event_schema import validate_event


def test_damage_event_schema_passes() -> None:
    event = {
        "type": "damage",
        "t": 123,
        "frame": 10,
        "payload": {
            "target_id": "Enemy",
            "amount": 12.0,
            "attacker_id": "Player",
        },
    }
    ok, errors = validate_event(event)
    assert ok is True
    assert errors == []


def test_missing_required_payload_key_fails() -> None:
    event = {
        "type": "damage",
        "t": 123,
        "frame": 10,
        "payload": {
            "amount": 12.0,
        },
    }
    ok, errors = validate_event(event)
    assert ok is False
    assert any("target_id" in err for err in errors)
