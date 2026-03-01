"""Cheat detection heuristics and enforcement."""

class CheatDetectionManager:
    """Detect basic suspicious activity such as impossible speed."""

    def __init__(self):
        self.flags = []

    def check_speed(self, speed: float, max_speed: float) -> bool:
        if speed > max_speed:
            self.flags.append("speed")
            return True
        return False
