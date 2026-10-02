'use client';

import React, { useEffect, useState } from 'react';
import { CloudRain, Wind, Thermometer, FileSpreadsheet } from 'lucide-react';
import { WeatherStation } from '../../types';
import { api } from '../../services/api';

interface WeatherImpactPanelProps {
  selectedSimDate: string;
}

export const WeatherImpactPanel: React.FC<WeatherImpactPanelProps> = ({ selectedSimDate }) => {
  const [stations, setStations] = useState<WeatherStation[]>([]);

  useEffect(() => {
    api.getWeatherStations(selectedSimDate).then(setStations).catch(console.error);
  }, [selectedSimDate]);

  const rainHazards = stations.filter((s) => s.rainfall_mm > 50.0);
  const fogHazards = stations.filter((s) => s.min_temp < 8.0 && s.air_pressure > 1018.0);
  const windHazards = stations.filter((s) => s.wind_speed > 45.0);

  return (
    <div className="glass-panel rounded-2xl p-6 shadow-sm border border-slate-200">
      <div className="flex items-center justify-between mb-4 border-b border-slate-200 pb-3.5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-blue-50 text-blue-700 border border-blue-200">
            <CloudRain className="h-4 w-4" />
          </div>
          <h2 className="text-sm font-extrabold text-slate-900 uppercase tracking-wider">
            Meteorological Telemetry & TSR Hazard Radar
          </h2>
        </div>
        <span className="text-xs text-slate-600 flex items-center gap-1.5 font-mono bg-slate-100 px-2.5 py-1 rounded-full border border-slate-200">
          <FileSpreadsheet className="h-3.5 w-3.5 text-emerald-600" /> india_weather_rainfall_data.xlsx
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4">
        
        {/* Rainfall Waterlogging Counter */}
        <div className="p-4 rounded-xl bg-blue-50/60 border border-blue-200 flex items-center justify-between shadow-xs">
          <div>
            <div className="text-[10px] text-blue-700 font-extrabold uppercase">WATERLOGGING HAZARDS (&gt;50mm)</div>
            <div className="text-2xl font-black text-blue-900">{rainHazards.length} Stations</div>
          </div>
          <div className="p-2 rounded-xl bg-blue-100 text-blue-600">
            <CloudRain className="h-6 w-6" />
          </div>
        </div>

        {/* Fog Protocol Speed Cap Counter */}
        <div className="p-4 rounded-xl bg-amber-50/60 border border-amber-200 flex items-center justify-between shadow-xs">
          <div>
            <div className="text-[10px] text-amber-700 font-extrabold uppercase">FOG PROTOCOL CAPS (60 km/h)</div>
            <div className="text-2xl font-black text-amber-900">{fogHazards.length} Stations</div>
          </div>
          <div className="p-2 rounded-xl bg-amber-100 text-amber-600">
            <Thermometer className="h-6 w-6" />
          </div>
        </div>

        {/* High Wind Caution Counter */}
        <div className="p-4 rounded-xl bg-cyan-50/60 border border-cyan-200 flex items-center justify-between shadow-xs">
          <div>
            <div className="text-[10px] text-cyan-700 font-extrabold uppercase">HIGH WIND CAUTIONS (&gt;45km/h)</div>
            <div className="text-2xl font-black text-cyan-900">{windHazards.length} Stations</div>
          </div>
          <div className="p-2 rounded-xl bg-cyan-100 text-cyan-600">
            <Wind className="h-6 w-6" />
          </div>
        </div>
      </div>

      {/* Weather Station Highlights Table */}
      <div className="overflow-x-auto bg-white rounded-xl border border-slate-200 p-2">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-slate-200 text-slate-500 text-[10px] font-black uppercase">
              <th className="py-2.5 px-3">Station</th>
              <th className="py-2.5 px-3">Rainfall</th>
              <th className="py-2.5 px-3">Min Temp</th>
              <th className="py-2.5 px-3">Wind</th>
              <th className="py-2.5 px-3">Pressure</th>
              <th className="py-2.5 px-3">TSR Restriction</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {stations.slice(0, 6).map((st, idx) => {
              const isHeavyRain = st.rainfall_mm > 50.0;
              const isFog = st.min_temp < 8.0 && st.air_pressure > 1018.0;

              return (
                <tr key={idx} className="hover:bg-slate-50/80 text-slate-800 font-semibold">
                  <td className="py-2.5 px-3 font-extrabold text-slate-900">{st.station_name}</td>
                  <td className="py-2.5 px-3">{st.rainfall_mm} mm</td>
                  <td className="py-2.5 px-3">{st.min_temp}°C</td>
                  <td className="py-2.5 px-3">{st.wind_speed} km/h</td>
                  <td className="py-2.5 px-3">{st.air_pressure} hPa</td>
                  <td className="py-2.5 px-3">
                    {isHeavyRain ? (
                      <span className="badge-red px-2 py-0.5 rounded-md text-[10px] font-black">
                        TSR Derate 40%-60%
                      </span>
                    ) : isFog ? (
                      <span className="badge-yellow px-2 py-0.5 rounded-md text-[10px] font-black">
                        Fog Cap 60 km/h
                      </span>
                    ) : (
                      <span className="text-slate-400 font-medium text-[10px]">Normal MPS</span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
