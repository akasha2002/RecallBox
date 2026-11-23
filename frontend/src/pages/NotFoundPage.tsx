import React from 'react';
import { Link } from 'react-router-dom';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="flex-1 flex flex-col items-center justify-center px-4 py-16 text-center">
      <h1 className="text-6xl font-extrabold text-slate-900">404</h1>
      <p className="text-lg text-slate-600 mt-2 mb-6">Page not found</p>
      <Link
        to="/"
        className="inline-flex items-center px-4 py-2 text-xs font-semibold rounded-lg text-white bg-sky-600 hover:bg-sky-700 transition"
      >
        Return to Home
      </Link>
    </div>
  );
};
