import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import type { User } from '../../domain/models/User';
import type { LoginDto } from '../../domain/dtos/LoginDto';
import type { RegisterDto } from '../../domain/dtos/RegisterDto';
import { authService } from '../../infrastructure/services/authService';
import { userService } from '../../infrastructure/services/userService';

interface AuthContextType {
  user: User | null;
  login: (credentials: LoginDto) => Promise<void>;
  register: (data: RegisterDto) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  isAuthenticated: boolean;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = async (credentials: LoginDto) => {
    const response = await authService.login(credentials);
    localStorage.setItem('token', response.token);
    localStorage.setItem('user', JSON.stringify(response.user));
    setUser(response.user);
  };

  const register = async (data: RegisterDto) => {
    const response = await authService.register(data);
    localStorage.setItem('token', response.token);
    localStorage.setItem('user', JSON.stringify(response.user));
    setUser(response.user);
  };

  const logout = async () => {
    try{
      await authService.logout();
      setUser(null);
    } catch(error) {
      console.error('Error logging out:', error);
    }
  };

  const refreshUser = async () => {
    if (!user) return;
    try {
      const updatedUser = await userService.getUserById(user.user_id);
      localStorage.setItem('user', JSON.stringify(updatedUser));
      setUser(updatedUser);
    } catch {
      console.error('Failed to refresh user data');
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        register,
        logout,
        refreshUser,
        isAuthenticated: !!user,
        loading
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
