import React from 'react';
import { ShieldCheck, ShieldAlert, ShieldX, Compass, Users, Activity, Eye, Zap, Sparkles } from 'lucide-react';

export default function TrustScoreGauge({
  score = 100,
  headPose = { yaw: 0, pitch: 0, roll: 0 },
  faceCount = 1,
  status = 'CLEAN'
}) {
  const normalizedScore = Math.max(0, Math.min(100, Math.round(score)));

  let strokeColor = '#00f59b';
  let badgeStyle = {
    label: 'VERIFIED INTEGRITY',
    icon: ShieldCheck,
    bg: 'bg-neon-emerald/20 text-neon-mint border-neon-emerald/50 shadow-neon-emerald'
  };

  if (normalizedScore < 50) {
    strokeColor = '#f43f5e';
    badgeStyle = {
      label: 'HIGH CHEAT RISK',
      icon: ShieldX,
      bg: 'bg-neon-rose/20 text-neon-rose border-neon-rose/50 shadow-neon-rose'
    };
  } else if (normalizedScore < 80) {
    strokeColor = '#fbbf24';
    badgeStyle = {
      label: 'SUSPICIOUS ACTIVITY',
      icon: ShieldAlert,
      bg: 'bg-neon-amber/20 text-neon-gold border-neon-amber/50 shadow-neon-amber'
    };
  }

  const StatusIcon = badgeStyle.icon;

  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (normalizedScore / 100) * circumference;

  return (
    <div className="liquid-glass rounded-3xl p-5 relative overflow-hidden backdrop-blur-2xl border border-white/20 shadow-glass-specular">
      {/* Liquid Sheen Ambient Refraction */}
      <div className="absolute -top-12 -right-12 w-36 h-36 bg-gradient-to-br from-neon-fuchsia/20 via-neon-violet/10 to-transparent rounded-full blur-2xl pointer-events-none" />
      <div className="absolute -bottom-10 -left-10 w-32 h-32 bg-gradient-to-tr from-neon-cyan/20 to-transparent rounded-full blur-2xl pointer-events-none" />

      {/* Top Header */}
      <div className="relative z-10 flex items-center justify-between mb-4">
        <div className="flex items-center gap-2 text-xs font-bold text-slate-100">
          <span className="p-1.5 rounded-xl bg-neon-fuchsia/15 border border-neon-fuchsia/30 text-neon-fuchsia shadow-neon-fuchsia">
            <Activity className="w-3.5 h-3.5 animate-pulse" />
          </span>
          <span className="uppercase tracking-wider font-mono">Real-time Trust Index</span>
        </div>

        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-black tracking-wider border font-mono shadow-sm ${badgeStyle.bg}`}>
          <StatusIcon className="w-3.5 h-3.5" />
          {badgeStyle.label}
        </span>
      </div>

      {/* Main Gauge & Telemetry Split */}
      <div className="relative z-10 flex flex-col sm:flex-row items-center gap-5 justify-between">
        
        {/* Speedometer Liquid Dial */}
        <div className="relative flex items-center justify-center">
          <svg className="w-32 h-32 transform -rotate-90">
            <circle
              cx="64"
              cy="64"
              r={radius}
              stroke="rgba(255, 255, 255, 0.08)"
              strokeWidth="9"
              fill="transparent"
            />
            <circle
              cx="64"
              cy="64"
              r={radius}
              stroke={strokeColor}
              strokeWidth="9"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              fill="transparent"
              style={{
                transition: 'stroke-dashoffset 0.6s ease-in-out, stroke 0.4s',
                filter: `drop-shadow(0 0 8px ${strokeColor})`
              }}
            />
          </svg>

          {/* Centered Digital Readout */}
          <div className="absolute flex flex-col items-center">
            <span className="text-3xl font-black font-mono tracking-tight text-white drop-shadow-[0_2px_10px_rgba(255,255,255,0.4)]">
              {normalizedScore}%
            </span>
            <span className="text-[9px] uppercase font-mono tracking-widest text-slate-300 font-bold">
              Trust Score
            </span>
          </div>
        </div>

        {/* 4 Distinct Color Telemetry Droplets */}
        <div className="grid grid-cols-2 gap-2.5 w-full sm:w-auto flex-1 font-mono">
          
          {/* Faces Count Card (Neon Cyan Droplet) */}
          <div className="p-3 rounded-2xl liquid-glass-subtle border border-neon-cyan/30 shadow-sm relative overflow-hidden group">
            <div className="text-[10px] text-neon-cyan flex items-center gap-1 mb-1 font-bold">
              <Users className="w-3 h-3" />
              <span>Face Count</span>
            </div>
            <div className="text-sm font-black text-white flex items-center gap-1.5">
              <span>{faceCount}</span>
              <span className={`text-[9px] px-1.5 py-0.5 rounded-full font-sans font-bold border ${
                faceCount === 1
                  ? 'bg-neon-emerald/20 text-neon-mint border-neon-emerald/40'
                  : 'bg-neon-rose/20 text-neon-rose border-neon-rose/40'
              }`}>
                {faceCount === 1 ? 'Centered' : faceCount === 0 ? 'Absent' : 'Multi'}
              </span>
            </div>
          </div>

          {/* Yaw Angle Card (Neon Fuchsia Droplet) */}
          <div className="p-3 rounded-2xl liquid-glass-subtle border border-neon-fuchsia/30 shadow-sm relative overflow-hidden">
            <div className="text-[10px] text-neon-fuchsia flex items-center gap-1 mb-1 font-bold">
              <Compass className="w-3 h-3" />
              <span>Head Yaw</span>
            </div>
            <div className="text-sm font-black text-white">
              {headPose?.yaw ?? 0}°
            </div>
          </div>

          {/* Pitch Angle Card (Neon Amber Droplet) */}
          <div className="p-3 rounded-2xl liquid-glass-subtle border border-neon-amber/30 shadow-sm relative overflow-hidden">
            <div className="text-[10px] text-neon-gold flex items-center gap-1 mb-1 font-bold">
              <Compass className="w-3 h-3" />
              <span>Head Pitch</span>
            </div>
            <div className="text-sm font-black text-white">
              {headPose?.pitch ?? 0}°
            </div>
          </div>

          {/* Roll Angle Card (Neon Mint Droplet) */}
          <div className="p-3 rounded-2xl liquid-glass-subtle border border-neon-mint/30 shadow-sm relative overflow-hidden">
            <div className="text-[10px] text-neon-mint flex items-center gap-1 mb-1 font-bold">
              <Compass className="w-3 h-3" />
              <span>Head Roll</span>
            </div>
            <div className="text-sm font-black text-white">
              {headPose?.roll ?? 0}°
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
