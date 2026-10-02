'use client';

import React from 'react';
import { 
  Train, 
  Activity, 
  CloudRain, 
  ShieldAlert, 
  UserCheck, 
  SlidersHorizontal, 
  Wifi, 
  WifiOff, 
  Sparkles 
} from 'lucide-react';
import { HistoricDay } from '../types';

interface NavbarProps {
  currentView: 'PASSENGER' | 'CONTROLLER';
  onViewChange: (view: 'PASSENGER' | 'CONTROLLER') => void;
  selectedSimDate: string;
  onSimDateChange: (date: string) => void;
  historicDays: HistoricDay[];
  wsConnected: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentView,
  onViewChange,
  selectedSimDate,
  onSimDateChange,
  historicDays,
  wsConnected
}) => {
  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-slate-200/90 px-4 py-3 shadow-sm transition-all">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
        
        {/* Left: Brand Logo & SIH Badge */}
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-500 p-0.5 shadow-md shadow-blue-500/20">
            <div className="h-full w-full bg-white rounded-[10px] flex items-center justify-center">
              <Train className="h-5 w-5 text-blue-600 animate-pulse" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-blue-700 via-indigo-700 to-cyan-600 bg-clip-text text-transparent">
                RailPulse AI
              </h1>
              <span className="px-2 py-0.5 text-[10px] font-bold tracking-wider rounded-full bg-blue-50 text-blue-700 border border-blue-200 shadow-xs">
                SIH26028
              </span>
            </div>
            <p className="text-[11px] text-slate-500 font-medium flex items-center gap-1">
              Ministry of Railways • Dynamic ETA & Dispatch Engine
            </p>
          </div>
        </div>

        {/* Middle: Live Marquee Status Bar */}
        <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 max-w-md overflow-hidden shadow-xs">
          <Sparkles className="h-3.5 w-3.5 text-amber-500 shrink-0" />
          <div className="truncate">
            <span className="font-bold text-blue-700">Live Telemetry:</span> 12951 Mumbai Rajdhani at Agra Cantt (118 km/h) • Monsoon TSR Active
          </div>
        </div>

        {/* Right: Controls (Historic Weather Picker + WS Status + View Switcher) */}
        <div className="flex flex-wrap items-center gap-3">
          
          {/* Historic Weather Simulator Dropdown */}
          <div className="flex items-center gap-1.5 bg-slate-50 border border-slate-200 rounded-xl px-2.5 py-1 text-xs shadow-xs">
            <CloudRain className="h-4 w-4 text-blue-600" />
            <select
              value={selectedSimDate}
              onChange={(e) => onSimDateChange(e.target.value)}
              className="bg-transparent text-slate-800 font-semibold focus:outline-none cursor-pointer text-xs"
            >
              {historicDays.length > 0 ? (
                historicDays.map((hd) => (
                  <option key={hd.id} value={hd.date} className="bg-white text-slate-800">
                    {hd.label}
                  </option>
                ))
              ) : (
                <>
                  <option value="2025-07-15" className="bg-white text-slate-800">Monsoon Hazard (July 15)</option>
                  <option value="2025-01-10" className="bg-white text-slate-800">Winter Fog (Jan 10)</option>
                  <option value="2025-05-20" className="bg-white text-slate-800">Summer Storm (May 20)</option>
                  <option value="2025-10-12" className="bg-white text-slate-800">Normal Operational (Oct 12)</option>
                </>
              )}
            </select>
          </div>

          {/* WebSocket Status Indicator */}
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-slate-50 border border-slate-200 text-xs shadow-xs">
            {wsConnected ? (
              <>
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span className="text-emerald-700 font-bold">WS Live</span>
              </>
            ) : (
              <>
                <span className="h-2 w-2 rounded-full bg-amber-500"></span>
                <span className="text-amber-700 font-semibold">Connecting...</span>
              </>
            )}
          </div>

          {/* Dual-Mode View Switcher Toggle */}
          <div className="flex items-center p-1 bg-slate-100 rounded-xl border border-slate-200 shadow-xs">
            <button
              onClick={() => onViewChange('PASSENGER')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all duration-200 ${
                currentView === 'PASSENGER'
                  ? 'bg-white text-blue-700 shadow-sm border border-slate-200/80'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <UserCheck className="h-3.5 w-3.5 text-blue-600" />
              <span>Passenger Portal</span>
            </button>

            <button
              onClick={() => onViewChange('CONTROLLER')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all duration-200 ${
                currentView === 'CONTROLLER'
                  ? 'bg-white text-indigo-700 shadow-sm border border-slate-200/80'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <SlidersHorizontal className="h-3.5 w-3.5 text-indigo-600" />
              <span>Controller Cockpit</span>
            </button>
          </div>

        </div>

      </div>
    </header>
  );
};
