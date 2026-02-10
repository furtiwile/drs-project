from dataclasses import asdict, dataclass
from typing import Any, Self

@dataclass
class AirportCreateDTO:
    name: str | None
    code: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            name=data.get('name'),
            code=data.get('code')
        )
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
