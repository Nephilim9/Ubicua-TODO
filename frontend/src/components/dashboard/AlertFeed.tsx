import { Link } from 'react-router-dom';
import { useAlerts } from '../../hooks/useAlerts';

const severityDot: Record<string, string> = {
  CRITICAL: 'bg-red-500 animate-pulse',
  HIGH:     'bg-orange-500',
  MEDIUM:   'bg-yellow-400',
  LOW:      'bg-green-500',
};

const AlertFeed = () => {
  const { data: alerts, isLoading } = useAlerts();
  const recent = alerts?.slice(0, 5) ?? [];

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden h-full flex flex-col">
      <div className="p-4 border-b border-slate-100 flex justify-between items-center shrink-0">
        <h3 className="font-bold text-slate-800">Alertas Recientes</h3>
        <Link to="/alerts" className="text-xs text-blue-600 font-semibold hover:underline">Ver todas</Link>
      </div>

      {isLoading && (
        <div className="p-4 space-y-3">
          {[1,2,3].map(i => (
            <div key={i} className="h-10 bg-slate-100 rounded animate-pulse" />
          ))}
        </div>
      )}

      {!isLoading && recent.length === 0 && (
        <div className="flex-1 flex items-center justify-center text-sm text-slate-400">
          Sin alertas recientes 🟢
        </div>
      )}

      <div className="divide-y divide-slate-50 overflow-y-auto">
        {recent.map((alert) => {
          const time = new Date(alert.created_at ?? alert.timestamp).toLocaleTimeString('es-CO', {
            hour: '2-digit', minute: '2-digit',
          });
          return (
            <div key={alert.id} className="p-4 flex items-start gap-4 hover:bg-slate-50 transition-colors">
              <div className={`w-2 h-2 mt-2 rounded-full shrink-0 ${severityDot[alert.severity] ?? 'bg-slate-400'}`} />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-slate-800 truncate">{alert.message}</p>
                <p className="text-xs text-slate-500">{alert.severity} · {time}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AlertFeed;