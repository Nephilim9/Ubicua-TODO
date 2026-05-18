import { io, Socket } from 'socket.io-client';

class WebSocketService {
  private socket: Socket | null = null;

  connect() {
    this.socket = io('http://localhost:8000', {
      path: '/ws/socket.io',
      transports: ['websocket'],
    });

    this.socket.on('connect', () => console.log('WebSocket Conectado'));
  }

  onAlert(callback: (alert: any) => void) {
    this.socket?.on('alert_triggered', callback);
  }

  disconnect() {
    this.socket?.disconnect();
  }
}

export const wsService = new WebSocketService();