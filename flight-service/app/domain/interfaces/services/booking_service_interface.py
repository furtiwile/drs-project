from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.flights import Booking
from app.domain.dtos.booking_dto import BookingCreateDTO, BookingCreateDTOReturn
from app.domain.interfaces.repositories.ibooking_repository import BookingPaginationResult
from ...types.task_types import TaskStatus

class BookingServiceInterface(ABC):
    @abstractmethod
    def get_booking(self, booking_id: int) -> Optional[Booking]:
        """Retrieve a booking by ID."""

    @abstractmethod
    def get_user_bookings(self, user_id: int, page: int, per_page: int) -> BookingPaginationResult:
        """Retrieve all bookings for a user with pagination."""

    @abstractmethod
    def get_all_bookings(self, page: int, per_page: int) -> BookingPaginationResult:
        """Retrieve all bookings with pagination."""

    @abstractmethod
    def delete_booking(self, booking_id: int) -> bool:
        """Delete a booking by ID."""

    @abstractmethod
    def create_booking(self, user_id: int, booking_data: BookingCreateDTO) -> Optional[BookingCreateDTOReturn]:
        """
        Asynchronously creates a booking and returns a task ID for tracking.
        
        Args:
            user_id (int): The ID of the user making the booking.
            booking_data (BookingCreateDTO): Validated booking creation data.
        
        Returns:
            Optional[BookingCreateDTOReturn]: Booking creation details if successful, None otherwise.
        """

    @abstractmethod
    def get_booking_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """
        Retrieves the status of an asynchronous booking task.
        
        Args:
            task_id (str): The task ID to check.
        
        Returns:
            Optional[TaskStatus]: Task status details if found, None otherwise.
        """
