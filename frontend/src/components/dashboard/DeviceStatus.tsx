import { Circle, Cpu, RefreshCw } from 'lucide-react';
import { useDevices } from '../../hooks/useDevices';
import api from '../../services/api';

const DeviceStatus = () => {
  const { data: devices, isLoading, refetch } = useDevices();

  const handlePing = async (id: number) => {
    try {
      await api.post(`/devices/${id}/ping`);
    } catch {}
    refetch();
  };

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <div className="flex justify-between items-center mb-6">
        <h3 className="font-bold text-slate-800">Red ESP-NOW — Estado de Dispositivos</h3>
        <button
          onClick={() => refetch()}
          className="text-slate-400 hover:text-slate-600 transition-colors"
          title="Actualizar"
        >
          <RefreshCw size={16} />
        </button>
      </div>

      {isLoading && (
        <div className="space-y-3">
          {[1,2,3].map(i => <div key={i} className="h-14 bg-slate-100 rounded-lg animate-pulse" />)}
        </div>
      )}

      <div className="space-y-3">
        {(devices ?? []).map((device) => (
          <div key={device.mac_address} className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-white rounded-md border border-slate-200 text-slate-600">
                <Cpu size={18} />
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-800">{device.name}</p>
                <p className="text-[10px] text-slate-500 font-mono">{device.mac_address}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${
                device.status === 'online'
                  ? 'text-green-700 bg-green-100'
                  : 'text-red-600 bg-red-50'
              }`}>
                {device.status}
              </span>
              <Circle
                size={8}
                fill={device.status === 'online' ? '#16a34a' : '#ef4444'}
                stroke="none"
                className={device.status === 'online' ? 'animate-pulse' : ''}
              />
              <button
                onClick={() => handlePing(device.id)}
                className="text-xs text-slate-400 hover:text-blue-600 transition-colors font-mono"
                title="Ping"
              >
                ping
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DeviceStatus;