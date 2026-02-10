from dataclasses import dataclass
from typing import Any, List, Self

from app.domain.dtos.gateway.flights.airport.airport_dto import AirportDTO

@dataclass
class PaginatedAirportsDTO:
    airports: List[AirportDTO]
    page: int
    per_page: int
    total: int
    pages: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            airports=[AirportDTO.from_dict(a) for a in data.get("airports", [])],
            page=data.get("page", 1),
            per_page=data.get("per_page", 10),
            total=data.get("total", 0),
            pages=data.get("pages", 1)
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "airports": [a.to_dict() for a in self.airports],
            "page": self.page,
            "per_page": self.per_page,
            "total": self.total,
            "pages": self.pages
        }