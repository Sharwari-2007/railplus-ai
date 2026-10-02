'use client';

import React, { useEffect, useState } from 'react';
import { Navbar } from '../components/Navbar';
import { PassengerView } from '../components/Passenger/PassengerView';
import { ControllerCockpitView } from '../components/Controller/ControllerCockpitView';
import { TrainData, WeatherStation, HistoricDay } from '../types';
import { api } from '../services/api';
import { wsClient } from '../services/websocket';

export default function Home() {
  const [currentView, setCurrentView] = useState<'PASSENGER' | 'CONTROLLER'>('PASSENGER');
  const [trains, setTrains] = useState<TrainData[]>([]);
  const [selectedTrainId, setSelectedTrainId] = useState<string>('12951');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedSimDate, setSelectedSimDate] = useState<string>('2025-07-15');
  const [weatherStations, setWeatherStations] = useState<WeatherStation[]>([]);
  const [historicDays, setHistoricDays] = useState<HistoricDay[]>([]);
  const [wsConnected, setWsConnected] = useState<boolean>(false);

  // Initial REST data fetch
  useEffect(() => {
    api.getTrains(selectedSimDate).then((data) => {
      setTrains(data);
      if (data.length > 0 && !selectedTrainId) {
        setSelectedTrainId(data[0].id);
      }
    }).catch(console.error);

    api.getWeatherStations(selectedSimDate).then(setWeatherStations).catch(console.error);
    api.getHistoricDays().then(setHistoricDays).catch(console.error);
  }, [selectedSimDate]);

  // Connect WebSocket for real-time telemetry feed
  useEffect(() => {
    wsClient.connect((status) => setWsConnected(status));

    const unsubscribe = wsClient.subscribe((msg) => {
      if (msg.trains && msg.trains.length > 0) {
        setTrains(msg.trains);
      }
    });

    return () => {
      unsubscribe();
      wsClient.disconnect();
    };
  }, []);

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-900 flex flex-col font-sans relative overflow-x-hidden">
      
      {/* Radiant ambient gradient blurs for light aesthetic */}
      <div className="fixed -top-40 -left-40 w-96 h-96 bg-blue-200/50 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed top-1/3 -right-40 w-96 h-96 bg-cyan-200/40 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed -bottom-40 left-1/3 w-96 h-96 bg-indigo-100/60 rounded-full blur-3xl pointer-events-none" />

      {/* Persistent Glassmorphic Header Navigation Bar */}
      <Navbar
        currentView={currentView}
        onViewChange={setCurrentView}
        selectedSimDate={selectedSimDate}
        onSimDateChange={setSelectedSimDate}
        historicDays={historicDays}
        wsConnected={wsConnected}
      />

      {/* Main App Container */}
      <main className="relative z-10 flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 space-y-6">
        
        {currentView === 'PASSENGER' ? (
          <PassengerView
            trains={trains}
            selectedTrainId={selectedTrainId}
            onSelectTrain={setSelectedTrainId}
            searchQuery={searchQuery}
            onSearchChange={setSearchQuery}
            selectedSimDate={selectedSimDate}
          />
        ) : (
          <ControllerCockpitView
            trains={trains}
            selectedTrainId={selectedTrainId}
            onSelectTrain={setSelectedTrainId}
            weatherStations={weatherStations}
            selectedSimDate={selectedSimDate}
          />
        )}

      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-slate-200 bg-white/80 backdrop-blur-md py-4 text-center text-xs text-slate-500 mt-8">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between px-4 gap-2">
          <span className="font-semibold text-slate-700">RailPulse AI • SIH26028 Ministry of Railways</span>
          <span>Powered by FastAPI, LightGBM, Leaflet GIS & Next.js</span>
        </div>
      </footer>

    </div>
  );
}
