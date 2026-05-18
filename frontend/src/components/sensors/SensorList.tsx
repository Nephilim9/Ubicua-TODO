import { Activity, Thermometer, Droplets, Wind, Eye } from 'lucide-react';

const sensors = [
  { id: 1, name: 'Sensor Gas Cocina', type: 'MQ135', value: '450 ppm', status: 'active' },
  { id: 2, name: 'Temp. Habitación', type: 'TEMP', value: '24°C', status: 'active' },
  { id: 3, name: 'Humedad Sala', type: 'HUMIDITY', value: '60%', status: 'active' },
];

const SensorList = () => {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <table className="w-full text-left border-collapse">
        <thead className="bg-slate-50 border-b border-slate-200">
          <tr>
            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Sensor</th>
            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Tipo</th>
            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Último Valor</th>
            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Estado</th>
            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase text-right">Acciones</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {sensors.map((sensor) => (
            <tr key={sensor.id} className="hover:bg-slate-50 transition-colors">
              <td className="px-6 py-4 font-semibold text-slate-800">{sensor.name}</td>
              <td className="px-6 py-4">
                <span className="flex items-center gap-2 text-sm text-slate-600">
                  {sensor.type === 'MQ135' ? <Wind size={16} /> : <Activity size={16} />}
                  {sensor.type}
                </span>
              </td>
              <td className="px-6 py-4 text-sm font-mono text-blue-600">{sensor.value}</td>
              <td className="px-6 py-4">
                <span className="px-2 py-1 bg-green-100 text-green-700 text-[10px] font-bold rounded-full uppercase">
                  {sensor.status}
                </span>
              </td>
              <td className="px-6 py-4 text-right">
                <button className="p-2 text-slate-400 hover:text-blue-600 transition-colors">
                  <Eye size={18} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SensorList;