import React, { useState } from 'react';
import { AlertTriangle, Clock, Eye, X, CheckCircle2, ShieldAlert, Sparkles, Filter } from 'lucide-react';

export default function IncidentTimeline({ incidents = [], onClear }) {
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [filterSeverity, setFilterSeverity] = useState('ALL');

  const filteredIncidents = incidents.filter((item) => {
    if (filterSeverity === 'ALL') return true;
    return item.severity === filterSeverity;
  });

  const getSeverityBadge = (severity) => {
    switch (severity) {
      case 'CRITICAL':
        return 'bg-neon-rose/20 text-neon-rose border-neon-rose/40 shadow-neon-rose';
      case 'HIGH':
        return 'bg-neon-amber/20 text-neon-gold border-neon-amber/40 shadow-neon-amber';
      case 'MEDIUM':
        return 'bg-neon-cyan/20 text-neon-cyan border-neon-cyan/40 shadow-neon-cyan';
      default:
        return 'bg-neon-violet/20 text-neon-purple border-neon-violet/40';
    }
  };

  return (
    <div className="flex flex-col h-full rounded-3xl liquid-glass border border-white/20 backdrop-blur-2xl shadow-glass-specular overflow-hidden">
      
      {/* Liquid Header */}
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-white/[0.12] bg-white/[0.04]">
        <div className="flex items-center gap-2">
          <span className="p-1.5 rounded-xl bg-neon-amber/15 border border-neon-amber/30 text-neon-gold shadow-neon-amber">
            <ShieldAlert className="w-3.5 h-3.5" />
          </span>
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-100 font-mono">
            Security Event Feed ({filteredIncidents.length})
          </h3>
        </div>

        <div className="flex items-center gap-2">
          {/* Liquid Glass Filter Pills */}
          <div className="flex items-center gap-1 bg-white/[0.04] p-1 rounded-xl border border-white/10 text-[10px]">
            {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM'].map((level) => (
              <button
                key={level}
                onClick={() => setFilterSeverity(level)}
                className={`px-2 py-0.5 rounded-lg font-mono font-bold transition-all ${
                  filterSeverity === level
                    ? 'liquid-pill-active text-white text-[10px]'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {level}
              </button>
            ))}
          </div>

          {incidents.length > 0 && onClear && (
            <button
              onClick={onClear}
              className="text-[10px] text-slate-400 hover:text-neon-rose font-mono transition px-2 py-1 rounded-lg hover:bg-white/[0.05]"
              title="Clear Incident History"
            >
              Reset
            </button>
          )}
        </div>
      </div>

      {/* Timeline Scroll Area with Liquid Droplets */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2.5 min-h-[220px] max-h-[380px] custom-scrollbar">
        {filteredIncidents.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center py-12 text-slate-400">
            <div className="p-3 rounded-2xl bg-neon-emerald/10 border border-neon-emerald/30 text-neon-mint mb-3 shadow-neon-emerald">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <p className="text-xs font-bold text-slate-200">Zero Infractions Detected</p>
            <p className="text-[11px] text-slate-400 mt-0.5 font-mono">Session complies with all security guidelines.</p>
          </div>
        ) : (
          filteredIncidents.map((incident) => (
            <div
              key={incident.id}
              className="p-3 rounded-2xl liquid-glass-subtle border border-white/10 hover:border-white/30 transition-all duration-200 flex items-start justify-between gap-3 text-xs"
            >
              <div className="space-y-1 flex-1">
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 text-[9px] font-extrabold font-mono rounded-full border ${getSeverityBadge(incident.severity)}`}>
                    {incident.severity}
                  </span>
                  <span className="text-[10px] font-mono text-slate-400 flex items-center gap-1">
                    <Clock className="w-3 h-3 text-slate-400" />
                    {incident.time_display || new Date(incident.timestamp * 1000).toLocaleTimeString()}
                  </span>
                  <span className="font-mono font-bold text-neon-cyan text-[10px]">{incident.code}</span>
                </div>
                <p className="text-slate-200 font-medium leading-relaxed text-xs">{incident.message}</p>
                {incident.head_pose && (
                  <p className="text-[10px] font-mono text-slate-400">
                    Yaw: {incident.head_pose.yaw}° | Pitch: {incident.head_pose.pitch}°
                  </p>
                )}
              </div>

              {incident.snapshot && (
                <button
                  onClick={() => setSelectedIncident(incident)}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl liquid-pill text-neon-cyan text-[10px] font-mono font-bold self-center border border-neon-cyan/40 hover:border-neon-cyan"
                >
                  <Eye className="w-3.5 h-3.5" />
                  <span>Snapshot</span>
                </button>
              )}
            </div>
          ))
        )}
      </div>

      {/* Snapshot Evidence Inspection Liquid Glass Modal */}
      {selectedIncident && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-void/80 backdrop-blur-2xl animate-in fade-in duration-200">
          <div className="relative w-full max-w-lg rounded-3xl liquid-glass border border-white/20 p-6 shadow-glass-specular">
            <div className="flex items-center justify-between pb-3 border-b border-white/[0.12]">
              <div className="flex items-center gap-2">
                <span className={`px-2.5 py-0.5 text-xs font-mono font-bold rounded-full border ${getSeverityBadge(selectedIncident.severity)}`}>
                  {selectedIncident.severity}
                </span>
                <span className="text-xs font-mono text-slate-200">
                  {selectedIncident.code} • {selectedIncident.time_display}
                </span>
              </div>
              <button
                onClick={() => setSelectedIncident(null)}
                className="p-1.5 rounded-xl bg-white/[0.05] hover:bg-white/[0.1] text-slate-300 hover:text-white transition"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="my-4 rounded-2xl overflow-hidden border border-white/15 bg-black/60 flex items-center justify-center shadow-inner">
              {selectedIncident.snapshot ? (
                <img
                  src={selectedIncident.snapshot}
                  alt="Audit Snapshot"
                  className="max-h-72 w-auto object-contain rounded-xl"
                />
              ) : (
                <div className="p-10 text-xs text-slate-400 font-mono">No snapshot frame recorded.</div>
              )}
            </div>

            <p className="text-xs text-slate-200 font-medium leading-relaxed">{selectedIncident.message}</p>
          </div>
        </div>
      )}
    </div>
  );
}
