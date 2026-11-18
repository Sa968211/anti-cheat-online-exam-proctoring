# ProctorLens-AI: Live Deployment Guide

This repository contains the complete full-stack **SKIT ProctorLens-AI** platform, unifying:
- **Vite React Frontend** (Glassmorphic UI, SKIT Branding, Test Stepper, 3-Tab Dashboard)
- **FastAPI Backend & Computer Vision Proctoring Engine** (OpenCV, MediaPipe, Gaze, Mobile Phone Detector, Backlight, Head Nodding, Code Sandbox, Gemini AI Viva)

---

## 🌐 1. Live Public Website (Active Now)

The entire full-stack application is currently hosted and accessible over the public internet with HTTPS:

🔗 **Live Website URL:** [https://great-papayas-bet.loca.lt](https://great-papayas-bet.loca.lt)

> **First-Time Browser Visit:**
> When opening the link for the first time, click **"Click to Continue"** (or enter the tunnel IP `157.50.199.190` if prompted by Localtunnel).
> Because the site is served over HTTPS, webcam and microphone permissions are fully enabled in Chrome, Safari, Edge, and mobile browsers.

---

## 🔐 Demo Credentials

### 1. Student / Candidate Access
- **Email:** `candidate@skit.org.in` (Any valid `@skit.org.in` email)
- **Password:** `candidate@123` (Format: `<name>@123`)
- **Features:** 25 Department examinations, MCQ Assessment, Coding Sandbox, Zam AI Viva, 3-Tab Proctoring Dashboard, Post-Exam Results & Trust Score.

### 2. Administrator Access
- **Email:** `admin@skit.org.in`
- **Password:** `admin@123`
- **Features:** Admit Student Console, Candidate Results & Trust Scores Audit Table, Live Proctor Telemetry Stream, Curriculum Test Studio, Push Alerts.

---

## ☁️ 2. Permanent 24/7 Cloud Deployment

### Option A: Render (Free Web Service)
1. Push this repository to GitHub.
2. Sign in to [Render.com](https://render.com) and click **"New +" -> "Web Service"**.
3. Select your GitHub repository.
4. Render automatically detects `render.yaml`:
   - **Build Command:** `npm install --prefix frontend && npm run build --prefix frontend && pip install -r backend/requirements.txt`
   - **Start Command:** `python -m uvicorn main:app --app-dir backend --host 0.0.0.0 --port $PORT`
5. Click **"Create Web Service"** to receive your permanent `https://your-app.onrender.com` domain.

---

### Option B: Docker Container Deployment (Railway / Fly.io / AWS / GCP)
Use the included multi-stage `Dockerfile`:

```bash
# 1. Build Docker image
docker build -t proctorlens-ai .

# 2. Run container
docker run -p 8000:8000 proctorlens-ai
```
The container builds the React frontend with Vite, sets up the Python backend with OpenCV and MediaPipe dependencies, and serves both through port 8000.

