"""
Standalone FastAPI Server for Factskoot Autonomous AI Quiz Generator
=====================================================================
Runs independently on port 8010 without touching or altering the proctoring engine.

Launch:
    python modules/quiz_generator/server.py
Or:
    python -m uvicorn modules.quiz_generator.server:app --host 127.0.0.1 --port 8010
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

# Local decoupled imports
from .router import quiz_router

app = FastAPI(
    title="Factskoot Autonomous AI Quiz & Assessment Generator",
    description="Decoupled pedagogical assessment generation and auto-grading microservice for Factskoot Live Campus.",
    version="1.0.0"
)

# CORS Middleware (permits frontend ports)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the decoupled router at both the root api and prefixed api for maximum flexibility
app.include_router(quiz_router)
# Direct problem statement endpoint aliases:
app.include_router(quiz_router, prefix="")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Serve standalone modern web application
@app.get("/")
@app.get("/dashboard")
def serve_dashboard():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "service": "Factskoot Autonomous AI Quiz & Assessment Generator",
        "status": "ONLINE",
        "port": 8010,
        "endpoints": [
            "/api/quiz-generator/generate-quiz",
            "/api/quiz-generator/grade-answers",
            "/api/quiz-generator/quizzes"
        ]
    }


if __name__ == "__main__":
    port = int(os.environ.get("QUIZ_GENERATOR_PORT", 8010))
    print(f"🚀 Starting Factskoot Autonomous AI Quiz Generator on http://127.0.0.1:{port}")
    uvicorn.run("modules.quiz_generator.server:app", host="127.0.0.1", port=port, reload=False)

