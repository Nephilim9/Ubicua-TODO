import { BellRing, BellOff, Edit2, Trash2 } from 'lucide-react';

const thresholds = [
  { id: 1, name: 'Fuga Gas Crítica', type: 'MQ135', operator: '>', value: 500, severity: 'CRITICAL', active: true },
  { id: 2, name: 'Movimiento Nocturno', type: 'PIR', operator: '==', value: 1, severity: 'HIGH', active: true },
  { id: 3, name: 'Temp. Alta Garage', type: 'TEMP', operator: '>', value: 45, severity: 'MEDIUM', active: false },
];

const ThresholdList = () => {
  return (
    <div className="space-y-4">
      {thresholds.map((t) => (
        <div key={t.id} className={`p-4 rounded-xl border flex items-center justify-between transition-all ${
          t.active ? 'bg-white border-slate-200' : 'bg-slate-50 border-slate-200 opacity-60'
        }`}>
          <div className="flex items-center gap-4">
            <div className={`p-2 rounded-lg ${
              t.severity === 'CRITICAL' ? 'bg-red-100 text-red-600' : 
              t.severity === 'HIGH' ? 'bg-orange-100 text-orange-600' : 'bg-yellow-100 text-yellow-600'
            }`}>
              {t.active ? <BellRing size={20} /> : <BellOff size={20} />}
            </div>
            <div>
              <h4 className="font-bold text-slate-800 text-sm">{t.name}</h4>
              <p className="text-xs text-slate-500">
                Si <span className="font-mono font-bold text-slate-700">{t.type} {t.operator} {t.value}</span> entonces alerta <span className="font-bold">{t.severity}</span>
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button className="p-2 text-slate-400 hover:text-blue-600 transition-colors"><Edit2 size={16} /></button>
            <button className="p-2 text-slate-400 hover:text-red-500 transition-colors"><Trash2 size={16} /></button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ThresholdList;