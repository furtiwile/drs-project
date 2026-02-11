import { FlightStatus } from '../enums/FlightStatus';
import type { Airline } from './Airline';
import type { Airport } from './Airport';

export interface Flight {
  flight_id: number;
  flight_name: string;
  airline_id: number;
  airline?: Airline;
  flight_distance_km: number;
  flight_duration: number;
  departure_time: string;
  arrival_time: string;
  departure_airport_id: number;
  departure_airport?: Airport;
  arrival_airport_id: number;
  arrival_airport?: Airport;
  created_by: number;
  price: number;
  total_seats: number;
  available_seats?: number;
  status: FlightStatus;
  rejection_reason?: string;
  approved_by?: number;
  actual_start_time?: string;
  created_at: string;
  updated_at: string;
}
