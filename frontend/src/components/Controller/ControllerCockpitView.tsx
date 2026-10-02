'use client';

import React from 'react';
import { LiveCorridorMap } from '../Map/LiveCorridorMap';
import { WhatIfSimulator } from './WhatIfSimulator';
import { DelayCascadeGraph } from './DelayCascadeGraph';
import { PlatformClashPredictor } from './PlatformClashPredictor';
import { WeatherImpactPanel } from './WeatherImpactPanel';
import { TrainData, WeatherStation } from '../../types';

interface ControllerCockpitViewProps {
  trains: TrainData[];
  selectedTrainId: string;
  onSelectTrain: (id: string) => void;
  weatherStations: WeatherStation[];
  selectedSimDate: string;
}

export const ControllerCockpitView: React.FC<ControllerCockpitViewProps> = ({
  trains,
  selectedTrainId,
  onSelectTrain,
  weatherStations,
  selectedSimDate
}) => {
  return (
    <div className="space-y-6">
      
      {/* 1. Interactive Multi-Layer GIS Corridor Map Canvas */}
      <LiveCorridorMap
        trains={trains}
        selectedTrainId={selectedTrainId}
        onSelectTrain={onSelectTrain}
        weatherStations={weatherStations}
      />

      {/* 2. Interactive "What-If" Precedence & Emergency Block Simulator */}
      <WhatIfSimulator selectedSimDate={selectedSimDate} />

      {/* 3. Ripple-Effect Delay Cascade Directed Node Graph */}
      <DelayCascadeGraph />

      {/* 4. Platform Clash & Loop Line Turnaround Predictor */}
      <PlatformClashPredictor />

      {/* 5. Meteorological Telemetry Radar & TSR Speed Restriction Panel */}
      <WeatherImpactPanel selectedSimDate={selectedSimDate} />

    </div>
  );
};
