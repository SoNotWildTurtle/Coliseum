"""Tournament scheduling and bracket helpers."""

class TournamentManager:
    """Schedule brackets for competitions."""

    def __init__(self):
        self.brackets = []

    def create_bracket(self, players: list) -> None:
        self.brackets.append(list(players))

    def list_brackets(self):
        return list(self.brackets)
