import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';
import { Alert } from '../types/alert';

export const useAlerts = () => {
  const queryClient = useQueryClient();

  // Obtener alertas
  const query = useQuery<Alert[]>({
    queryKey: ['alerts'],
    queryFn: async () => {
      const { data } = await api.get('/alerts/');
      return data;
    },
  });

  // Mutación para resolver alertas
  const resolveMutation = useMutation({
    mutationFn: async (alertId: number) => {
      await api.patch(`/alerts/${alertId}/resolve`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    },
  });

  return { ...query, resolveAlert: resolveMutation.mutate };
};