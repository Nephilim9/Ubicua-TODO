import { useQuery } from '@tanstack/react-query';
import { Activity, ShieldAlert, Signal, Wind } from 'lucide-react';
import api from '../../services/api';

interface Summary {
  active_sensors: number;
  active_alerts: number;
  devices_online: number;
  devices_total: number;
  air_quality_pct: number;
  system_status: string;
}

const KPICard = ({
  title, value, icon, color, loading,
}: {
  title: string; value: string | number; icon: React.ReactNode; color: string; loading?: boolean;
}) => (
  <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
    <div className={`p-3 rounded-lg ${color} text-white shrink-0`}>{icon}</div>
    <div className="min-w-0">
      <p className="text-sm text-slate-500 font-medium">{title}</p>
      {loading ? (
        <div className="h-7 w-16 bg-slate-200 rounded animate-pulse mt-1" />
      ) : (
        <p className="text-2xl font-bold text-slate-800">{value}</p>
      )}
    </div>
  </div>
);

const KPIGrid = () => {
  const { data, isLoading } = useQuery<Summary>({
    queryKey: ['dashboard-summary'],
    queryFn: async () => (await api.get('/dashboard/summary')).data,
    refetchInterval: 10_000,
  });

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <KPICard
        title="Sensores Activos"
        value={data?.active_sensors ?? '—'}
        icon={<Activity size={24} />}
        color="bg-blue-500"
        loading={isLoading}
      />
      <KPICard
        title="Alertas Activas"
        value={data?.active_alerts ?? '—'}
        icon={<ShieldAlert size={24} />}
        color={data?.active_alerts ? 'bg-red-500' : 'bg-slate-400'}
        loading={isLoading}
      />
      <KPICard
        title="Nodos Online"
        value={data ? `${data.devices_online}/${data.devices_total}` : '—'}
        icon={<Signal size={24} />}
        color="bg-green-500"
        loading={isLoading}
      />
      <KPICard
        title="Calidad del Aire"
        value={data ? `${data.air_quality_pct}%` : '—'}
        icon={<Wind size={24} />}
        color={
          (data?.air_quality_pct ?? 100) > 70 ? 'bg-teal-500' :
          (data?.air_quality_pct ?? 100) > 40 ? 'bg-orange-500' : 'bg-red-500'
        }
        loading={isLoading}
      />
    </div>
  );
};

export default KPIGrid;