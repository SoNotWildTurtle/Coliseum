"""UI state orchestration for screens and overlays."""

class UIManager:
    """Track active UI elements for drawing."""

    def __init__(self):
        self.elements = []

    def add(self, elem) -> None:
        self.elements.append(elem)

    def remove(self, elem) -> None:
        if elem in self.elements:
            self.elements.remove(elem)
