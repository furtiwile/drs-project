from dataclasses import dataclass
from typing import Any, Self

@dataclass
class TransactionDTO:
    amount: float | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            amount=data.get('amount')
        )