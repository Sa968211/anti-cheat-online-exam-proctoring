"""
Factskoot Live Campus Project - Problem Statement 1
Autonomous AI Quiz & Assessment Generator Module
=================================================
A decoupled, plug-and-play module for:
1. Automated 10-Question Balanced Quiz Generation from Syllabus text or PDFs (MCQs + Short Answers)
2. Automated Intelligent AI Grading & Personalized Feedback
3. Teacher Dashboard & Student Quiz-Taking Interfaces
"""

from .quiz_service import QuizService
from .router import quiz_router

__all__ = ["QuizService", "quiz_router"]

