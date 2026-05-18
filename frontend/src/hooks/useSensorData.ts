import { useQuery } from '@tanstack/react-query';
import api from '../services/api';
import { Sensor } from '../types/sensor';

export const useSensorData = () => {
  return useQuery<Sensor[]>({
    queryKey: ['sensors'],
    queryFn: async () => {
      const { data } = await api.get('/sensors/');
      return data;
    },
    refetchInterval: 5000, // Polling cada 5 segundos como respaldo
  });
};