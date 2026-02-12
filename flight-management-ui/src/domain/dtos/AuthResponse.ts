import type { User } from "../models/User";

export interface AuthResponse {
  token: string;
  user: User;
}