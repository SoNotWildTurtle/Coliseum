"""Telemetry collection and event batching."""

class TelemetryManager:
    """Collect gameplay analytics for heatmaps and metrics."""

    def __init__(self):
        self.events = []

    def log(self, event: str) -> None:
        self.events.append(event)

    def get_events(self):
        return list(self.events)
