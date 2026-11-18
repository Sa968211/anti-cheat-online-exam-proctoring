# 🛡️ ProctorLens-AI

> **Advanced AI-Powered Real-Time Anti-Cheat Camera Proctoring System**  
> Built with FastAPI, OpenCV, MediaPipe, React 18, and Tailwind CSS.

---

## 📌 Architecture Overview

ProctorLens-AI is an end-to-end automated proctoring platform designed for continuous examination integrity monitoring. The system continuously samples candidate webcam video frames at configurable intervals, performs non-intrusive computer vision inference, computes a real-time **Trust Score**, and visualizes logged infractions with image snapshot evidence.

```
┌─────────────────────────────────┐           ┌───────────────────────────────────┐
│        Candidate Browser        │           │          FastAPI Backend          │
│   (React + Tailwind Frontend)   │           │   (OpenCV + MediaPipe Vision)     │
├─────────────────────────────────┤           ├───────────────────────────────────┤
│ • WebcamFeed (Canvas Capturer)  │  Base64   │ • ProctorEngine Frame Ingestion   │
│ • Candidate Exam Sheet HUD      │ ────────> │ • Multi-Face Detection (Presence) │
│ • TrustScoreGauge (Radial/HUD)  │  JSON     │ • 3D Head Pose (Pitch, Yaw, Roll) │
│ • IncidentTimeline & Snapshots  │ <──────── │ • Infraction Weighting & Trust    │
└─────────────────────────────────┘           └───────────────────────────────────┘
```

---

## 🚀 Key Features

- **Presence & Absence Tracking**: Flags periods where no candidate is detected in the video stream.
- **Multi-Person Intrusion Detection**: Detects multiple faces in frame with instant `CRITICAL` severity penalty.
- **3D Head Orientation (Yaw/Pitch/Roll)**: Uses MediaPipe 3D face mesh and `cv2.solvePnP` to detect when a candidate turns left, right, up, or down outside permitted visual thresholds.
- **Dynamic Trust Score Degradation**: Automatically subtracts score points based on infraction severity with gradual score recovery for compliant behavior.
- **Incident Audit Timeline**: Stores timestamped violations with base64 evidence snapshot thumbnails and inspection modal.
- **Split-View Mock Interface**: Dual interface featuring candidate mock examination alongside live proctor auditor telemetry.

---

## 📂 Project Directory Structure

```text
ProctorLens-AI/
├── backend/
│   ├── main.py               # FastAPI entrypoint, CORS, routes & WebSocket
│   ├── proctor_engine.py     # OpenCV & MediaPipe vision logic & pose tracking
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── index.html            # Vite entrypoint HTML
│   ├── package.json          # Node dependencies (React, Lucide, Tailwind, Axios)
│   ├── vite.config.js        # Vite build & dev server config
│   ├── tailwind.config.js    # Tailwind styling theme
│   ├── postcss.config.js     # PostCSS configuration
│   └── src/
│       ├── main.jsx          # React DOM entrypoint
│       ├── App.jsx           # Split-view layout (Student Exam + Proctor Dashboard)
│       ├── index.css         # Tailwind base stylesheet
│       └── components/
│           ├── WebcamFeed.jsx         # Client-side stream capture & HUD
│           ├── TrustScoreGauge.jsx    # Real-time circular trust score & angles
│           └── IncidentTimeline.jsx   # Infraction audit log & snapshot modal
└── README.md                 # System documentation & setup guide
```

---

## 🛠️ Getting Started

### 1. Backend Setup (FastAPI & OpenCV)

1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   The API will be available at:
   - **Interactive API Docs (Swagger UI)**: `http://localhost:8000/docs`
   - **Health Check**: `http://localhost:8000/api/health`

---

### 2. Frontend Setup (React & Vite)

1. Open a second terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install npm packages:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5173
   ```
   Grant webcam permission when prompted by the browser.

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Returns backend service status and engine state |
| `POST` | `/api/analyze-frame` | Evaluates base64 frame, detects faces & pose, updates trust score |
| `GET` | `/api/session/status` | Returns session trust score and full incident list |
| `POST` | `/api/session/reset` | Resets trust score to 100% and purges incident log |
| `WS` | `/ws/proctor` | WebSocket stream for low-latency bidirectional telemetry |

---

## ⚖️ Infraction Penalties & Thresholds

| Infraction Code | Severity | Trust Deduction | Trigger Condition |
|---|---|---|---|
| `NO_FACE_DETECTED` | `HIGH` | -15.0 pts | Face count = 0 |
| `MULTIPLE_FACES_DETECTED` | `CRITICAL` | -25.0 pts | Face count > 1 |
| `HEAD_TURNED_AWAY` | `MEDIUM` | -10.0 pts | Yaw > ±28° or Pitch > ±25° |
| `SUSPICIOUS_GAZE` | `LOW` | -5.0 pts | Persistent off-screen glance |

---

## 📄 License
MIT License. Built for proctoring research, candidate authentication, and academic integrity automation.

