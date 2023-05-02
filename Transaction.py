from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    DEDUCTION = "deduction"


@dataclass(frozen=True)
class Transaction:
    date: datetime
    wallet: str
    transaction_type: TransactionType.DEDUCTION
    amount: int
    description: str
    balance_before: int
    balance_after: int
