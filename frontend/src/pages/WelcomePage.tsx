import React, { useState, useEffect } from 'react';
import { checkBackendHealth } from '../services/api';
import type { HealthStatus } from '../types';

export const WelcomePage: React.FC = () => {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchHealth = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await checkBackendHealth();
      setHealth(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Failed to reach backend server. Ensure FastAPI is running on port 8000.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  return (
    <div className="max-w-4xl mx-auto px-4 py-12 flex-1 flex flex-col justify-center">
      {/* Hero section */}
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 mb-4">
          <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
          Phase 2 Complete: Database Connected &amp; Migrated
        </div>
        <h1 className="text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-tight mb-4">
          Welcome to <span className="text-sky-600">RecallBox</span>
        </h1>
        <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
          A personal workspace-based note management application built with React, Vite, TypeScript, FastAPI, and Supabase PostgreSQL.
        </p>
      </div>

      {/* Backend & Database Health Check Card */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 mb-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
          <div>
            <h2 className="text-lg font-bold text-slate-900 m-0">Backend &amp; Database Status</h2>
            <p className="text-xs text-slate-500 mt-1 m-0">
              Verifies live communication between React frontend, FastAPI backend, and Supabase PostgreSQL.
            </p>
          </div>
          <button
            onClick={fetchHealth}
            disabled={loading}
            className="self-start sm:self-auto inline-flex items-center px-4 py-2 border border-transparent text-xs font-semibold rounded-lg text-white bg-sky-600 hover:bg-sky-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 transition disabled:opacity-50 cursor-pointer"
          >
            {loading ? 'Checking...' : 'Re-check Status'}
          </button>
        </div>

        <div className="mt-4">
          {loading && (
            <div className="py-4 text-center text-sm text-slate-500">
              Pinging health endpoint...
            </div>
          )}

          {!loading && error && (
            <div className="p-4 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 text-sm">
              <div className="font-semibold flex items-center gap-2">
                <span>⚠️ Backend Unreachable</span>
              </div>
              <p className="mt-1 text-xs text-amber-700 m-0">
                {error}
              </p>
              <p className="mt-2 text-xs text-amber-600 m-0">
                Start the backend using: <code>.\start_dev.bat</code> or <code>uvicorn app.main:app --reload --port 8000</code> in the <code>backend/</code> directory.
              </p>
            </div>
          )}

          {!loading && health && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2">
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <span className="text-[11px] font-medium text-slate-500 uppercase tracking-wider block">API Status</span>
                <span className="text-sm font-bold text-emerald-600 capitalize flex items-center gap-1.5 mt-1">
                  <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                  {health.status}
                </span>
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <span className="text-[11px] font-medium text-slate-500 uppercase tracking-wider block">Database</span>
                <span className={`text-sm font-bold capitalize flex items-center gap-1.5 mt-1 ${health.database === 'connected' ? 'text-emerald-600' : 'text-amber-600'}`}>
                  <span className={`w-2 h-2 rounded-full ${health.database === 'connected' ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
                  {health.database === 'connected' ? 'Connected (Supabase)' : 'Pending Config'}
                </span>
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <span className="text-[11px] font-medium text-slate-500 uppercase tracking-wider block">Version</span>
                <span className="text-sm font-semibold text-slate-800 block mt-1">
                  v{health.version}
                </span>
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <span className="text-[11px] font-medium text-slate-500 uppercase tracking-wider block">Environment</span>
                <span className="text-sm font-semibold text-slate-800 block mt-1 capitalize">
                  {health.environment}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Database Schema & Next Phase Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200">
          <h3 className="text-sm font-bold text-slate-900 mb-2 flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
            Database Schema (Live on Supabase)
          </h3>
          <ul className="text-xs text-slate-600 space-y-1.5 pl-4 list-disc m-0">
            <li><strong>Workspaces:</strong> Root entity with hashed access keys</li>
            <li><strong>Categories:</strong> Workspace-scoped topic classification</li>
            <li><strong>Notes:</strong> Title, content, timestamps, cascade deletion</li>
            <li><strong>Tags &amp; Note_Tags:</strong> Many-to-many relationship</li>
          </ul>
        </div>
        <div className="bg-white p-5 rounded-xl border border-slate-200">
          <h3 className="text-sm font-bold text-slate-900 mb-2 flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-sky-500"></span>
            Next: Phase 3 (Backend Foundation)
          </h3>
          <ul className="text-xs text-slate-600 space-y-1.5 pl-4 list-disc m-0">
            <li>Centralized API exception handling &amp; status codes</li>
            <li>Request/response validation with Pydantic v2 schemas</li>
            <li>Service &amp; Repository 3-tier business architecture</li>
            <li>Structured logging and test configuration</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
