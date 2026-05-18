import KPIGrid from '../components/dashboard/KPIGrid';
import SensorChart from '../components/dashboard/SensorChart';
import AlertFeed from '../components/dashboard/AlertFeed';
import DeviceStatus from '../components/dashboard/DeviceStatus';

const DashboardPage = () => {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Panel de Control General</h1>
        <p className="text-slate-500">Monitoreo en tiempo real de seguridad doméstica.</p>
      </div>

      <KPIGrid />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <SensorChart />
        </div>
        <div className="lg:col-span-1">
          <AlertFeed />
        </div>
      </div>

      <div className="grid grid-cols-1 gap-8">
        <DeviceStatus />
      </div>
    </div>
  );
};

export default DashboardPage;