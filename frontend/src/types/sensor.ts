export interface Sensor {
  id: number;
  name: string;
  sensor_type: 'MQ135' | 'TEMP' | 'HUMIDITY' | 'PIR';
  device_id: number;
  last_value?: number;
  status: 'active' | 'inactive';
}