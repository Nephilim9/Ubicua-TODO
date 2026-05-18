import { useState } from 'react';
import { useThresholds } from '../../hooks/useThresholds';

const ThresholdEditor = () => {
  const { updateThreshold } = useThresholds();
  const [form, setForm] = useState({
    name: '', sensor_type: 'MQ135', operator: 'GT',
    value_max: '', severity: 'HIGH',
  });

  const set = (k: string, v: string) => setForm(f => ({ ...f, [k]: v }));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updateThreshold({ ...form, value_max: parseFloat(form.value_max), is_active: true });
    setForm({ name: '', sensor_type: 'MQ135', operator: 'GT', value_max: '', severity: 'HIGH' });
  };

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <h3 className="font-bold text-slate-800 mb-6">Configurar Nuevo Umbral</h3>
      <form className="space-y-4" onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Nombre de la Regla</label>
            <input type="text" required value={form.name} onChange={e => set('name', e.target.value)}
              className="w-full p-2 bg-slate-50 border rounded-lg text-sm" placeholder="Ej: Alerta Incendio" />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Tipo de Sensor</label>
            <select value={form.sensor_type} onChange={e => set('sensor_type', e.target.value)}
              className="w-full p-2 bg-slate-50 border rounded-lg text-sm">
              <option value="MQ135">MQ135 (Humo/Gas)</option>
              <option value="PIR">PIR (Movimiento)</option>
              <option value="TEMP">TEMP (Temperatura)</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Operador</label>
            <select value={form.operator} onChange={e => set('operator', e.target.value)}
              className="w-full p-2 bg-slate-50 border rounded-lg text-sm">
              <option value="GT">Mayor que {'>'}</option>
              <option value="LT">Menor que {'<'}</option>
              <option value="EQ">Igual a (==)</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Valor Límite</label>
            <input type="number" required value={form.value_max} onChange={e => set('value_max', e.target.value)}
              className="w-full p-2 bg-slate-50 border rounded-lg text-sm" placeholder="500" />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Severidad</label>
            <select value={form.severity} onChange={e => set('severity', e.target.value)}
              className="w-full p-2 bg-slate-50 border rounded-lg text-sm">
              <option value="CRITICAL">CRITICAL</option>
              <option value="HIGH">HIGH</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="LOW">LOW</option>
            </select>
          </div>
        </div>

        <button type="submit"
          className="w-full py-3 bg-slate-800 text-white rounded-lg font-bold hover:bg-slate-700 transition-colors mt-4">
          Guardar Configuración
        </button>
      </form>
    </div>
  );
};

export default ThresholdEditor;