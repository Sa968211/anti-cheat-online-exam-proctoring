# Factskoot Live Campus Project: Autonomous AI Quiz & Assessment Generator
**Hackathon Problem Statement 1 Integration Module**

---

## 📌 Executive Summary

This module implements a **completely decoupled, autonomous AI assessment and quiz generation microservice**. Designed according to the specifications of **Factskoot Hackathon Problem Statement 1**, it operates independently without touching, altering, or modifying any existing anti-cheat proctoring scripts (`proctor_engine.py`, `database.py`, etc.).

---

## 🏗️ Architecture & Component Directory

All files reside in `/modules/quiz_generator/`:

```
modules/quiz_generator/
├── __init__.py                     # Package export
├── requirements.txt               # Isolated dependencies (pypdf, fastapi, uvicorn, requests, streamlit)
├── quiz_service.py                # Core Assessment Synthesis & Semantic Auto-Grading Engine
├── router.py                      # FastAPI APIRouter exposing /generate-quiz & /grade-answers
├── server.py                      # Standalone FastAPI Server (Port 8010)
├── ui_app.py                      # Standalone Streamlit App (Teacher Dashboard + Student Quiz)
├── static/
│   └── index.html                 # Standalone React-Style Modern Web SPA (Tailwind + Lucide)
├── QuizGeneratorDashboard.jsx     # Decoupled React UI Component for frontend drop-in
└── README.md                      # Comprehensive integration & mounting documentation
```

---

## ⚡ Core Capabilities

1. **Multi-Source Content Ingestion:**
   - Ingests raw text (lecture notes, syllabus modules, textbook excerpts) or binary PDF documents (`pypdf` extraction).
2. **Balanced 10-Question Formulation:**
   - Synthesizes exactly 10 questions: a configurable balance of **6 Multiple Choice Questions** (4 distractors, answer key, and pedagogical rationale) and **4 Analytical Short Answer Questions** (with ideal sample answers, key concepts, and grading rubrics).
3. **Dual AI Generation Pipeline:**
   - **LLM Pipeline:** Direct integration with Google Gemini 1.5/2.0 Flash or OpenAI GPT-4o-mini using direct REST callers.
   - **Local NLP Heuristic Engine:** Offline deterministic fallback that extracts conceptual keywords, entities, and definitions to formulate realistic MCQs and short answers even with zero API key configuration.
4. **Intelligent Semantic Auto-Grading:**
   - Evaluates student MCQs (100% precision with letter/option matching).
   - Evaluates descriptive short answers using semantic concept coverage and keyword presence.
   - Outputs:
     - Total score, percentage, and official letter grade (`A+`, `A`, `B`, etc.).
     - Personalized constructive feedback summary.
     - Identified student strengths and areas for improvement.
     - Question-by-question itemized breakdown.

---

## 🚀 How to Run Standalone

### Mode 1: Dedicated FastAPI Server & Modern Web UI (Port 8010)
Run the standalone server:
```bash
python modules/quiz_generator/server.py
```
Or via uvicorn:
```bash
python -m uvicorn modules.quiz_generator.server:app --host 127.0.0.1 --port 8010
```
Open **[http://127.0.0.1:8010](http://127.0.0.1:8010)** in your browser to access the complete interactive Teacher Dashboard & Student Examination interface.

---

### Mode 2: Interactive Streamlit Application (Port 8501)
Launch the Streamlit app:
```bash
streamlit run modules/quiz_generator/ui_app.py --server.port 8501
```
Open **[http://localhost:8501](http://localhost:8501)** for the Streamlit dashboard with PDF drag-and-drop, question editing, and real-time auto-grading.

---

## 🔌 How to Mount Into the Main App (Optional 2-Line Integration)

Because the router is fully modular and decoupled, you can mount it into your main FastAPI application (`backend/main.py`) in two lines without altering any existing anti-cheat code:

### 1. Mount Backend Endpoints (`backend/main.py`):
```python
# At the bottom of backend/main.py (or with your router includes):
from modules.quiz_generator.router import quiz_router

app.include_router(quiz_router)
```
This immediately registers:
- `POST /api/quiz-generator/generate-quiz` (and `/api/generate-quiz`)
- `POST /api/quiz-generator/grade-answers` (and `/api/grade-answers`)
- `GET /api/quiz-generator/quizzes`

### 2. Mount React Frontend (`frontend/src/`):
Copy or reference `modules/quiz_generator/QuizGeneratorDashboard.jsx`:
```jsx
import QuizGeneratorDashboard from '../../modules/quiz_generator/QuizGeneratorDashboard';

// Render anywhere in your navigation or admin suite:
<QuizGeneratorDashboard />
```

---

## 📡 API Endpoint Reference

### 1. Generate Quiz: `POST /api/quiz-generator/generate-quiz`
#### Request (JSON):
```json
{
  "text": "Virtual memory is a memory management technique that provides an idealized abstraction of the storage resources that are actually available on a given machine...",
  "topic": "Operating Systems: Virtual Memory",
  "num_questions": 10,
  "mcq_count": 6,
  "short_answer_count": 4,
  "difficulty": "Intermediate",
  "api_key": "optional-gemini-or-openai-key"
}
```
*Note: Also accepts `multipart/form-data` with a `file: UploadFile` (.pdf or .txt).*

#### Response (JSON):
```json
{
  "status": "SUCCESS",
  "message": "Successfully synthesized 10 questions for 'Operating Systems: Virtual Memory'.",
  "quiz": {
    "id": "quiz-a1b2c3d4",
    "title": "Autonomous Assessment: Operating Systems: Virtual Memory",
    "topic": "Operating Systems: Virtual Memory",
    "total_marks": 24,
    "questions": [
      {
        "id": "q1",
        "type": "mcq",
        "question": "What primary abstraction does virtual memory provide?",
        "options": ["A) Contiguous address space", "B) Direct hardware cache", "C) Raw disk partitions", "D) Unpaged DRAM"],
        "correct_option": "A",
        "explanation": "Virtual memory creates the illusion of a large, contiguous memory space.",
        "marks": 2
      },
      {
        "id": "q7",
        "type": "short_answer",
        "question": "Explain the role of the Translation Lookaside Buffer (TLB).",
        "sample_answer": "The TLB is a high-speed hardware cache used to reduce the overhead of page table lookups by caching recent virtual-to-physical address mappings.",
        "key_concepts": ["cache", "page table", "address mapping"],
        "grading_rubric": "Award 3 marks for mentioning virtual-to-physical address caching and speed optimization.",
        "marks": 3
      }
    ]
  }
}
```

---

### 2. Auto-Grade Answers: `POST /api/quiz-generator/grade-answers`
#### Request (JSON):
```json
{
  "quiz": { ... },
  "student_answers": {
    "q1": "A",
    "q7": "The TLB caches address mappings from virtual to physical memory so CPU accesses are faster."
  }
}
```

#### Response (JSON):
```json
{
  "status": "GRADED",
  "report": {
    "quiz_id": "quiz-a1b2c3d4",
    "total_score": 21.5,
    "max_score": 24.0,
    "percentage": 89.6,
    "letter_grade": "A (Excellent)",
    "personalized_feedback_summary": "Candidate demonstrated strong foundational comprehension across core multiple-choice and conceptual formulations.",
    "strengths": [
      "Mastery on question #q1",
      "Solid articulation on 'Explain the role of the TLB'"
    ],
    "areas_for_improvement": [
      "Review descriptive answers for additional detail."
    ],
    "question_breakdown": [ ... ]
  }
}
```

