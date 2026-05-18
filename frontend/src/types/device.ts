export interface Device {
  id: number;
  name: string;
  mac_address: string;
  device_type: 'MASTER' | 'SLAVE';
  status: 'online' | 'offline';
  last_seen?: string; // ISO format string
  ip_address?: string; // Solo para el Master si está en WiFi
}

export interface DeviceLog {
  id: number;
  device_id: number;
  event: string;
  level: 'INFO' | 'WARNING' | 'ERROR';
  timestamp: string;
}