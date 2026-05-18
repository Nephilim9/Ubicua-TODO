export const APP_CONFIG = {
  PROJECT_NAME: 'SafeHome ESP-NOW',
  VERSION: '1.0.0',
  AUTHORS: ['Adriana Bonilla', 'Eduar Ramos', 'Grupo 4'],
  API_BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  WS_URL: import.meta.env.VITE_WS_URL || 'http://localhost:8000',
};

export const SEVERITY_COLORS = {
  CRITICAL: 'text-red-600 bg-red-100 border-red-200',
  HIGH: 'text-orange-600 bg-orange-100 border-orange-200',
  MEDIUM: 'text-yellow-600 bg-yellow-100 border-yellow-200',
  LOW: 'text-green-600 bg-green-100 border-green-200',
};

export const SENSOR_TYPES = {
  MQ135: 'Calidad de Aire / Gas',
  PIR: 'Presencia / Movimiento',
  TEMP: 'Temperatura',
  HUMIDITY: 'Humedad Relativa',
};