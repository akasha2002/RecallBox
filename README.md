# RecallBox

RecallBox is a workspace-based personal note management application built with **React**, **Vite**, **TypeScript**, and **FastAPI**, with **PostgreSQL** as the persistent database.

## Architecture

- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS, React Router 7
- **Backend**: Python 3.13, FastAPI, Pydantic v2, Uvicorn
- **Database** *(Phase 2)*: Supabase PostgreSQL, SQLAlchemy
- **Containerization** *(Phase 10)*: Docker & Docker Compose

---

## Quick Start: One-Click Startup (Frontend + Backend)

You can launch both the frontend and backend servers together using any of these options:

### Option 1: Double-Click Batch File (Windows)
Double-click [start_dev.bat](file:///d:/Akash/RecallBox%20App/start_dev.bat) in the project root (or run `.\start_dev.bat` in Command Prompt).
> Opens two dedicated terminal windows: one running FastAPI on port 8000 and one running Vite on port 5173.

### Option 2: PowerShell Script
```powershell
.\start_dev.ps1
```

### Option 3: Python Runner (Single Terminal with graceful Ctrl+C exit)
```bash
python run_dev.py
```

---

## Server URLs

- **Frontend Application**: [http://localhost:5173](http://localhost:5173)
- **Backend API Root**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Health Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## Project Structure

```text
RecallBox/
│
├── start_dev.bat               # One-click Windows starter (Frontend + Backend)
├── start_dev.ps1               # One-command PowerShell starter
├── run_dev.py                  # Single-terminal concurrent runner
├── documentation/              # Project specifications and progress tracking
│   ├── SRS.md                  # Software Requirements Specification
│   ├── DEVELOPMENT_PLAN.md     # Implementation phases and guidelines
│   ├── DATABASE_DESIGN.md      # Database schema specifications
│   ├── API_DOCUMENTATION.md    # API contracts and endpoint documentation
│   └── DEVELOPMENT_PROGRESS.md # Real-time implementation tracking
│
├── frontend/                   # React + Vite + TypeScript application
│   ├── src/
│   │   ├── components/         # Reusable UI components (Header, Footer)
│   │   ├── layouts/            # Page layouts (MainLayout)
│   │   ├── pages/              # Route view pages (WelcomePage)
│   │   ├── routes/             # Client-side router configuration
│   │   ├── services/           # Backend API integration clients
│   │   ├── hooks/              # Custom React hooks (useHealthCheck)
│   │   ├── types/              # TypeScript interface definitions
│   │   └── utils/              # Application constants and helpers
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── backend/                    # FastAPI REST API application
│   ├── app/
│   │   ├── api/                # Versioned API routes (v1 health router)
│   │   ├── core/               # Pydantic Settings and configurations
│   │   ├── models/             # SQLAlchemy ORM models (Phase 2)
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── services/           # Business logic layer
│   │   ├── repositories/       # Data access layer
│   │   ├── db/                 # Database session and base configuration (Phase 2)
│   │   └── main.py             # FastAPI entry point
│   ├── tests/                  # Pytest test suite
│   └── requirements.txt
│
├── .gitignore                  # Git ignore rules for node, python, secrets
├── .env.example                # Root environment variable template
└── README.md
```

---

## Manual Startup (Separate Terminals)

If you prefer running frontend and backend in separate terminals:

### 1. Backend Setup

```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm run dev
```

---

## Current Status

**Phase 1 – Project Initialization and Setup** is completed.
Database integration is scheduled for **Phase 2**.
