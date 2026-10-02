'use client';

import React, { useEffect, useState } from 'react';
import { GitCommit, ArrowRight, AlertTriangle, CheckCircle, ShieldAlert } from 'lucide-react';
import { CascadeGraphResult } from '../../types';
import { api } from '../../services/api';

export const DelayCascadeGraph: React.FC = () => {
  const [graph, setGraph] = useState<CascadeGraphResult | null>(null);

  useEffect(() => {
    api.getCascadeGraph().then(setGraph).catch(console.error);
  }, []);

  if (!graph) return null;

  return (
    <div className="glass-panel rounded-2xl p-6 shadow-sm border border-slate-200">
      <div className="flex items-center justify-between mb-4 border-b border-slate-200 pb-3.5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-indigo-50 text-indigo-700 border border-indigo-200">
            <GitCommit className="h-4 w-4" />
          </div>
          <h2 className="text-sm font-extrabold text-slate-900 uppercase tracking-wider">
            Ripple-Effect Delay Cascade Directed Node Graph
          </h2>
        </div>
        <span className="text-xs font-bold text-slate-600 bg-slate-100 px-2.5 py-1 rounded-full border border-slate-200">
          Downstream Bottleneck Analysis
        </span>
      </div>

      <p className="text-xs text-slate-600 mb-4 font-medium">
        Visualizes how an initial delay at an upstream junction propagates downstream across signal blocks:
      </p>

      {/* Graph Visual Pipeline */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-3 overflow-x-auto p-4 bg-slate-50 rounded-2xl border border-slate-200 shadow-2xs">
        {graph.nodes.map((node, idx) => {
          const edge = graph.edges.find((e) => e.source === node.id);

          return (
            <React.Fragment key={node.id}>
              {/* Node Card */}
              <div className="flex-1 min-w-[160px] p-4 rounded-xl bg-white border border-slate-200 shadow-sm flex flex-col items-center text-center">
                <div className="flex items-center gap-1.5 mb-1.5">
                  <span className="font-black text-xs text-slate-900">{node.label.split(' ')[0]}</span>
                  <span className="text-[11px] text-slate-500 font-bold">({node.id})</span>
                </div>

                <div
                  className={`px-2.5 py-0.5 text-[10px] font-black rounded-full mb-2.5 ${
                    node.status === 'CLEAR'
                      ? 'badge-green'
                      : node.status === 'CAUTION'
                      ? 'badge-yellow'
                      : 'badge-red'
                  }`}
                >
                  {node.status}
                </div>

                <div className="text-xs font-black text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded-md">
                  +{node.delay}m Net Delay
                </div>
              </div>

              {/* Edge Connection Arrow */}
              {edge && (
                <div className="flex flex-col items-center justify-center shrink-0 px-2 my-2 md:my-0">
                  <div className="text-[10px] font-black text-blue-700 max-w-[120px] text-center mb-1 bg-blue-50 border border-blue-200 px-2 py-0.5 rounded-md shadow-2xs">
                    {edge.label}
                  </div>
                  <ArrowRight className="h-4 w-4 text-blue-600 animate-pulse hidden md:block" />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};
