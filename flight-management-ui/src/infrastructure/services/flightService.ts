import axios from 'axios';
import { apiClient } from '../api/apiClient';
import type { Flight } from '../../domain/models/Flight';
import type {
  CreateFlightDto,
  UpdateFlightDto,
  ApproveFlightDto,
  RejectFlightDto,
} from '../../domain/dtos/FlightDtos';
import { FlightStatus } from '../../domain/enums/FlightStatus';

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://metro.proxy.rlwy.net:12922";
const API_PREFIX = import.meta.env.VITE_API_PREFIX || '/api/v1';
const API_URL = `${API_BASE_URL}${API_PREFIX}`;

interface PaginatedResponse<T> {
  flights: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
  tab?: string;
}

interface GetFlightsParams {
  page?: number;
  per_page?: number;
  status?: FlightStatus;
  airline_id?: number;
  departure_airport_id?: number;
  arrival_airport_id?: number;
  min_price?: number;
  max_price?: number;
  departure_date?: string;
}

class FlightService {
  private basePath = 'flights';

  /**
   * Create a new flight using user-id header
   */
  async createFlight(dto: CreateFlightDto): Promise<Flight> {
    const userId = this.getUserId();
    const response = await axios.post<Flight>(
      `${API_URL}/${this.basePath}`,
      dto,
      {
        headers: {
          'user-id': userId,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  }

  async getAllFlights(params?: GetFlightsParams): Promise<PaginatedResponse<Flight>> {
    const response = await apiClient.get<PaginatedResponse<Flight>>(this.basePath, {
      params,
    });
    return response.data;
  }

  async getFlightsByTab(
    tab: string, 
    params?: GetFlightsParams
  ): Promise<PaginatedResponse<Flight>> {
    const response = await apiClient.get<PaginatedResponse<Flight>>(
      `${this.basePath}/tabs/${tab}`, 
      { params }
    );
    return response.data;
  }

  async getFlightById(id: number): Promise<Flight> {
    const response = await apiClient.get<Flight>(`${this.basePath}/${id}`);
    return response.data;
  }

  async updateFlight(id: number, dto: UpdateFlightDto): Promise<Flight> {
    const response = await apiClient.patch<Flight>(`${this.basePath}/${id}`, dto);
    return response.data;
  }

  async approveFlight(id: number): Promise<Flight> {
    const dto: ApproveFlightDto = { status: 'APPROVED' };
    const response = await apiClient.patch<Flight>(
      `${this.basePath}/${id}/status`,
      dto
    );
    return response.data;
  }

  async rejectFlight(id: number, reason: string): Promise<Flight> {
    const dto: RejectFlightDto = { status: 'REJECTED', rejection_reason: reason };
    const response = await apiClient.patch<Flight>(
      `${this.basePath}/${id}/status`,
      dto
    );
    return response.data;
  }

  async cancelFlight(id: number): Promise<Flight> {
    const response = await apiClient.post<Flight>(`${this.basePath}/${id}/cancel`, {});
    return response.data;
  }

  async deleteFlight(id: number): Promise<void> {
    await apiClient.delete(`${this.basePath}/${id}`);
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

export const flightService = new FlightService();

