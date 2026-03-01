"""Raid setup and encounter coordination."""

class RaidManager:
    """Manage raid lockouts and groups."""

    def __init__(self):
        self.groups = []

    def create_group(self, players: list) -> None:
        self.groups.append(list(players))

    def list_groups(self):
        return list(self.groups)
