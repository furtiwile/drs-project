import React, { createContext, useContext, useEffect } from 'react';
import type { ReactNode } from 'react';
import { socketService } from '../../infrastructure/websocket/socketService';
import { useAuth } from './AuthContext';

interface SocketContextValue {
  isConnected: boolean;
  joinFlightRoom: (flightId: number) => void;
  leaveFlightRoom: (flightId: number) => void;
  on: (event: string, handler: Function) => void;
  off: (event: string) => void;
}

const SocketContext = createContext<SocketContextValue | undefined>(undefined);

export const useSocket = () => {
  const context = useContext(SocketContext);
  if (!context) {
    throw new Error('useSocket must be used within SocketProvider');
  }
  return context;
};

interface SocketProviderProps {
  children: ReactNode;
}

export const SocketProvider: React.FC<SocketProviderProps> = ({ children }) => {
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      const token = localStorage.getItem('token');
      if (token) {
        socketService.connect(token, user.user_id, user.role);

        return () => {
          socketService.disconnect();
        };
      }
    }
  }, [user]);

  const value: SocketContextValue = {
    isConnected: socketService.isConnected(),
    joinFlightRoom: socketService.joinFlightRoom.bind(socketService),
    leaveFlightRoom: socketService.leaveFlightRoom.bind(socketService),
    on: socketService.on.bind(socketService),
    off: socketService.off.bind(socketService),
  };

  return (
    <SocketContext.Provider value={value}>{children}</SocketContext.Provider>
  );
};
