import { Filter, Search } from 'lucide-react';

const AlertFilters = () => {
  return (
    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-wrap gap-4 items-center">
      <div className="relative flex-1 min-w-[200px]">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
        <input 
          type="text" 
          placeholder="Buscar alertas..." 
          className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      
      <select className="px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-600 focus:outline-none">
        <option value="">Todas las Severidades</option>
        <option value="CRITICAL">Crítica 🔴</option>
        <option value="HIGH">Alta 🟠</option>
        <option value="MEDIUM">Media 🟡</option>
        <option value="LOW">Baja 🟢</option>
      </select>

      <select className="px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-600 focus:outline-none">
        <option value="active">Activas</option>
        <option value="resolved">Resueltas</option>
        <option value="acknowledged">Reconocidas</option>
      </select>

      <button className="flex items-center gap-2 px-4 py-2 bg-slate-800 text-white rounded-lg text-sm font-bold hover:bg-slate-700 transition-colors">
        <Filter size={16} />
        Filtrar
      </button>
    </div>
  );
};

export default AlertFilters;