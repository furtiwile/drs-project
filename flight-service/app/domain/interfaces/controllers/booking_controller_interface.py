from abc import ABC, abstractmethod
from typing import Any


class BookingControllerInterface(ABC):
    @abstractmethod
    def create_booking(self) -> Any:
        pass

    @abstractmethod
    def get_booking(self, booking_id: int) -> Any:
        pass

    @abstractmethod
    def get_user_bookings(self, user_id: int) -> Any:
        pass

    @abstractmethod
    def get_all_bookings(self) -> Any:
        pass

    @abstractmethod
    def delete_booking(self, booking_id: int) -> Any:
        pass