'use client';

import React, { useState } from 'react';
import { GitCompare, Clock, ShieldAlert, CheckCircle, AlertTriangle, ArrowRight, Train } from 'lucide-react';
import { TrainData, ConnectionRiskResult } from '../../types';
import { api } from '../../services/api';

interface ConnectionRiskEvaluatorProps {
  currentTrain: TrainData | null;
  allTrains: TrainData[];
  selectedSimDate: string;
}

export const ConnectionRiskEvaluator: React.FC<ConnectionRiskEvaluatorProps> = ({
  currentTrain,
  allTrains,
  selectedSimDate
}) => {
  const [connectingTrainId, setConnectingTrainId] = useState<string>('12009');
  const [scheduledBuffer, setScheduledBuffer] = useState<number>(40);
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<ConnectionRiskResult | null>(null);

  const handleEvaluate = async () => {
    if (!currentTrain) return;
    setLoading(true);
    try {
      const res = await api.evaluateConnectionRisk(
        currentTrain.id,
        connectingTrainId,
        scheduledBuffer,
        selectedSimDate
      );
      setResult(res);
    } catch (e) {
      console.error('Connection risk evaluation error', e);
    } finally {
      setLoading(false);
    }
  };

  if (!currentTrain) return null;

  return (
    <div className="glass-panel rounded-2xl p-6 shadow-sm border border-slate-200">
      <div className="flex items-center gap-2 mb-3">
        <div className="p-1.5 rounded-lg bg-indigo-50 text-indigo-600 border border-indigo-200">
          <GitCompare className="h-4 w-4" />
        </div>
        <h2 className="text-sm font-extrabold text-slate-900 uppercase tracking-wider">
          Connecting Train Transfer Risk Evaluator
        </h2>
      </div>

      <p className="text-xs text-slate-600 mb-4 font-medium">
        Calculate whether your train delay will impact your onward connection at upcoming junction stations:
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
        
        {/* Current Arriving Train */}
        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 shadow-xs">
          <label className="text-[10px] font-extrabold text-slate-500 uppercase block mb-1">INCOMING TRAIN</label>
          <div className="font-extrabold text-xs text-slate-900">{currentTrain.number} {currentTrain.name}</div>
          <div className="text-[11px] text-amber-700 font-bold mt-0.5">
            Est. Delay: ~{Math.round(currentTrain.eta_analysis?.net_delay_mins || 0)} mins
          </div>
        </div>

        {/* Connecting Train Dropdown */}
        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 shadow-xs">
          <label className="text-[10px] font-extrabold text-slate-500 uppercase block mb-1">CONNECTING TRAIN</label>
          <select
            value={connectingTrainId}
            onChange={(e) => setConnectingTrainId(e.target.value)}
            className="w-full bg-white text-xs font-bold text-slate-800 p-1.5 rounded-lg border border-slate-300 focus:outline-none shadow-2xs"
          >
            {allTrains
              .filter((t) => t.id !== currentTrain.id)
              .map((t) => (
                <option key={t.id} value={t.id}>
                  {t.number} - {t.name}
                </option>
              ))}
          </select>
        </div>

        {/* Scheduled Transfer Buffer Mins */}
        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 shadow-xs">
          <label className="text-[10px] font-extrabold text-slate-500 uppercase block mb-1">SCHEDULED BUFFER (MINS)</label>
          <div className="flex items-center gap-2">
            <input
              type="number"
              min={10}
              max={180}
              value={scheduledBuffer}
              onChange={(e) => setScheduledBuffer(Number(e.target.value))}
              className="w-20 bg-white border border-slate-300 rounded-lg px-2.5 py-1 text-xs font-extrabold text-slate-900 shadow-2xs"
            />
            <button
              onClick={handleEvaluate}
              disabled={loading}
              className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-extrabold text-xs py-1.5 px-3 rounded-lg transition-all shadow-md shadow-blue-500/20 cursor-pointer"
            >
              {loading ? 'Evaluating...' : 'Evaluate Risk'}
            </button>
          </div>
        </div>
      </div>

      {/* Evaluation Results Card */}
      {result && (
        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm animate-fadeIn space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {result.risk_level === 'SAFE' ? (
                <div className="p-2 rounded-xl bg-emerald-50 text-emerald-600 border border-emerald-200">
                  <CheckCircle className="h-6 w-6" />
                </div>
              ) : result.risk_level === 'MODERATE RISK' ? (
                <div className="p-2 rounded-xl bg-amber-50 text-amber-600 border border-amber-200">
                  <AlertTriangle className="h-6 w-6" />
                </div>
              ) : (
                <div className="p-2 rounded-xl bg-rose-50 text-rose-600 border border-rose-200">
                  <ShieldAlert className="h-6 w-6" />
                </div>
              )}
              <div>
                <span className="font-black text-sm text-slate-900">{result.risk_level}</span>
                <p className="text-xs text-slate-600 font-medium">{result.risk_message}</p>
              </div>
            </div>

            <div className="text-right">
              <div className="text-[10px] text-slate-500 font-bold uppercase">REALIZED BUFFER</div>
              <div className="font-black text-lg" style={{ color: result.risk_color }}>
                {result.realized_buffer_mins} mins
              </div>
            </div>
          </div>

          {/* Suggested Alternative Trains */}
          {result.suggested_alternatives && result.suggested_alternatives.length > 0 && (
            <div className="border-t border-slate-100 pt-3">
              <h4 className="text-[11px] font-extrabold text-slate-700 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
                <Train className="h-3.5 w-3.5 text-blue-600" />
                Recommended Alternative Connections
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {result.suggested_alternatives.map((alt, idx) => (
                  <div key={idx} className="p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs shadow-2xs">
                    <div>
                      <div className="font-extrabold text-slate-900">{alt.train_number} {alt.train_name}</div>
                      <div className="text-[11px] text-slate-500 font-medium">Dep: {alt.dep_time} • Seats: {alt.available_seats}</div>
                    </div>
                    <span className="px-2.5 py-0.5 text-[11px] font-extrabold rounded-md bg-blue-100 text-blue-800 border border-blue-200">
                      +{alt.buffer_mins}m buffer
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
