const AlertDetail = ({ alertId }: { alertId: number }) => {
  return (
    <div className="bg-slate-50 p-6 rounded-xl border-2 border-dashed border-slate-200">
      <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
        <Info size={18} className="text-blue-500" />
        Análisis Técnico de la Alerta #{alertId}
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <p className="text-slate-500 mb-1 font-medium">Valor Disparador</p>
          <p className="text-xl font-mono font-bold text-red-600">650.45 ppm</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <p className="text-slate-500 mb-1 font-medium">Umbral Configurado</p>
          <p className="text-xl font-mono font-bold text-slate-800">&gt; 500.00 ppm</p>
        </div>
      </div>
      <div className="mt-4 p-4 bg-white rounded-lg shadow-sm">
        <p className="text-slate-500 mb-1 font-medium text-xs uppercase">Acciones del Sistema</p>
        <ul className="text-xs text-slate-600 space-y-1 list-disc pl-4">
          <li>Notificación WebSocket enviada.</li>
          <li>Comando Buzzer enviado al ESP32 Master.</li>
          <li>Registro persistido en SQLite.</li>
        </ul>
      </div>
    </div>
  );
};

export default AlertDetail;