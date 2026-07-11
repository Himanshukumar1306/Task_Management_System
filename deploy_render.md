# Render Deployment Guide - Taskify System

This guide walks you through deploying your **Taskify Task Management System** (FastAPI Backend + SQLite + HTML Frontend) to the web using **Render** (free hosting platform).

---

## Prerequisites
1. **GitHub Account**: Render deploys directly from GitHub repositories.
2. **Render Account**: Register for a free account at [render.com](https://render.com).

---

## Step 1: Create a GitHub Repository and Push Code
Render requires your project code to be on GitHub.

1. **Initialize Git** in your project root folder (`Snehal wanii Assignment`):
   Open a terminal in the folder and run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: taskify system"
   ```
2. **Push to GitHub**:
   * Create a new **public or private** repository on GitHub.
   * Link it and push:
     ```bash
     git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
     git branch -M main
     git push -u origin main
     ```

---

## Step 2: Deploy the FastAPI Backend Web Service
Render will host the FastAPI app as a **Web Service** (running in the `backend/` directory).

1. Log in to your **Render Dashboard** and click **New +** ➔ **Web Service**.
2. Select **Connect a repository** and choose your GitHub repository.
3. Configure the Web Service settings:
   * **Name**: `taskify-backend` (or a name of your choice)
   * **Region**: Select the closest region to you.
   * **Language**: `Python`
   * **Root Directory**: `backend` *(Crucial: This tells Render to look inside the backend folder)*
   * **Build Command**: `pip install -r requirements.txt && python seed.py` *(This installs libraries and seeds the SQLite database)*
   * **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   * **Instance Type**: `Free`
4. Click **Create Web Service** at the bottom of the page.
5. Once deployment completes, Render will provide you with a backend URL (e.g. `https://taskify-backend.onrender.com`). **Copy this URL**.

---

## Step 3: Link the Frontend to the Deployed Backend
Before deploying the frontend, we must update the frontend's API library to point to your new Render backend URL instead of localhost.

1. In VS Code, open the file [frontend/js/api.js](file:///c:/Users/kumar/OneDrive/Desktop/Snehal%20wanii%20Assignment/frontend/js/api.js).
2. Locate the variable `RENDER_BACKEND_URL` on line 2:
   ```javascript
   const RENDER_BACKEND_URL = 'https://task-management-system-backend.onrender.com';
   ```
3. Replace the placeholder URL with your **copied Render backend URL** from Step 2. (Make sure there is no trailing slash `/` at the end).
4. Commit and push this change to GitHub:
   ```bash
   git add frontend/js/api.js
   git commit -m "Update API endpoint to Render production URL"
   git push origin main
   ```

---

## Step 4: Deploy the Frontend Static Site
Render will host your frontend HTML/CSS/JS files as a **Static Site** for free.

1. In the Render Dashboard, click **New +** ➔ **Static Site**.
2. Connect the same GitHub repository.
3. Configure the Static Site settings:
   * **Name**: `taskify-app` (or any name)
   * **Root Directory**: (Leave blank)
   * **Build Command**: (Leave blank)
   * **Publish Directory**: `frontend` *(Crucial: This tells Render to only publish files inside the frontend folder)*
4. Click **Create Static Site**.

---

## Step 5: Test Your Live Site!
Once the Static Site finishes deploying, Render will give you a live frontend URL (e.g. `https://taskify-app.onrender.com`).

1. Open the frontend URL in your browser. You will see the SaaS landing website live!
2. Click **Launch Dashboard** to go to the login page.
3. Sign in using the seeded test accounts:
   * Username: `admin` | Password: `admin123`
   * Username: `snehal` | Password: `snehal123`
