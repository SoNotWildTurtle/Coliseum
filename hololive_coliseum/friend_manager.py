"""Friend list and social invite management."""

class FriendManager:
    """Keep track of friends."""
    def __init__(self):
        self.friends = set()

    def add_friend(self, user: str) -> None:
        self.friends.add(user)

    def remove_friend(self, user: str) -> None:
        self.friends.discard(user)

    def is_friend(self, user: str) -> bool:
        return user in self.friends

    def list_friends(self):
        return sorted(self.friends)
