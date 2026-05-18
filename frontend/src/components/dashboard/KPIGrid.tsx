import { Activity, ShieldAlert, Signal, Wind } from 'lucide-react';

const KPICard = ({ title, value, icon, color }: { title: string, value: string | number, icon: any, color: string }) => (
  <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
    <div className={`p-3 rounded-lg ${color} text-white`}>
      {icon}
    </div>
    <div>
      <p className="text-sm text-slate-500 font-medium">{title}</p>
      <p className="text-2xl font-bold text-slate-800">{value}</p>
    </div>
  </div>
);

const KPIGrid = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <KPICard 
        title="Sensores Activos" 
        value="12" 
        icon={<Activity size={24} />} 
        color="bg-blue-500" 
      />
      <KPICard 
        title="Alertas Hoy" 
        value="3" 
        icon={<ShieldAlert size={24} />} 
        color="bg-red-500" 
      />
      <KPICard 
        title="Nodos Online" 
        value="4/5" 
        icon={<Signal size={24} />} 
        color="bg-green-500" 
      />
      <KPICard 
        title="Calidad Aire" 
        value="98%" 
        icon={<Wind size={24} />} 
        color="bg-teal-500" 
      />
    </div>
  );
};

export default KPIGrid;