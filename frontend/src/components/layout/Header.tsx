import { Bell, User, Wifi } from 'lucide-react';

const Header = () => {
  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
          <Wifi size={16} />
          <span>Sistema: Online</span>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <button className="text-slate-500 hover:text-slate-800 relative">
          <Bell size={20} />
          <span className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
        
        <div className="flex items-center gap-3 border-l pl-6 border-slate-200">
          <div className="text-right">
            <p className="text-sm font-semibold text-slate-800">Admin - Grupo 4</p>
            <p className="text-xs text-slate-500">Administrador</p>
          </div>
          <div className="w-10 h-10 bg-slate-200 rounded-full flex items-center justify-center text-slate-600">
            <User size={24} />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;