const SensorDetail = ({ sensorId }: { sensorId: number }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="md:col-span-1 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <h3 className="text-lg font-bold text-slate-800 mb-4">Metadatos</h3>
        <div className="space-y-3 text-sm">
          <div className="flex justify-between border-b pb-2"><span className="text-slate-500">ID:</span> <span className="font-mono">{sensorId}</span></div>
          <div className="flex justify-between border-b pb-2"><span className="text-slate-500">Pin GPIO:</span> <span className="font-mono">34</span></div>
          <div className="flex justify-between border-b pb-2"><span className="text-slate-500">Dispositivo:</span> <span>ESP-Master</span></div>
        </div>
      </div>
      <div className="md:col-span-2 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <h3 className="text-lg font-bold text-slate-800 mb-4">Estado de Salud</h3>
        <p className="text-sm text-slate-600">El sensor está operando dentro de los rangos normales de calibración.</p>
      </div>
    </div>
  );
};

export default SensorDetail;