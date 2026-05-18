    import { AlertTriangle, CheckCircle2, Info } from 'lucide-react';

const alerts = [
  { id: 1, sensor: 'MQ135 - Cocina', severity: 'CRITICAL', msg: 'Fuga de Gas detectada', status: 'active', time: '2026-05-17 22:15' },
  { id: 2, sensor: 'PIR - Pasillo', severity: 'HIGH', msg: 'Movimiento no autorizado', status: 'acknowledged', time: '2026-05-17 21:00' },
];

const AlertList = () => {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <div className="divide-y divide-slate-100">
        {alerts.map((alert) => (
          <div key={alert.id} className="p-6 flex flex-wrap items-center justify-between gap-4 hover:bg-slate-50 transition-colors">
            <div className="flex items-center gap-4">
              <div className={`p-3 rounded-full ${
                alert.severity === 'CRITICAL' ? 'bg-red-100 text-red-600' : 'bg-orange-100 text-orange-600'
              }`}>
                <AlertTriangle size={24} />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h4 className="font-bold text-slate-800">{alert.msg}</h4>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    alert.status === 'active' ? 'bg-red-100 text-red-700 animate-pulse' : 'bg-slate-100 text-slate-600'
                  }`}>
                    {alert.status.toUpperCase()}
                  </span>
                </div>
                <p className="text-xs text-slate-500">{alert.sensor} • {alert.time}</p>
              </div>
            </div>
            
            <div className="flex gap-2">
              <button className="px-4 py-2 text-xs font-bold border border-slate-200 rounded-lg hover:bg-slate-100 text-slate-600 transition-colors">
                Ver Detalle
              </button>
              {alert.status === 'active' && (
                <button className="px-4 py-2 text-xs font-bold bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2">
                  <CheckCircle2 size={14} />
                  Resolver
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AlertList;