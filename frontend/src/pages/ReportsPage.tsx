import { FileText, Download, Calendar } from 'lucide-react';

const ReportsPage = () => {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Reportes y Exportación</h1>
        <p className="text-slate-500">Genera archivos de auditoría sobre el estado de la seguridad.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Card de Reporte de Sensores */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center gap-3 text-blue-600">
            <FileText size={24} />
            <h3 className="font-bold text-slate-800">Histórico de Lecturas</h3>
          </div>
          <p className="text-sm text-slate-500">Descarga todas las mediciones de gas, temperatura y movimiento en formato CSV o JSON.</p>
          <div className="flex gap-2 pt-2">
            <button className="flex-1 bg-slate-800 text-white py-2 rounded-lg text-sm font-bold flex items-center justify-center gap-2 hover:bg-slate-700 transition-colors">
              <Download size={16} /> CSV
            </button>
            <button className="flex-1 border border-slate-200 py-2 rounded-lg text-sm font-bold flex items-center justify-center gap-2 hover:bg-slate-100 transition-colors">
               JSON
            </button>
          </div>
        </div>

        {/* Card de Reporte de Alertas */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center gap-3 text-red-600">
            <Calendar size={24} />
            <h3 className="font-bold text-slate-800">Log de Incidentes</h3>
          </div>
          <p className="text-sm text-slate-500">Resumen detallado de alertas disparadas, tiempos de respuesta y resoluciones manuales.</p>
          <button className="w-full bg-red-600 text-white py-2 rounded-lg text-sm font-bold flex items-center justify-center gap-2 hover:bg-red-700 transition-colors pt-2">
            <Download size={16} /> Generar PDF de Auditoría
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReportsPage;