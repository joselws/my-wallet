from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    DEDUCTION = "deduction"
    TRANSFER = "transfer"


@dataclass(frozen=True)
class DeductTransaction:
    date: datetime
    wallet: str
    transaction_type: TransactionType.DEDUCTION
    amount: int
    description: str
    balance_before: int
    balance_after: int


@dataclass(frozen=True)
class TransferTransaction:
    date: datetime
    transaction_type: TransactionType.TRANSFER
    from_wallet_name: str
    to_wallet_name: str
    amount: int
    description: str
    from_wallet_balance_before: int
    from_wallet_balance_after: int
    to_wallet_balance_before: int
    to_wallet_balance_after: int
