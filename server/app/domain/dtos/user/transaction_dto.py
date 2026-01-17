from dataclasses import dataclass
from typing import Self

@dataclass
class TransactionDTO:
    amount: float | None

    @classmethod
    def from_dict(cls, data: dict[str, float | None]) -> Self:
        return cls(
            amount=data.get('amount')
        )