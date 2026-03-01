"""Geographic metadata helpers for world regions."""

class GeoManager:
    """Track GPS coordinates for AR-style events."""

    def __init__(self):
        self.points = []

    def update(self, lat: float, lon: float) -> None:
        self.points.append((lat, lon))

    def last(self):
        return self.points[-1] if self.points else None
