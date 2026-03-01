"""Party creation, membership, and invites."""

class PartyManager:
    """Handle party invites and membership."""

    def __init__(self):
        self.parties = {}

    def create_party(self, host: str) -> None:
        self.parties[host] = [host]

    def join(self, host: str, member: str) -> None:
        if host in self.parties:
            self.parties[host].append(member)

    def get_party(self, host: str):
        return self.parties.get(host)
