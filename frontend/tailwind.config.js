/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      colors: {
        void: '#06040e',
        obsidian: '#0a0717',
        surface: {
          50: 'rgba(255, 255, 255, 0.03)',
          100: 'rgba(255, 255, 255, 0.05)',
          200: 'rgba(255, 255, 255, 0.08)',
          300: 'rgba(255, 255, 255, 0.12)',
          border: 'rgba(255, 255, 255, 0.15)',
        },
        neon: {
          fuchsia: '#ec4899',
          pink: '#f43f5e',
          violet: '#8b5cf6',
          purple: '#a855f7',
          cyan: '#06b6d4',
          teal: '#14b8a6',
          emerald: '#10b981',
          mint: '#00f59b',
          amber: '#f59e0b',
          gold: '#fbbf24',
          orange: '#ff6b35',
          rose: '#e11d48'
        }
      },
      backgroundImage: {
        'liquid-sheen': 'linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.05) 50%, rgba(255, 255, 255, 0) 100%)',
        'liquid-card': 'linear-gradient(180deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.02) 100%)',
        'aurora-fluid': 'linear-gradient(135deg, #d946ef 0%, #8b5cf6 50%, #06b6d4 100%)',
        'sunset-fluid': 'linear-gradient(135deg, #f59e0b 0%, #ff6b35 50%, #f43f5e 100%)',
      },
      boxShadow: {
        'liquid': '0 8px 32px 0 rgba(0, 0, 0, 0.45), inset 0 1px 1px 0 rgba(255, 255, 255, 0.25), inset 0 -1px 1px 0 rgba(0, 0, 0, 0.3)',
        'liquid-hover': '0 15px 45px -10px rgba(0, 0, 0, 0.6), inset 0 1px 2px 0 rgba(255, 255, 255, 0.4), inset 0 -1px 1px 0 rgba(0, 0, 0, 0.2)',
        'liquid-glow-fuchsia': '0 0 35px -5px rgba(236, 72, 153, 0.5), inset 0 1px 1px 0 rgba(255, 255, 255, 0.3)',
        'liquid-glow-cyan': '0 0 35px -5px rgba(6, 182, 212, 0.5), inset 0 1px 1px 0 rgba(255, 255, 255, 0.3)',
        'liquid-glow-emerald': '0 0 35px -5px rgba(16, 185, 129, 0.5), inset 0 1px 1px 0 rgba(255, 255, 255, 0.3)',
        'liquid-glow-amber': '0 0 35px -5px rgba(245, 158, 11, 0.5), inset 0 1px 1px 0 rgba(255, 255, 255, 0.3)',
        'liquid-glow-rose': '0 0 35px -5px rgba(244, 63, 94, 0.5), inset 0 1px 1px 0 rgba(255, 255, 255, 0.3)',
      },
      animation: {
        'float-slow': 'floatBlob 12s ease-in-out infinite alternate',
        'float-reverse': 'floatBlobReverse 14s ease-in-out infinite alternate',
        'pulse-glow': 'pulseGlow 6s ease-in-out infinite',
      },
      keyframes: {
        floatBlob: {
          '0%': { transform: 'translate(0px, 0px) scale(1)' },
          '50%': { transform: 'translate(60px, -40px) scale(1.1)' },
          '100%': { transform: 'translate(-40px, 50px) scale(0.95)' }
        },
        floatBlobReverse: {
          '0%': { transform: 'translate(0px, 0px) scale(1)' },
          '50%': { transform: 'translate(-50px, 40px) scale(1.15)' },
          '100%': { transform: 'translate(40px, -30px) scale(0.9)' }
        },
        pulseGlow: {
          '0%, 100%': { opacity: '0.4' },
          '50%': { opacity: '0.75' }
        }
      }
    },
  },
  plugins: [],
}
