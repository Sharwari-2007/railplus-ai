'use client';

import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import { TrainData, WeatherStation } from '../../types';
import { Layers, CloudRain, ShieldAlert, RefreshCw } from 'lucide-react';

interface LiveCorridorMapProps {
  trains: TrainData[];
  selectedTrainId: string;
  onSelectTrain: (id: string) => void;
  weatherStations: WeatherStation[];
}

// Dynamically import Leaflet components with SSR disabled
const LeafletContainer = dynamic(() => import('./LeafletMapInner'), {
  ssr: false,
  loading: () => (
    <div className="h-[460px] w-full rounded-2xl bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-600 gap-2 font-semibold">
      <RefreshCw className="h-5 w-5 animate-spin text-blue-600" />
      <span>Loading Indian Railways GIS Corridor Canvas...</span>
    </div>
  )
});

export const LiveCorridorMap: React.FC<LiveCorridorMapProps> = (props) => {
  const [showWeatherOverlay, setShowWeatherOverlay] = useState<boolean>(true);
  const [showSectionOccupancy, setShowSectionOccupancy] = useState<boolean>(true);

  return (
    <div className="glass-panel rounded-2xl p-5 shadow-sm border border-slate-200 space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-3.5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-blue-50 text-blue-600 border border-blue-200">
            <Layers className="h-4 w-4" />
          </div>
          <h2 className="text-sm font-extrabold text-slate-900 uppercase tracking-wider">
            Indian Railways Multi-Layer GIS Corridor Canvas
          </h2>
        </div>

        {/* Map Layer Toggles */}
        <div className="flex items-center gap-2 text-xs">
          <button
            onClick={() => setShowWeatherOverlay(!showWeatherOverlay)}
            className={`px-3 py-1.5 rounded-xl border font-bold flex items-center gap-1.5 transition-all shadow-xs cursor-pointer ${
              showWeatherOverlay
                ? 'bg-blue-50 text-blue-700 border-blue-300'
                : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
            }`}
          >
            <CloudRain className="h-3.5 w-3.5 text-blue-600" />
            <span>Rain Radar Heatmap</span>
          </button>

          <button
            onClick={() => setShowSectionOccupancy(!showSectionOccupancy)}
            className={`px-3 py-1.5 rounded-xl border font-bold flex items-center gap-1.5 transition-all shadow-xs cursor-pointer ${
              showSectionOccupancy
                ? 'bg-emerald-50 text-emerald-700 border-emerald-300'
                : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
            }`}
          >
            <ShieldAlert className="h-3.5 w-3.5 text-emerald-600" />
            <span>Section Block Occupancy</span>
          </button>
        </div>
      </div>

      <LeafletContainer
        {...props}
        showWeatherOverlay={showWeatherOverlay}
        showSectionOccupancy={showSectionOccupancy}
      />
    </div>
  );
};
