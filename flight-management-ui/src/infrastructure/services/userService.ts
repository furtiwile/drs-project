import { apiClient } from '../api/apiClient';
import type { User } from '../../domain/models/User';
import type { Role } from '../../domain/enums/Role';

export class UserService {
  async getAllUsers(): Promise<User[]> {
    const response = await apiClient.get<User[]>('users/');
    return response.data;
  }

  async getUserById(userId: number): Promise<User> {
    const response = await apiClient.get<User>(`/users/${userId}`);
    return response.data;
  }

  async updateUserRole(userId: number, role: Role): Promise<void> {
    await apiClient.patch(`/users/${userId}`, { role });
  }

  async updateProfile(formData: any): Promise<void> {
    await apiClient.patch('/users/', formData);
  }

  async deleteUser(userId: number): Promise<void> {
    await apiClient.delete(`/users/${userId}`);
  }

  async deposit(amount: number): Promise<void> {
    await apiClient.patch('/users/deposit', { amount });
  }

  async withdraw(amount: number): Promise<void> {
    await apiClient.patch('/users/withdraw', { amount });
  }

  async updateProfilePicture(profilePictureBase64: string): Promise<void> {
    await apiClient.patch('/users/', { profile_picture: profilePictureBase64 });
  }
}

export const userService = new UserService();
