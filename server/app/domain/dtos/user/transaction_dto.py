from dataclasses import dataclass

@dataclass
class TransactionDTO:
    amount: float

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            amount=data.get('amount')
        )