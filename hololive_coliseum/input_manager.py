"""Helpers for querying keyboard and controller input bindings."""


class InputManager:
    """Store keyboard and controller bindings and check pressed actions."""

    def __init__(
        self,
        key_bindings: dict[str, int] | None = None,
        controller_bindings: dict[str, int] | None = None,
        joysticks: list | None = None,
        mode: str = "auto",
    ) -> None:
        self.key_bindings = dict(key_bindings or {})
        self.controller_bindings = dict(controller_bindings or {})
        self.joysticks = list(joysticks or [])
        self.mode = mode

    def get(self, action: str) -> int | None:
        return self.key_bindings.get(action)

    def set(self, action: str, key: int) -> None:
        self.key_bindings[action] = key

    def set_button(self, action: str, button: int) -> None:
        self.controller_bindings[action] = button

    def set_mode(self, mode: str) -> None:
        """Update the preferred input device."""
        self.mode = mode

    def pressed(self, action: str, keys) -> bool:
        key = self.key_bindings.get(action)
        if self.mode in {"auto", "keyboard"} and key is not None and keys[key]:
            return True
        btn = self.controller_bindings.get(action)
        if self.mode in {"auto", "controller"} and btn is not None:
            for joy in self.joysticks:
                if joy.get_button(btn):
                    return True
        return False
