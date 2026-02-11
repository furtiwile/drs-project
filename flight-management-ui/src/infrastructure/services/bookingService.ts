import { apiClient } from '../api/apiClient';
import type { Booking } from '../../domain/models/Booking';
import type { CreateBookingDto } from '../../domain/dtos/FlightDtos';

class BookingService {
  private basePath = '/bookings';

  async createBooking(dto: CreateBookingDto): Promise<Booking> {
    const response = await apiClient.post<Booking>(this.basePath, dto);
    return response.data;
  }

  async getUserBookings(): Promise<Booking[]> {
    const response = await apiClient.get<{bookings: Booking[]}>('/users/bookings');
    return response.data.bookings;
  }

  async cancelBooking(bookingId: number): Promise<void> {
    await apiClient.delete(`${this.basePath}/${bookingId}`);
  }
}

export const bookingService = new BookingService();
