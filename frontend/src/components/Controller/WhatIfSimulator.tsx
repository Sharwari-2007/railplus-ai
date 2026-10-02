'use client';

import React, { useState } from 'react';
import { Sliders, AlertOctagon, Play, RefreshCw, CheckCircle2, TrendingUp } from 'lucide-react';
import { WhatIfSimulationResult } from '../../types';
import { api } from '../../services/api';

interface WhatIfSimulatorProps {
  selectedSimDate: string;
}

export const WhatIfSimulator: React.FC<WhatIfSimulatorProps> = ({ selectedSimDate }) => {
  const [prioritizeRajdhani, setPrioritizeRajdhani] = useState<boolean>(true);
  const [emergencyBlockMins, setEmergencyBlockMins] = useState<number>(0);
  const [blockSection, setBlockSection] = useState<string>('Agra-Gwalior');
  const [loading, setLoading] = useState<boolean>(false);
  const [simResult, setSimResult] = useState<WhatIfSimulationResult | null>(null);

  const handleRunSimulation = async () => {
    setLoading(true);
    try {
      const res = await api.runWhatIfSimulation(
        prioritizeRajdhani,
        emergencyBlockMins,
        blockSection,
        selectedSimDate
      );
      setSimResult(res);
    } catch (e) {
      console.error('What-If Simulation error', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-6 shadow-sm border border-slate-200">
      <div className="flex items-center justify-between mb-4 border-b border-slate-200 pb-3.5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-cyan-50 text-cyan-700 border border-cyan-200">
            <Sliders className="h-4 w-4" />
          </div>
          <h2 className="text-sm font-extrabold text-slate-900 uppercase tracking-wider">
            Interactive "What-If" Precedence & Emergency Block Simulator
          </h2>
        </div>
        <span className="px-2.5 py-0.5 text-[10px] font-black rounded-full bg-cyan-50 text-cyan-700 border border-cyan-200 shadow-xs">
          Dispatcher Cockpit
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        
        {/* Toggle Precedence: Rajdhani Over Express */}
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-black text-slate-800">PRIORITIZE RAJDHANI</span>
            <input
              type="checkbox"
              checked={prioritizeRajdhani}
              onChange={(e) => setPrioritizeRajdhani(e.target.checked)}
              className="h-4 w-4 text-blue-600 rounded focus:ring-0 cursor-pointer"
            />
          </div>
          <p className="text-[11px] text-slate-500 font-medium">
            {prioritizeRajdhani
              ? 'Priority 1 (Rajdhani) given green signal through-pass; Express held on loop lines.'
              : 'Equal section precedence scheduling without prioritization.'}
          </p>
        </div>

        {/* Emergency Maintenance Block Slider */}
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1.5 shadow-xs">
          <div className="flex justify-between items-center text-xs">
            <span className="font-black text-slate-800">EMERGENCY BLOCK DURATION</span>
            <span className="font-black text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded-md">{emergencyBlockMins} mins</span>
          </div>
          <input
            type="range"
            min={0}
            max={60}
            step={5}
            value={emergencyBlockMins}
            onChange={(e) => setEmergencyBlockMins(Number(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
          />
          <div className="flex justify-between text-[10px] text-slate-400 font-medium">
            <span>0m (Normal)</span>
            <span>30m</span>
            <span>60m (Major)</span>
          </div>
        </div>

        {/* Target Track Section & Run Button */}
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col justify-between shadow-xs">
          <div>
            <label className="text-[10px] font-extrabold text-slate-500 uppercase block mb-1">TARGET SECTION</label>
            <select
              value={blockSection}
              onChange={(e) => setBlockSection(e.target.value)}
              className="w-full bg-white text-xs font-bold text-slate-800 p-1.5 rounded-lg border border-slate-300 focus:outline-none shadow-2xs"
            >
              <option value="Agra-Gwalior">Agra Cantt - Gwalior (Section 4)</option>
              <option value="Gwalior-Jhansi">Gwalior - VGL Jhansi (Section 5)</option>
              <option value="Bhopal-Itarsi">Bhopal - Itarsi Junction (Section 7)</option>
            </select>
          </div>

          <button
            onClick={handleRunSimulation}
            disabled={loading}
            className="mt-3 w-full bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-black text-xs py-2 px-3 rounded-xl transition-all shadow-md shadow-blue-500/20 flex items-center justify-center gap-2 cursor-pointer"
          >
            {loading ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4 fill-current" />}
            <span>Recalculate Cascading Delays</span>
          </button>
        </div>

      </div>

      {/* Simulation Results Table */}
      {simResult && (
        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm animate-fadeIn space-y-3">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2.5">
            <span className="text-xs font-black text-blue-700 uppercase tracking-wider flex items-center gap-1.5">
              <TrendingUp className="h-4 w-4 text-blue-600" /> Real-Time Corridor Impact Results
            </span>
            <span className="text-xs font-bold text-slate-700">
              Corridor Efficiency Score: <span className="text-emerald-700 font-black">{simResult.overall_corridor_efficiency}</span>
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 text-slate-500 text-[10px] font-black uppercase">
                  <th className="py-2.5">Train</th>
                  <th className="py-2.5">Original Delay</th>
                  <th className="py-2.5">Simulated Delay</th>
                  <th className="py-2.5">Delta</th>
                  <th className="py-2.5">Sim Speed</th>
                  <th className="py-2.5">Confidence</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {simResult.train_impacts.map((t, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/80 text-slate-800 font-semibold">
                    <td className="py-2.5 font-extrabold text-slate-900">{t.train_number} {t.train_name}</td>
                    <td className="py-2.5 text-slate-600">{Math.round(t.original_delay_mins)}m</td>
                    <td className="py-2.5 font-black text-amber-700">{Math.round(t.simulated_delay_mins)}m</td>
                    <td className="py-2.5">
                      <span className={`px-2 py-0.5 rounded-md text-[10px] font-black ${
                        t.delay_delta_mins > 0 ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                      }`}>
                        {t.delay_delta_mins > 0 ? `+${t.delay_delta_mins}m` : `${t.delay_delta_mins}m`}
                      </span>
                    </td>
                    <td className="py-2.5 font-bold text-slate-800">{t.simulated_speed_kmh} km/h</td>
                    <td className="py-2.5 text-blue-700 font-black">{t.confidence_score}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
