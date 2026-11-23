"""
RecallBox - Single Terminal Development Runner
Runs both FastAPI backend and Vite frontend concurrently in one terminal.
Press Ctrl+C to terminate both servers simultaneously.
"""

import os
import sys
import subprocess
import signal
import time

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

# Path to python in venv
if sys.platform == "win32":
    VENV_PYTHON = os.path.join(BACKEND_DIR, "venv", "Scripts", "python.exe")
    NPM_CMD = "npm.cmd"
else:
    VENV_PYTHON = os.path.join(BACKEND_DIR, "venv", "bin", "python")
    NPM_CMD = "npm"

if not os.path.exists(VENV_PYTHON):
    print(f"[Error] Virtual environment not found at: {VENV_PYTHON}")
    print("Please create the virtual environment first in backend/venv")
    sys.exit(1)


def main():
    print("=" * 70)
    print("             RecallBox - Unified Development Server Runner")
    print("=" * 70)
    print("Starting FastAPI backend and React frontend concurrently...")
    print(" - Backend:  http://localhost:8000 (Swagger docs: http://localhost:8000/docs)")
    print(" - Frontend: http://localhost:5173")
    print("Press Ctrl+C at any time to stop both servers.")
    print("=" * 70)
    print()

    # Start backend process
    backend_proc = subprocess.Popen(
        [VENV_PYTHON, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"],
        cwd=BACKEND_DIR,
    )

    # Start frontend process
    frontend_proc = subprocess.Popen(
        [NPM_CMD, "run", "dev"],
        cwd=FRONTEND_DIR,
    )

    def shutdown(signum=None, frame=None):
        print("\n[RecallBox] Shutting down servers...")
        try:
            backend_proc.terminate()
        except Exception:
            pass
        try:
            frontend_proc.terminate()
        except Exception:
            pass
        backend_proc.wait()
        frontend_proc.wait()
        print("[RecallBox] Both servers have stopped cleanly.")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        while True:
            time.sleep(1)
            # Check if any process died unexpectedly
            if backend_proc.poll() is not None:
                print(f"[RecallBox] Backend process terminated with code {backend_proc.returncode}")
                shutdown()
            if frontend_proc.poll() is not None:
                print(f"[RecallBox] Frontend process terminated with code {frontend_proc.returncode}")
                shutdown()
    except KeyboardInterrupt:
        shutdown()


if __name__ == "__main__":
    main()
