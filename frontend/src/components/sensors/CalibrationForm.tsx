const CalibrationForm = () => {
  return (
    <div className="bg-slate-900 text-white p-6 rounded-xl shadow-xl">
      <h3 className="text-lg font-bold mb-4">Calibración Manual MQ135</h3>
      <form className="space-y-4">
        <div>
          <label className="block text-xs font-bold text-slate-400 uppercase mb-1">Factor R0 (Offset)</label>
          <input 
            type="number" 
            className="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Ej: 4.12"
          />
        </div>
        <p className="text-[10px] text-slate-500 italic">Asegúrese de que el sensor haya precalentado 24h antes de calibrar.</p>
        <button type="button" className="w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-lg font-bold transition-colors">
          Aplicar Calibración
        </button>
      </form>
    </div>
  );
};

export default CalibrationForm;