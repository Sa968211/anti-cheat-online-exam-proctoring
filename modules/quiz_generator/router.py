"""
FastAPI APIRouter for Factskoot Autonomous AI Quiz & Assessment Generator
========================================================================
Mounts directly into any FastAPI server:
    from modules.quiz_generator.router import quiz_router
    app.include_router(quiz_router)
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Body
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from .quiz_service import QuizService

quiz_router = APIRouter(prefix="/api/quiz-generator", tags=["Autonomous Quiz Generator"])
quiz_service = QuizService()


# -----------------------------------------------------------------------------
# Request Models
# -----------------------------------------------------------------------------
class GenerateQuizRequest(BaseModel):
    text: Optional[str] = Field(None, description="Raw syllabus or chapter content text")
    topic: Optional[str] = Field(None, description="Topic or subject name")
    num_questions: int = Field(10, description="Total questions to generate (default 10)")
    mcq_count: int = Field(6, description="Number of Multiple Choice Questions")
    short_answer_count: int = Field(4, description="Number of Short Answer Questions")
    difficulty: str = Field("Intermediate", description="Difficulty: Beginner, Intermediate, Advanced")
    api_key: Optional[str] = Field(None, description="Optional Google Gemini or OpenAI API Key")


class GradeAnswersRequest(BaseModel):
    quiz_id: Optional[str] = None
    quiz: Optional[Dict[str, Any]] = None
    student_answers: Dict[str, Any] = Field(..., description="Mapping of question ID to student's answer")
    api_key: Optional[str] = None


# -----------------------------------------------------------------------------
# 1. Generate Quiz Endpoint
# -----------------------------------------------------------------------------
@quiz_router.post("/generate-quiz")
async def generate_quiz(
    # Supports JSON payload
    payload: Optional[GenerateQuizRequest] = Body(None),
    # Also supports multipart form data with file upload
    file: Optional[UploadFile] = File(None),
    topic: Optional[str] = Form(None),
    num_questions: int = Form(10),
    mcq_count: int = Form(6),
    short_answer_count: int = Form(4),
    difficulty: str = Form("Intermediate"),
    api_key: Optional[str] = Form(None),
    text: Optional[str] = Form(None)
):
    """
    Generates a balanced assessment of 10 questions (MCQs + Short Answer)
    from raw text or an uploaded PDF document.
    """
    extracted_text = ""
    req_topic = topic
    req_num = num_questions
    req_mcq = mcq_count
    req_short = short_answer_count
    req_diff = difficulty
    req_key = api_key

    if payload is not None:
        extracted_text = payload.text or ""
        req_topic = payload.topic or req_topic
        req_num = payload.num_questions
        req_mcq = payload.mcq_count
        req_short = payload.short_answer_count
        req_diff = payload.difficulty
        req_key = payload.api_key or req_key

    # Handle file upload if present
    if file is not None:
        try:
            file_bytes = await file.read()
            if file.filename.lower().endswith(".pdf"):
                extracted_text = quiz_service.extract_text_from_pdf(file_bytes)
            else:
                extracted_text = file_bytes.decode("utf-8", errors="ignore")

            if not req_topic and file.filename:
                req_topic = file.filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to process uploaded file: {str(e)}")
    elif text:
        extracted_text = text

    if not extracted_text or len(extracted_text.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="Source content too short or missing. Please paste syllabus text or upload a chapter PDF document."
        )

    try:
        quiz = quiz_service.generate_quiz(
            source_text=extracted_text,
            topic=req_topic,
            num_questions=req_num,
            mcq_count=req_mcq,
            short_answer_count=req_short,
            difficulty=req_diff,
            api_key=req_key
        )
        return {
            "status": "SUCCESS",
            "message": f"Successfully synthesized {len(quiz['questions'])} questions for '{quiz['topic']}'.",
            "quiz": quiz
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quiz generation failed: {str(e)}")


# -----------------------------------------------------------------------------
# 2. Grade Answers Endpoint
# -----------------------------------------------------------------------------
@quiz_router.post("/grade-answers")
def grade_answers(payload: GradeAnswersRequest):
    """
    Compares student submitted answers against the source rubric/options
    and outputs a score, itemized feedback, strengths, and personalized summary.
    """
    quiz = payload.quiz
    if not quiz and payload.quiz_id:
        quiz = quiz_service.in_memory_quizzes.get(payload.quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz reference not found. Please provide the 'quiz' object or valid 'quiz_id'."
        )

    try:
        report = quiz_service.grade_answers(
            quiz=quiz,
            student_answers=payload.student_answers,
            api_key=payload.api_key
        )
        return {
            "status": "GRADED",
            "report": report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Grading failed: {str(e)}")


# -----------------------------------------------------------------------------
# 3. Quiz Management Endpoints
# -----------------------------------------------------------------------------
@quiz_router.get("/quizzes")
def list_quizzes():
    """Returns list of active generated quizzes."""
    return {
        "total": len(quiz_service.in_memory_quizzes),
        "quizzes": [
            {
                "id": q["id"],
                "title": q["title"],
                "topic": q["topic"],
                "total_marks": q.get("total_marks", 25),
                "questions_count": len(q.get("questions", [])),
                "created_at": q.get("created_at")
            }
            for q in quiz_service.in_memory_quizzes.values()
        ]
    }


@quiz_router.get("/quizzes/{quiz_id}")
def get_quiz(quiz_id: str):
    """Retrieves full quiz data for student taking."""
    quiz = quiz_service.in_memory_quizzes.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail=f"Quiz '{quiz_id}' not found.")
    return {"quiz": quiz}


@quiz_router.post("/quizzes/save")
def save_quiz(quiz_data: Dict[str, Any] = Body(...)):
    """Allows educator to save an edited quiz."""
    quiz_id = quiz_data.get("id") or f"quiz-{uuid.uuid4().hex[:8]}"
    quiz_data["id"] = quiz_id
    quiz_service.in_memory_quizzes[quiz_id] = quiz_data
    return {
        "status": "SAVED",
        "message": f"Quiz '{quiz_data.get('title', quiz_id)}' saved successfully.",
        "quiz_id": quiz_id
    }

