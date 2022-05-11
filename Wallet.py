from __future__ import annotations
from typing import Union, Type

class Wallet():
    """
    Create your own wallet to manage a particular financial purpose. Attributes:
    name (string): Required
    percent (integer): Optional, None if not provided
    balance (integer): Optional, 0 if not provided
    cap (integer): Optional, None if not provided
    """
    
    def __init__(self, name: str, percent: Union[int, None] = None, balance: int = 0, cap: Union[int, None] = None):
        self.name = name
        self.percent = percent
        self.balance = balance
        self.cap = cap

    def __repr__(self):
        return f"{self.name}: ${self.balance} ({self.percent}%)"

    def __add__(self, value: int) -> Wallet:
        """ Sums the balance when the wallet is on addition operations """
        self.balance += value
        return self
    
    def __sub__(self, value: int) -> Wallet:
        """ Substracts the wallet balance from the value """
        self.balance -= value
        return self