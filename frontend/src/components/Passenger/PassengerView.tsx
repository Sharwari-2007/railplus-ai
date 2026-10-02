'use client';

import React from 'react';
import { TrainSelector } from './TrainSelector';
import { EtaCard } from './EtaCard';
import { RouteTimelineBar } from './RouteTimelineBar';
import { ConnectionRiskEvaluator } from './ConnectionRiskEvaluator';
import { TrainData } from '../../types';

interface PassengerViewProps {
  trains: TrainData[];
  selectedTrainId: string;
  onSelectTrain: (id: string) => void;
  searchQuery: string;
  onSearchChange: (q: string) => void;
  selectedSimDate: string;
}

export const PassengerView: React.FC<PassengerViewProps> = ({
  trains,
  selectedTrainId,
  onSelectTrain,
  searchQuery,
  onSearchChange,
  selectedSimDate
}) => {
  const selectedTrain = trains.find((t) => t.id === selectedTrainId) || trains[0] || null;

  return (
    <div className="space-y-6">
      
      {/* 1. Train Selector & Search Bar */}
      <TrainSelector
        trains={trains}
        selectedTrainId={selectedTrainId}
        onSelectTrain={onSelectTrain}
        searchQuery={searchQuery}
        onSearchChange={onSearchChange}
      />

      {/* 2. Dynamic ETA Display (Probabilistic Band & XAI Delay Card) */}
      <EtaCard train={selectedTrain} />

      {/* 3. Interactive Route Milestone Timeline */}
      <RouteTimelineBar train={selectedTrain} />

      {/* 4. Connection Risk Evaluator */}
      <ConnectionRiskEvaluator
        currentTrain={selectedTrain}
        allTrains={trains}
        selectedSimDate={selectedSimDate}
      />

    </div>
  );
};
