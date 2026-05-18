export interface Alert {
  id: number;
  sensor_id: number;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  message: string;
  value_triggered: number;
  timestamp: string;
  is_resolved: boolean;
}