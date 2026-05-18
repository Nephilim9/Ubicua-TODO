const logs = [
  { id: 1, time: '22:45:10', device: 'MASTER', event: 'Sincronización ESP-NOW exitosa', level: 'info' },
  { id: 2, time: '22:40:05', device: 'Node 02', event: 'Pérdida de señal (Timeout)', level: 'error' },
  { id: 3, time: '22:35:12', device: 'Node 01', event: 'Reporte de batería baja (15%)', level: 'warning' },
];

const DeviceLogs = () => {
  return (
    <div className="bg-slate-900 rounded-xl border border-slate-800 shadow-lg overflow-hidden">
      <div className="p-4 border-b border-slate-800 bg-slate-800/50 flex justify-between items-center">
        <h3 className="font-bold text-slate-200 text-sm">System Terminal Logs</h3>
        <span className="text-[10px] text-slate-500 font-mono">dev/ttyUSB0</span>
      </div>
      <div className="p-4 font-mono text-[11px] h-64 overflow-y-auto space-y-2">
        {logs.map((log) => (
          <div key={log.id} className="flex gap-4">
            <span className="text-slate-500">[{log.time}]</span>
            <span className={`font-bold ${
              log.level === 'error' ? 'text-red-400' : 
              log.level === 'warning' ? 'text-yellow-400' : 'text-green-400'
            }`}>
              {log.level.toUpperCase()}
            </span>
            <span className="text-blue-300">[{log.device}]</span>
            <span className="text-slate-300">{log.event}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DeviceLogs;