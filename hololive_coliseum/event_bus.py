"""Lightweight event bus for internal game telemetry and tooling."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable

EventHandler = Callable[[dict[str, Any]], None]


class EventBus:
    """Simple publish/subscribe dispatcher with low no-subscriber overhead."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
        self._wildcard_handlers: list[EventHandler] = []

    @property
    def has_subscribers(self) -> bool:
        return bool(self._wildcard_handlers) or any(self._handlers.values())

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        if event_type == "*":
            if handler not in self._wildcard_handlers:
                self._wildcard_handlers.append(handler)
            return
        handlers = self._handlers[event_type]
        if handler not in handlers:
            handlers.append(handler)

    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        if event_type == "*":
            if handler in self._wildcard_handlers:
                self._wildcard_handlers.remove(handler)
            return
        handlers = self._handlers.get(event_type)
        if not handlers:
            return
        if handler in handlers:
            handlers.remove(handler)
        if not handlers:
            self._handlers.pop(event_type, None)

    def publish(self, event: dict[str, Any]) -> None:
        if not self.has_subscribers:
            return
        event_type = str(event.get("type", "unknown"))
        envelope = {
            "type": event_type,
            "t": event.get("t"),
            "frame": event.get("frame"),
            "payload": event.get("payload", {}),
        }
        handlers = self._handlers.get(event_type, ())
        for handler in handlers:
            handler(envelope)
        for handler in self._wildcard_handlers:
            handler(envelope)
