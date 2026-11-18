import React from 'react';
import { Bell, Clock, Building2, CheckCircle2, AlertTriangle, X, Radio } from 'lucide-react';

export default function NotificationCenterModal({
  isOpen,
  onClose,
  notifications = []
}) {
  if (!isOpen) return null;

  const getPriorityBadge = (p) => {
    switch (p) {
      case 'URGENT':
        return 'bg-neon-rose/20 text-neon-rose border-neon-rose/40 shadow-neon-rose';
      case 'HIGH':
        return 'bg-neon-amber/20 text-neon-gold border-neon-amber/40 shadow-neon-amber';
      default:
        return 'bg-neon-cyan/20 text-neon-cyan border-neon-cyan/40 shadow-neon-cyan';
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-void/80 backdrop-blur-3xl animate-in fade-in duration-200">
      <div className="relative w-full max-w-lg rounded-3xl liquid-glass border border-white/20 shadow-glass-specular overflow-hidden flex flex-col max-h-[85vh]">
        
        {/* Header */}
        <div className="p-5 bg-white/[0.04] border-b border-white/[0.12] flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-2xl bg-neon-amber/20 text-neon-gold border border-neon-amber/30 shadow-neon-amber">
              <Bell className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white">Department Notification Center</h3>
              <p className="text-[11px] text-slate-300 font-mono">Real-time examination alerts</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1.5 rounded-xl liquid-pill text-slate-300 hover:text-white transition">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Notifications Stream */}
        <div className="flex-1 overflow-y-auto p-5 space-y-3.5 divide-y divide-white/[0.08] custom-scrollbar">
          {notifications.length === 0 ? (
            <div className="p-12 text-center text-xs text-slate-400 font-mono">
              Zero unread announcements for your department.
            </div>
          ) : (
            notifications.map((n) => (
              <div key={n.id} className="pt-3.5 first:pt-0 space-y-1.5 text-xs font-mono">
                <div className="flex items-center justify-between gap-2">
                  <span className={`px-2.5 py-0.5 rounded-full text-[9px] font-bold border ${getPriorityBadge(n.priority)}`}>
                    {n.priority}
                  </span>
                  <span className="text-[10px] text-slate-400 flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {n.time_display}
                  </span>
                </div>

                <h4 className="font-bold text-white text-xs font-sans">{n.title}</h4>
                <p className="text-slate-200 leading-relaxed text-[11px] font-sans font-medium">{n.message}</p>

                <div className="pt-1 flex items-center gap-1 text-[10px] text-neon-cyan font-bold">
                  <Building2 className="w-3 h-3" />
                  <span>Target: {n.department}</span>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="p-4 bg-white/[0.03] border-t border-white/[0.12] text-center">
          <button
            onClick={onClose}
            className="w-full py-2.5 rounded-2xl liquid-pill hover:bg-white/[0.1] text-slate-200 text-xs font-bold transition font-mono"
          >
            Acknowledge & Close
          </button>
        </div>
      </div>
    </div>
  );
}
