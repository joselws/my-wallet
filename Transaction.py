from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Transaction:
    date: datetime
    wallet_name: str
    transaction_type: str
    amount: int
    description: str
    balance_before: int
    balance_after: int


class TransactionHistory:
    pass
