"""Currency balances and transaction helpers."""

class CurrencyManager:
    """Track balances of in-game currency."""
    def __init__(self, starting: int = 0):
        self.balance = starting

    def add(self, amount: int) -> int:
        self.balance += amount
        return self.balance

    def spend(self, amount: int) -> bool:
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self) -> int:
        return self.balance
