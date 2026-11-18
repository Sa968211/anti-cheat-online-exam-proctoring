"""
Streamlit Standalone Web Application: Autonomous AI Quiz & Assessment Generator
==============================================================================
Launch with:
    streamlit run modules/quiz_generator/ui_app.py --server.port 8501
"""

import streamlit as st
import json
import time
from quiz_service import QuizService

st.set_page_config(
    page_title="Factskoot AI Quiz Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize QuizService in session state
if "quiz_service" not in st.session_state:
    st.session_state.quiz_service = QuizService()

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

if "graded_report" not in st.session_state:
    st.session_state.graded_report = None

# Custom Modern Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #06b6d4, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .quiz-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .score-badge {
        font-size: 2.5rem;
        font-weight: 900;
        color: #10b981;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 Autonomous AI Quiz & Assessment Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Factskoot Live Campus Integration • Problem Statement 1: Decoupled Syllabus Ingestion & Auto-Grading</div>', unsafe_allow_html=True)

# Top Navigation Tabs
tab_teacher, tab_student, tab_info = st.tabs([
    "👩‍🏫 Teacher Dashboard (Generate & Edit)",
    "✍️ Student Quiz Taking & Auto-Grading",
    "ℹ️ Integration & API Docs"
])

# -----------------------------------------------------------------------------
# TAB 1: TEACHER DASHBOARD
# -----------------------------------------------------------------------------
with tab_teacher:
    st.header("Step 1: Ingest Syllabus or Chapter Content")
    col_input_type, col_params = st.columns([2, 1])

    with col_input_type:
        input_mode = st.radio(
            "Select Input Source Mode:",
            ["📝 Paste Syllabus Text", "📄 Upload Chapter PDF"],
            horizontal=True
        )

        source_text = ""
        if input_mode == "📝 Paste Syllabus Text":
            source_text = st.text_area(
                "Paste Syllabus / Chapter Notes / Reading Material:",
                height=260,
                placeholder="Paste chapter notes, lecture summaries, key concepts, or curriculum objectives here..."
            )
        else:
            uploaded_pdf = st.file_uploader("Upload Chapter PDF:", type=["pdf"])
            if uploaded_pdf is not None:
                with st.spinner("Parsing and extracting text from PDF pages..."):
                    try:
                        source_text = st.session_state.quiz_service.extract_text_from_pdf(uploaded_pdf.read())
                        st.success(f"Extracted {len(source_text)} characters from '{uploaded_pdf.name}'.")
                        with st.expander("Preview Extracted Text"):
                            st.write(source_text[:1200] + ("..." if len(source_text) > 1200 else ""))
                    except Exception as err:
                        st.error(f"Error reading PDF: {err}")

    with col_params:
        st.subheader("Quiz Parameters")
        topic_name = st.text_input("Subject / Topic Name:", placeholder="e.g. Operating Systems: Virtual Memory")
        difficulty = st.selectbox("Difficulty Level:", ["Beginner", "Intermediate", "Advanced"], index=1)
        
        c_mcq, c_short = st.columns(2)
        with c_mcq:
            mcq_count = st.number_input("MCQs Count:", min_value=1, max_value=15, value=6)
        with c_short:
            short_count = st.number_input("Short Answers:", min_value=1, max_value=10, value=4)

        total_q = mcq_count + short_count
        st.info(f"Total Questions to Generate: **{total_q} questions**")

        api_key_input = st.text_input(
            "Optional Gemini / OpenAI API Key:",
            type="password",
            help="If omitted, uses local smart NLP heuristic engine."
        )

    st.markdown("---")
    if st.button("🚀 Synthesize Balanced Assessment with AI", type="primary", use_container_width=True):
        if not source_text or len(source_text.strip()) < 30:
            st.warning("Please provide syllabus text or upload a PDF first!")
        else:
            with st.spinner("AI analyzing syllabus concepts, drafting distractors, and formulating rubrics..."):
                try:
                    generated_quiz = st.session_state.quiz_service.generate_quiz(
                        source_text=source_text,
                        topic=topic_name or "Curriculum Assessment",
                        num_questions=total_q,
                        mcq_count=mcq_count,
                        short_answer_count=short_count,
                        difficulty=difficulty,
                        api_key=api_key_input or None
                    )
                    st.session_state.current_quiz = generated_quiz
                    st.session_state.graded_report = None
                    st.success(f"🎉 Successfully generated {len(generated_quiz['questions'])} questions for '{generated_quiz['topic']}'!")
                except Exception as ex:
                    st.error(f"Generation error: {ex}")

    # Display & Edit Generated Quiz
    if st.session_state.current_quiz:
        quiz = st.session_state.current_quiz
        st.markdown("### 📋 Review & Refine Generated Questions")
        st.markdown(f"**Quiz Title:** `{quiz['title']}` | **Total Marks:** `{quiz['total_marks']}` | **Difficulty:** `{quiz['difficulty']}`")

        edited_questions = []
        for idx, q in enumerate(quiz["questions"]):
            with st.expander(f"Question #{idx + 1} ({q['type'].upper()} - {q.get('marks', 2)} Marks): {q['question'][:75]}...", expanded=(idx < 2)):
                eq_title = st.text_input(f"Question Statement #{idx + 1}:", value=q["question"], key=f"edit_q_{idx}")
                eq_marks = st.number_input(f"Marks #{idx + 1}:", min_value=1, max_value=10, value=int(q.get("marks", 2)), key=f"edit_m_{idx}")
                
                if q["type"] == "mcq":
                    opts = q.get("options", [])
                    st.write("Multiple Choice Options:")
                    new_opts = []
                    for o_idx, opt in enumerate(opts):
                        new_opts.append(st.text_input(f"Option {chr(65 + o_idx)}:", value=opt, key=f"edit_opt_{idx}_{o_idx}"))
                    eq_ans = st.selectbox(
                        "Correct Option:",
                        ["A", "B", "C", "D"],
                        index=ord(q.get("correct_option", "A")[0]) - 65 if q.get("correct_option") in "ABCD" else 0,
                        key=f"edit_ans_{idx}"
                    )
                    eq_exp = st.text_area("Explanation:", value=q.get("explanation", ""), key=f"edit_exp_{idx}")
                    edited_questions.append({
                        **q,
                        "question": eq_title,
                        "marks": eq_marks,
                        "options": new_opts,
                        "correct_option": eq_ans,
                        "explanation": eq_exp
                    })
                else:
                    eq_sample = st.text_area("Expected Sample Answer:", value=q.get("sample_answer", ""), key=f"edit_sample_{idx}")
                    eq_rubric = st.text_area("Grading Rubric:", value=q.get("grading_rubric", ""), key=f"edit_rubric_{idx}")
                    edited_questions.append({
                        **q,
                        "question": eq_title,
                        "marks": eq_marks,
                        "sample_answer": eq_sample,
                        "grading_rubric": eq_rubric
                    })

        col_save, col_push = st.columns([1, 1])
        with col_save:
            if st.button("💾 Save Questions to Assessment Catalog", use_container_width=True):
                quiz["questions"] = edited_questions
                quiz["total_marks"] = sum(q.get("marks", 2) for q in edited_questions)
                st.session_state.quiz_service.in_memory_quizzes[quiz["id"]] = quiz
                st.success("Quiz updated and ready for students!")
        with col_push:
            if st.button("👉 Proceed to Student Quiz Taking View", use_container_width=True):
                st.info("Switch to the 'Student Quiz Taking' tab above to test answering!")


# -----------------------------------------------------------------------------
# TAB 2: STUDENT QUIZ TAKING & AUTO-GRADING
# -----------------------------------------------------------------------------
with tab_student:
    st.header("Student Examination Interface")

    active_quiz = st.session_state.current_quiz
    if not active_quiz:
        # Check if any saved quizzes exist in catalog
        catalog = st.session_state.quiz_service.in_memory_quizzes
        if catalog:
            chosen_id = st.selectbox(
                "Select an active quiz to take:",
                options=list(catalog.keys()),
                format_func=lambda x: f"{catalog[x]['title']} ({catalog[x]['topic']})"
            )
            active_quiz = catalog[chosen_id]
        else:
            st.info("No active quiz loaded. Please generate a quiz in the 'Teacher Dashboard' tab first!")

    if active_quiz:
        st.subheader(active_quiz["title"])
        st.caption(f"Topic: **{active_quiz['topic']}** | Difficulty: **{active_quiz['difficulty']}** | Total Marks: **{active_quiz['total_marks']}**")
        st.markdown("---")

        student_answers = {}
        with st.form("student_quiz_form"):
            for idx, q in enumerate(active_quiz["questions"]):
                st.markdown(f"#### Q{idx + 1}. {q['question']}")
                st.caption(f"Type: {q['type'].upper()} • Weightage: {q.get('marks', 2)} Marks")

                if q["type"] == "mcq":
                    options = q.get("options", [])
                    choice = st.radio(
                        f"Select your answer for Q{idx + 1}:",
                        options=options,
                        index=None,
                        key=f"student_ans_{q['id']}"
                    )
                    # Extract option letter e.g. "A" from "A) Option text"
                    if choice:
                        student_answers[q["id"]] = choice[0] if len(choice) > 0 else ""
                else:
                    ans_text = st.text_area(
                        f"Enter your descriptive explanation for Q{idx + 1}:",
                        placeholder="Type your response here in 2 to 4 sentences...",
                        key=f"student_ans_{q['id']}"
                    )
                    student_answers[q["id"]] = ans_text

                st.markdown("<br>", unsafe_allow_html=True)

            submitted = st.form_submit_button("🏁 Submit Answers for Instant AI Auto-Grading", use_container_width=True, type="primary")

        if submitted:
            with st.spinner("AI evaluating MCQ accuracy, analyzing descriptive semantic overlap, and computing marks..."):
                report = st.session_state.quiz_service.grade_answers(
                    quiz=active_quiz,
                    student_answers=student_answers
                )
                st.session_state.graded_report = report
                st.balloons()

    # Display Grading Report
    if st.session_state.graded_report:
        rep = st.session_state.graded_report
        st.markdown("---")
        st.header("📊 AI Auto-Grading & Performance Scorecard")

        col_metric1, col_metric2, col_metric3 = st.columns(3)
        with col_metric1:
            st.metric("Total Score Earned", f"{rep['total_score']} / {rep['max_score']}")
        with col_metric2:
            st.metric("Percentage", f"{rep['percentage']}%")
        with col_metric3:
            st.metric("Letter Grade", rep["letter_grade"])

        # Personalized Feedback Alert Box
        st.info(f"💡 **AI Evaluator Summary:** {rep['personalized_feedback_summary']}")

        col_strengths, col_improvements = st.columns(2)
        with col_strengths:
            st.success("##### 🌟 Demonstrated Strengths")
            for s in rep.get("strengths", []):
                st.markdown(f"- {s}")
        with col_improvements:
            st.warning("##### 🎯 Priority Areas for Revision")
            for imp in rep.get("areas_for_improvement", []):
                st.markdown(f"- {imp}")

        # Item-by-Item Detailed Breakdown
        st.markdown("### 📝 Detailed Question-by-Question Breakdown")
        for q_res in rep["question_breakdown"]:
            status_color = "🟢" if q_res["status"] in ("CORRECT", "STRONG", "EXCELLENT") else ("🟡" if q_res["status"] == "PARTIAL" else "🔴")
            with st.expander(f"{status_color} {q_res['question_id'].upper()}: {q_res['question'][:65]}... ({q_res['marks_earned']} / {q_res['marks_possible']} Marks)"):
                st.markdown(f"**Question:** {q_res['question']}")
                st.markdown(f"**Your Answer:** `{q_res['student_answer']}`")

                if q_res["type"] == "mcq":
                    st.markdown(f"**Correct Option:** `{q_res['correct_answer']}`")
                    st.markdown(f"**Explanation:** {q_res['explanation']}")
                else:
                    st.markdown(f"**Ideal Sample Answer:** {q_res['sample_answer']}")
                    st.markdown(f"**Rubric:** {q_res['grading_rubric']}")

                st.markdown(f"**AI Examiner Feedback:** *{q_res['feedback']}*")


# -----------------------------------------------------------------------------
# TAB 3: INTEGRATION & API DOCUMENTATION
# -----------------------------------------------------------------------------
with tab_info:
    st.header("Factskoot Hackathon Problem Statement 1 Integration Guide")
    st.markdown("""
This autonomous quiz generation and auto-grading module is **completely decoupled** from the existing camera proctoring module.

### Architecture Overview:
1. **`quiz_service.py`**: Standalone class encapsulating PDF extraction, LLM synthesis (Gemini/OpenAI), local NLP heuristic generation, and auto-grading.
2. **`router.py`**: FastAPI router providing `/api/quiz-generator/generate-quiz` and `/api/quiz-generator/grade-answers`.
3. **`ui_app.py`**: This interactive Streamlit application for educators and students.
4. **`server.py`**: Dedicated FastAPI runner on port `8010`.

### Mounting Router in Main App (Optional 2-Line Integration):
To expose the quiz generator endpoints directly on the existing backend (`port 8000`) without modifying proctoring logic:

```python
# In backend/main.py:
from modules.quiz_generator.router import quiz_router
app.include_router(quiz_router)
```

### Running Standalone Services:
- **FastAPI Standalone Server:**
  ```bash
  python modules/quiz_generator/server.py
  ```
- **Streamlit App:**
  ```bash
  streamlit run modules/quiz_generator/ui_app.py --server.port 8501
  ```
    """)

