import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, ShieldAlert, Radio, Activity, Settings } from 'lucide-react';

const Sidebar = () => {
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: <LayoutDashboard size={20} /> },
    { name: 'Sensores', path: '/sensors', icon: <Activity size={20} /> },
    { name: 'Alertas', path: '/alerts', icon: <ShieldAlert size={20} /> },
    { name: 'Dispositivos', path: '/devices', icon: <Radio size={20} /> },
    { name: 'Configuración', path: '/settings', icon: <Settings size={20} /> },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col h-screen sticky top-0">
      <div className="p-6">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <ShieldAlert className="text-red-500" />
          SafeHome
        </h1>
        <p className="text-xs text-slate-400 mt-1">Sist. Seguridad ESP-NOW</p>
      </div>

      <nav className="flex-1 px-4 space-y-2 mt-4">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
              location.pathname === item.path
                ? 'bg-blue-600 text-white'
                : 'text-slate-300 hover:bg-slate-800 hover:text-white'
            }`}
          >
            {item.icon}
            <span className="font-medium">{item.name}</span>
          </Link>
        ))}
      </nav>

      <div className="p-6 border-t border-slate-800 text-xs text-slate-500 text-center">
        Desarrollado por Grupo 4
      </div>
    </aside>
  );
};

export default Sidebar;