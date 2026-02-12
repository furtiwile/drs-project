// DTOs for Rating/Comment operations following SOLID principles
// Using Single Responsibility Principle - each DTO has one purpose

export interface CreateRatingDto {
  flight_id: number;
  rating: number; // 1-5
}

export interface UpdateRatingDto {
  rating: number; // 1-5
}

export interface RatingResponse {
  id: number;
  user_id: number;
  flight_id: number;
  rating: number;
  created_at: string;
}

export interface RatingWithUserInfo extends RatingResponse {
  user_name: string;
  user_email: string;
  flight_name: string;
}

export interface RatingsListResponse {
  ratings: RatingResponse[];
  page: number;
  per_page: number;
  total: number;
  pages: number;
}

export interface AdminRatingsListResponse {
  ratings: RatingWithUserInfo[];
  page: number;
  per_page: number;
  total: number;
  pages: number;
}
