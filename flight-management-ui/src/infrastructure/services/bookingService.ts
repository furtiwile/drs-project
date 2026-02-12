import axios from 'axios';
import type { Booking } from '../../domain/models/Booking';
import type { CreateBookingDto } from '../../domain/dtos/FlightDtos';

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://metro.proxy.rlwy.net:12922";
const API_PREFIX = import.meta.env.VITE_API_PREFIX || '/api/v1';
const API_URL = `${API_BASE_URL}${API_PREFIX}`;

class BookingService {
  private basePath = '/bookings';

  /**
   * Create a new booking using Bearer token authentication
   */
  async createBooking(dto: CreateBookingDto): Promise<void> {
    const token = this.getAuthToken();
    await axios.post<Booking>(
      `${API_URL}${this.basePath}`,
      dto,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );
  }

  /**
   * Get all bookings for the current user
   * Endpoint: GET /users/bookings
   * Uses Bearer token authentication - user ID is extracted from token on server
   */
  async getUserBookings(): Promise<Booking[]> {
    const token = this.getAuthToken();
    const response = await axios.get<{ bookings: Booking[] }>(
      `${API_URL}/users/bookings`,
      {
        headers: { 
          'Authorization': `Bearer ${token}`,
        },
      }
    );
    return response.data.bookings;
  }

  /**
   * Cancel a booking using Bearer token authentication
   */
  async cancelBooking(bookingId: number): Promise<void> {
    const token = this.getAuthToken();
    await axios.delete(`${API_URL}${this.basePath}/${bookingId}`, {
      headers: { 
        'Authorization': `Bearer ${token}`,
      },
    });
  }

  /**
   * Helper method to get authentication token from localStorage
   */
  private getAuthToken(): string {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('User not authenticated');
    }
    return token;
  }
}

export const bookingService = new BookingService();

