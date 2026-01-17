import { apiClient } from '../api/apiClient';
import type { User } from '../../domain/models/User';
import type { Role } from '../../domain/enums/Role';

export class UserService {
  async getAllUsers(): Promise<User[]> {
    const response = await apiClient.get<User[]>('/api/v1/users/');
    return response.data;
  }

  async getUserById(userId: number): Promise<User> {
    const response = await apiClient.get<User>(`/api/v1/users/${userId}`);
    return response.data;
  }

  async updateUserRole(userId: number, role: Role): Promise<void> {
    await apiClient.patch(`/api/v1/users/${userId}`, { role });
  }

  async deleteUser(userId: number): Promise<void> {
    await apiClient.delete(`/api/v1/users/${userId}`);
  }

  async deposit(amount: number): Promise<void> {
    await apiClient.patch('/api/v1/users/deposit', { amount });
  }

  async withdraw(amount: number): Promise<void> {
    await apiClient.patch('/api/v1/users/withdraw', { amount });
  }

  async updateProfilePicture(profilePictureBase64: string): Promise<void> {
    await apiClient.patch('/api/v1/users/', { profile_picture: profilePictureBase64 });
  }
}

export const userService = new UserService();
