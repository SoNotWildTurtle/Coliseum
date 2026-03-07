"""Tests for event bus pub/sub behavior."""

from hololive_coliseum.event_bus import EventBus


def test_event_bus_publish_subscribe() -> None:
    bus = EventBus()
    received: list[dict] = []

    def on_damage(event: dict) -> None:
        received.append(event)

    bus.subscribe("damage", on_damage)
    bus.publish({"type": "damage", "t": 10, "frame": 2, "payload": {"amount": 5}})

    assert len(received) == 1
    assert received[0]["type"] == "damage"
    assert received[0]["payload"]["amount"] == 5


def test_event_bus_wildcard_and_unsubscribe() -> None:
    bus = EventBus()
    all_events: list[str] = []

    def on_any(event: dict) -> None:
        all_events.append(str(event["type"]))

    bus.subscribe("*", on_any)
    bus.publish({"type": "xp_delta", "t": 0, "frame": 0, "payload": {"delta": 1}})
    bus.unsubscribe("*", on_any)
    bus.publish({"type": "currency_delta", "t": 0, "frame": 1, "payload": {"delta": 2}})

    assert all_events == ["xp_delta"]


def test_event_bus_publish_no_subscribers_is_noop() -> None:
    bus = EventBus()
    bus.publish({"type": "noop", "t": 1, "frame": 1, "payload": {}})
    assert bus.has_subscribers is False
