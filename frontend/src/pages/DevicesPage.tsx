import DeviceList from '../components/devices/DeviceList';
import DeviceLogs from '../components/devices/DeviceLogs';

const DevicesPage = () => {
  return (
    <div className="space-y-8 animate-in zoom-in-95 duration-500">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Red de Dispositivos</h1>
        <p className="text-slate-500">Estado de conexión y diagnóstico de nodos ESP32.</p>
      </div>

      <DeviceList />
      
      <div className="pt-4">
        <h3 className="text-lg font-semibold text-slate-700 mb-4">Consola de Eventos en Tiempo Real</h3>
        <DeviceLogs />
      </div>
    </div>
  );
};

export default DevicesPage;