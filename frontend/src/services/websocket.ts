import { TrainData } from '../types';

type MessageHandler = (data: { type: string; trains?: TrainData[] }) => void;

class WebSocketClient {
  private socket: WebSocket | null = null;
  private url: string = 'ws://127.0.0.1:8000/ws/live-feed';
  private listeners: MessageHandler[] = [];
  private isConnected: boolean = false;
  private reconnectTimer: any = null;

  public connect(onStatusChange?: (connected: boolean) => void) {
    if (typeof window === 'undefined') return;

    try {
      this.socket = new WebSocket(this.url);

      this.socket.onopen = () => {
        this.isConnected = true;
        if (onStatusChange) onStatusChange(true);
        console.log('RailPulse AI WebSocket connected.');
      };

      this.socket.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data);
          this.listeners.forEach((fn) => fn(parsed));
        } catch (e) {
          console.error('Failed to parse WebSocket message', e);
        }
      };

      this.socket.onclose = () => {
        this.isConnected = false;
        if (onStatusChange) onStatusChange(false);
        console.log('RailPulse AI WebSocket closed. Retrying in 4s...');
        this.reconnectTimer = setTimeout(() => this.connect(onStatusChange), 4000);
      };

      this.socket.onerror = (err) => {
        console.warn('WebSocket error', err);
        if (this.socket) this.socket.close();
      };
    } catch (e) {
      console.error('WebSocket connection initialization error', e);
    }
  }

  public subscribe(handler: MessageHandler) {
    this.listeners.push(handler);
    return () => {
      this.listeners = this.listeners.filter((h) => h !== handler);
    };
  }

  public disconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    this.isConnected = false;
  }

  public getStatus() {
    return this.isConnected;
  }
}

export const wsClient = new WebSocketClient();
