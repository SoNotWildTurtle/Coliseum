"""Support ticket and escalation helpers."""

class SupportManager:
    """Track support tickets from players."""

    def __init__(self) -> None:
        self.tickets: dict[int, str] = {}
        self.next_id = 1

    def submit(self, message: str) -> int:
        ticket_id = self.next_id
        self.next_id += 1
        self.tickets[ticket_id] = message
        return ticket_id

    def get(self, ticket_id: int) -> str | None:
        return self.tickets.get(ticket_id)
