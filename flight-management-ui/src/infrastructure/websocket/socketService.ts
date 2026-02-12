import { io, Socket } from 'socket.io-client';

const SOCKET_URL = import.meta.env.VITE_SOCKET_URL || 'http://localhost:5001';

class SocketService {
  private socket: Socket | null = null;
  private listeners: Map<string, Function> = new Map();
  
  connect(token: string, userId: number, role: string): void {
    if (this.socket?.connected) {
      return;
    }
    
    console.log('Connecting to WebSocket at:', SOCKET_URL);
    
    this.socket = io(SOCKET_URL, {
      auth: {
        token,
      },
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    });

    this.socket.on('connect', () => {
      console.log('WebSocket connected');

      // Join appropriate rooms based on role
      if (role === 'ADMINISTRATOR') {
        this.socket?.emit('join_admin_room', { user_id: userId, role });
      } else if (role === 'MANAGER') {
        this.socket?.emit('join_manager_room', { user_id: userId, role });
      } else if (role === 'USER') {
        this.socket?.emit('join_user_room', { user_id: userId, role });
      }
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    this.socket.on('connected', (data) => {
      console.log('WebSocket handshake:', data);
    });
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.listeners.clear();
    }
  }

  on(event: string, handler: Function): void {
    if (this.socket) {
      this.socket.on(event, (data: any) => handler(data));
      this.listeners.set(event, handler);
    }
  }

  off(event: string): void {
    if (this.socket) {
      this.socket.off(event);
      this.listeners.delete(event);
    }
  }

  joinFlightRoom(flightId: number): void {
    if (this.socket) {
      this.socket.emit('join_flight_room', { flight_id: flightId });
    }
  }

  leaveFlightRoom(flightId: number): void {
    if (this.socket) {
      this.socket.emit('leave_flight_room', { flight_id: flightId });
    }
  }

  isConnected(): boolean {
    return this.socket?.connected || false;
  }
}

export const socketService = new SocketService();
