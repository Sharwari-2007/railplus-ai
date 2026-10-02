'use client';

import React from 'react';
import { 
  Clock, 
  ShieldCheck, 
  AlertTriangle, 
  CloudRain, 
  Wind, 
  Thermometer, 
  Gauge, 
  Sparkles,
  Info
} from 'lucide-react';
import { TrainData } from '../../types';

interface EtaCardProps {
  train: TrainData | null;
}

export const EtaCard: React.FC<EtaCardProps> = ({ train }) => {
  if (!train) return null;

  const etaInfo = train.eta_analysis;
  const confidence = etaInfo?.probabilistic_eta?.confidence_score_pct || 94;
  const interval = etaInfo?.probabilistic_eta?.interval_mins || 4;
  const netDelay = etaInfo?.net_delay_mins || 0;
  const weather = etaInfo?.weather_impact;
  const xaiBreakdown = etaInfo?.xai_delay_breakdown || [];

  return (
    <div className="glass-panel rounded-2xl p-6 shadow-sm relative overflow-hidden border border-slate-200">
      
      {/* Radiant gradient accent in background */}
      <div className="absolute -top-24 -right-24 h-56 w-56 bg-blue-100/60 rounded-full blur-3xl pointer-events-none" />

      {/* Header Info */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 pb-4 mb-5">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 text-xs font-black rounded-md bg-blue-100 text-blue-800 border border-blue-200 shadow-xs">
              {train.number}
            </span>
            <h2 className="text-xl font-black text-slate-900 tracking-tight">
              {train.name}
            </h2>
          </div>
          <p className="text-xs text-slate-600 font-medium flex items-center gap-1.5">
            <span>Route: {train.origin}</span>
            <span className="text-slate-400">→</span>
            <span>{train.destination}</span>
          </p>
        </div>

        {/* Live Speed & Section Badge */}
        <div className="flex items-center gap-2">
          <div className="px-3 py-1.5 rounded-xl bg-white border border-slate-200 flex items-center gap-2.5 text-xs shadow-xs">
            <Gauge className="h-4 w-4 text-blue-600" />
            <div>
              <div className="text-[10px] text-slate-500 font-bold uppercase">EFFECTIVE SPEED</div>
              <div className="font-black text-slate-900">{etaInfo?.effective_speed_kmh || 0} km/h</div>
            </div>
          </div>

          <div
            className={`px-3 py-1.5 rounded-xl border text-xs font-black shadow-xs ${
              train.section_occupancy === 'GREEN'
                ? 'badge-green'
                : train.section_occupancy === 'YELLOW'
                ? 'badge-yellow'
                : 'badge-red'
            }`}
          >
            {train.section_occupancy} SIGNAL BLOCK
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Left Column: Dynamic ETA Display (Probabilistic Band) */}
        <div className="space-y-4">
          <div className="p-5 rounded-2xl bg-gradient-to-br from-blue-50 via-indigo-50/40 to-white border border-blue-200/80 shadow-xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-black text-blue-700 uppercase tracking-wider flex items-center gap-1.5">
                <Clock className="h-4 w-4 text-blue-600" />
                Dynamic Forecast ETA
              </span>
              <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-blue-100 text-blue-800 border border-blue-300">
                AI Probabilistic Model
              </span>
            </div>

            <div className="flex items-baseline gap-3 mb-3">
              <span className="text-3xl font-black text-slate-900 tracking-tight">
                {netDelay < 5 ? 'On Schedule' : `Delayed ~${Math.round(netDelay)} mins`}
              </span>
              <span className="text-sm font-semibold text-slate-500">
                (Est. Transit: {Math.round(etaInfo?.estimated_transit_mins || 0)}m)
              </span>
            </div>

            {/* Confidence Band Gauge */}
            <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-xs flex items-center justify-between text-xs">
              <div className="flex items-center gap-2.5">
                <div className="p-1.5 rounded-lg bg-emerald-50 text-emerald-600 border border-emerald-200">
                  <ShieldCheck className="h-4 w-4" />
                </div>
                <div>
                  <div className="font-extrabold text-slate-900">Confidence Band: {confidence}%</div>
                  <div className="text-[11px] text-slate-500 font-medium">Uncertainty Interval: ±{interval} mins</div>
                </div>
              </div>

              {/* Progress bar visual */}
              <div className="w-28 bg-slate-100 h-2.5 rounded-full overflow-hidden border border-slate-200">
                <div 
                  className="bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500 h-full rounded-full transition-all duration-500" 
                  style={{ width: `${confidence}%` }}
                />
              </div>
            </div>
          </div>

          {/* Live Weather Impact Readout */}
          <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-xs font-extrabold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                <CloudRain className="h-4 w-4 text-blue-600" />
                Nearest Weather Telemetry ({weather?.met_station || 'KDTree Lookup'})
              </h3>
              <span className="text-[10px] text-slate-500 font-mono">india_weather_rainfall_data.xlsx</span>
            </div>

            <div className="grid grid-cols-3 gap-2.5 mb-3 text-center">
              <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 shadow-xs">
                <div className="text-[11px] text-slate-500 font-semibold flex items-center justify-center gap-1 mb-0.5">
                  <CloudRain className="h-3.5 w-3.5 text-blue-500" /> Rain
                </div>
                <div className="font-black text-sm text-slate-900">{weather?.rainfall_mm || 0} mm/d</div>
              </div>

              <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 shadow-xs">
                <div className="text-[11px] text-slate-500 font-semibold flex items-center justify-center gap-1 mb-0.5">
                  <Thermometer className="h-3.5 w-3.5 text-amber-500" /> Min Temp
                </div>
                <div className="font-black text-sm text-slate-900">{weather?.min_temp_c || 20}°C</div>
              </div>

              <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 shadow-xs">
                <div className="text-[11px] text-slate-500 font-semibold flex items-center justify-center gap-1 mb-0.5">
                  <Wind className="h-3.5 w-3.5 text-cyan-500" /> Wind
                </div>
                <div className="font-black text-sm text-slate-900">{weather?.wind_speed_kmh || 15} km/h</div>
              </div>
            </div>

            {/* Active TSR Cautions */}
            {weather?.active_cautions && weather.active_cautions.length > 0 ? (
              <div className="space-y-1.5">
                {weather.active_cautions.map((c, i) => (
                  <div key={i} className="text-xs p-2.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 flex items-center gap-2 font-semibold shadow-xs">
                    <AlertTriangle className="h-4 w-4 shrink-0 text-amber-600" />
                    <span>{c}</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-xs text-emerald-700 bg-emerald-50 border border-emerald-200 p-2.5 rounded-xl flex items-center gap-1.5 font-bold shadow-xs">
                <ShieldCheck className="h-4 w-4 text-emerald-600" /> No active Speed Restriction (TSR) caution order.
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Explainable AI (XAI) Delay Card */}
        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3 border-b border-slate-200 pb-2.5">
              <h3 className="text-xs font-extrabold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles className="h-4 w-4 text-amber-500" />
                Explainable AI (XAI) Delay Attribution
              </h3>
              <span className="text-[11px] text-slate-500 font-bold">Attribution %</span>
            </div>

            <p className="text-xs text-slate-600 mb-4 font-medium">
              Real-time ML feature breakdown explaining the primary drivers behind current transit delay:
            </p>

            <div className="space-y-4">
              {xaiBreakdown.map((item, idx) => {
                const colors = [
                  'from-blue-600 to-indigo-600',
                  'from-amber-500 to-orange-500',
                  'from-cyan-500 to-blue-600',
                  'from-rose-500 to-red-600'
                ];
                const barColor = colors[idx % colors.length];

                return (
                  <div key={idx} className="space-y-1.5">
                    <div className="flex justify-between text-xs">
                      <span className="font-bold text-slate-800">{item.factor}</span>
                      <span className="font-black text-blue-700">{item.percentage}%</span>
                    </div>
                    <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden border border-slate-200">
                      <div
                        className={`bg-gradient-to-r ${barColor} h-full rounded-full transition-all duration-500 shadow-xs`}
                        style={{ width: `${item.percentage}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="mt-4 p-3.5 rounded-xl bg-blue-50 border border-blue-200 text-xs text-blue-900 flex items-start gap-2.5 font-medium shadow-xs">
            <Info className="h-4 w-4 text-blue-600 shrink-0 mt-0.5" />
            <span>
              XAI model updates dynamically as section block signal clearances are requested and weather conditions fluctuate across track segments.
            </span>
          </div>
        </div>

      </div>
    </div>
  );
};
