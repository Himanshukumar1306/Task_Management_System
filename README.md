# Taskify - Premium Task Management System

Name - Himanshu Kumar
Reg. no . - 23BCE11375

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


