import axios from 'axios';
import type { Booking } from '../../domain/models/Booking';
import type { CreateBookingDto } from '../../domain/dtos/FlightDtos';

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://metro.proxy.rlwy.net:12922";
const API_PREFIX = import.meta.env.VITE_API_PREFIX || '/api/v1';
const API_URL = `${API_BASE_URL}${API_PREFIX}`;

class BookingService {
  private basePath = '/bookings';

  /**
   * Create a new booking using user-id header
   */
  async createBooking(dto: CreateBookingDto): Promise<void> {
    const userId = this.getUserId();
    await axios.post<Booking>(
      `${API_URL}${this.basePath}`,
      dto,
      {
        headers: {
          'user-id': userId,
          'Content-Type': 'application/json',
        },
      }
    );
  }

  /**
   * Get all bookings for the current user
   * Endpoint: GET /users/{user_id}/bookings
   */
  async getUserBookings(): Promise<Booking[]> {
    const userId = this.getUserId();
    const response = await axios.get<{ bookings: Booking[] }>(
      `${API_URL}/users/${userId}/bookings`,
      {
        headers: { 'user-id': userId },
      }
    );
    return response.data.bookings;
  }

  /**
   * Cancel a booking using user-id header
   */
  async cancelBooking(bookingId: number): Promise<void> {
    const userId = this.getUserId();
    await axios.delete(`${API_URL}${this.basePath}/${bookingId}`, {
      headers: { 'user-id': userId },
    });
  }

  /**
   * Helper method to get user ID from localStorage
   */
  private getUserId(): string {
    const userJson = localStorage.getItem('user');
    if (!userJson) {
      throw new Error('User not authenticated');
    }
    const user = JSON.parse(userJson);
    return user.user_id?.toString();
  }
}

export const bookingService = new BookingService();

