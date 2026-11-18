import React, { useState } from 'react';
import { Key, Sparkles, CheckCircle2, X, ExternalLink, Cpu } from 'lucide-react';
import axios from 'axios';

import { API_BASE_URL } from '../config';

export default function GeminiConfigModal({ isOpen, onClose, onKeySaved }) {
  const [apiKey, setApiKey] = useState(localStorage.getItem('proctor_gemini_key') || '');
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  if (!isOpen) return null;

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSuccessMsg('');

    try {
      await axios.post(`${API_BASE_URL}/api/interview/config`, {
        api_key: apiKey.trim()
      });
      localStorage.setItem('proctor_gemini_key', apiKey.trim());
      setSuccessMsg('Google Gemini API key linked successfully!');
      if (onKeySaved) onKeySaved(apiKey.trim());
      setTimeout(() => {
        setSuccessMsg('');
        onClose();
      }, 1500);
    } catch (err) {
      alert('Failed to configure API key.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-void/80 backdrop-blur-3xl animate-in fade-in duration-200">
      <div className="relative w-full max-w-md rounded-3xl liquid-glass border border-white/20 p-7 shadow-glass-specular">
        
        {/* Top Header */}
        <div className="flex items-center justify-between pb-4 border-b border-white/[0.12]">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-2xl bg-neon-fuchsia/20 text-neon-fuchsia border border-neon-fuchsia/30 shadow-neon-fuchsia">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Google Gemini API Link</h3>
              <p className="text-[11px] text-slate-300 font-mono">Agentic Interview Intelligence</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1.5 rounded-xl liquid-pill text-slate-300 hover:text-white transition">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="my-4 p-3.5 rounded-2xl bg-white/[0.04] border border-white/10 text-[11px] space-y-2 text-slate-300">
          <div className="font-bold text-neon-cyan flex items-center gap-1.5 font-mono">
            <span>⚡ Where to store your Gemini API Key:</span>
          </div>
          <p className="leading-relaxed">
            <span className="text-white font-bold">Method A (One-Click):</span> Paste your key below and click <span className="text-neon-fuchsia font-bold">Link API Key</span> (saved to browser & synced to backend).
          </p>
          <p className="leading-relaxed">
            <span className="text-white font-bold">Method B (Config File):</span> Add <code className="bg-void/80 px-1.5 py-0.5 rounded text-neon-mint font-mono">GEMINI_API_KEY=AIzaSy...</code> in your <code className="bg-void/80 px-1.5 py-0.5 rounded text-neon-gold font-mono">backend/.env</code> file.
          </p>
          <p className="text-[10px] text-slate-400 font-mono">
            Powers the <span className="text-neon-fuchsia font-bold">Zam AI</span> live technical evaluator.
          </p>
        </div>

        {successMsg && (
          <div className="p-3.5 mb-4 rounded-2xl bg-neon-emerald/20 border border-neon-emerald/40 text-neon-mint text-xs flex items-center gap-2 font-mono">
            <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        <form onSubmit={handleSave} className="space-y-4 text-xs font-medium">
          <div>
            <label className="block font-bold text-slate-300 mb-1.5 flex items-center justify-between">
              <span>Gemini API Key</span>
              <a
                href="https://aistudio.google.com/app/apikey"
                target="_blank"
                rel="noreferrer"
                className="text-neon-cyan hover:underline flex items-center gap-1 text-[11px] font-mono"
              >
                Get Free Key <ExternalLink className="w-3 h-3" />
              </a>
            </label>
            <div className="relative">
              <Key className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="AIzaSy..."
                className="w-full pl-10 pr-3.5 py-3 rounded-2xl liquid-glass-subtle border border-white/15 text-white font-mono placeholder:text-slate-500 focus:outline-none focus:border-neon-fuchsia"
              />
            </div>
            <p className="text-[10px] text-slate-400 mt-1.5 font-mono">
              Note: When unconfigured, an autonomous local heuristic agent runs smoothly without interruption.
            </p>
          </div>

          <div className="flex items-center justify-end gap-2.5 pt-3 border-t border-white/[0.12]">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2.5 rounded-2xl liquid-pill text-slate-300 hover:text-white"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-2.5 rounded-2xl bg-gradient-to-r from-neon-fuchsia to-neon-violet hover:opacity-90 active:scale-95 disabled:opacity-40 text-white font-bold text-xs shadow-neon-fuchsia transition flex items-center gap-2 font-mono"
            >
              {saving ? <Cpu className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
              <span>Link API Key</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
