const ThresholdEditor = () => {
  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <h3 className="font-bold text-slate-800 mb-6">Configurar Nuevo Umbral</h3>
      <form className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Nombre de la Regla</label>
            <input type="text" className="w-full p-2 bg-slate-50 border rounded-lg text-sm" placeholder="Ej: Alerta Incendio" />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Tipo de Sensor</label>
            <select className="w-full p-2 bg-slate-50 border rounded-lg text-sm">
              <option>MQ135 (Humo/Gas)</option>
              <option>PIR (Movimiento)</option>
              <option>TEMP (Temperatura)</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Operador</label>
            <select className="w-full p-2 bg-slate-50 border rounded-lg text-sm">
              <option value="GT">Mayor que (>)</option>
              <option value="LT">Menor que (&lt;)</option>
              <option value="EQ">Igual a (==)</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Valor Límite</label>
            <input type="number" className="w-full p-2 bg-slate-50 border rounded-lg text-sm" placeholder="500" />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Severidad</label>
            <select className="w-full p-2 bg-slate-50 border rounded-lg text-sm">
              <option className="text-red-600 font-bold">CRITICAL</option>
              <option className="text-orange-600">HIGH</option>
              <option className="text-yellow-600">MEDIUM</option>
              <option className="text-green-600">LOW</option>
            </select>
          </div>
        </div>

        <button type="button" className="w-full py-3 bg-slate-800 text-white rounded-lg font-bold hover:bg-slate-700 transition-colors mt-4">
          Guardar Configuración
        </button>
      </form>
    </div>
  );
};

export default ThresholdEditor;