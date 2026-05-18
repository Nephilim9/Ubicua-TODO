const ReadingHistory = () => {
  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <div className="flex justify-between items-center mb-6">
        <h3 className="font-bold text-slate-800">Historial de Lecturas (24h)</h3>
        <div className="flex gap-2">
          <button className="px-3 py-1 text-xs font-semibold bg-slate-100 text-slate-600 rounded-md">JSON</button>
          <button className="px-3 py-1 text-xs font-semibold bg-blue-600 text-white rounded-md">Exportar CSV</button>
        </div>
      </div>
      <div className="h-48 bg-slate-50 rounded-lg flex items-center justify-center text-slate-400 italic">
        [Gráfico histórico detallado similar al del Dashboard]
      </div>
    </div>
  );
};

export default ReadingHistory;