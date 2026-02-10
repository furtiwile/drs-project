from dataclasses import asdict, dataclass
from typing import Any, Self

@dataclass
class RatingUpdateDTO:
    rating: int | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            rating=data.get('rating')
        )
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)