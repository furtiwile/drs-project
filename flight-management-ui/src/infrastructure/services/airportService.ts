import { apiClient } from '../api/apiClient';
import type { Airport } from '../../domain/models/Airport';

class AirportService {
  private basePath = '/api/airports';

  async getAllAirports(): Promise<Airport[]> {
    const response = await apiClient.get<Airport[]>(this.basePath);
    return response.data;
  }

  async getAirportById(id: number): Promise<Airport> {
    const response = await apiClient.get<Airport>(`${this.basePath}/${id}`);
    return response.data;
  }
}

export const airportService = new AirportService();
