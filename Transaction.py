from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    DEDUCTION = "deduction"


@dataclass(frozen=True)
class Transaction:
    """
    Each transaction represents a single entry from the transactions.csv file
    """

    date: datetime
    wallet: str
    transaction_type: TransactionType.DEDUCTION
    amount: int
    description: str
    balance_before: int
    balance_after: int

    def __repr__(self) -> str:
        return f"Transaction {self.wallet} ${self.amount} ({self.date}): {self.description}"