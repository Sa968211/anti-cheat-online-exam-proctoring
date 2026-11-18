import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught error:', error, errorInfo);
    this.setState({ errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-[#050508] text-white flex items-center justify-center p-6">
          <div className="max-w-xl w-full p-8 rounded-3xl bg-slate-900/90 border border-rose-500/40 shadow-2xl backdrop-blur-2xl text-center">
            <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-rose-500/20 text-rose-400 flex items-center justify-center text-3xl font-bold">
              ⚠️
            </div>
            <h2 className="text-xl font-black mb-2 text-rose-300 font-mono">
              SKIT ProctorLens Recovery
            </h2>
            <p className="text-xs text-slate-300 mb-4 font-mono">
              An unexpected render issue was safely intercepted:
            </p>
            <div className="p-4 rounded-xl bg-black/60 border border-white/10 text-left text-xs font-mono text-rose-300 overflow-x-auto mb-6 max-h-40">
              {this.state.error?.toString()}
            </div>
            <button
              onClick={() => {
                localStorage.removeItem('proctor_active_user');
                window.location.reload();
              }}
              className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-neon-cyan to-blue-600 text-white font-bold text-xs uppercase tracking-wider font-mono hover:opacity-90 transition"
            >
              Reset Session & Reload
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
)


