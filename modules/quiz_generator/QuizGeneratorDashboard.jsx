import React, { useState } from 'react';
import {
  Sparkles,
  FileText,
  UploadCloud,
  Zap,
  Sliders,
  CheckCircle2,
  AlertCircle,
  Award,
  Send,
  ArrowRight,
  GraduationCap,
  PenTool,
  Clock,
  BookOpen,
  RefreshCw
} from 'lucide-react';
import axios from 'axios';

// Defaults to standalone quiz generator microservice (port 8010) or main backend (port 8000)
const API_BASE_URL = 'http://localhost:8010';

export default function QuizGeneratorDashboard() {
  const [activeTab, setActiveTab] = useState('teacher'); // 'teacher' | 'student'

  // Teacher State
  const [sourceText, setSourceText] = useState('');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [topic, setTopic] = useState('');
  const [difficulty, setDifficulty] = useState('Intermediate');
  const [mcqCount, setMcqCount] = useState(6);
  const [shortCount, setShortCount] = useState(4);
  const [apiKey, setApiKey] = useState('');
  const [generating, setGenerating] = useState(false);

  // Active Quiz State
  const [currentQuiz, setCurrentQuiz] = useState(null);

  // Student State
  const [studentAnswers, setStudentAnswers] = useState({});
  const [gradingReport, setGradingReport] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  // Handle PDF / Text file upload
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setUploadedFile(file);
      if (!topic) {
        setTopic(file.name.replace(/\.[^/.]+$/, '').replace(/[-_]/g, ' '));
      }
    }
  };

  // 1. Synthesize Assessment with AI
  const handleGenerateQuiz = async () => {
    if (!sourceText && !uploadedFile) {
      alert('Please paste syllabus text or upload a chapter PDF document!');
      return;
    }

    try {
      setGenerating(true);
      let res;
      if (uploadedFile) {
        const formData = new FormData();
        formData.append('file', uploadedFile);
        if (topic) formData.append('topic', topic);
        formData.append('difficulty', difficulty);
        formData.append('mcq_count', mcqCount);
        formData.append('short_answer_count', shortCount);
        formData.append('num_questions', Number(mcqCount) + Number(shortCount));
        if (apiKey) formData.append('api_key', apiKey);

        res = await axios.post(`${API_BASE_URL}/api/quiz-generator/generate-quiz`, formData);
      } else {
        res = await axios.post(`${API_BASE_URL}/api/quiz-generator/generate-quiz`, {
          text: sourceText,
          topic: topic,
          difficulty: difficulty,
          mcq_count: Number(mcqCount),
          short_answer_count: Number(shortCount),
          num_questions: Number(mcqCount) + Number(shortCount),
          api_key: apiKey || null
        });
      }

      if (res.data.status === 'SUCCESS') {
        setCurrentQuiz(res.data.quiz);
        setGradingReport(null);
        setStudentAnswers({});
      }
    } catch (err) {
      alert('Generation error: ' + (err.response?.data?.detail || err.message));
    } finally {
      setGenerating(false);
    }
  };

  // 2. Submit Answers for Auto-Grading
  const handleSubmitQuiz = async () => {
    if (!currentQuiz) return;
    try {
      setSubmitting(true);
      const res = await axios.post(`${API_BASE_URL}/api/quiz-generator/grade-answers`, {
        quiz: currentQuiz,
        student_answers: studentAnswers,
        api_key: apiKey || null
      });

      if (res.data.status === 'GRADED') {
        setGradingReport(res.data.report);
      }
    } catch (err) {
      alert('Grading error: ' + (err.response?.data?.detail || err.message));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto p-4 sm:p-6 font-sans text-slate-100">
      
      {/* Module Title Header */}
      <div className="p-6 rounded-3xl bg-slate-900/80 border border-white/10 flex flex-wrap items-center justify-between gap-4 backdrop-blur-2xl">
        <div className="flex items-center gap-3.5">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-cyan-500 to-purple-600 flex items-center justify-center font-bold text-white shadow-lg shadow-cyan-500/20">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-black text-white tracking-tight">Factskoot AI Quiz & Assessment Generator</h2>
              <span className="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 font-bold">
                Problem Statement 1
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Decoupled Pedagogical Assessment Module • Syllabus & PDF Ingestion + Automated Grading
            </p>
          </div>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center gap-1.5 p-1 rounded-2xl bg-black/40 border border-white/10 text-xs font-mono font-bold">
          <button
            onClick={() => setActiveTab('teacher')}
            className={`px-4 py-2 rounded-xl transition flex items-center gap-2 ${
              activeTab === 'teacher'
                ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <GraduationCap className="w-4 h-4" /> Teacher Dashboard
          </button>
          <button
            onClick={() => {
              if (!currentQuiz) {
                alert('Please generate or load a quiz in the Teacher Dashboard first!');
                return;
              }
              setActiveTab('student');
            }}
            className={`px-4 py-2 rounded-xl transition flex items-center gap-2 ${
              activeTab === 'student'
                ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <PenTool className="w-4 h-4" /> Student Quiz Taking
          </button>
        </div>
      </div>

      {/* ------------------------------------------------------------- */}
      {/* VIEW 1: TEACHER DASHBOARD */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'teacher' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Left: Content Ingestion */}
            <div className="lg:col-span-2 p-6 rounded-3xl bg-slate-900/60 border border-white/10 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-white/10">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <FileText className="w-4 h-4 text-cyan-400" />
                  Syllabus or Chapter Content Ingestion
                </h3>
                <span className="text-[11px] font-mono text-slate-400">PDF / Text</span>
              </div>

              {/* PDF Dropzone */}
              <div className="relative border-2 border-dashed border-white/20 hover:border-cyan-500/50 rounded-2xl p-6 text-center transition cursor-pointer bg-black/20">
                <input
                  type="file"
                  accept=".pdf,.txt"
                  onChange={handleFileChange}
                  className="absolute inset-0 opacity-0 cursor-pointer"
                />
                <UploadCloud className="w-10 h-10 text-cyan-400 mx-auto mb-2" />
                <p className="text-xs font-bold text-white">
                  {uploadedFile ? `Selected: ${uploadedFile.name}` : 'Upload Chapter PDF or Syllabus Document'}
                </p>
                <p className="text-[10px] text-slate-400 mt-1">Drag and drop .pdf or .txt (auto-extracts pages)</p>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-300 mb-1.5">
                  Or Paste Syllabus / Chapter Reading Text:
                </label>
                <textarea
                  rows={7}
                  value={sourceText}
                  onChange={(e) => setSourceText(e.target.value)}
                  placeholder="Paste lecture notes, chapter summaries, key technical principles, or syllabus specifications here..."
                  className="w-full rounded-2xl p-3.5 text-xs font-mono bg-black/40 border border-white/10 text-white focus:outline-none focus:border-cyan-400 transition"
                />
              </div>
            </div>

            {/* Right: Synthesis Parameters */}
            <div className="p-6 rounded-3xl bg-slate-900/60 border border-white/10 space-y-4 flex flex-col justify-between">
              <div className="space-y-3.5">
                <h3 className="text-sm font-bold text-white flex items-center gap-2 pb-2 border-b border-white/10">
                  <Sliders className="w-4 h-4 text-purple-400" />
                  Generation Parameters
                </h3>

                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Subject / Topic Name:</label>
                  <input
                    type="text"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="e.g. Distributed Computing"
                    className="w-full rounded-xl px-3 py-2 text-xs bg-black/40 border border-white/10 text-white focus:outline-none focus:border-cyan-400 font-mono"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Difficulty Level:</label>
                  <select
                    value={difficulty}
                    onChange={(e) => setDifficulty(e.target.value)}
                    className="w-full rounded-xl px-3 py-2 text-xs bg-slate-950 border border-white/10 text-white focus:outline-none focus:border-cyan-400"
                  >
                    <option value="Beginner">Beginner (Foundational definitions)</option>
                    <option value="Intermediate">Intermediate (Core concepts & analysis)</option>
                    <option value="Advanced">Advanced (Critical architecture & scenarios)</option>
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">MCQs (2 marks):</label>
                    <input
                      type="number"
                      min={1}
                      max={15}
                      value={mcqCount}
                      onChange={(e) => setMcqCount(e.target.value)}
                      className="w-full rounded-xl px-3 py-2 text-xs bg-black/40 border border-white/10 text-white font-mono"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Short Answers (3 marks):</label>
                    <input
                      type="number"
                      min={1}
                      max={10}
                      value={shortCount}
                      onChange={(e) => setShortCount(e.target.value)}
                      className="w-full rounded-xl px-3 py-2 text-xs bg-black/40 border border-white/10 text-white font-mono"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1 flex items-center justify-between">
                    <span>Optional LLM Key:</span>
                    <span className="text-[10px] text-cyan-400 font-mono">Gemini / OpenAI</span>
                  </label>
                  <input
                    type="password"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder="AIzaSy... (Leave empty for Smart NLP)"
                    className="w-full rounded-xl px-3 py-2 text-xs bg-black/40 border border-white/10 text-white font-mono"
                  />
                </div>
              </div>

              <button
                onClick={handleGenerateQuiz}
                disabled={generating}
                className="w-full py-3.5 rounded-2xl bg-gradient-to-r from-cyan-500 via-blue-600 to-purple-600 hover:opacity-90 active:scale-95 text-white font-black text-xs font-mono uppercase tracking-wider shadow-lg shadow-cyan-500/20 transition flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
              >
                {generating ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Synthesizing Questions with AI...</span>
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4" />
                    <span>Generate 10-Question Balanced Quiz</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Generated Questions List Preview */}
          {currentQuiz && (
            <div className="p-6 rounded-3xl bg-slate-900/60 border border-white/10 space-y-5">
              <div className="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-white/10">
                <div>
                  <h3 className="text-lg font-black text-white">{currentQuiz.title}</h3>
                  <p className="text-xs text-slate-400 font-mono">
                    Topic: {currentQuiz.topic} • Total Marks: {currentQuiz.total_marks} • Total Questions: {currentQuiz.questions?.length}
                  </p>
                </div>
                <button
                  onClick={() => setActiveTab('student')}
                  className="px-5 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black font-bold font-mono text-xs transition flex items-center gap-1.5"
                >
                  <span>Take Quiz as Student</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>

              <div className="space-y-3.5">
                {currentQuiz.questions?.map((q, idx) => (
                  <div key={q.id || idx} className="p-4 rounded-2xl bg-black/30 border border-white/10 space-y-2 text-xs">
                    <div className="flex items-center justify-between font-mono">
                      <span className="font-bold text-cyan-400">Q{idx + 1} • {q.type.toUpperCase()}</span>
                      <span className="px-2 py-0.5 rounded bg-white/10 text-slate-300 font-bold">{q.marks} Marks</span>
                    </div>
                    <p className="text-sm font-semibold text-white">{q.question}</p>
                    {q.type === 'mcq' ? (
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 font-mono mt-1">
                        {q.options?.map((opt, oIdx) => (
                          <div
                            key={oIdx}
                            className={`p-2 rounded-xl ${
                              opt.startsWith(q.correct_option)
                                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                                : 'bg-slate-800/40 text-slate-300'
                            }`}
                          >
                            {opt}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="p-3 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-200 font-mono">
                        <span className="font-bold block mb-1">Expected Sample Answer:</span>
                        {q.sample_answer}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ------------------------------------------------------------- */}
      {/* VIEW 2: STUDENT QUIZ TAKING & AUTO-GRADING */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'student' && currentQuiz && (
        <div className="space-y-6">
          <div className="p-6 rounded-3xl bg-slate-900/80 border border-white/10 flex flex-wrap items-center justify-between gap-4">
            <div>
              <span className="text-[10px] font-mono px-2.5 py-1 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-bold uppercase">
                {currentQuiz.topic}
              </span>
              <h2 className="text-xl font-black text-white mt-1.5">{currentQuiz.title}</h2>
              <p className="text-xs text-slate-400 font-mono">Total Questions: {currentQuiz.questions?.length} | Total Marks: {currentQuiz.total_marks}</p>
            </div>
            <div className="flex items-center gap-2 text-xs font-mono">
              <span className="px-3 py-1.5 rounded-xl bg-white/10 text-slate-200">
                Difficulty: {currentQuiz.difficulty}
              </span>
            </div>
          </div>

          {/* Questions Answering Form */}
          <div className="space-y-4">
            {currentQuiz.questions?.map((q, idx) => (
              <div key={q.id || idx} className="p-6 rounded-3xl bg-slate-900/60 border border-white/10 space-y-3">
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="font-bold text-cyan-400">QUESTION #{idx + 1} OF {currentQuiz.questions.length}</span>
                  <span className="text-slate-400">{q.type.toUpperCase()} • {q.marks} Marks</span>
                </div>
                <h4 className="text-sm font-bold text-white">{q.question}</h4>

                {q.type === 'mcq' ? (
                  <div className="space-y-2 mt-2 font-mono text-xs">
                    {q.options?.map((opt, oIdx) => {
                      const letter = opt.charAt(0);
                      const isSelected = studentAnswers[q.id] === letter;
                      return (
                        <label
                          key={oIdx}
                          className={`flex items-center gap-3 p-3 rounded-2xl border cursor-pointer transition ${
                            isSelected
                              ? 'bg-cyan-500/20 border-cyan-500 text-cyan-200'
                              : 'bg-black/30 border-white/10 hover:border-white/30 text-slate-300'
                          }`}
                        >
                          <input
                            type="radio"
                            name={`ans_${q.id}`}
                            value={letter}
                            checked={isSelected}
                            onChange={() => setStudentAnswers((prev) => ({ ...prev, [q.id]: letter }))}
                            className="text-cyan-500 focus:ring-cyan-500"
                          />
                          <span>{opt}</span>
                        </label>
                      );
                    })}
                  </div>
                ) : (
                  <div className="mt-2">
                    <textarea
                      rows={3}
                      value={studentAnswers[q.id] || ''}
                      onChange={(e) => setStudentAnswers((prev) => ({ ...prev, [q.id]: e.target.value }))}
                      placeholder="Type your descriptive analytical response here in 2 to 4 sentences..."
                      className="w-full rounded-2xl p-3.5 text-xs font-mono bg-black/40 border border-white/10 text-white focus:outline-none focus:border-cyan-400 transition"
                    />
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Submit Action */}
          <div className="p-6 rounded-3xl bg-slate-900/80 border border-white/10 flex items-center justify-between">
            <span className="text-xs text-slate-400 font-mono">
              Ready to submit? Automated AI grading will compare your answers with source concepts.
            </span>
            <button
              onClick={handleSubmitQuiz}
              disabled={submitting}
              className="px-6 py-3.5 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:opacity-90 active:scale-95 text-white font-black text-xs font-mono uppercase tracking-wider shadow-lg shadow-emerald-500/25 transition flex items-center gap-2 cursor-pointer disabled:opacity-50"
            >
              {submitting ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Evaluating with AI...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Submit for AI Auto-Grading</span>
                </>
              )}
            </button>
          </div>

          {/* Grading Report */}
          {gradingReport && (
            <div className="p-6 sm:p-8 rounded-3xl bg-slate-900/90 border border-emerald-500/40 space-y-6">
              <div className="flex items-center justify-between pb-4 border-b border-white/10">
                <div>
                  <h3 className="text-lg font-black text-white flex items-center gap-2">
                    <Award className="w-5 h-5 text-yellow-400" />
                    AI Auto-Grading Scorecard
                  </h3>
                  <p className="text-xs text-slate-400 font-mono">Assessment evaluation completed.</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-black text-emerald-400 font-mono">
                    {gradingReport.total_score} / {gradingReport.max_score}
                  </div>
                  <span className="text-xs font-bold text-slate-300 font-mono">
                    {gradingReport.percentage}% • {gradingReport.letter_grade}
                  </span>
                </div>
              </div>

              {/* Feedback Summary */}
              <div className="p-4 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-200 text-xs font-mono leading-relaxed">
                {gradingReport.personalized_feedback_summary}
              </div>

              {/* Strengths & Improvements */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-xs">
                  <h4 className="font-bold text-emerald-400 mb-2 flex items-center gap-1.5 font-mono">
                    <CheckCircle2 className="w-4 h-4" /> Demonstrated Strengths
                  </h4>
                  <ul className="space-y-1 text-slate-200 font-medium">
                    {gradingReport.strengths?.map((s, i) => (
                      <li key={i}>• {s}</li>
                    ))}
                  </ul>
                </div>

                <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-xs">
                  <h4 className="font-bold text-amber-400 mb-2 flex items-center gap-1.5 font-mono">
                    <AlertCircle className="w-4 h-4" /> Areas for Improvement
                  </h4>
                  <ul className="space-y-1 text-slate-200 font-medium">
                    {gradingReport.areas_for_improvement?.map((imp, i) => (
                      <li key={i}>• {imp}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Itemized Questions Breakdown */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-slate-300 uppercase font-mono">Itemized Breakdown:</h4>
                {gradingReport.question_breakdown?.map((item, idx) => {
                  const isSuccess = ['CORRECT', 'STRONG', 'EXCELLENT'].includes(item.status);
                  return (
                    <div key={idx} className="p-4 rounded-2xl bg-black/40 border border-white/10 space-y-1.5 text-xs font-mono">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-white">Q{idx + 1} ({item.type.toUpperCase()}): {item.question}</span>
                        <span className={`font-bold px-2 py-0.5 rounded border ${isSuccess ? 'text-emerald-400 border-emerald-500/30' : 'text-rose-400 border-rose-500/30'}`}>
                          {item.marks_earned} / {item.marks_possible} Marks
                        </span>
                      </div>
                      <div className="text-slate-400">
                        <b>Your Answer:</b> <span className="text-slate-200">{item.student_answer}</span>
                      </div>
                      {item.type === 'mcq' ? (
                        <div className="text-[11px] text-slate-400">
                          Correct: <b className="text-emerald-400">{item.correct_answer}</b> • {item.explanation}
                        </div>
                      ) : (
                        <div className="text-[11px] text-slate-400">
                          Sample Answer: <span className="text-slate-300">{item.sample_answer}</span>
                        </div>
                      )}
                      <div className="text-[11px] text-cyan-400">
                        Feedback: {item.feedback}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
