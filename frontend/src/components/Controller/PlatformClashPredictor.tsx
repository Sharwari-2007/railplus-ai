'use client';

import React, { useEffect, useState } from 'react';
import { Layers, ArrowUpRight } from 'lucide-react';
import { PlatformClash } from '../../types';
import { api } from '../../services/api';

export const PlatformClashPredictor: React.FC = () => {
  const [clashes, setClashes] = useState<PlatformClash[]>([]);

  useEffect(() => {
    api.getPlatformClashes().then(setClashes).catch(console.error);
  }, []);

  return (
    <div className="glass-panel rounded-2xl p-6 shadow-sm border border-slate-200">
      <div className="flex items-center justify-between mb-4 border-b border-slate-200 pb-3.5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-amber-50 text-amber-700 border border-amber-200">
            <Layers className="h-4 w-4" />
          </div>
          <h2 className="text-sm font-extrabold text-slate-900 uppercase tracking-wider">
            Platform Overlap Clash & Turnaround Loop Line Predictor
          </h2>
        </div>
        <span className="px-2.5 py-0.5 text-[10px] font-black rounded-full bg-amber-50 text-amber-700 border border-amber-200 shadow-xs">
          Conflict Radar
        </span>
      </div>

      <p className="text-xs text-slate-600 mb-4 font-medium">
        AI predictive engine scans station platform schedules for high-risk ETA overlaps and recommends open loop lines:
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {clashes.map((c, idx) => (
          <div key={idx} className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-black text-sm text-slate-900">{c.junction}</span>
                <span
                  className={`px-2.5 py-0.5 text-[10px] font-black rounded-full ${
                    c.severity === 'HIGH' ? 'badge-red' : 'badge-yellow'
                  }`}
                >
                  {c.severity} RISK CLASH
                </span>
              </div>

              <div className="text-xs text-slate-600 font-semibold mb-3">
                Target: <span className="text-blue-700 font-bold">{c.platform}</span> • Overlap Duration: <span className="font-bold text-slate-900">{c.overlap_duration_mins} mins</span>
              </div>

              {/* Conflicting trains */}
              <div className="space-y-2 mb-3.5">
                {c.conflicting_trains.map((ct, i) => (
                  <div key={i} className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs shadow-2xs">
                    <span className="font-extrabold text-slate-900">{ct.number} {ct.name}</span>
                    <span className="text-[11px] text-blue-700 font-mono font-bold bg-blue-50 px-2 py-0.5 rounded-md border border-blue-200">ETA: {ct.eta}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Loop line recommendation */}
            <div className="p-3 rounded-xl bg-blue-50 border border-blue-200 text-xs text-blue-900 flex items-start gap-2 font-medium shadow-2xs">
              <ArrowUpRight className="h-4 w-4 text-blue-600 shrink-0 mt-0.5" />
              <span>{c.recommendation}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
