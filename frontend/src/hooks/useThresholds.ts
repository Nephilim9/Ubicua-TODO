import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';

export const useThresholds = () => {
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ['thresholds'],
    queryFn: async () => {
      const { data } = await api.get('/thresholds/');
      return data;
    },
  });

  const updateMutation = useMutation({
    mutationFn: async (newConfig: any) => {
      await api.post('/thresholds/', newConfig);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['thresholds'] });
    },
  });

  return { ...query, updateThreshold: updateMutation.mutate };
};