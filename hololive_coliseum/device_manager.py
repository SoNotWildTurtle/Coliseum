"""Device capability and settings management."""

class DeviceManager:
    """Handle haptic and motion device details."""

    def __init__(self):
        self.devices = {}

    def register(self, name: str, info: dict) -> None:
        self.devices[name] = info

    def get(self, name: str):
        return self.devices.get(name)
