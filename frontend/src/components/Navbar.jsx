import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, BrainCircuit, Activity } from 'lucide-react';

export default function Navbar() {
  const { pathname } = useLocation();

  return (
    <nav className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 h-20 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Activity className="text-indigo-600" />
          <h1 className="text-xl font-black tracking-tighter text-slate-800">OPTISPRINT <span className="text-indigo-600 font-medium">AI</span></h1>
        </div>
        
        <div className="flex gap-2">
          <NavLink to="/" active={pathname === "/"} icon={<LayoutDashboard size={18}/>} label="Dashboard" />
          <NavLink to="/input" active={pathname === "/input"} icon={<BrainCircuit size={18}/>} label="Task Input" />
        </div>
      </div>
    </nav>
  );
}

const NavLink = ({ to, active, icon, label }) => (
  <Link to={to} className={`flex items-center gap-2 px-6 py-2.5 rounded-2xl font-bold text-sm transition-all ${active ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-100' : 'text-slate-400 hover:bg-slate-50 hover:text-slate-600'}`}>
    {icon} {label}
  </Link>
);