from dataclasses import asdict, dataclass
from typing import Any, Self

@dataclass
class RatingCreateDTO:
    flight_id: int | None
    rating: int | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            flight_id=data.get('flight_id'),
            rating=data.get('rating')
        )
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)