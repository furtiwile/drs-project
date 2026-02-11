import type { Flight } from './Flight';

export interface Booking {
  booking_id: number;
  user_id: number;
  flight_id: number;
  flight?: Flight;
  purchased_at: string;
  created_at: string;
  updated_at: string;
}
