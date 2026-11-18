import React, { useState, useMemo } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  Monitor,
  AppWindow,
  Copy,
  Terminal,
  AlertTriangle,
  Clock,
  CheckCircle2,
  XCircle,
  Download,
  Filter,
  Flame,
  Zap,
  Lock,
  Eye,
  Maximize2,
  Minimize2,
  ArrowRight
} from 'lucide-react';

export default function FocusSecurityTab({
  focusEvents = [],
  isWindowFocused = true,
  warningsCount = {},
  totalLostFocusDuration = 0,
  onSimulateEvent,
  onClearEvents
}) {
  const [filterType, setFilterType] = useState('ALL');
  const [searchTerm, setSearchTerm] = useState('');

  // Calculate telemetry counters
  const stats = useMemo(() => {
    let tabSwitches = 0;
    let windowBlurs = 0;
    let fullscreenExits = 0;
    let clipboardAttempts = 0;
    let hotkeyViolations = 0;
    let audioViolations = 0;

    focusEvents.forEach((evt) => {
      const type = (evt.type || '').toUpperCase();
      if (type.includes('TAB_SWITCH') || type.includes('VISIBILITY')) tabSwitches++;
      else if (type.includes('BLUR') || type.includes('MINIMIZE')) windowBlurs++;
      else if (type.includes('FULLSCREEN')) fullscreenExits++;
      else if (type.includes('COPY') || type.includes('PASTE') || type.includes('CLIPBOARD')) clipboardAttempts++;
      else if (type.includes('HOTKEY')) hotkeyViolations++;
      else if (type.includes('VOICE') || type.includes('AUDIO')) audioViolations++;
    });

    return {
      total: focusEvents.length,
      tabSwitches,
      windowBlurs,
      fullscreenExits,
      clipboardAttempts,
      hotkeyViolations,
      audioViolations
    };
  }, [focusEvents]);

  // Filtered event log
  const filteredEvents = useMemo(() => {
    return focusEvents.filter((item) => {
      const matchesFilter =
        filterType === 'ALL' ||
        (filterType === 'TAB_SWITCH' && (item.type?.includes('TAB') || item.type?.includes('VISIBILITY'))) ||
        (filterType === 'WINDOW_BLUR' && (item.type?.includes('BLUR') || item.type?.includes('MINIMIZE'))) ||
        (filterType === 'FULLSCREEN' && item.type?.includes('FULLSCREEN')) ||
        (filterType === 'CLIPBOARD_HOTKEY' && (item.type?.includes('COPY') || item.type?.includes('PASTE') || item.type?.includes('HOTKEY')));

      const matchesSearch =
        !searchTerm ||
        item.message?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.type?.toLowerCase().includes(searchTerm.toLowerCase());

      return matchesFilter && matchesSearch;
    });
  }, [focusEvents, filterType, searchTerm]);

  // Export logs to JSON
  const handleExportJSON = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(focusEvents, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `browser_focus_security_audit_${Date.now()}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  const getSeverityStyle = (severity) => {
    switch (severity) {
      case 'CRITICAL':
        return 'bg-neon-rose/20 text-neon-rose border-neon-rose/50 shadow-neon-rose';
      case 'HIGH':
        return 'bg-neon-amber/20 text-neon-gold border-neon-amber/50 shadow-neon-amber';
      case 'MEDIUM':
        return 'bg-neon-cyan/20 text-neon-cyan border-neon-cyan/50 shadow-neon-cyan';
      default:
        return 'bg-neon-violet/20 text-neon-purple border-neon-violet/40';
    }
  };

  const getEventIcon = (type) => {
    const t = (type || '').toUpperCase();
    if (t.includes('TAB')) return AppWindow;
    if (t.includes('BLUR') || t.includes('MINIMIZE')) return Minimize2;
    if (t.includes('FULLSCREEN')) return Maximize2;
    if (t.includes('COPY') || t.includes('PASTE')) return Copy;
    if (t.includes('HOTKEY')) return Terminal;
    return AlertTriangle;
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* ----------------------------------------------------------------- */}
      {/* Top Banner: Real-Time Focus Health Bar & Status                   */}
      {/* ----------------------------------------------------------------- */}
      <div className="liquid-glass rounded-3xl p-5 sm:p-7 border border-white/20 shadow-glass-specular backdrop-blur-2xl relative overflow-hidden">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-5 relative z-10">
          <div className="space-y-2">
            <div className="flex items-center gap-3">
              <span className="p-2.5 rounded-2xl bg-neon-cyan/15 border border-neon-cyan/30 text-neon-cyan shadow-neon-cyan">
                <Monitor className="w-6 h-6" />
              </span>
              <div>
                <h2 className="text-lg sm:text-xl font-black text-white tracking-tight flex items-center gap-2">
                  Browser & Focus Security Telemetry
                  <span className="text-[10px] font-mono uppercase px-2.5 py-0.5 rounded-full bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/40">
                    Live Surveillance
                  </span>
                </h2>
                <p className="text-xs text-slate-300 font-mono mt-0.5">
                  Real-time telemetry tracking window focus, application switching, minimization, and lockdown adherence.
                </p>
              </div>
            </div>
          </div>

          {/* Current Real-Time Focus State Pill */}
          <div className="flex flex-wrap items-center gap-3">
            <div className={`px-4 py-2 rounded-2xl border font-mono text-xs font-black flex items-center gap-2.5 shadow-lg transition-all ${
              isWindowFocused
                ? 'bg-neon-emerald/20 border-neon-emerald text-neon-mint shadow-neon-emerald'
                : 'bg-neon-rose/25 border-neon-rose text-neon-rose shadow-neon-rose animate-pulse'
            }`}>
              <span className={`w-3 h-3 rounded-full ${
                isWindowFocused ? 'bg-neon-mint animate-pulse' : 'bg-neon-rose animate-ping'
              }`} />
              <span>
                {isWindowFocused
                  ? '🟢 ACTIVE & FOCUSED ON EXAM WINDOW'
                  : '🔴 FOCUS LOST / WINDOW BLURRED / MINIMIZED'}
              </span>
            </div>

            <div className="px-3.5 py-2 rounded-2xl liquid-pill border-white/10 text-xs font-mono text-slate-300 flex items-center gap-2">
              <Clock className="w-4 h-4 text-neon-gold" />
              <span>Lost Focus Time: <strong className="text-white">{totalLostFocusDuration}s</strong></span>
            </div>
          </div>
        </div>
      </div>

      {/* ----------------------------------------------------------------- */}
      {/* 4 Telemetry Counters Grid                                         */}
      {/* ----------------------------------------------------------------- */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Tab Switches */}
        <div className="liquid-glass rounded-2xl p-4 sm:p-5 border border-white/15 backdrop-blur-xl relative overflow-hidden group hover:border-neon-cyan/40 transition">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-wider font-bold">Tab Switches</span>
            <div className="p-2 rounded-xl bg-neon-cyan/15 text-neon-cyan border border-neon-cyan/30">
              <AppWindow className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl sm:text-3xl font-black text-white font-mono">{stats.tabSwitches}</div>
          <p className="text-[11px] text-slate-400 mt-1 font-mono">Document visibility hidden events</p>
        </div>

        {/* Card 2: Window Blurs & Minimizations */}
        <div className="liquid-glass rounded-2xl p-4 sm:p-5 border border-white/15 backdrop-blur-xl relative overflow-hidden group hover:border-neon-amber/40 transition">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-wider font-bold">Window Blurs / Minimized</span>
            <div className="p-2 rounded-xl bg-neon-amber/15 text-neon-gold border border-neon-amber/30">
              <Minimize2 className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl sm:text-3xl font-black text-white font-mono">{stats.windowBlurs}</div>
          <p className="text-[11px] text-slate-400 mt-1 font-mono">Alt+Tab or lost window focus</p>
        </div>

        {/* Card 3: Fullscreen Exits */}
        <div className="liquid-glass rounded-2xl p-4 sm:p-5 border border-white/15 backdrop-blur-xl relative overflow-hidden group hover:border-neon-rose/40 transition">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-wider font-bold">Fullscreen Exits</span>
            <div className="p-2 rounded-xl bg-neon-rose/15 text-neon-rose border border-neon-rose/30">
              <Maximize2 className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl sm:text-3xl font-black text-white font-mono">{stats.fullscreenExits}</div>
          <p className="text-[11px] text-slate-400 mt-1 font-mono">Fullscreen lockdown exit attempts</p>
        </div>

        {/* Card 4: Clipboard & Prohibited Hotkeys */}
        <div className="liquid-glass rounded-2xl p-4 sm:p-5 border border-white/15 backdrop-blur-xl relative overflow-hidden group hover:border-neon-fuchsia/40 transition">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-wider font-bold">Hotkey & Clipboard</span>
            <div className="p-2 rounded-xl bg-neon-fuchsia/15 text-neon-fuchsia border border-neon-fuchsia/30">
              <Terminal className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl sm:text-3xl font-black text-white font-mono">
            {stats.clipboardAttempts + stats.hotkeyViolations}
          </div>
          <p className="text-[11px] text-slate-400 mt-1 font-mono">Copy, paste, inspect or hotkeys</p>
        </div>
      </div>

      {/* ----------------------------------------------------------------- */}
      {/* Active Lockdown Safeguards Grid                                   */}
      {/* ----------------------------------------------------------------- */}
      <div className="liquid-glass rounded-2xl p-4 border border-white/15 backdrop-blur-xl flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 font-mono text-slate-300">
          <Lock className="w-4 h-4 text-neon-mint" />
          <span className="font-bold text-white uppercase tracking-wider">Browser Security Protocols Active:</span>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <span className="px-3 py-1 rounded-full bg-neon-emerald/15 text-neon-mint border border-neon-emerald/30 font-mono text-[10px] font-bold flex items-center gap-1.5">
            <CheckCircle2 className="w-3 h-3" /> Fullscreen Enforced
          </span>
          <span className="px-3 py-1 rounded-full bg-neon-emerald/15 text-neon-mint border border-neon-emerald/30 font-mono text-[10px] font-bold flex items-center gap-1.5">
            <CheckCircle2 className="w-3 h-3" /> Tab Switch Trap
          </span>
          <span className="px-3 py-1 rounded-full bg-neon-emerald/15 text-neon-mint border border-neon-emerald/30 font-mono text-[10px] font-bold flex items-center gap-1.5">
            <CheckCircle2 className="w-3 h-3" /> Clipboard Locked
          </span>
          <span className="px-3 py-1 rounded-full bg-neon-emerald/15 text-neon-mint border border-neon-emerald/30 font-mono text-[10px] font-bold flex items-center gap-1.5">
            <CheckCircle2 className="w-3 h-3" /> Right-Click Blocked
          </span>
          <span className="px-3 py-1 rounded-full bg-neon-emerald/15 text-neon-mint border border-neon-emerald/30 font-mono text-[10px] font-bold flex items-center gap-1.5">
            <CheckCircle2 className="w-3 h-3" /> DevTools Protected
          </span>
        </div>
      </div>

      {/* ----------------------------------------------------------------- */}
      {/* Interactive Mock Exam Simulation Bar                              */}
      {/* ----------------------------------------------------------------- */}
      <div className="liquid-glass rounded-2xl p-4 sm:p-5 border border-neon-cyan/30 backdrop-blur-xl bg-neon-cyan/[0.03]">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-3">
          <div>
            <h3 className="text-xs font-mono font-black uppercase text-neon-cyan tracking-wider flex items-center gap-2">
              <Zap className="w-4 h-4" /> Mock Exam Focus Event Simulator (Faculty / Evaluator Testing)
            </h3>
            <p className="text-[11px] text-slate-400 font-mono mt-0.5">
              Trigger simulated events to test real-time focus detection and trust score degradation without switching actual tabs.
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <button
            onClick={() => onSimulateEvent && onSimulateEvent('TAB_SWITCH_DETECTED', 'Simulated tab switch to background document.')}
            className="px-3.5 py-1.5 rounded-xl bg-neon-cyan/20 hover:bg-neon-cyan/30 border border-neon-cyan/50 text-neon-cyan font-mono text-xs font-bold transition flex items-center gap-1.5 active:scale-95"
          >
            <AppWindow className="w-3.5 h-3.5" />
            <span>Simulate Tab Switch</span>
          </button>

          <button
            onClick={() => onSimulateEvent && onSimulateEvent('WINDOW_BLUR_DETECTED', 'Simulated window minimization or Alt+Tab blur.')}
            className="px-3.5 py-1.5 rounded-xl bg-neon-amber/20 hover:bg-neon-amber/30 border border-neon-amber/50 text-neon-gold font-mono text-xs font-bold transition flex items-center gap-1.5 active:scale-95"
          >
            <Minimize2 className="w-3.5 h-3.5" />
            <span>Simulate Window Blur</span>
          </button>

          <button
            onClick={() => onSimulateEvent && onSimulateEvent('FULLSCREEN_EXITED', 'Simulated candidate exiting fullscreen view.')}
            className="px-3.5 py-1.5 rounded-xl bg-neon-rose/20 hover:bg-neon-rose/30 border border-neon-rose/50 text-neon-rose font-mono text-xs font-bold transition flex items-center gap-1.5 active:scale-95"
          >
            <Maximize2 className="w-3.5 h-3.5" />
            <span>Simulate Fullscreen Exit</span>
          </button>

          <button
            onClick={() => onSimulateEvent && onSimulateEvent('HOTKEY_BLOCKED', 'Simulated Ctrl+C clipboard copy attempt.')}
            className="px-3.5 py-1.5 rounded-xl bg-neon-fuchsia/20 hover:bg-neon-fuchsia/30 border border-neon-fuchsia/50 text-neon-fuchsia font-mono text-xs font-bold transition flex items-center gap-1.5 active:scale-95"
          >
            <Terminal className="w-3.5 h-3.5" />
            <span>Simulate Clipboard / Hotkey</span>
          </button>
        </div>
      </div>

      {/* ----------------------------------------------------------------- */}
      {/* Detailed Focus Events Log Table                                   */}
      {/* ----------------------------------------------------------------- */}
      <div className="liquid-glass rounded-3xl border border-white/20 shadow-glass-specular backdrop-blur-2xl overflow-hidden">
        {/* Controls Bar */}
        <div className="p-4 sm:p-5 border-b border-white/10 flex flex-wrap items-center justify-between gap-3 bg-white/[0.03]">
          <div className="flex items-center gap-2">
            <span className="p-1.5 rounded-xl bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/40">
              <ShieldAlert className="w-4 h-4" />
            </span>
            <h3 className="text-xs font-mono font-black uppercase tracking-wider text-white">
              Focus Security Audit Stream ({filteredEvents.length})
            </h3>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            {/* Filter Pills */}
            <div className="flex items-center gap-1 bg-white/[0.04] p-1 rounded-xl border border-white/10 text-[10px] font-mono font-bold">
              {[
                { id: 'ALL', label: 'All' },
                { id: 'TAB_SWITCH', label: 'Tab Switches' },
                { id: 'WINDOW_BLUR', label: 'Window Blurs' },
                { id: 'FULLSCREEN', label: 'Fullscreen' },
                { id: 'CLIPBOARD_HOTKEY', label: 'Clipboard / Keys' }
              ].map((f) => (
                <button
                  key={f.id}
                  onClick={() => setFilterType(f.id)}
                  className={`px-2.5 py-1 rounded-lg transition ${
                    filterType === f.id
                      ? 'bg-neon-cyan/30 text-neon-cyan border border-neon-cyan/50 font-black'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>

            {/* Export JSON Button */}
            <button
              onClick={handleExportJSON}
              disabled={focusEvents.length === 0}
              className="px-3 py-1.5 rounded-xl liquid-pill text-xs font-mono font-bold text-slate-300 hover:text-white transition flex items-center gap-1.5 disabled:opacity-40"
              title="Download Security Audit Log (.JSON)"
            >
              <Download className="w-3.5 h-3.5 text-neon-cyan" />
              <span>Export Audit</span>
            </button>

            {focusEvents.length > 0 && onClearEvents && (
              <button
                onClick={onClearEvents}
                className="text-[10px] font-mono text-slate-400 hover:text-neon-rose px-2.5 py-1.5 rounded-xl hover:bg-white/[0.05] transition"
              >
                Reset
              </button>
            )}
          </div>
        </div>

        {/* Events Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-sans">
            <thead>
              <tr className="border-b border-white/10 bg-white/[0.02] text-slate-400 font-mono text-[11px] uppercase tracking-wider">
                <th className="py-3 px-4">Event Type</th>
                <th className="py-3 px-4">Severity</th>
                <th className="py-3 px-4">Details & Action Taken</th>
                <th className="py-3 px-4">Timestamp</th>
                <th className="py-3 px-4 text-right">Window Lost Duration</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.06]">
              {filteredEvents.length === 0 ? (
                <tr>
                  <td colSpan={5} className="py-12 text-center text-slate-400 font-mono">
                    <div className="flex flex-col items-center justify-center gap-2">
                      <div className="p-3 rounded-2xl bg-neon-emerald/10 border border-neon-emerald/30 text-neon-mint shadow-neon-emerald">
                        <CheckCircle2 className="w-6 h-6" />
                      </div>
                      <span className="text-white font-bold text-sm">No Focus Security Violations Recorded</span>
                      <span className="text-xs text-slate-400">Candidate has maintained continuous window focus.</span>
                    </div>
                  </td>
                </tr>
              ) : (
                filteredEvents.map((evt) => {
                  const Icon = getEventIcon(evt.type);
                  return (
                    <tr key={evt.id} className="hover:bg-white/[0.02] transition">
                      <td className="py-3.5 px-4">
                        <div className="flex items-center gap-2.5">
                          <span className="p-1.5 rounded-lg bg-white/[0.05] border border-white/10 text-slate-300">
                            <Icon className="w-4 h-4 text-neon-cyan" />
                          </span>
                          <span className="font-mono font-bold text-white text-xs">
                            {evt.type || 'FOCUS_EVENT'}
                          </span>
                        </div>
                      </td>
                      <td className="py-3.5 px-4">
                        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-black border ${getSeverityStyle(evt.severity)}`}>
                          {evt.severity || 'HIGH'}
                        </span>
                      </td>
                      <td className="py-3.5 px-4 text-slate-200 font-medium max-w-md">
                        {evt.message}
                      </td>
                      <td className="py-3.5 px-4 font-mono text-slate-400 text-[11px]">
                        {evt.timeDisplay || (evt.timestamp ? new Date(evt.timestamp).toLocaleTimeString() : 'Just now')}
                      </td>
                      <td className="py-3.5 px-4 text-right font-mono font-bold text-neon-gold text-xs">
                        {evt.durationSec ? `${evt.durationSec}s` : 'Instant'}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

