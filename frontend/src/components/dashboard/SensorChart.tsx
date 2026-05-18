import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { time: '10:00', value: 300 },
  { time: '11:00', value: 350 },
  { time: '12:00', value: 420 },
  { time: '13:00', value: 380 },
  { time: '14:00', value: 500 },
  { time: '15:00', value: 450 },
];

const SensorChart = () => {
  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-[350px]">
      <div className="flex justify-between items-center mb-6">
        <h3 className="font-bold text-slate-800">Lecturas MQ135 (PPM)</h3>
        <span className="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded font-semibold">Tiempo Real</span>
      </div>
      <ResponsiveContainer width="100%" height="80%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
          <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} />
          <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} />
          <Tooltip 
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
          />
          <Line 
            type="monotone" 
            dataKey="value" 
            stroke="#3b82f6" 
            strokeWidth={3} 
            dot={{ r: 4, fill: '#3b82f6' }} 
            activeDot={{ r: 6 }} 
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SensorChart;