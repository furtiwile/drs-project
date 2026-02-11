import { apiClient } from '../api/apiClient';
import type { Flight } from '../../domain/models/Flight';
import type {
  CreateFlightDto,
  UpdateFlightDto,
  ApproveFlightDto,
  RejectFlightDto,
} from '../../domain/dtos/FlightDtos';
import { FlightStatus } from '../../domain/enums/FlightStatus';

interface PaginatedResponse<T> {
  flights: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
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

  async createFlight(dto: CreateFlightDto): Promise<Flight> {
    const response = await apiClient.post<Flight>(this.basePath, dto);
    return response.data;
  }

  async getAllFlights(params?: GetFlightsParams): Promise<PaginatedResponse<Flight>> {
    const response = await apiClient.get<PaginatedResponse<Flight>>(this.basePath, {
      params,
    });
    return response.data;
  }

  async getFlightsByTab(tab: string): Promise<Flight[]> {
    const response = await apiClient.get<{flights: Flight[]}>(`${this.basePath}/tabs/${tab}`);
    return response.data.flights;
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
}

export const flightService = new FlightService();
