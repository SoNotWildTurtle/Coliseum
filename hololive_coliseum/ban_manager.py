"""Account ban tracking and enforcement."""

class BanManager:
    """Maintain a list of banned users."""

    def __init__(self):
        self.banned = set()

    def ban(self, user: str) -> None:
        self.banned.add(user)

    def unban(self, user: str) -> None:
        self.banned.discard(user)

    def is_banned(self, user: str) -> bool:
        return user in self.banned
