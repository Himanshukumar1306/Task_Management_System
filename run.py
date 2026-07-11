import subprocess
import sys
import os
import time
import webbrowser
import threading

# Get absolute directory of this project root
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def run_backend():
    backend_dir = os.path.join(ROOT_DIR, "backend")
    # Run uvicorn via python -m uvicorn to ensure it works even if uvicorn.exe is not in PATH
    subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8000"], cwd=backend_dir)

def run_frontend():
    frontend_dir = os.path.join(ROOT_DIR, "frontend")
    # Run python http.server
    subprocess.run([sys.executable, "-m", "http.server", "8080"], cwd=frontend_dir)

if __name__ == "__main__":
    print("========================================================")
    print("         Starting Taskify Local Environment...          ")
    print("========================================================")
    
    # Create threads
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    frontend_thread = threading.Thread(target=run_frontend, daemon=True)
    
    # Start threads
    backend_thread.start()
    frontend_thread.start()
    
    # Wait 2 seconds for servers to start
    time.sleep(2)
    
    url = "http://localhost:8080/index.html"
    print(f"\n[Taskify] Launching browser: {url}...")
    webbrowser.open(url)
    
    print("\n========================================================")
    print(" Taskify is running successfully!")
    print(" - Press Ctrl+C in this window to stop both servers.")
    print("========================================================\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Taskify] Shutting down servers...")
