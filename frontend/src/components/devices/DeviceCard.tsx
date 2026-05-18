import { Cpu, Wifi, WifiOff, RefreshCw } from 'lucide-react';

interface DeviceProps {
  device: {
    name: string;
    mac: string;
    type: string;
    status: 'online' | 'offline';
    lastSeen: string;
  };
}

const DeviceCard = ({ device }: DeviceProps) => {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 flex flex-col justify-between">
      <div className="flex justify-between items-start mb-4">
        <div className={`p-3 rounded-lg ${device.status === 'online' ? 'bg-green-100 text-green-600' : 'bg-slate-100 text-slate-400'}`}>
          <Cpu size={24} />
        </div>
        <button className="text-slate-400 hover:text-blue-600 transition-colors" title="Reiniciar nodo">
          <RefreshCw size={18} />
        </button>
      </div>

      <div>
        <h4 className="font-bold text-slate-800 text-lg">{device.name}</h4>
        <p className="text-xs font-mono text-slate-500 mb-2">{device.mac}</p>
        <div className="flex items-center gap-2 mb-4">
          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase ${
            device.status === 'online' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
          }`}>
            {device.status}
          </span>
          <span className="text-[10px] text-slate-400">Tipo: {device.type}</span>
        </div>
      </div>

      <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
        <span>Última vez visto:</span>
        <span className="font-medium">{device.lastSeen}</span>
      </div>
    </div>
  );
};

export default DeviceCard;