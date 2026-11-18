import React from 'react';
import {
  Shield,
  Bell,
  Sparkles,
  LogOut,
  Building2
} from 'lucide-react';

export default function Navbar({
  user,
  onLogout,
  notifications = [],
  unreadCount = 0,
  onOpenNotifications,
  onOpenGeminiConfig,
  geminiKeySet = false
}) {
  const getDeptColor = (deptName = '') => {
    if (deptName.includes('Computer Science'))
      return 'text-neon-cyan border-neon-cyan/50 bg-neon-cyan/20 shadow-[0_0_18px_rgba(6,182,212,0.35)]';
    if (deptName.includes('Artificial Intelligence'))
      return 'text-neon-fuchsia border-neon-fuchsia/50 bg-neon-fuchsia/20 shadow-[0_0_18px_rgba(236,72,153,0.35)]';
    if (deptName.includes('Electronics'))
      return 'text-neon-amber border-neon-gold/50 bg-neon-amber/20 shadow-[0_0_18px_rgba(245,158,11,0.35)]';
    if (deptName.includes('Information Tech'))
      return 'text-neon-mint border-neon-emerald/50 bg-neon-mint/20 shadow-[0_0_18px_rgba(0,245,155,0.35)]';
    return 'text-neon-orange border-neon-orange/50 bg-neon-orange/20 shadow-[0_0_18px_rgba(255,107,53,0.35)]';
  };

  return (
    <header className="sticky top-0 z-40 relative backdrop-blur-3xl bg-slate-950/75 border-b border-white/20 shadow-[0_12px_40px_rgba(0,0,0,0.8)] transition-all">
      {/* Top Iridescent Ambient Light Edge */}
      <div className="absolute top-0 left-0 right-0 h-[2.5px] bg-gradient-to-r from-neon-fuchsia via-neon-cyan via-neon-mint to-neon-gold shadow-[0_0_12px_rgba(236,72,153,0.6)]" />

      {/* Subtle Background Glow Orbs for Authentic Liquid Glass Refraction */}
      <div className="absolute top-0 left-10 w-48 h-12 bg-neon-fuchsia/20 rounded-full blur-2xl pointer-events-none" />
      <div className="absolute top-0 right-20 w-56 h-12 bg-neon-cyan/20 rounded-full blur-2xl pointer-events-none" />

      <div className="max-w-[1700px] mx-auto px-4 sm:px-8 py-3.5 flex items-center justify-between gap-4 relative z-10">
        
        {/* Brand Holographic Logo & Title */}
        <div className="flex items-center gap-3.5">
          <div className="relative group cursor-pointer">
            <div className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-neon-fuchsia via-neon-violet to-neon-cyan opacity-85 blur-md group-hover:opacity-100 transition duration-500" />
            <div className="relative flex items-center justify-center w-12 h-12 rounded-2xl bg-white p-1 border border-white/35 shadow-neon-fuchsia backdrop-blur-xl overflow-hidden">
              <img src="/skit-logo.png" alt="SKIT Logo" className="w-full h-full object-contain rounded-xl" />
              <span className="absolute top-1 right-1 w-2.5 h-2.5 rounded-full bg-neon-mint ring-2 ring-slate-900 animate-pulse shadow-[0_0_10px_#00f59b]" />
            </div>
          </div>

          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg sm:text-xl font-black tracking-tight text-white drop-shadow-md">
                SKIT ProctorLens<span className="bg-gradient-to-r from-neon-fuchsia via-neon-violet to-neon-cyan bg-clip-text text-transparent font-mono">.AI</span>
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-neon-emerald/20 border border-neon-emerald/40 text-neon-mint font-bold hidden md:inline-block">
                SKIT Bangalore
              </span>
            </div>
            <p className="text-[11px] text-slate-300 font-medium hidden sm:block tracking-wide">
              Sri Krishna Institute of Technology • Autonomous Examination System
            </p>
          </div>
        </div>

        {/* Action Controls & Capsules */}
        <div className="flex items-center gap-3 sm:gap-4">
          
          {/* Candidate Department Badge (Only if student candidate) */}
          {user && user.role !== 'admin' && user.department && (
            <div className={`hidden lg:flex items-center gap-2 px-4 py-1.5 rounded-full border text-xs font-mono font-bold backdrop-blur-xl ${getDeptColor(user.department)}`}>
              <Building2 className="w-3.5 h-3.5" />
              <span className="truncate max-w-[240px]">
                {user.department}
              </span>
            </div>
          )}

          {/* Department Notification Bell */}
          <button
            onClick={onOpenNotifications}
            className="relative p-2.5 rounded-2xl liquid-pill text-slate-200 hover:text-neon-gold hover:border-neon-amber/50 transition-all duration-200"
            title="Notification Center"
          >
            <Bell className="w-4 h-4 text-neon-gold" />
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-gradient-to-r from-neon-rose to-neon-fuchsia text-[9px] font-black text-white shadow-neon-rose animate-bounce ring-2 ring-slate-900">
                {unreadCount}
              </span>
            )}
          </button>

          {/* User Profile & Avatar Capsule */}
          {user && (
            <div className="flex items-center gap-3 pl-3 border-l border-white/20">
              <div className="text-right hidden sm:block">
                <div className="text-xs font-black text-white flex items-center justify-end gap-1.5">
                  <span>{user.name}</span>
                  <span className={`text-[9px] uppercase px-2 py-0.5 rounded-full font-mono font-black tracking-wider border ${
                    user.role === 'admin'
                      ? 'bg-neon-rose/25 text-neon-rose border-neon-rose/50 shadow-neon-rose'
                      : 'bg-neon-emerald/25 text-neon-mint border-neon-emerald/50 shadow-neon-emerald'
                  }`}>
                    {user.role}
                  </span>
                </div>
                <div className="text-[10px] font-mono text-neon-cyan truncate max-w-[170px] mt-0.5">
                  {user.email}
                </div>
              </div>

              {/* Glowing User Avatar Ring */}
              <div className={`w-10 h-10 rounded-2xl flex items-center justify-center text-xs font-black shadow-lg border border-white/35 ${
                user.role === 'admin'
                  ? 'bg-gradient-to-tr from-neon-rose via-neon-orange to-neon-gold text-white shadow-neon-rose'
                  : 'bg-gradient-to-tr from-neon-fuchsia via-neon-violet to-neon-cyan text-white shadow-neon-fuchsia'
              }`}>
                {user.name ? user.name.charAt(0).toUpperCase() : 'U'}
              </div>

              {/* Logout Button */}
              <button
                onClick={onLogout}
                className="p-2.5 rounded-2xl liquid-pill hover:text-neon-rose hover:border-neon-rose/50 hover:bg-neon-rose/15 text-slate-300 transition"
                title="Sign Out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
