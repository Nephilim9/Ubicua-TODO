import SensorList from '../components/sensors/SensorList';
import ReadingHistory from '../components/sensors/ReadingHistory';
import CalibrationForm from '../components/sensors/CalibrationForm';

const SensorsPage = () => {
  return (
    <div className="space-y-8 animate-in slide-in-from-bottom-4 duration-500">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Gestión de Sensores</h1>
        <p className="text-slate-500">Administración técnica y calibración de nodos de detección.</p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        <div className="xl:col-span-2 space-y-8">
          <SensorList />
          <ReadingHistory />
        </div>
        <div className="xl:col-span-1">
          <CalibrationForm />
        </div>
      </div>
    </div>
  );
};

export default SensorsPage;