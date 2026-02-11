export interface CreateFlightDto {
  flight_name: string;
  airline_id: number;
  departure_airport_id: number;
  arrival_airport_id: number;
  departure_time: string;
  arrival_time: string;
  price: number;
  total_seats: number;
  flight_distance_km: number;
  flight_duration: number;
}

export interface UpdateFlightDto {
  flight_name?: string;
  airline_id?: number;
  departure_airport_id?: number;
  arrival_airport_id?: number;
  departure_time?: string;
  arrival_time?: string;
  price?: number;
  total_seats?: number;
  flight_distance_km?: number;
  flight_duration?: number;
}

export interface ApproveFlightDto {
  status: 'APPROVED';
}

export interface RejectFlightDto {
  status: 'REJECTED';
  rejection_reason: string;
}

export interface CreateBookingDto {
  flight_id: number;
}
