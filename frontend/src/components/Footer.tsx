import React from 'react';
import { APP_NAME, APP_VERSION } from '../utils/constants';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-200 bg-slate-50 py-6 text-center text-xs text-slate-500">
      <div className="max-w-6xl mx-auto px-4">
        <p className="m-0">
          {APP_NAME} v{APP_VERSION} &bull; Personal Workspace-Based Note Management
        </p>
        <p className="mt-1 text-slate-400">
          React + Vite + TypeScript &bull; Python FastAPI &bull; PostgreSQL
        </p>
      </div>
    </footer>
  );
};
