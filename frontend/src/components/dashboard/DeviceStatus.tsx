import { Circle, Cpu } from 'lucide-react';

const devices = [
  { name: 'ESP-Master (Cocina)', status: 'online', mac: 'A4:CF:12:34:56:78' },
  { name: 'ESP-Node 01 (Sala)', status: 'online', mac: 'B4:CF:12:34:56:79' },
  { name: 'ESP-Node 02 (Garage)', status: 'offline', mac: 'C4:CF:12:34:56:80' },
];

const DeviceStatus = () => {
  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-full">
      <h3 className="font-bold text-slate-800 mb-6">Estado de Dispositivos</h3>
      <div className="space-y-4">
        {devices.map((device) => (
          <div key={device.mac} className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-white rounded-md border border-slate-200 text-slate-600">
                <Cpu size={18} />
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-800">{device.name}</p>
                <p className="text-[10px] text-slate-500 font-mono">{device.mac}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className={`text-[10px] font-bold uppercase ${device.status === 'online' ? 'text-green-600' : 'text-red-500'}`}>
                {device.status}
              </span>
              <Circle size={8} fill={device.status === 'online' ? '#16a34a' : '#ef4444'} stroke="none" className={device.status === 'online' ? 'animate-pulse' : ''} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DeviceStatus;