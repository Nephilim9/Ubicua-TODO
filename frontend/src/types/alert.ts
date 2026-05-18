export interface Alert {
  id: number;
  sensor_id: number | null;
  device_id: number | null;
  threshold_id: number | null;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  message: string;
  value_triggered: number;
  status: 'active' | 'acknowledged' | 'resolved';
  created_at: string;
  resolved_at: string | null;
  resolved_by: string | null;
  // legacy alias kept for compatibility
  timestamp?: string;
}