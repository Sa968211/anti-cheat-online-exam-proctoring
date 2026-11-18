import React, { useMemo } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  ShieldX,
  FileText,
  Printer,
  Award,
  AlertTriangle,
  Clock,
  Eye,
  Camera,
  AppWindow,
  Mic,
  Maximize2,
  CheckCircle2,
  XCircle,
  Sparkles,
  Download,
  Building2,
  User,
  Activity,
  Layers,
  ChevronRight
} from 'lucide-react';

export default function ForensicReportTab({
  incidents = [],
  focusEvents = [],
  warningsCount = {},
  trustScore = 100,
  user = {},
  test = {},
  onSubmitExam
}) {
  // 1. Classify & compile all incidents across Visual, Focus, and Audio categories
  const compiledData = useMemo(() => {
    const visual = [];
    const focus = [];
    const audio = [];

    // Process CV proctor incidents
    incidents.forEach((inc) => {
      const code = (inc.code || '').toUpperCase();
      if (code.includes('VOICE') || code.includes('AUDIO') || code.includes('SPEECH')) {
        audio.push({
          ...inc,
          category: 'Acoustic / Voice',
          penalty: 15
        });
      } else if (
        code.includes('TAB') ||
        code.includes('BLUR') ||
        code.includes('FULLSCREEN') ||
        code.includes('COPY') ||
        code.includes('HOTKEY')
      ) {
        focus.push({
          ...inc,
          category: 'Browser Focus',
          penalty: code.includes('TAB') ? 20 : code.includes('FULLSCREEN') ? 20 : 10
        });
      } else {
        // Visual infractions: Phone, Backlight, Nodding, Partial face, Gaze away, Multiple faces
        let penalty = 10;
        if (code.includes('PHONE')) penalty = 30;
        else if (code.includes('MULTIPLE') || code.includes('NO_FACE')) penalty = 20;
        else if (code.includes('BACKLIGHT') || code.includes('LIGHT')) penalty = 12;
        else if (code.includes('NODDING')) penalty = 10;
        else if (code.includes('PARTIAL') || code.includes('HALF') || code.includes('ZONE')) penalty = 12;
        else if (code.includes('GAZE') || code.includes('LOOKING')) penalty = 8;

        visual.push({
          ...inc,
          category: 'Visual & Biometric',
          penalty
        });
      }
    });

    // Process Browser Focus events
    focusEvents.forEach((evt) => {
      const type = (evt.type || '').toUpperCase();
      let penalty = 15;
      if (type.includes('TAB')) penalty = 20;
      else if (type.includes('FULLSCREEN')) penalty = 20;
      else if (type.includes('BLUR') || type.includes('MINIMIZE')) penalty = 15;
      else if (type.includes('COPY') || type.includes('PASTE')) penalty = 10;

      focus.push({
        id: evt.id || `foc-${Math.random()}`,
        code: evt.type,
        message: evt.message,
        severity: evt.severity || 'HIGH',
        timestamp: evt.timestamp ? evt.timestamp / 1000 : Date.now() / 1000,
        time_display: evt.timeDisplay || new Date().toLocaleTimeString(),
        category: 'Browser Focus',
        penalty
      });
    });

    // Calculate penalty deductions
    const visualDeductions = visual.reduce((acc, curr) => acc + (curr.penalty || 10), 0);
    const focusDeductions = focus.reduce((acc, curr) => acc + (curr.penalty || 15), 0);
    const audioDeductions = audio.reduce((acc, curr) => acc + (curr.penalty || 15), 0);

    const totalDeductions = visualDeductions + focusDeductions + audioDeductions;
    const computedTrust = Math.max(0, Math.min(100, Math.round(100 - totalDeductions)));

    // Total strikes
    const totalStrikes = (warningsCount.total !== undefined ? Number(warningsCount.total) : 0) ||
      (visual.length + focus.length + audio.length);

    const isDisqualified = totalStrikes >= 5 || computedTrust < 40;
    const finalScore = isDisqualified ? Math.min(computedTrust, 25) : computedTrust;

    return {
      visual,
      focus,
      audio,
      all: [...visual, ...focus, ...audio],
      visualDeductions,
      focusDeductions,
      audioDeductions,
      totalDeductions,
      finalScore,
      isDisqualified,
      totalStrikes
    };
  }, [incidents, focusEvents, warningsCount]);

  const { finalScore, isDisqualified, totalStrikes, visual, focus, audio, all } = compiledData;

  // Grade classification
  let gradeBadge = {
    grade: 'A',
    label: 'CERTIFIED HONEST • HIGH INTEGRITY',
    desc: 'Candidate maintained full biometric compliance and window focus throughout the session.',
    color: 'emerald',
    badgeClass: 'bg-neon-emerald/20 text-neon-mint border-neon-emerald/50 shadow-neon-emerald',
    icon: ShieldCheck
  };

  if (isDisqualified || finalScore < 50) {
    gradeBadge = {
      grade: 'F',
      label: 'INTEGRITY BREACH • DISQUALIFIED',
      desc: 'Critical security infractions exceeded permissible thresholds (5 strikes or severe biometric anomalies).',
      color: 'rose',
      badgeClass: 'bg-neon-rose/20 text-neon-rose border-neon-rose/50 shadow-neon-rose',
      icon: ShieldX
    };
  } else if (finalScore < 80) {
    gradeBadge = {
      grade: 'C',
      label: 'SUSPICIOUS ACTIVITY • REVIEW RECOMMENDED',
      desc: 'Minor or intermittent infractions detected. Faculty manual review advised.',
      color: 'amber',
      badgeClass: 'bg-neon-amber/20 text-neon-gold border-neon-amber/50 shadow-neon-amber',
      icon: ShieldAlert
    };
  }

  const GradeIcon = gradeBadge.icon;

  // Circular Dial Gauge Parameters
  const radius = 64;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (finalScore / 100) * circumference;

  let gaugeColor = '#00f59b';
  if (finalScore < 50) gaugeColor = '#f43f5e';
  else if (finalScore < 80) gaugeColor = '#fbbf24';

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* ----------------------------------------------------------------- */}
      {/* Top Forensic Executive Banner                                     */}
      {/* ----------------------------------------------------------------- */}
      <div className="liquid-glass rounded-3xl p-6 sm:p-8 border border-white/20 shadow-glass-specular backdrop-blur-2xl relative overflow-hidden">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6 relative z-10">
          <div className="space-y-2">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-white p-0.5 border border-white/20 flex items-center justify-center flex-shrink-0 shadow-sm overflow-hidden">
                <img src="/skit-logo.png" alt="SKIT" className="w-full h-full object-contain" />
              </div>
              <div>
                <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight flex items-center gap-2">
                  Post-Exam Forensic Audit & Trust Score
                  <span className="text-[10px] font-mono uppercase px-2.5 py-0.5 rounded-full bg-neon-emerald/20 text-neon-mint border border-neon-emerald/40">
                    Cryptographic Log
                  </span>
                </h2>
                <p className="text-xs text-slate-300 font-mono mt-0.5">
                  Automated triangulation of Visual Biometrics, Browser Focus Telemetry, and Acoustic VAD.
                </p>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-3 pt-2 text-xs font-mono text-slate-300">
              <span className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-white/[0.04] border border-white/10">
                <User className="w-3.5 h-3.5 text-neon-cyan" />
                <span>{user.name || 'Candidate'} ({user.email || 'student@skit.org.in'})</span>
              </span>
              <span className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-white/[0.04] border border-white/10">
                <Building2 className="w-3.5 h-3.5 text-neon-fuchsia" />
                <span>{test.department || user.department || 'Computer Science Engineering'}</span>
              </span>
              <span className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-white/[0.04] border border-white/10">
                <Clock className="w-3.5 h-3.5 text-neon-gold" />
                <span>Session: {new Date().toLocaleDateString()}</span>
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handlePrint}
              className="px-4 py-2.5 rounded-2xl bg-gradient-to-r from-neon-fuchsia to-neon-violet hover:opacity-90 active:scale-95 text-white text-xs font-bold transition flex items-center gap-2 shadow-neon-fuchsia font-mono"
            >
              <Printer className="w-4 h-4" />
              <span>Print / Save PDF</span>
            </button>

            {onSubmitExam && (
              <button
                onClick={onSubmitExam}
                className="px-5 py-2.5 rounded-2xl bg-gradient-to-r from-neon-emerald via-neon-teal to-neon-mint hover:opacity-90 active:scale-95 text-void text-xs font-black transition flex items-center gap-2 shadow-neon-emerald font-mono uppercase tracking-wider"
              >
                <CheckCircle2 className="w-4 h-4" />
                <span>Submit Final Exam</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* ----------------------------------------------------------------- */}
      {/* Overall Trust Score Gauge & Mathematical Formula Breakdown        */}
      {/* ----------------------------------------------------------------- */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Radial Trust Dial (Col 5) */}
        <div className="lg:col-span-5 liquid-glass rounded-3xl p-6 sm:p-7 border border-white/20 shadow-glass-specular backdrop-blur-2xl flex flex-col items-center justify-center text-center relative overflow-hidden">
          <div className="absolute top-0 right-0 w-44 h-44 bg-gradient-to-bl from-neon-cyan/20 to-transparent rounded-full blur-3xl pointer-events-none" />

          <span className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider mb-2">
            Final Overall Exam Trust Score
          </span>

          {/* Dial SVG */}
          <div className="relative flex items-center justify-center my-3">
            <svg className="w-40 h-40 transform -rotate-90">
              <circle
                cx="80"
                cy="80"
                r={radius}
                stroke="rgba(255, 255, 255, 0.08)"
                strokeWidth="12"
                fill="transparent"
              />
              <circle
                cx="80"
                cy="80"
                r={radius}
                stroke={gaugeColor}
                strokeWidth="12"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                fill="transparent"
                className="transition-all duration-1000 ease-out"
              />
            </svg>

            <div className="absolute flex flex-col items-center justify-center">
              <span className="text-4xl font-black font-mono text-white tracking-tight">
                {finalScore}%
              </span>
              <span className="text-[10px] font-mono font-bold text-slate-400 uppercase">
                Trust Index
              </span>
            </div>
          </div>

          {/* Verdict Grade Badge */}
          <div className={`mt-2 px-4 py-2 rounded-2xl border font-mono text-xs font-black flex items-center gap-2 ${gradeBadge.badgeClass}`}>
            <GradeIcon className="w-4 h-4" />
            <span>{gradeBadge.label}</span>
          </div>

          <p className="text-xs text-slate-300 font-sans mt-3 max-w-sm leading-relaxed">
            {gradeBadge.desc}
          </p>

          <div className="w-full mt-4 pt-4 border-t border-white/10 flex items-center justify-around text-xs font-mono">
            <div>
              <span className="text-slate-400 block text-[10px]">Total Infractions</span>
              <span className="font-black text-white text-sm">{all.length}</span>
            </div>
            <div className="h-6 w-px bg-white/10" />
            <div>
              <span className="text-slate-400 block text-[10px]">Warning Strikes</span>
              <span className={`font-black text-sm ${totalStrikes >= 5 ? 'text-neon-rose' : 'text-neon-gold'}`}>
                {totalStrikes} / 5
              </span>
            </div>
            <div className="h-6 w-px bg-white/10" />
            <div>
              <span className="text-slate-400 block text-[10px]">Verdict</span>
              <span className={`font-black text-sm ${isDisqualified ? 'text-neon-rose' : 'text-neon-mint'}`}>
                {isDisqualified ? 'FAIL' : 'PASS'}
              </span>
            </div>
          </div>
        </div>

        {/* Mathematical Deductions Breakdown Cards (Col 7) */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          {/* Formula Card */}
          <div className="liquid-glass rounded-2xl p-4 sm:p-5 border border-white/15 backdrop-blur-xl">
            <span className="text-xs font-mono font-bold text-neon-cyan uppercase tracking-wider flex items-center gap-1.5 mb-2">
              <Sparkles className="w-3.5 h-3.5" /> Algorithmic Trust Score Formulation
            </span>
            <div className="p-3 rounded-xl bg-void/80 border border-white/10 font-mono text-xs sm:text-sm text-slate-200">
              <span className="text-white font-bold">Trust Score = </span>
              <span className="text-neon-mint font-bold">100 (Base)</span>
              <span className="text-slate-400"> - </span>
              <span className="text-neon-rose font-bold">({compiledData.visualDeductions} Visual)</span>
              <span className="text-slate-400"> - </span>
              <span className="text-neon-gold font-bold">({compiledData.focusDeductions} Focus)</span>
              <span className="text-slate-400"> - </span>
              <span className="text-neon-fuchsia font-bold">({compiledData.audioDeductions} Audio)</span>
              <span className="text-white font-bold"> = {finalScore}%</span>
            </div>
          </div>

          {/* 3 Categories Split */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 flex-1">
            {/* Visual Telemetry */}
            <div className="liquid-glass rounded-2xl p-4 border border-white/15 backdrop-blur-xl flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-mono font-bold text-slate-400 uppercase">1. Visual Flags</span>
                  <div className="p-1.5 rounded-lg bg-neon-cyan/20 text-neon-cyan">
                    <Camera className="w-3.5 h-3.5" />
                  </div>
                </div>
                <div className="text-xl font-mono font-black text-white">{visual.length} Incidents</div>
                <p className="text-[10px] text-slate-400 mt-1 font-mono">Mobile phone, nodding, backlight, partial face</p>
              </div>
              <div className="mt-3 pt-2 border-t border-white/10 font-mono text-xs text-neon-rose font-bold">
                -{compiledData.visualDeductions} pts deduction
              </div>
            </div>

            {/* Browser Focus */}
            <div className="liquid-glass rounded-2xl p-4 border border-white/15 backdrop-blur-xl flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-mono font-bold text-slate-400 uppercase">2. Focus Losses</span>
                  <div className="p-1.5 rounded-lg bg-neon-amber/20 text-neon-gold">
                    <AppWindow className="w-3.5 h-3.5" />
                  </div>
                </div>
                <div className="text-xl font-mono font-black text-white">{focus.length} Incidents</div>
                <p className="text-[10px] text-slate-400 mt-1 font-mono">Tab switch, minimization, fullscreen breach</p>
              </div>
              <div className="mt-3 pt-2 border-t border-white/10 font-mono text-xs text-neon-gold font-bold">
                -{compiledData.focusDeductions} pts deduction
              </div>
            </div>

            {/* Audio Anomalies */}
            <div className="liquid-glass rounded-2xl p-4 border border-white/15 backdrop-blur-xl flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-mono font-bold text-slate-400 uppercase">3. Audio Anomalies</span>
                  <div className="p-1.5 rounded-lg bg-neon-fuchsia/20 text-neon-fuchsia">
                    <Mic className="w-3.5 h-3.5" />
                  </div>
                </div>
                <div className="text-xl font-mono font-black text-white">{audio.length} Incidents</div>
                <p className="text-[10px] text-slate-400 mt-1 font-mono">Audible speech or room acoustic noise</p>
              </div>
              <div className="mt-3 pt-2 border-t border-white/10 font-mono text-xs text-neon-fuchsia font-bold">
                -{compiledData.audioDeductions} pts deduction
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ----------------------------------------------------------------- */}
      {/* Evidence Gallery: Captured Violation Screenshots                  */}
      {/* ----------------------------------------------------------------- */}
      <div className="liquid-glass rounded-3xl p-6 sm:p-7 border border-white/20 shadow-glass-specular backdrop-blur-2xl space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-4 border-b border-white/10">
          <div className="flex items-center gap-2.5">
            <span className="p-2 rounded-xl bg-neon-rose/20 text-neon-rose border border-neon-rose/40 shadow-neon-rose">
              <Camera className="w-5 h-5" />
            </span>
            <div>
              <h3 className="text-sm sm:text-base font-black uppercase tracking-wider text-white font-mono flex items-center gap-2">
                Violation Evidence Gallery & Visual Proof
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-neon-rose/20 text-neon-rose border border-neon-rose/40 font-bold">
                  {all.filter((x) => x.snapshot || x.snapshot_base64).length} Captured Frames
                </span>
              </h3>
              <p className="text-xs text-slate-300 font-mono mt-0.5">
                Cryptographically watermarked video frames captured automatically by AI proctor during security infractions.
              </p>
            </div>
          </div>
        </div>

        {all.filter((x) => x.snapshot || x.snapshot_base64).length === 0 ? (
          <div className="py-8 text-center text-slate-400 font-mono text-xs">
            <div className="p-3 rounded-2xl bg-white/[0.04] border border-white/10 text-slate-400 w-12 h-12 flex items-center justify-center mx-auto mb-2">
              <Camera className="w-6 h-6 opacity-60" />
            </div>
            <p className="font-bold text-slate-200">No High-Risk Snapshot Violations Recorded</p>
            <p className="text-[11px] text-slate-400 mt-0.5">Frame snapshots trigger automatically upon mobile phone or multi-person detections.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 pt-2">
            {all
              .filter((x) => x.snapshot || x.snapshot_base64)
              .map((item, idx) => (
                <div
                  key={item.id || idx}
                  className="rounded-2xl liquid-glass-subtle border border-neon-rose/30 overflow-hidden hover:border-neon-rose transition shadow-md group"
                >
                  <div className="relative aspect-video w-full bg-slate-950 flex items-center justify-center overflow-hidden border-b border-white/10">
                    <img
                      src={item.snapshot || item.snapshot_base64}
                      alt={item.code}
                      className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
                    />
                    <div className="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-void/80 border border-white/20 text-[9px] font-mono font-bold text-white backdrop-blur-md">
                      {item.time_display || 'Violation'}
                    </div>
                    <div className="absolute top-2 right-2 px-2 py-0.5 rounded-md bg-neon-rose/80 text-white text-[9px] font-mono font-black shadow-neon-rose">
                      -{item.penalty || 15} pts
                    </div>
                  </div>
                  <div className="p-3 space-y-1 text-xs font-mono">
                    <div className="flex items-center justify-between">
                      <span className="font-black text-neon-cyan text-[11px] truncate max-w-[180px]">
                        {item.code}
                      </span>
                      <span className="text-[9px] font-black text-neon-rose uppercase">
                        {item.severity}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-300 font-sans line-clamp-2 leading-relaxed">
                      {item.message}
                    </p>
                  </div>
                </div>
              ))}
          </div>
        )}
      </div>

      {/* ----------------------------------------------------------------- */}
      {/* Comprehensive Forensic Incident Summary Table                     */}
      {/* ----------------------------------------------------------------- */}
      <div className="liquid-glass rounded-3xl border border-white/20 shadow-glass-specular backdrop-blur-2xl overflow-hidden">
        <div className="p-4 sm:p-5 border-b border-white/10 flex items-center justify-between gap-3 bg-white/[0.03]">
          <div className="flex items-center gap-2">
            <span className="p-1.5 rounded-xl bg-neon-emerald/20 text-neon-mint border border-neon-emerald/40">
              <Layers className="w-4 h-4" />
            </span>
            <h3 className="text-xs font-mono font-black uppercase tracking-wider text-white">
              Compiled Forensic Audit Matrix ({all.length} Recorded Anomalies)
            </h3>
          </div>

          <span className="text-[11px] font-mono text-slate-400">
            Categorized Visual, Focus & Audio Compilation
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-sans">
            <thead>
              <tr className="border-b border-white/10 bg-white/[0.02] text-slate-400 font-mono text-[11px] uppercase tracking-wider">
                <th className="py-3.5 px-4">Category</th>
                <th className="py-3.5 px-4">Infraction Code</th>
                <th className="py-3.5 px-4">Details & AI Evidence</th>
                <th className="py-3.5 px-4">Severity</th>
                <th className="py-3.5 px-4">Timestamp</th>
                <th className="py-3.5 px-4 text-right">Trust Penalty</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.06]">
              {all.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-slate-400 font-mono">
                    <div className="flex flex-col items-center justify-center gap-2">
                      <div className="p-3 rounded-2xl bg-neon-emerald/10 border border-neon-emerald/30 text-neon-mint shadow-neon-emerald">
                        <CheckCircle2 className="w-6 h-6" />
                      </div>
                      <span className="text-white font-bold text-sm">Pristine Examination Record</span>
                      <span className="text-xs text-slate-400">Zero visual, focus, or acoustic infractions detected.</span>
                    </div>
                  </td>
                </tr>
              ) : (
                all.map((item, idx) => (
                  <tr key={item.id || idx} className="hover:bg-white/[0.02] transition">
                    <td className="py-3.5 px-4">
                      <span className="px-2.5 py-1 rounded-lg bg-white/[0.05] border border-white/10 text-[10px] font-mono font-bold text-slate-200">
                        {item.category || 'General'}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-mono font-bold text-white text-xs">
                      {item.code || 'INCIDENT'}
                    </td>
                    <td className="py-3.5 px-4 text-slate-200 font-medium max-w-md">
                      {item.message}
                    </td>
                    <td className="py-3.5 px-4">
                      <span className={`px-2 py-0.5 rounded-full text-[9px] font-mono font-black border ${
                        item.severity === 'CRITICAL'
                          ? 'bg-neon-rose/20 text-neon-rose border-neon-rose/50 shadow-neon-rose'
                          : item.severity === 'HIGH'
                          ? 'bg-neon-amber/20 text-neon-gold border-neon-amber/50 shadow-neon-amber'
                          : 'bg-neon-cyan/20 text-neon-cyan border-neon-cyan/50'
                      }`}>
                        {item.severity || 'HIGH'}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-mono text-slate-400 text-[11px]">
                      {item.time_display || (item.timestamp ? new Date(item.timestamp * 1000).toLocaleTimeString() : 'N/A')}
                    </td>
                    <td className="py-3.5 px-4 text-right font-mono font-bold text-neon-rose text-xs">
                      -{item.penalty || 10} pts
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Submit Exam Callout Bar */}
        {onSubmitExam && (
          <div className="p-4 border-t border-white/10 bg-white/[0.02] flex flex-wrap items-center justify-between gap-3">
            <span className="text-xs text-slate-300 font-mono">
              Ready to submit your examination? AI will evaluate all sections and issue your verified certificate.
            </span>
            <button
              onClick={onSubmitExam}
              className="px-6 py-2.5 rounded-2xl bg-gradient-to-r from-neon-emerald via-neon-teal to-neon-mint hover:opacity-95 text-void font-extrabold text-xs shadow-neon-emerald transition flex items-center gap-2 font-mono uppercase tracking-wider ring-1 ring-neon-mint"
            >
              <CheckCircle2 className="w-4 h-4 text-void" />
              <span>Conclude & Submit Final Exam</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

