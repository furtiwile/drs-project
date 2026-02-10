from dataclasses import asdict, dataclass
from typing import Any, Self

@dataclass
class AirlineCreateDTO:
    name: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(name=data.get('name'))
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)