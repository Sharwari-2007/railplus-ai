'use client';

import React from 'react';
import { MapPin, CheckCircle, Clock, Navigation, CloudRain, Sun, CloudFog } from 'lucide-react';
import { TrainData } from '../../types';

interface RouteTimelineBarProps {
  train: TrainData | null;
}

export const RouteTimelineBar: React.FC<RouteTimelineBarProps> = ({ train }) => {
  if (!train || !train.route_junctions) return null;

  const junctions = train.route_junctions;
  const progressPct = train.progress_pct || 35;

  return (
    <div className="glass-panel rounded-2xl p-6 shadow-sm border border-slate-200">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-blue-50 text-blue-600 border border-blue-200">
            <Navigation className="h-4 w-4" />
          </div>
          <h2 className="text-sm font-extrabold text-slate-900 uppercase tracking-wider">
            Interactive Route Milestone Timeline & Weather Status
          </h2>
        </div>
        <span className="text-xs font-bold text-blue-700 bg-blue-50 border border-blue-200 px-3 py-1 rounded-full shadow-xs">
          Remaining Distance: {Math.round(train.remaining_distance_km)} km
        </span>
      </div>

      {/* Progress Bar Container */}
      <div className="relative my-7 px-4">
        
        {/* Background Track Line */}
        <div className="absolute left-6 right-6 top-5 h-2 bg-slate-200 rounded-full" />
        
        {/* Active Progress Line */}
        <div 
          className="absolute left-6 top-5 h-2 bg-gradient-to-r from-blue-600 via-indigo-600 to-emerald-500 rounded-full transition-all duration-700 shadow-xs" 
          style={{ width: `calc(${progressPct}% - 24px)` }}
        />

        {/* Milestone Junction Nodes */}
        <div className="relative flex items-center justify-between">
          {junctions.map((j, idx) => {
            const isPassed = (idx / (junctions.length - 1)) * 100 <= progressPct;
            const isCurrent = j.name.toLowerCase().includes(train.current_station.split(' ')[0].toLowerCase());

            return (
              <div key={idx} className="flex flex-col items-center group cursor-pointer">
                
                {/* Weather icon indicator above milestone */}
                <div className="mb-2 transition-transform group-hover:scale-110">
                  {idx % 3 === 0 ? (
                    <CloudRain className="h-4 w-4 text-blue-500" />
                  ) : idx % 3 === 1 ? (
                    <CloudFog className="h-4 w-4 text-amber-500" />
                  ) : (
                    <Sun className="h-4 w-4 text-amber-500" />
                  )}
                </div>

                {/* Node Circle */}
                <div 
                  className={`h-7 w-7 rounded-full flex items-center justify-center border-2 transition-all duration-300 ${
                    isCurrent
                      ? 'bg-blue-600 border-white ring-4 ring-blue-500/30 scale-125 z-10 shadow-md text-white'
                      : isPassed
                      ? 'bg-blue-600 border-blue-300 text-white shadow-xs'
                      : 'bg-white border-slate-300 text-slate-400 shadow-xs'
                  }`}
                >
                  {isCurrent ? (
                    <MapPin className="h-3.5 w-3.5 text-white animate-bounce" />
                  ) : isPassed ? (
                    <CheckCircle className="h-3.5 w-3.5 text-white" />
                  ) : (
                    <span className="text-[10px] font-black">{idx + 1}</span>
                  )}
                </div>

                {/* Milestone Details */}
                <div className="mt-2.5 text-center max-w-[80px]">
                  <div className={`text-xs font-black truncate ${isCurrent ? 'text-blue-700' : 'text-slate-800'}`}>
                    {j.code}
                  </div>
                  <div className="text-[11px] text-slate-500 font-semibold truncate">{j.name.split(' ')[0]}</div>
                  <div className="text-[10px] text-slate-400 font-mono mt-0.5">{j.arr}</div>
                </div>

              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
