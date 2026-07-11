# Taskify - Premium Task Management System

Taskify is a modern, responsive **Task Management System (TMS)** built with a high-fidelity glassmorphic user interface. It provides project leads, managers, and developers a unified interface to create task lists, monitor status progress, manage roles, and review directory statistics.

This repository was developed as part of the **MpOnline Internship** project, reconstructed and modernized with a premium SaaS product design system.

---

## 🚀 Key Features

* **Premium Glassmorphic Interface**: Fully custom CSS styling featuring ambient color gradients, frosted glass panel backdrops (`backdrop-filter`), smooth transitional micro-animations, and glowing badge states.
* **Role-Based Workspaces**: Secure token-based OAuth2 authentication (JWT) with separate workspaces:
  * **Administrators**: Full capabilities to register new employees, manage staff status, create tasks, and read analytics summaries.
  * **Managers**: Create, assign, filter, and delete tasks across all employees.
  * **Employees**: Interactive personalized dashboard showing assigned task lists and a quick status update manager.
* **OpenAPI REST API Backend**: A robust, auto-documenting FastAPI backend with complete Swagger UI integration for developers.
* **Docker & Local Modes**: Support for docker-compose (MySQL container) and quick-start local environment (SQLite).

---

## 🛠️ Tech Stack

* **Backend**: Python 3.12+, FastAPI, SQLAlchemy ORM, Pydantic, Passlib (bcrypt), python-jose (JWT).
* **Frontend**: Semantic HTML5, Vanilla CSS3 (Custom Variables, Flexbox, Keyframes), Vanilla JavaScript (async-fetch client).
* **Database**: SQLite (default local) / MySQL 8.0 (production/Docker).
* **Hosting / Containers**: Docker, Docker-Compose, Nginx, Render.

---

## 💻 Running the Project Locally

### 1. Quick-Start (Automatic Windows Script)
The simplest way to start both the backend API and frontend website is using the unified Python wrapper:
1. Double-click the `run_local.bat` file in the root directory.
2. It will automatically start:
   * **FastAPI Backend**: `http://localhost:8000`
   * **Frontend Server**: `http://localhost:8080`
3. A web browser window will automatically open to: [http://localhost:8080/index.html](http://localhost:8080/index.html)

### 2. Manual Startup Commands
If you prefer running the commands manually:
* **Install dependencies & seed database**:
  ```powershell
  cd backend
  pip install -r requirements.txt
  python seed.py
  ```
* **Run Backend Server**:
  ```powershell
  python -m uvicorn app.main:app --port 8000 --reload
  ```
* **Run Frontend HTTP Server**:
  ```powershell
  cd frontend
  python -m http.server 8080
  ```

---

## 🔐 Seed User Accounts
The database seeder (`seed.py`) creates the following test credentials:

| Role | Username | Password | Email |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | `admin@taskify.io` |
| **Manager** | `manager` | `manager123` | `manager@taskify.io` |
| **Employee (Intern)** | `snehal` | `snehal123` | `snehal@taskify.io` |
| **Employee (Frontend)** | `aman` | `aman123` | `aman@taskify.io` |

---

## ☁️ Deployment on Render

This project is configured for direct deployment on **Render**:
1. **Backend Web Service**:
   * Language: `Python`
   * Root Directory: `backend`
   * Build Command: `pip install -r requirements.txt && python seed.py`
   * Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
2. **Link URL**: Update `RENDER_BACKEND_URL` in `frontend/js/api.js` to your deployed Render URL.
3. **Frontend Static Site**:
   * Root Directory: (Leave blank)
   * Build Command: (Leave blank)
   * Publish Directory: `frontend`
