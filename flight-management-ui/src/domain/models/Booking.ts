import type { Flight } from './Flight';

export interface Booking {
  id: number;
  user_id: number;
  flight_id: number;
  flight?: Flight;
  created_at: string;
}
