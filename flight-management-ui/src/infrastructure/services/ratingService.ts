// Rating Service following Clean Architecture and SOLID principles
// Single Responsibility: Managing all rating/comment related API calls
// Uses user-id header as defined by server (not Bearer token)

import axios from 'axios';
import type {
  CreateRatingDto,
  UpdateRatingDto,
  RatingResponse,
  RatingWithUserInfo,
  RatingsListResponse,
} from '../../domain/dtos/RatingDtos';

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://metro.proxy.rlwy.net:12922";
const API_PREFIX = import.meta.env.VITE_API_PREFIX || '/api/v1';
const API_URL = `${API_BASE_URL}${API_PREFIX}`;

/**
 * Service for managing ratings/comments
 * Follows Interface Segregation Principle - only exposes rating-related methods
 * Uses user-id header for authentication as per server specification
 */
class RatingService {
  private basePath = '/ratings';

  /**
   * Create a new rating for a flight
   * Uses user-id header from authenticated user
   */
  async createRating(dto: CreateRatingDto): Promise<RatingResponse> {
    const userId = this.getUserId();
    const token = localStorage.getItem('token');
    
    const response = await axios.post<RatingResponse>(
      `${API_URL}${this.basePath}`,
      dto,
      {
        headers: {
          'user-id': userId,
          'Authorization': token ? `Bearer ${token}` : '',
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  }

  /**
   * Get all ratings for the current user
   * Endpoint: GET /users/{user_id}/ratings
   */
  async getUserRatings(page: number = 1, per_page: number = 10): Promise<RatingsListResponse> {
    const userId = this.getUserId();
    const token = localStorage.getItem('token');
    
    const response = await axios.get<RatingsListResponse>(
      `${API_URL}/users/${userId}/ratings`,
      {
        params: { page, per_page },
        headers: { 
          'user-id': userId,
          'Authorization': token ? `Bearer ${token}` : '',
        },
      }
    );
    return response.data;
  }

  /**
   * Get all ratings (fetches all and filters by flight on frontend)
   * This gets all ratings for display, filtered by flight_id in component
   */
  async getAllRatings(page: number = 1, per_page: number = 10): Promise<RatingsListResponse> {
    const userId = this.getUserId();
    const token = localStorage.getItem('token');
    
    const response = await axios.get<RatingsListResponse>(
      `${API_URL}${this.basePath}`,
      {
        params: { page, per_page },
        headers: { 
          'user-id': userId,
          'Authorization': token ? `Bearer ${token}` : '',
        },
      }
    );
    return response.data;
  }

  /**
   * Get all ratings for a specific flight
   * Fetches all ratings and filters by flight_id on the client side
   * (No server-side flight filtering available)
   */
  async getFlightRatings(flightId: number, page: number = 1, per_page: number = 10): Promise<RatingsListResponse> {
    // Get all ratings and filter by flight_id
    const userId = this.getUserId();
    const token = localStorage.getItem('token');
    
    const response = await axios.get<RatingsListResponse>(
      `${API_URL}${this.basePath}`,
      {
        params: { page, per_page },
        headers: { 
          'user-id': userId,
          'Authorization': token ? `Bearer ${token}` : '',
        },
      }
    );
    
    // Filter ratings for the specific flight
    const filteredRatings = response.data.ratings?.filter(r => r.flight_id === flightId) || [];
    
    return {
      ...response.data,
      ratings: filteredRatings,
    };
  }

  /**
   * Update a rating (only if user is the author)
   */
  async updateRating(ratingId: number, dto: UpdateRatingDto): Promise<RatingResponse> {
    const userId = this.getUserId();
    const token = localStorage.getItem('token');
    
    const response = await axios.put<RatingResponse>(
      `${API_URL}${this.basePath}/${ratingId}`,
      dto,
      {
        headers: {
          'user-id': userId,
          'Authorization': token ? `Bearer ${token}` : '',
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  }

  /**
   * Delete a rating (only if user is the author or admin)
   */
  async deleteRating(ratingId: number): Promise<void> {
    const userId = this.getUserId();
    const token = localStorage.getItem('token');
    
    await axios.delete(`${API_URL}${this.basePath}/${ratingId}`, {
      headers: { 
        'user-id': userId,
        'Authorization': token ? `Bearer ${token}` : '',
      },
    });
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

  /**
   * Get a specific rating by ID
   */
  async getRatingById(ratingId: number): Promise<RatingWithUserInfo> {
    const userId = this.getUserId();
    const token = localStorage.getItem('token');
    
    const response = await axios.get<RatingWithUserInfo>(
      `${API_URL}${this.basePath}/${ratingId}`,
      {
        headers: { 
          'user-id': userId,
          'Authorization': token ? `Bearer ${token}` : '',
        },
      }
    );
    return response.data;
  }
}

// Export singleton instance following Singleton pattern
export const ratingService = new RatingService();
