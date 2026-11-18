"""
QuizService: Core AI Assessment & Question Generation Engine
============================================================
Supports:
1. PDF and Raw Text Syllabus / Chapter Ingestion
2. Balanced 10-Question Generation (6 MCQs + 4 Short Answer)
3. Multi-LLM Provider Integration (Google Gemini / OpenAI / Local Heuristic Fallback)
4. Automated AI Grading with Semantic Comparison & Personalized Feedback Summary
"""

import os
import re
import json
import time
import uuid
import io
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional, Tuple

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


class QuizService:
    def __init__(self, default_api_key: Optional[str] = None):
        self.default_api_key = (
            default_api_key
            or os.environ.get("GEMINI_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
        )
        self.in_memory_quizzes: Dict[str, Dict[str, Any]] = {}

    # -------------------------------------------------------------------------
    # 1. Document Extraction & Preprocessing
    # -------------------------------------------------------------------------
    @staticmethod
    def extract_text_from_pdf(file_bytes_or_stream) -> str:
        """Extracts and normalizes text from a PDF file stream or bytes."""
        if not PYPDF_AVAILABLE:
            raise RuntimeError("pypdf is not installed. Please install pypdf to parse PDF files.")

        if isinstance(file_bytes_or_stream, bytes):
            stream = io.BytesIO(file_bytes_or_stream)
        else:
            stream = file_bytes_or_stream

        reader = PdfReader(stream)
        extracted_pages = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                extracted_pages.append(page_text.strip())

        full_text = "\n\n".join(extracted_pages)
        # Clean extra whitespace
        cleaned = re.sub(r"[ \t]+", " ", full_text)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned.strip()

    # -------------------------------------------------------------------------
    # 2. Automated Balanced Quiz Generation (10 Questions)
    # -------------------------------------------------------------------------
    def generate_quiz(
        self,
        source_text: str,
        topic: Optional[str] = None,
        num_questions: int = 10,
        mcq_count: int = 6,
        short_answer_count: int = 4,
        difficulty: str = "Intermediate",
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a balanced assessment containing MCQs and Short Answer questions
        from the provided syllabus/chapter content.
        """
        source_clean = source_text.strip()
        if not source_clean:
            raise ValueError("Source text cannot be empty. Please provide syllabus or chapter text.")

        active_key = api_key or self.default_api_key
        quiz_data: Optional[Dict[str, Any]] = None

        # 1. Attempt LLM generation if API Key is available
        if active_key:
            try:
                quiz_data = self._generate_with_llm(
                    source_text=source_clean,
                    topic=topic,
                    num_questions=num_questions,
                    mcq_count=mcq_count,
                    short_answer_count=short_answer_count,
                    difficulty=difficulty,
                    api_key=active_key
                )
            except Exception as e:
                print(f"[QuizService] LLM Generation encountered an error: {e}. Falling back to Smart Heuristic Engine.")
                quiz_data = None

        # 2. Fallback to Local Deterministic NLP Heuristic Engine
        if not quiz_data:
            quiz_data = self._generate_with_nlp_heuristics(
                source_text=source_clean,
                topic=topic or "Curriculum Assessment",
                mcq_count=mcq_count,
                short_answer_count=short_answer_count,
                difficulty=difficulty
            )

        quiz_id = f"quiz-{uuid.uuid4().hex[:8]}"
        quiz_data["id"] = quiz_id
        quiz_data["created_at"] = time.time()
        quiz_data["topic"] = topic or quiz_data.get("topic") or "General Syllabus"
        quiz_data["difficulty"] = difficulty

        # Calculate total marks
        total_marks = sum(q.get("marks", 2) for q in quiz_data["questions"])
        quiz_data["total_marks"] = total_marks

        # Store in memory
        self.in_memory_quizzes[quiz_id] = quiz_data
        return quiz_data

    # -------------------------------------------------------------------------
    # 3. LLM API Integration (Gemini & OpenAI)
    # -------------------------------------------------------------------------
    def _generate_with_llm(
        self,
        source_text: str,
        topic: Optional[str],
        num_questions: int,
        mcq_count: int,
        short_answer_count: int,
        difficulty: str,
        api_key: str
    ) -> Dict[str, Any]:
        """Calls Google Gemini or OpenAI to formulate a structured assessment in strict JSON."""
        # Truncate source if extremely large (up to ~18,000 characters for optimal prompt size)
        truncated_source = source_text[:18000]

        prompt = f"""
You are an expert university professor and pedagogical assessment designer.
Generate a rigorous, high-quality, balanced examination of exactly {num_questions} questions ({mcq_count} Multiple Choice Questions and {short_answer_count} Short Answer Questions) based SOLELY on the provided syllabus/chapter text.

Difficulty Level: {difficulty}
Topic/Subject: {topic or 'Extracted from content'}

Source Text Content:
\"\"\"{truncated_source}\"\"\"

Output your response in STRICT valid JSON format with NO markdown wrapping, conforming to this exact schema:
{{
  "title": "Comprehensive Assessment on [Topic]",
  "topic": "[Inferred Topic]",
  "summary": "Brief 1-2 sentence overview of the syllabus coverage.",
  "questions": [
    {{
      "id": "q1",
      "type": "mcq",
      "question": "Clear conceptual question statement?",
      "options": [
        "A) Option 1",
        "B) Option 2",
        "C) Option 3",
        "D) Option 4"
      ],
      "correct_option": "A",
      "explanation": "Detailed explanation of why this answer is correct based on the text.",
      "marks": 2
    }},
    {{
      "id": "q{mcq_count + 1}",
      "type": "short_answer",
      "question": "Analytical question requiring 2-4 sentences explanation?",
      "sample_answer": "Complete expected exemplary answer for grading.",
      "key_concepts": ["concept 1", "key phrase 2", "essential term 3"],
      "grading_rubric": "Full marks for identifying X and explaining Y.",
      "marks": 3
    }}
  ]
}}
Ensure exactly {mcq_count} items have "type": "mcq" and {short_answer_count} items have "type": "short_answer".
Return only the raw JSON string.
"""

        if api_key.startswith("AIza"):
            raw_json = self._call_gemini_api(prompt, api_key)
        else:
            raw_json = self._call_openai_api(prompt, api_key)

        # Parse JSON output safely
        clean_json_str = raw_json.strip()
        if clean_json_str.startswith("```json"):
            clean_json_str = clean_json_str[7:]
        if clean_json_str.startswith("```"):
            clean_json_str = clean_json_str[3:]
        if clean_json_str.endswith("```"):
            clean_json_str = clean_json_str[:-3]
        clean_json_str = clean_json_str.strip()

        data = json.loads(clean_json_str)
        if "questions" not in data or not isinstance(data["questions"], list):
            raise ValueError("Malformed LLM response missing 'questions' list.")

        # Assign unique IDs
        for idx, q in enumerate(data["questions"]):
            q["id"] = f"q{idx + 1}"
            if "marks" not in q:
                q["marks"] = 2 if q.get("type") == "mcq" else 3

        return data

    def _call_gemini_api(self, prompt: str, api_key: str) -> str:
        """Direct REST caller for Google Gemini."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json"
            }
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            res_body = json.loads(response.read().decode("utf-8"))
            candidates = res_body.get("candidates", [])
            if candidates:
                return candidates[0]["content"]["parts"][0]["text"]
            raise ValueError("No candidates returned from Gemini API.")

    def _call_openai_api(self, prompt: str, api_key: str) -> str:
        """Direct REST caller for OpenAI GPT models."""
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a professional educational assessment generator that returns strict JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            res_body = json.loads(response.read().decode("utf-8"))
            return res_body["choices"][0]["message"]["content"]

    # -------------------------------------------------------------------------
    # 4. Local NLP Heuristic Engine (Deterministic Fallback)
    # -------------------------------------------------------------------------
    def _generate_with_nlp_heuristics(
        self,
        source_text: str,
        topic: str,
        mcq_count: int,
        short_answer_count: int,
        difficulty: str
    ) -> Dict[str, Any]:
        """
        Parses sentences, key terms, definitions, and concepts to construct
        balanced MCQs and Short Answer questions when offline or without an API key.
        """
        paragraphs = [p.strip() for p in source_text.split("\n\n") if len(p.strip()) > 40]
        sentences = re.split(r"(?<=[.!?])\s+", source_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 35 and not s.strip().startswith("#")]

        # Extract technical keywords (words >= 5 chars capitalized or frequent nouns)
        words = re.findall(r"\b[A-Za-z]{4,}\b", source_text)
        freq: Dict[str, int] = {}
        for w in words:
            wl = w.lower()
            if wl not in {"which", "their", "there", "about", "would", "these", "other", "after", "first", "could", "should", "using", "being"}:
                freq[w] = freq.get(w, 0) + 1
        sorted_terms = sorted(freq.keys(), key=lambda k: freq[k], reverse=True)
        top_terms = sorted_terms[:30] if sorted_terms else ["Algorithm", "Architecture", "Data", "Security", "Protocol"]

        questions = []

        # 1. Generate MCQs
        for i in range(mcq_count):
            q_id = f"q{i + 1}"
            if i < len(sentences):
                sentence = sentences[i % len(sentences)]
            else:
                sentence = f"The primary operational principle of {topic} relies on structured system constraints."

            # Find a focal keyword to blank out or question
            focal_word = None
            for w in top_terms:
                if w in sentence:
                    focal_word = w
                    break
            if not focal_word:
                match = re.search(r"\b[A-Z][a-z]{3,}\b", sentence)
                focal_word = match.group(0) if match else "Core Concept"

            # Create plausible distractors
            distractors = [w for w in top_terms if w.lower() != focal_word.lower()][:3]
            while len(distractors) < 3:
                distractors.append(f"Alternative {len(distractors) + 1}")

            all_opts = [focal_word] + distractors
            # Deterministic pseudo-shuffle based on question index
            shift = i % 4
            all_opts = all_opts[shift:] + all_opts[:shift]
            correct_letter = chr(ord('A') + all_opts.index(focal_word))

            formatted_options = [
                f"A) {all_opts[0]}",
                f"B) {all_opts[1]}",
                f"C) {all_opts[2]}",
                f"D) {all_opts[3]}"
            ]

            masked_q = sentence.replace(focal_word, "__________", 1)
            q_stmt = f"According to the text, complete the following principle: \"{masked_q}\""

            questions.append({
                "id": q_id,
                "type": "mcq",
                "question": q_stmt,
                "options": formatted_options,
                "correct_option": correct_letter,
                "explanation": f"The source text explicitly states: '{sentence}', identifying '{focal_word}' as the correct term.",
                "marks": 2
            })

        # 2. Generate Short Answer Questions
        for j in range(short_answer_count):
            q_idx = mcq_count + j + 1
            q_id = f"q{q_idx}"
            para = paragraphs[j % len(paragraphs)] if paragraphs else (sentences[j % len(sentences)] if sentences else source_text[:200])

            # Pick a core concept
            term = top_terms[j % len(top_terms)] if top_terms else "System Component"
            first_sent = para.split(".")[0].strip() + "."

            question_prompts = [
                f"Explain the purpose and function of '{term}' as described in the syllabus.",
                f"Analyze how '{term}' contributes to the overall architecture or workflow discussed.",
                f"Summarize the key attributes and implementation considerations of '{term}'.",
                f"Discuss the practical implications of the following concept: \"{first_sent}\""
            ]

            q_text = question_prompts[j % len(question_prompts)]
            key_concepts = [term.lower(), "implementation", "efficiency", "structure"]
            rubric = f"Award 3 marks for comprehensive explanation of '{term}', including its definition and functional context."

            questions.append({
                "id": q_id,
                "type": "short_answer",
                "question": q_text,
                "sample_answer": f"In the context of the curriculum, {para[:220]}...",
                "key_concepts": key_concepts,
                "grading_rubric": rubric,
                "marks": 3
            })

        return {
            "title": f"Autonomous Assessment: {topic}",
            "topic": topic,
            "summary": f"Automated 10-question evaluation extracted from {len(source_text)} characters of curriculum content.",
            "questions": questions
        }

    # -------------------------------------------------------------------------
    # 5. Automated AI Grading & Personalized Feedback
    # -------------------------------------------------------------------------
    def grade_answers(
        self,
        quiz: Dict[str, Any],
        student_answers: Dict[str, Any],
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Auto-grades student submissions:
        - Evaluates MCQs with exact/semantic match.
        - Evaluates Short Answers with NLP key-concept coverage / semantic alignment.
        - Generates itemized marks, strengths, areas for improvement, and personalized feedback.
        """
        active_key = api_key or self.default_api_key
        questions = quiz.get("questions", [])
        total_possible = sum(q.get("marks", 2) for q in questions)
        total_earned = 0.0

        itemized_results = []
        strengths = []
        improvements = []

        for q in questions:
            q_id = q["id"]
            q_type = q.get("type", "mcq")
            q_marks = float(q.get("marks", 2))
            raw_answer = str(student_answers.get(q_id, "")).strip()

            if q_type == "mcq":
                correct_opt = str(q.get("correct_option", "")).strip().upper()
                # Accept both letter "A" or "A) text" or plain text match
                user_opt = raw_answer.upper()
                if len(user_opt) > 0:
                    user_letter = user_opt[0]
                else:
                    user_letter = ""

                is_correct = (user_letter == correct_opt) or (raw_answer.lower() == str(q.get("options", [""])[0]).lower())

                if is_correct:
                    earned = q_marks
                    status = "CORRECT"
                    strengths.append(f"Mastery on question #{q_id}: {q['question'][:50]}...")
                else:
                    earned = 0.0
                    status = "INCORRECT"
                    improvements.append(f"Review question #{q_id}: {q.get('explanation', 'Consult source material.')[:70]}...")

                total_earned += earned
                itemized_results.append({
                    "question_id": q_id,
                    "type": "mcq",
                    "question": q["question"],
                    "student_answer": raw_answer or "(No answer provided)",
                    "correct_answer": q.get("correct_option", "A"),
                    "options": q.get("options", []),
                    "explanation": q.get("explanation", ""),
                    "marks_possible": q_marks,
                    "marks_earned": earned,
                    "status": status,
                    "feedback": "Correct selection!" if is_correct else f"Incorrect. Correct option was {correct_opt}."
                })

            else:
                # Short Answer Grading
                earned, feedback, status = self._grade_short_answer(
                    question=q,
                    student_text=raw_answer,
                    api_key=active_key
                )
                total_earned += earned
                if earned >= (q_marks * 0.7):
                    strengths.append(f"Solid articulation on '{q['question'][:45]}...'")
                else:
                    improvements.append(f"Deeper conceptual detail required for '{q['question'][:45]}...'")

                itemized_results.append({
                    "question_id": q_id,
                    "type": "short_answer",
                    "question": q["question"],
                    "student_answer": raw_answer or "(No answer provided)",
                    "sample_answer": q.get("sample_answer", ""),
                    "grading_rubric": q.get("grading_rubric", ""),
                    "marks_possible": q_marks,
                    "marks_earned": round(earned, 1),
                    "status": status,
                    "feedback": feedback
                })

        percentage = round((total_earned / total_possible) * 100, 1) if total_possible > 0 else 0.0

        # Determine Letter Grade
        if percentage >= 90:
            letter = "A+ (Outstanding)"
        elif percentage >= 80:
            letter = "A (Excellent)"
        elif percentage >= 70:
            letter = "B (Proficient)"
        elif percentage >= 60:
            letter = "C (Competent)"
        elif percentage >= 50:
            letter = "D (Passing)"
        else:
            letter = "F (Needs Intensive Revision)"

        # Generate Personalized Summary
        summary = (
            f"Candidate completed the assessment on '{quiz.get('topic', 'Syllabus')}' earning "
            f"{total_earned:.1f} of {total_possible:.1f} marks ({percentage}% - {letter}). "
        )
        if percentage >= 75:
            summary += "Demonstrated strong foundational comprehension across core multiple-choice and conceptual formulations."
        elif percentage >= 50:
            summary += "Satisfactory grasp of key topics, though technical depth in descriptive responses can be enhanced."
        else:
            summary += "Recommended to revisit foundational chapter sections and practice applying concepts to concrete scenarios."

        return {
            "quiz_id": quiz.get("id"),
            "topic": quiz.get("topic"),
            "total_score": round(total_earned, 1),
            "max_score": total_possible,
            "percentage": percentage,
            "letter_grade": letter,
            "personalized_feedback_summary": summary,
            "strengths": strengths[:4] or ["Attempted all assessment sections."],
            "areas_for_improvement": improvements[:4] or ["Review descriptive answers for additional detail."],
            "question_breakdown": itemized_results
        }

    def _grade_short_answer(
        self,
        question: Dict[str, Any],
        student_text: str,
        api_key: Optional[str] = None
    ) -> Tuple[float, str, str]:
        """Evaluates a single short answer response."""
        q_marks = float(question.get("marks", 3))
        text = student_text.strip()
        if not text:
            return 0.0, "No answer submitted.", "EMPTY"

        # 1. If LLM available, evaluate semantic match
        if api_key:
            try:
                eval_prompt = f"""
Evaluate this student's short answer response against the question and rubric.
Question: {question['question']}
Sample Ideal Answer: {question.get('sample_answer', '')}
Key Concepts to cover: {json.dumps(question.get('key_concepts', []))}
Grading Rubric: {question.get('grading_rubric', '')}
Maximum Marks: {q_marks}

Student Submitted Answer:
\"{text}\"

Return STRICT JSON:
{{
  "marks_awarded": float between 0.0 and {q_marks},
  "feedback": "1-2 sentences of personalized constructive feedback."
}}
"""
                raw = self._call_gemini_api(eval_prompt, api_key) if api_key.startswith("AIza") else self._call_openai_api(eval_prompt, api_key)
                clean = raw.strip().replace("```json", "").replace("```", "").strip()
                res = json.loads(clean)
                awarded = max(0.0, min(q_marks, float(res.get("marks_awarded", 0))))
                feedback = res.get("feedback", "Automated LLM semantic evaluation.")
                status = "EXCELLENT" if awarded >= q_marks * 0.8 else ("PARTIAL" if awarded >= q_marks * 0.4 else "NEEDS_IMPROVEMENT")
                return awarded, feedback, status
            except Exception as e:
                print(f"[QuizService] LLM grading failed: {e}. Falling back to NLP similarity.")

        # 2. NLP Semantic Concept Overlap Fallback
        key_concepts = [k.lower() for k in question.get("key_concepts", [])]
        text_lower = text.lower()

        # Check concept keyword presence
        matched_concepts = [k for k in key_concepts if k in text_lower]
        concept_coverage = len(matched_concepts) / max(1, len(key_concepts))

        # Sentence length and completeness check (50 - 250 characters ideal)
        length_factor = min(1.0, len(text) / 80.0)

        # Weighted calculation
        raw_score = (concept_coverage * 0.7 + length_factor * 0.3) * q_marks
        awarded = round(max(0.5, min(q_marks, raw_score)), 1)

        if concept_coverage >= 0.7:
            status = "STRONG"
            fb = f"Well explained! Addressed key concepts: {', '.join(matched_concepts)}."
        elif concept_coverage >= 0.3:
            status = "PARTIAL"
            fb = f"Partially correct. Identified {', '.join(matched_concepts)}, but missed other core aspects."
        else:
            status = "NEEDS_IMPROVEMENT"
            fb = "Answer lacks essential concepts described in the curriculum source text."

        return awarded, fb, status

