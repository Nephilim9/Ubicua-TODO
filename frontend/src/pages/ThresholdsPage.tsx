import ThresholdList from '../components/threshold/ThresholdList';
import ThresholdEditor from '../components/threshold/ThresholdEditor';

const ThresholdsPage = () => {
  return (
    <div className="space-y-8 animate-in slide-in-from-right-4 duration-500">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Configuración de Umbrales</h1>
        <p className="text-slate-500">Definición de límites y reglas de seguridad para disparar alertas.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-4">
          <h3 className="font-semibold text-slate-700">Reglas Activas</h3>
          <ThresholdList />
        </div>
        <div>
          <ThresholdEditor />
        </div>
      </div>
    </div>
  );
};

export default ThresholdsPage;