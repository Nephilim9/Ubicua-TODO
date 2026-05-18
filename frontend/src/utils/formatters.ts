// Proyecto: SafeHome ESP-NOW | Grupo 4
export const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('es-CO', {
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit', 
    minute: '2-digit'
  }).format(date);
};

export const formatSensorValue = (value: number, type: string): string => {
  if (type === 'MQ135') return `${value.toFixed(1)} ppm`;
  if (type === 'TEMP') return `${value.toFixed(1)} °C`;
  if (type === 'HUMIDITY') return `${value.toFixed(0)} %`;
  return value.toString();
};