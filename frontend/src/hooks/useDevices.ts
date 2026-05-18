import { useQuery } from '@tanstack/react-query';
import api from '../services/api';
import { Device } from '../types/device';

export const useDevices = () => {
  return useQuery<Device[]>({
    queryKey: ['devices'],
    queryFn: async () => {
      const { data } = await api.get('/devices/');
      return data;
    },
    refetchInterval: 10000, // Cada 10 segundos para ver si siguen online
  });
};