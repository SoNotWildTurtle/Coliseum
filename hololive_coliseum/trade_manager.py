"""Trade requests and market interactions."""

class TradeManager:
    """Handle simple item trades between players."""

    def __init__(self) -> None:
        self._pending: dict[int, tuple[str, str, str]] = {}
        self._next_id: int = 1

    def propose_trade(self, from_player: str, to_player: str, item: str) -> int:
        tid = self._next_id
        self._next_id += 1
        self._pending[tid] = (from_player, to_player, item)
        return tid

    def accept_trade(self, trade_id: int):
        """Accept and remove a pending trade, returning its info."""
        return self._pending.pop(trade_id, None)
