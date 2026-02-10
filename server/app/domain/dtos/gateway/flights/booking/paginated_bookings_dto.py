from dataclasses import dataclass
from typing import Any, List, Self

from app.domain.dtos.gateway.flights.booking.booking_dto import BookingDTO

@dataclass
class PaginatedBookingsDTO:
    bookings: List[BookingDTO]
    page: int
    per_page: int
    total: int
    pages: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            bookings=[BookingDTO.from_dict(a) for a in data.get("bookings", [])],
            page=data.get("page", 1),
            per_page=data.get("per_page", 10),
            total=data.get("total", 0),
            pages=data.get("pages", 1)
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "bookings": [a.to_dict() for a in self.bookings],
            "page": self.page,
            "per_page": self.per_page,
            "total": self.total,
            "pages": self.pages
        }