"""Guild membership, roles, and reputation tracking."""

class GuildManager:
    """Track multiple guilds and their member ranks."""

    def __init__(self) -> None:
        self.guilds: dict[str, dict[str, str]] = {}

    def create(self, name: str, owner: str) -> None:
        """Create a guild with ``owner`` as leader."""
        self.guilds[name] = {owner: "leader"}

    def delete(self, name: str) -> None:
        """Remove a guild entirely."""
        self.guilds.pop(name, None)

    def add_member(self, guild: str, user: str, rank: str = "member") -> None:
        """Add ``user`` to ``guild`` with the given ``rank``."""
        if guild in self.guilds:
            self.guilds[guild][user] = rank

    def remove_member(self, guild: str, user: str) -> None:
        """Remove ``user`` from ``guild``."""
        if guild in self.guilds:
            self.guilds[guild].pop(user, None)

    def set_rank(self, guild: str, user: str, rank: str) -> None:
        """Update ``user``'s rank inside ``guild``."""
        if guild in self.guilds and user in self.guilds[guild]:
            self.guilds[guild][user] = rank

    def get_rank(self, guild: str, user: str):
        """Return ``user``'s rank in ``guild`` if present."""
        return self.guilds.get(guild, {}).get(user)

    def list_members(self, guild: str):
        """List members of ``guild`` mapped to their ranks."""
        return dict(self.guilds.get(guild, {}))

    def list_guilds(self):
        """Return the names of all guilds."""
        return sorted(self.guilds.keys())
