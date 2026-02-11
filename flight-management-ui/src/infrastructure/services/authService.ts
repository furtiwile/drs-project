import { apiClient } from '../api/apiClient';
import type { LoginDto } from '../../domain/dtos/LoginDto';
import type { RegisterDto } from '../../domain/dtos/RegisterDto';
import type { AuthResponse } from '../../domain/dtos/AuthResponse';

export class AuthService {
  async login(credentials: LoginDto): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/login', credentials);
    return response.data;
  }

  async register(data: RegisterDto): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/register', data);
    return response.data;
  }

  async logout(): Promise<void> {
    await apiClient.post<AuthResponse>("/auth/logout");
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}

export const authService = new AuthService();
