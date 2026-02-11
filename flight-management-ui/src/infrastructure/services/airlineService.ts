import { apiClient } from '../api/apiClient';
import type { Airline } from '../../domain/models/Airline';

class AirlineService {
  private basePath = '/airlines';

  async getAllAirlines(): Promise<Airline[]> {
    const response = await apiClient.get<{airlines: Airline[]}>(this.basePath);
    return response.data.airlines;
  }

  async getAirlineById(id: number): Promise<Airline> {
    const response = await apiClient.get<Airline>(`${this.basePath}/${id}`);
    return response.data;
  }
}

export const airlineService = new AirlineService();
