import React from 'react';
import { Link } from 'react-router-dom';
import { APP_NAME } from '../utils/constants';

export const Header: React.FC = () => {
  return (
    <header className="border-b border-slate-200 bg-white sticky top-0 z-50 shadow-sm">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 text-decoration-none group">
          <div className="w-9 h-9 rounded-lg bg-sky-600 flex items-center justify-center text-white font-bold text-lg shadow-sm group-hover:bg-sky-700 transition">
            R
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-slate-900 text-lg leading-tight tracking-tight">
              {APP_NAME}
            </span>
            <span className="text-[10px] text-slate-500 font-medium tracking-wide uppercase">
              Personal Note Management
            </span>
          </div>
        </Link>

        <div className="flex items-center gap-3">
          <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-sky-50 text-sky-700 border border-sky-200">
            Phase 1: Setup
          </span>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="text-xs font-medium text-slate-600 hover:text-sky-600 transition hidden sm:inline"
          >
            API Swagger Docs ↗
          </a>
        </div>
      </div>
    </header>
  );
};
