import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import api from '../../services/api';

const SENSOR_TYPES = ['MQ135', 'PIR'] as const;
type SensorType = typeof SENSOR_TYPES[number];

interface ChartRow { time: string; value: number; min: number; max: number; }
interface ChartData { sensor_type: string; hours: number; data: ChartRow[]; }

const SensorChart = () => {
  const [sensorType, setSensorType] = useState<SensorType>('MQ135');

  const { data, isLoading } = useQuery<ChartData>({
    queryKey: ['chart-data', sensorType],
    queryFn: async () => (await api.get('/dashboard/chart-data', { params: { sensor_type: sensorType, hours: 6 } })).data,
    refetchInterval: 10_000,
  });

  const formatTime = (iso: string) => iso.slice(11, 16); // HH:MM

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-[350px]">
      <div className="flex justify-between items-center mb-6">
        <h3 className="font-bold text-slate-800">
          Lecturas {sensorType} {sensorType === 'MQ135' ? '(ppm)' : '(detección)'}
        </h3>
        <div className="flex items-center gap-3">
          <select
            id="sensor-type-select"
            className="text-xs border border-slate-200 rounded px-2 py-1 text-slate-600 bg-slate-50"
            value={sensorType}
            onChange={e => setSensorType(e.target.value as SensorType)}
          >
            {SENSOR_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
          <span className="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded font-semibold">
            {isLoading ? 'Actualizando…' : 'Tiempo Real'}
          </span>
        </div>
      </div>

      {isLoading && !data ? (
        <div className="h-[200px] flex items-center justify-center text-slate-400 text-sm">Cargando datos…</div>
      ) : (
        <ResponsiveContainer width="100%" height="80%">
          <LineChart data={data?.data ?? []}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
            <XAxis dataKey="time" tickFormatter={formatTime} axisLine={false} tickLine={false} tick={{ fill: '#64748b', fontSize: 12 }} />
            <YAxis axisLine={false} tickLine={false} tick={{ fill: '#64748b', fontSize: 12 }} />
            <Tooltip
              labelFormatter={formatTime}
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            />
            {sensorType === 'MQ135' && (
              <ReferenceLine y={500} stroke="#ef4444" strokeDasharray="4 2" label={{ value: 'Umbral', fill: '#ef4444', fontSize: 11 }} />
            )}
            <Line type="monotone" dataKey="value" name={sensorType} stroke="#3b82f6" strokeWidth={2.5} dot={false} activeDot={{ r: 5 }} />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
};

export default SensorChart;