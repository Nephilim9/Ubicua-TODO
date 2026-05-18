import { Lock, Bell, Server, User } from 'lucide-react';

const SettingsPage = () => {
  return (
    <div className="max-w-4xl space-y-8 animate-in slide-in-from-left-4 duration-500">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Configuración Global</h1>
        <p className="text-slate-500">Ajustes del servidor y perfil de administrador.</p>
      </div>

      <div className="space-y-6">
        {/* Sección Perfil */}
        <section className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center gap-2 mb-4 text-slate-800 font-bold">
            <User size={20} className="text-blue-500" />
            <h3>Perfil del Administrador</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input type="text" className="p-2 border rounded-lg text-sm bg-slate-50" value="Adriana María Bonilla Arias" readOnly />
            <input type="email" className="p-2 border rounded-lg text-sm bg-slate-50" value="admin@safehome.local" readOnly />
          </div>
        </section>

        {/* Sección Seguridad */}
        <section className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center gap-2 mb-4 text-slate-800 font-bold">
            <Lock size={20} className="text-orange-500" />
            <h3>Seguridad y Acceso</h3>
          </div>
          <button className="text-sm text-blue-600 font-semibold hover:underline">Cambiar contraseña del Dashboard</button>
        </section>

        {/* Sección API/Backend */}
        <section className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center gap-2 mb-4 text-slate-800 font-bold">
            <Server size={20} className="text-green-500" />
            <h3>Conexión con el Backend</h3>
          </div>
          <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
            <span className="text-xs font-mono text-slate-500">Endpoint: http://localhost:8000/api/v1</span>
            <span className="text-[10px] bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-bold">ACTIVO</span>
          </div>
        </section>
      </div>
    </div>
  );
};

export default SettingsPage;