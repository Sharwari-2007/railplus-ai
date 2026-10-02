'use client';

import React, { useState } from 'react';
import { Search, Train, Clock, ArrowRight, Sparkles, Zap, Shield } from 'lucide-react';
import { TrainData } from '../../types';

interface TrainSelectorProps {
  trains: TrainData[];
  selectedTrainId: string;
  onSelectTrain: (trainId: string) => void;
  searchQuery: string;
  onSearchChange: (q: string) => void;
}

export const TrainSelector: React.FC<TrainSelectorProps> = ({
  trains,
  selectedTrainId,
  onSelectTrain,
  searchQuery,
  onSearchChange
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');

  const categories = [
    { id: 'ALL', label: 'All Trains', icon: Train },
    { id: 'Vande Bharat', label: 'Vande Bharat', icon: Zap },
    { id: 'Rajdhani', label: 'Rajdhani', icon: Sparkles },
    { id: 'Shatabdi', label: 'Shatabdi & Tejas', icon: Shield },
    { id: 'Duronto', label: 'Duronto', icon: Clock },
    { id: 'Superfast', label: 'Superfast & Mail', icon: ArrowRight }
  ];

  const filteredTrains = trains.filter((t) => {
    const matchesSearch =
      t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.number.includes(searchQuery) ||
      t.origin.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.destination.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.current_station.toLowerCase().includes(searchQuery.toLowerCase());

    if (!matchesSearch) return false;

    if (selectedCategory === 'ALL') return true;
    if (selectedCategory === 'Vande Bharat') return t.type.includes('Vande Bharat');
    if (selectedCategory === 'Rajdhani') return t.type.includes('Rajdhani');
    if (selectedCategory === 'Shatabdi') return t.type.includes('Shatabdi') || t.type.includes('Tejas');
    if (selectedCategory === 'Duronto') return t.type.includes('Duronto');
    if (selectedCategory === 'Superfast') return t.type.includes('Superfast') || t.type.includes('Mail') || t.type.includes('Garib');

    return true;
  });

  return (
    <div className="glass-panel rounded-2xl p-5 shadow-sm border border-slate-200 space-y-4">
      
      {/* Top Header & Search Bar */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-blue-50 border border-blue-200 text-blue-600 shadow-2xs">
            <Train className="h-5 w-5" />
          </div>
          <div>
            <h2 className="text-sm font-extrabold text-slate-900 uppercase tracking-wider">
              Pan-India Live Train Fleet & ETA Monitor
            </h2>
            <p className="text-[11px] text-slate-500 font-medium">
              Tracking {trains.length} trains across Golden Quadrilateral & Trunk Corridors
            </p>
          </div>
        </div>

        {/* Live Search Input */}
        <div className="relative w-full md:w-80">
          <Search className="absolute left-3.5 top-2.5 h-4 w-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search by train no., name, station (e.g. 22436, Varanasi)..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-full glass-input rounded-xl pl-9 pr-3.5 py-2 text-xs font-semibold focus:outline-none shadow-xs"
          />
        </div>
      </div>

      {/* Category Filter Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
        {categories.map((cat) => {
          const Icon = cat.icon;
          const count = trains.filter((t) => {
            if (cat.id === 'ALL') return true;
            if (cat.id === 'Vande Bharat') return t.type.includes('Vande Bharat');
            if (cat.id === 'Rajdhani') return t.type.includes('Rajdhani');
            if (cat.id === 'Shatabdi') return t.type.includes('Shatabdi') || t.type.includes('Tejas');
            if (cat.id === 'Duronto') return t.type.includes('Duronto');
            if (cat.id === 'Superfast') return t.type.includes('Superfast') || t.type.includes('Mail') || t.type.includes('Garib');
            return true;
          }).length;

          const isActive = selectedCategory === cat.id;

          return (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl font-bold whitespace-nowrap transition-all shadow-xs cursor-pointer ${
                isActive
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                  : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-50'
              }`}
            >
              <Icon className={`h-3.5 w-3.5 ${isActive ? 'text-white' : 'text-blue-600'}`} />
              <span>{cat.label}</span>
              <span
                className={`px-1.5 py-0.2 rounded-full text-[10px] font-extrabold ${
                  isActive ? 'bg-blue-800 text-white' : 'bg-slate-100 text-slate-600'
                }`}
              >
                {count}
              </span>
            </button>
          );
        })}
      </div>

      {/* Train Selector Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 max-h-[460px] overflow-y-auto pr-1">
        {filteredTrains.length > 0 ? (
          filteredTrains.map((t) => {
            const isSelected = t.id === selectedTrainId;
            const delay = t.eta_analysis?.net_delay_mins || 0;
            const speed = t.eta_analysis?.effective_speed_kmh || t.max_speed;
            
            return (
              <div
                key={t.id}
                onClick={() => onSelectTrain(t.id)}
                className={`cursor-pointer rounded-xl p-3.5 border transition-all duration-200 ${
                  isSelected
                    ? 'bg-gradient-to-br from-blue-50 via-indigo-50/70 to-white border-blue-500 shadow-md shadow-blue-500/15 ring-2 ring-blue-500/25 scale-[1.01]'
                    : 'bg-white border-slate-200 hover:border-blue-300 hover:bg-slate-50/80 shadow-xs'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="px-2 py-0.5 text-[11px] font-black rounded-md bg-blue-100 text-blue-800 border border-blue-200">
                    {t.number}
                  </span>
                  <span
                    className={`px-2 py-0.5 text-[10px] font-black rounded-full ${
                      delay === 0
                        ? 'badge-green'
                        : delay < 15
                        ? 'badge-yellow'
                        : 'badge-red'
                    }`}
                  >
                    {delay === 0 ? 'On Time' : `+${Math.round(delay)}m Delay`}
                  </span>
                </div>

                <div className="text-[10px] font-extrabold text-indigo-700 uppercase tracking-wide truncate">
                  {t.type}
                </div>

                <h3 className="text-xs font-black text-slate-900 truncate mb-1">
                  {t.name}
                </h3>

                <div className="flex items-center text-[11px] text-slate-600 gap-1 truncate mb-3 font-medium">
                  <span className="truncate">{t.origin.split(' ')[0]}</span>
                  <ArrowRight className="h-3 w-3 shrink-0 text-slate-400" />
                  <span className="truncate">{t.destination.split(' ')[0]}</span>
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-500 border-t border-slate-100 pt-2.5">
                  <span className="flex items-center gap-1 font-semibold truncate max-w-[130px]">
                    <Clock className="h-3 w-3 text-blue-600 shrink-0" />
                    <span className="truncate">At: {t.current_station.split(' ')[0]}</span>
                  </span>
                  <span className="font-black text-slate-800 shrink-0">
                    {speed} km/h
                  </span>
                </div>
              </div>
            );
          })
        ) : (
          <div className="col-span-full py-8 text-center text-slate-500 text-xs font-semibold">
            No trains found matching "{searchQuery}". Try searching by train number (e.g. 12951) or station.
          </div>
        )}
      </div>
    </div>
  );
};
