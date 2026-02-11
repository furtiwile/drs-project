import { apiClient } from '../api/apiClient';
import type { Booking } from '../../domain/models/Booking';
import type { CreateBookingDto } from '../../domain/dtos/FlightDtos';

class BookingService {
  private basePath = '/api/bookings';

  async createBooking(dto: CreateBookingDto): Promise<Booking> {
    const response = await apiClient.post<Booking>(this.basePath, dto);
    return response.data;
  }

  async getUserBookings(userId: number): Promise<Booking[]> {
    const response = await apiClient.get<Booking[]>(`/api/users/${userId}/bookings`);
    return response.data;
  }

  async cancelBooking(bookingId: number): Promise<void> {
    await apiClient.delete(`${this.basePath}/${bookingId}`);
  }
}

export const bookingService = new BookingService();
