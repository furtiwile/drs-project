from abc import ABC, abstractmethod
from typing import Optional, Dict
from ..domain.models.flights import Airport, Airline, Flight, Booking


class IAirportRepository(ABC):
    @abstractmethod
    def save_airport(self, airport: Airport) -> Airport:
        pass

    @abstractmethod
    def get_airport_by_id(self, airport_id: int) -> Optional[Airport]:
        pass

    @abstractmethod
    def get_airport_by_code(self, airport_code: str) -> Optional[Airport]:
        pass

    @abstractmethod
    def get_all_airports(self, page: int = 1, per_page: int = 10) -> Dict:
        pass

    @abstractmethod
    def update_airport(self, airport_id: int, data: Dict) -> Optional[Airport]:
        pass

    @abstractmethod
    def delete_airport(self, airport_id: int) -> bool:
        pass


class IAirlineRepository(ABC):
    @abstractmethod
    def save_airline(self, airline: Airline) -> Airline:
        pass

    @abstractmethod
    def get_airline_by_id(self, airline_id: int) -> Optional[Airline]:
        pass

    @abstractmethod
    def get_all_airlines(self, page: int = 1, per_page: int = 10) -> Dict:
        pass

    @abstractmethod
    def update_airline(self, airline_id: int, data: Dict) -> Optional[Airline]:
        pass

    @abstractmethod
    def delete_airline(self, airline_id: int) -> bool:
        pass


class IFlightRepository(ABC):
    @abstractmethod
    def save_flight(self, flight: Flight) -> Flight:
        pass

    @abstractmethod
    def get_flight_by_id(self, flight_id: int) -> Optional[Flight]:
        pass

    @abstractmethod
    def get_all_flights(self, page: int = 1, per_page: int = 10, filters: Optional[Dict] = None) -> Dict:
        pass

    @abstractmethod
    def update_flight(self, flight_id: int, status: str, rejection_reason: Optional[str] = None) -> bool:
        pass

    @abstractmethod
    def get_available_seats(self, flight_id: int) -> int:
        pass

    @abstractmethod
    def delete_flight(self, flight_id: int) -> bool:
        pass


class IBookingRepository(ABC):
    @abstractmethod
    def save_booking(self, booking: Booking) -> Booking:
        pass

    @abstractmethod
    def get_booking_by_id(self, booking_id: int) -> Optional[Booking]:
        pass

    @abstractmethod
    def get_bookings_by_user(self, user_id: int, page: int = 1, per_page: int = 10) -> Dict:
        pass

    @abstractmethod
    def get_all_bookings(self, page: int = 1, per_page: int = 10) -> Dict:
        pass

    @abstractmethod
    def update_booking_rating(self, booking_id: int, rating: int) -> bool:
        pass

    @abstractmethod
    def delete_booking(self, booking_id: int) -> bool:
        pass