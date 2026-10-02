'use client';

import React from 'react';
import { MapContainer, TileLayer, Polyline, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { TrainData, WeatherStation } from '../../types';

interface LeafletMapInnerProps {
  trains: TrainData[];
  selectedTrainId: string;
  onSelectTrain: (id: string) => void;
  weatherStations: WeatherStation[];
  showWeatherOverlay: boolean;
  showSectionOccupancy: boolean;
}

// Custom SVG train marker generator with crisp light aesthetics
const createTrainIcon = (number: string, color: string, isSelected: boolean) => {
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="38" height="38">
      <circle cx="12" cy="12" r="11" fill="${color}" fill-opacity="0.25" stroke="${color}" stroke-width="2.5" />
      <circle cx="12" cy="12" r="7" fill="${color}" />
      <path d="M7 10h10v6H7z" fill="#FFFFFF" />
      <circle cx="9" cy="14" r="1.2" fill="${color}" />
      <circle cx="15" cy="14" r="1.2" fill="${color}" />
    </svg>
  `;
  return L.divIcon({
    className: 'custom-train-marker',
    html: `
      <div style="position: relative; display: flex; flex-direction: column; align-items: center; cursor: pointer;">
        <div style="background: rgba(255,255,255,0.95); color: #0F172A; font-weight: 800; font-size: 11px; padding: 2px 7px; border-radius: 6px; border: 1.5px solid ${color}; white-space: nowrap; margin-bottom: -5px; box-shadow: 0 4px 12px rgba(15,23,42,0.15);">
          ${number}
        </div>
        ${svg}
      </div>
    `,
    iconSize: [42, 50],
    iconAnchor: [21, 42]
  });
};

export default function LeafletMapInner({
  trains,
  selectedTrainId,
  onSelectTrain,
  weatherStations,
  showWeatherOverlay,
  showSectionOccupancy
}: LeafletMapInnerProps) {
  // Main North-South Trunk Corridor coordinates
  const trunkCorridor: [number, number][] = [
    [28.6139, 77.2090], // New Delhi
    [27.1577, 78.0076], // Agra Cantt
    [26.2183, 78.1828], // Gwalior
    [25.4484, 78.5685], // Jhansi
    [23.2599, 77.4126], // Bhopal
    [22.6114, 77.7656], // Itarsi
    [21.1458, 79.0882], // Nagpur
    [19.8540, 79.3414], // Balharshah
    [16.5062, 80.6480], // Vijayawada
    [13.0827, 80.2707]  // Chennai
  ];

  // Western Corridor
  const westernCorridor: [number, number][] = [
    [18.9696, 72.8193], // Mumbai Central
    [21.1702, 72.8311], // Surat
    [22.3072, 73.1812], // Vadodara
    [23.0225, 72.5714]  // Ahmedabad
  ];

  // Eastern Corridor (Grand Chord)
  const easternCorridor: [number, number][] = [
    [28.6139, 77.2090], // New Delhi
    [26.4499, 80.3319], // Kanpur
    [25.4358, 81.8463], // Prayagraj
    [25.3176, 82.9739], // Varanasi
    [22.5858, 88.3426]  // Howrah
  ];

  return (
    <div className="h-[460px] w-full rounded-2xl overflow-hidden border border-slate-200 shadow-sm z-0">
      <MapContainer
        center={[22.5, 78.5]}
        zoom={5}
        scrollWheelZoom={true}
        style={{ height: '100%', width: '100%', background: '#F8FAFC' }}
      >
        {/* Completely Free OpenStreetMap Tile Layer (No API Key Required & No Watermarks) */}
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors'
          maxZoom={19}
        />

        {/* Railway Corridor Track Polylines */}
        {showSectionOccupancy && (
          <>
            <Polyline positions={trunkCorridor} pathOptions={{ color: '#059669', weight: 4.5, opacity: 0.85 }} />
            <Polyline positions={westernCorridor} pathOptions={{ color: '#D97706', weight: 4.5, opacity: 0.85 }} />
            <Polyline positions={easternCorridor} pathOptions={{ color: '#2563EB', weight: 4.5, opacity: 0.85 }} />
          </>
        )}

        {/* Weather Radar Hazard Circles derived from india_weather_rainfall_data.xlsx */}
        {showWeatherOverlay &&
          weatherStations.map((st, idx) => {
            if (st.rainfall_mm > 40.0) {
              return (
                <Circle
                  key={idx}
                  center={[st.lat, st.lon]}
                  radius={st.rainfall_mm * 1200}
                  pathOptions={{ color: '#2563EB', fillColor: '#3B82F6', fillOpacity: 0.22, weight: 1.5 }}
                >
                  <Popup>
                    <div className="text-xs space-y-1 p-1">
                      <div className="font-extrabold text-blue-700">{st.station_name} Weather Radar</div>
                      <div className="text-slate-700 font-medium">Rainfall: <strong className="text-slate-900">{st.rainfall_mm} mm/day</strong></div>
                      <div className="text-slate-700 font-medium">Min Temp: <strong className="text-slate-900">{st.min_temp}°C</strong></div>
                      <div className="text-slate-700 font-medium">Wind: <strong className="text-slate-900">{st.wind_speed} km/h</strong></div>
                      <div className="text-[11px] text-amber-700 font-bold bg-amber-50 border border-amber-200 px-2 py-0.5 rounded-md mt-1">
                        TSR Waterlogging Hazard Active
                      </div>
                    </div>
                  </Popup>
                </Circle>
              );
            }
            return null;
          })}

        {/* Moving Train Rake Markers */}
        {trains.map((t) => {
          const isSelected = t.id === selectedTrainId;
          const color = t.section_occupancy === 'GREEN' ? '#059669' : t.section_occupancy === 'YELLOW' ? '#D97706' : '#DC2626';
          const icon = createTrainIcon(t.number, color, isSelected);

          return (
            <Marker
              key={t.id}
              position={[t.lat, t.lon]}
              icon={icon}
              eventHandlers={{
                click: () => onSelectTrain(t.id)
              }}
            >
              <Popup>
                <div className="p-1.5 text-xs space-y-1.5 max-w-[220px]">
                  <div className="font-extrabold text-slate-900 border-b border-slate-100 pb-1.5 flex justify-between items-center">
                    <span>{t.number} {t.name}</span>
                    <span 
                      className="px-1.5 py-0.5 rounded text-[10px] font-black text-white" 
                      style={{ backgroundColor: color }}
                    >
                      {t.section_occupancy}
                    </span>
                  </div>
                  <div className="text-slate-700 font-medium">Current Station: <strong className="text-blue-700 font-bold">{t.current_station}</strong></div>
                  <div className="text-slate-700 font-medium">Live Speed: <strong className="text-slate-900">{t.eta_analysis?.effective_speed_kmh || 0} km/h</strong></div>
                  <div className="text-slate-700 font-medium">Est Delay: <strong className="text-amber-700 font-bold">~{Math.round(t.eta_analysis?.net_delay_mins || 0)} mins</strong></div>
                  <div className="text-slate-700 font-medium">Confidence Band: <strong className="text-emerald-700 font-bold">{t.eta_analysis?.probabilistic_eta?.confidence_score_pct}%</strong></div>
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
}
