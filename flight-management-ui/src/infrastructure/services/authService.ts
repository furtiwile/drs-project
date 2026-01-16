import { apiClient } from '../api/apiClient';
import type { LoginDto } from '../../domain/dtos/LoginDto';
import type { RegisterDto } from '../../domain/dtos/RegisterDto';
import type { AuthResponse } from '../../domain/dtos/AuthResponse';

export class AuthService {
  async login(credentials: LoginDto): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/api/v1/auth/login', credentials);
    return response.data;
  }

  async register(data: RegisterDto): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/api/v1/auth/register', data);
    return response.data;
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    apiClient.post<AuthResponse>("/api/v1/auth/logout");
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}

export const authService = new AuthService();
