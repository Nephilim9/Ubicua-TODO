import AlertList from '../components/alerts/AlertList';
import AlertFilters from '../components/alerts/AlertFilters';

const AlertsPage = () => {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Historial de Alertas</h1>
        <p className="text-slate-500">Registro de eventos críticos y resoluciones del sistema.</p>
      </div>

      <AlertFilters />
      <AlertList />
    </div>
  );
};

export default AlertsPage;