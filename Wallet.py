from __future__ import annotations

class Wallet():
    """
    Create your own wallet to manage a particular financial purpose. Attributes:
    name (string): Required
    percent (integer): Optional, None if not provided
    balance (integer): Optional, 0 if not provided
    cap (integer): Optional, None if not provided
    """
    
    def __init__(self, name: str, balance: int = 0, percent: int = 0, cap: int = 0):
        self.name = name
        self.percent = percent
        self.balance = balance
        self.cap = cap

    def __repr__(self) -> str:
        return f"Wallet: {self.name} (${self.balance})"

    def __add__(self, value: int) -> Wallet:
        """ Sums the balance when the wallet is on addition operations """
        self.balance += value
        return self
    
    def __sub__(self, value: int) -> Wallet:
        """ Substracts the wallet balance from the value """
        self.balance -= value
        return self