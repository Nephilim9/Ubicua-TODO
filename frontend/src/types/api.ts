// Proyecto: SafeHome ESP-NOW | Grupo 4
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface ApiError {
  detail: string | { msg: string; type: string }[];
}

export interface DashboardStats {
  active_sensors: number;
  alerts_today: number;
  nodes_online: number;
  nodes_total: number;
  system_health: number; // 0-100
}