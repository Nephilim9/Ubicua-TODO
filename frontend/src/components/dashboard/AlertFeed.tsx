const alerts = [
  { id: 1, time: '14:30', msg: 'MQ135 > 500 ppm', severity: 'critical', location: 'Cocina' },
  { id: 2, time: '14:25', msg: 'Movimiento Detectado', severity: 'high', location: 'Garage' },
  { id: 3, time: '14:20', msg: 'NFC Auth Correcta', severity: 'low', location: 'Puerta Principal' },
];

const AlertFeed = () => {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden h-full">
      <div className="p-4 border-b border-slate-100 flex justify-between items-center">
        <h3 className="font-bold text-slate-800">Alertas Recientes</h3>
        <button className="text-xs text-blue-600 font-semibold hover:underline">Ver todas</button>
      </div>
      <div className="divide-y divide-slate-50">
        {alerts.map((alert) => (
          <div key={alert.id} className="p-4 flex items-start gap-4 hover:bg-slate-50 transition-colors">
            <div className={`w-2 h-2 mt-2 rounded-full shrink-0 ${
              alert.severity === 'critical' ? 'bg-red-500 animate-pulse' : 
              alert.severity === 'high' ? 'bg-orange-500' : 'bg-green-500'
            }`} />
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-slate-800 truncate">{alert.msg}</p>
              <p className="text-xs text-slate-500">{alert.location} • {alert.time}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AlertFeed;