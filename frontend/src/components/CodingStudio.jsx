import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Code2,
  Play,
  CheckCircle2,
  AlertCircle,
  CopyX,
  FileCode,
  Terminal,
  RotateCcw,
  Sparkles,
  Layers,
  Cpu,
  Flame,
  Zap,
  ChevronRight,
  HelpCircle,
  AlertTriangle,
  Bug,
  Check,
  Info
} from 'lucide-react';
import axios from 'axios';

import { API_BASE_URL } from '../config';

// Initial boilerplate templates ONLY - No solutions provided
const DEFAULT_TEMPLATES = {
  python: `# Python 3.12 / 3.13 Standard Environment
def solution():
    # Write your algorithmic solution here
    pass

# Test call with sample inputs:
print(solution())
`,
  javascript: `// JavaScript (Node.js LTS)
function solution() {
    // Write your algorithmic solution here
    
}

// Test call with sample inputs:
console.log(solution());
`,
  typescript: `// TypeScript 5.3
function solution(): any {
    // Write your algorithmic solution here
    
}

console.log(solution());
`,
  java: `// OpenJDK 21
public class Solution {
    public static void main(String[] args) {
        // Write your solution here
        
    }
}
`,
  cpp: `// C++20 (GCC)
#include <iostream>
using namespace std;

int main() {
    // Write your solution here
    
    return 0;
}
`,
  c: `// C17 (GCC)
#include <stdio.h>

int main() {
    // Write your solution here
    
    return 0;
}
`,
  go: `// Go 1.22
package main
import "fmt"

func main() {
    // Write your solution here
    
}
`,
  rust: `// Rust 1.76
fn main() {
    // Write your solution here
    
}
`
};

export default function CodingStudio({
  questions = [],
  question = null,
  onCodeChange,
  onProceedToInterview,
  onSubmitExam
}) {
  const problemsList = questions && questions.length > 0 ? questions : (question ? [question] : []);
  const [activeIdx, setActiveIdx] = useState(0);
  const activeProblem = problemsList[activeIdx] || problemsList[0] || {
    title: "Algorithmic Challenge",
    description: "Write code to solve the challenge according to specifications.",
    starter_templates: {}
  };

  const [language, setLanguage] = useState('python');
  const [codes, setCodes] = useState({});
  const [isRunning, setIsRunning] = useState(false);
  const [consoleOutput, setConsoleOutput] = useState('');
  const [testResult, setTestResult] = useState(null);
  const [copyToast, setCopyToast] = useState(false);

  // Line Analysis & Diagnostics State
  const [activeLine, setActiveLine] = useState(1);
  const [errorLines, setErrorLines] = useState(new Set());
  const [warningLines, setWarningLines] = useState(new Set());
  const [diagnosticsMsg, setDiagnosticsMsg] = useState({ error: '', warning: '' });

  const textareaRef = useRef(null);
  const lineNumbersRef = useRef(null);

  // Initialize starter template for current problem & language
  useEffect(() => {
    const key = `${activeIdx}-${language}`;
    if (!codes[key]) {
      const template = activeProblem.starter_templates?.[language] || DEFAULT_TEMPLATES[language] || '';
      setCodes(prev => ({ ...prev, [key]: template }));
    }
  }, [activeIdx, language, activeProblem]);

  const currentCode = codes[`${activeIdx}-${language}`] || (activeProblem.starter_templates?.[language] || DEFAULT_TEMPLATES[language] || '');
  const lines = currentCode.split('\n');

  // Live syntax & warning analyzer
  const runLiveAnalysis = useCallback((code, lang) => {
    const newErrors = new Set();
    const newWarnings = new Set();
    let errText = '';
    let warnText = '';

    const codeLines = code.split('\n');

    codeLines.forEach((line, idx) => {
      const lineNum = idx + 1;
      const trimmed = line.trim();

      if (lang === 'python') {
        // Unclosed statement check (def/class/if/for/while without colon)
        if (
          (trimmed.startsWith('def ') ||
            trimmed.startsWith('class ') ||
            trimmed.startsWith('if ') ||
            trimmed.startsWith('elif ') ||
            trimmed === 'else' ||
            trimmed.startsWith('for ') ||
            trimmed.startsWith('while ') ||
            trimmed === 'try' ||
            trimmed.startsWith('except')) &&
          !trimmed.endsWith(':') &&
          !trimmed.includes('#')
        ) {
          newErrors.add(lineNum);
          if (!errText) errText = `Line ${lineNum}: SyntaxError: Expected ':' at end of header`;
        }

        // Unresolved stub warning
        if (trimmed === 'pass' && codeLines.length > 4) {
          newWarnings.add(lineNum);
          if (!warnText) warnText = `Line ${lineNum}: Warning: Algorithmic stub incomplete ('pass' statement)`;
        }

        if (trimmed.startsWith('# TODO')) {
          newWarnings.add(lineNum);
          if (!warnText) warnText = `Line ${lineNum}: Note: Unresolved TODO item`;
        }
      } else if (lang === 'javascript' || lang === 'typescript') {
        // Missing closing parenthesis in basic call
        const opens = (line.match(/\(/g) || []).length;
        const closes = (line.match(/\)/g) || []).length;
        if (opens !== closes && !trimmed.endsWith('{') && !trimmed.startsWith('//')) {
          newWarnings.add(lineNum);
          if (!warnText) warnText = `Line ${lineNum}: Unbalanced parentheses`;
        }

        if (trimmed.includes('// Write your') || trimmed.includes('// TODO')) {
          newWarnings.add(lineNum);
          if (!warnText) warnText = `Line ${lineNum}: Note: Incomplete implementation stub`;
        }
      }
    });

    setErrorLines(newErrors);
    setWarningLines(newWarnings);
    setDiagnosticsMsg({ error: errText, warning: warnText });
  }, []);

  // Run live analysis on code or language change
  useEffect(() => {
    runLiveAnalysis(currentCode, language);
  }, [currentCode, language, runLiveAnalysis]);

  const updateCode = (newCode) => {
    const key = `${activeIdx}-${language}`;
    setCodes(prev => ({ ...prev, [key]: newCode }));
    if (onCodeChange) onCodeChange(activeIdx, newCode, language);
    runLiveAnalysis(newCode, language);
  };

  const handleLanguageChange = (lang) => {
    setLanguage(lang);
    const key = `${activeIdx}-${lang}`;
    const newCode = codes[key] || activeProblem.starter_templates?.[lang] || DEFAULT_TEMPLATES[lang] || '';
    setCodes(prev => ({ ...prev, [key]: newCode }));
    if (onCodeChange) onCodeChange(activeIdx, newCode, lang);
    setConsoleOutput('');
    setTestResult(null);
    setErrorLines(new Set());
    setWarningLines(new Set());
    runLiveAnalysis(newCode, lang);
  };

  // Anti-Cheat Clipboard Shield (Block Copy / Paste / Cut)
  const blockClipboard = (e) => {
    if (e && e.preventDefault) e.preventDefault();
    setCopyToast(true);
    setTimeout(() => setCopyToast(false), 2500);
  };

  // Synchronize Line Number scroll with Textarea
  const handleScroll = () => {
    if (textareaRef.current && lineNumbersRef.current) {
      lineNumbersRef.current.scrollTop = textareaRef.current.scrollTop;
    }
  };

  // Update cursor position & active line
  const updateCursorPosition = () => {
    if (!textareaRef.current) return;
    const { selectionStart, value } = textareaRef.current;
    const currentLineNum = value.substring(0, selectionStart).split('\n').length;
    setActiveLine(currentLineNum);
  };

  // Perfect Tabspace & IDE Key Handling
  const handleKeyDown = (e) => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const { selectionStart, selectionEnd, value } = textarea;

    // 1. Anti-Cheat: Intercept Copy / Paste Shortcuts
    if ((e.ctrlKey || e.metaKey) && (e.key === 'v' || e.key === 'V')) {
      e.preventDefault();
      blockClipboard(e);
      return;
    }
    if ((e.ctrlKey || e.metaKey) && (e.key === 'c' || e.key === 'C')) {
      e.preventDefault();
      blockClipboard(e);
      return;
    }
    if ((e.ctrlKey || e.metaKey) && (e.key === 'x' || e.key === 'X')) {
      e.preventDefault();
      blockClipboard(e);
      return;
    }

    // 2. TAB & SHIFT+TAB: Maintain exact 4-space tabspace without focus shift!
    if (e.key === 'Tab') {
      e.preventDefault();
      const tabSpace = '    '; // 4 spaces

      if (selectionStart === selectionEnd) {
        if (!e.shiftKey) {
          // Insert 4 spaces at cursor
          const nextValue = value.substring(0, selectionStart) + tabSpace + value.substring(selectionEnd);
          updateCode(nextValue);
          setTimeout(() => {
            textarea.selectionStart = textarea.selectionEnd = selectionStart + 4;
            updateCursorPosition();
          }, 0);
        } else {
          // Shift+Tab: Dedent current line up to 4 spaces
          const lineStart = value.lastIndexOf('\n', selectionStart - 1) + 1;
          const lineText = value.substring(lineStart, selectionStart);
          const leadingSpaces = lineText.match(/^ {1,4}/);
          if (leadingSpaces) {
            const count = leadingSpaces[0].length;
            const nextValue = value.substring(0, lineStart) + value.substring(lineStart + count);
            updateCode(nextValue);
            setTimeout(() => {
              textarea.selectionStart = textarea.selectionEnd = Math.max(lineStart, selectionStart - count);
              updateCursorPosition();
            }, 0);
          }
        }
      } else {
        // Multi-line block indent / dedent
        const lineStart = value.lastIndexOf('\n', selectionStart - 1) + 1;
        const lineEnd = value.indexOf('\n', selectionEnd);
        const effectiveEnd = lineEnd === -1 ? value.length : lineEnd;
        const selectedBlock = value.substring(lineStart, effectiveEnd);
        const blockLines = selectedBlock.split('\n');

        if (!e.shiftKey) {
          // Indent all selected lines by 4 spaces
          const newBlock = blockLines.map(l => tabSpace + l).join('\n');
          const nextValue = value.substring(0, lineStart) + newBlock + value.substring(effectiveEnd);
          updateCode(nextValue);
          setTimeout(() => {
            textarea.selectionStart = selectionStart + 4;
            textarea.selectionEnd = selectionEnd + (blockLines.length * 4);
            updateCursorPosition();
          }, 0);
        } else {
          // Dedent all selected lines
          let totalRemoved = 0;
          let firstLineRemoved = 0;
          const newBlock = blockLines.map((l, idx) => {
            const match = l.match(/^ {1,4}/);
            if (match) {
              const count = match[0].length;
              totalRemoved += count;
              if (idx === 0) firstLineRemoved = count;
              return l.substring(count);
            }
            return l;
          }).join('\n');
          const nextValue = value.substring(0, lineStart) + newBlock + value.substring(effectiveEnd);
          updateCode(nextValue);
          setTimeout(() => {
            textarea.selectionStart = Math.max(lineStart, selectionStart - firstLineRemoved);
            textarea.selectionEnd = Math.max(lineStart, selectionEnd - totalRemoved);
            updateCursorPosition();
          }, 0);
        }
      }
      return;
    }

    // 3. ENTER KEY: Smart auto-indentation and colon/brace expansion
    if (e.key === 'Enter') {
      e.preventDefault();
      const lineStart = value.lastIndexOf('\n', selectionStart - 1) + 1;
      const currentLine = value.substring(lineStart, selectionStart);
      const leadingIndent = currentLine.match(/^\s*/)[0];
      const trimmed = currentLine.trim();

      let extraIndent = '';
      if (trimmed.endsWith(':') || trimmed.endsWith('{')) {
        extraIndent = '    ';
      }

      // Check if cursor is between matching braces '{|}'
      const charBefore = value[selectionStart - 1];
      const charAfter = value[selectionStart];
      if (charBefore === '{' && charAfter === '}') {
        const nextValue =
          value.substring(0, selectionStart) +
          '\n' +
          leadingIndent +
          '    \n' +
          leadingIndent +
          value.substring(selectionEnd);
        updateCode(nextValue);
        setTimeout(() => {
          textarea.selectionStart = textarea.selectionEnd = selectionStart + leadingIndent.length + 5;
          updateCursorPosition();
        }, 0);
        return;
      }

      const nextValue =
        value.substring(0, selectionStart) +
        '\n' +
        leadingIndent +
        extraIndent +
        value.substring(selectionEnd);
      updateCode(nextValue);
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd =
          selectionStart + 1 + leadingIndent.length + extraIndent.length;
        updateCursorPosition();
      }, 0);
      return;
    }

    // 4. SMART BACKSPACE: Dedent 4 spaces if preceded by 4 spaces
    if (e.key === 'Backspace' && selectionStart === selectionEnd) {
      if (selectionStart >= 4 && value.substring(selectionStart - 4, selectionStart) === '    ') {
        const lineStart = value.lastIndexOf('\n', selectionStart - 1) + 1;
        const beforeCursor = value.substring(lineStart, selectionStart);
        if (/^\s+$/.test(beforeCursor)) {
          e.preventDefault();
          const nextValue = value.substring(0, selectionStart - 4) + value.substring(selectionEnd);
          updateCode(nextValue);
          setTimeout(() => {
            textarea.selectionStart = textarea.selectionEnd = selectionStart - 4;
            updateCursorPosition();
          }, 0);
          return;
        }
      }
    }

    // 5. BRACKET & QUOTE AUTO-PAIRING
    const pairs = {
      '(': ')',
      '[': ']',
      '{': '}',
      '"': '"',
      "'": "'",
      '`': '`'
    };
    if (pairs[e.key] && selectionStart !== selectionEnd) {
      e.preventDefault();
      const closeChar = pairs[e.key];
      const selected = value.substring(selectionStart, selectionEnd);
      const nextValue =
        value.substring(0, selectionStart) + e.key + selected + closeChar + value.substring(selectionEnd);
      updateCode(nextValue);
      setTimeout(() => {
        textarea.selectionStart = selectionStart + 1;
        textarea.selectionEnd = selectionEnd + 1;
        updateCursorPosition();
      }, 0);
      return;
    }

    setTimeout(updateCursorPosition, 0);
  };

  // Compile and execute code against sandbox
  const runCode = async () => {
    setIsRunning(true);
    setConsoleOutput('Compiling source code in secure sandbox...\n');
    setErrorLines(new Set());
    setWarningLines(new Set());

    try {
      const res = await axios.post(`${API_BASE_URL}/api/execute-code`, {
        language: language,
        code: currentCode,
        input_data: ''
      });
      const data = res.data;

      // Extract error / warning lines from API response
      const apiErrLines = new Set(data.error_lines || []);
      const apiWarnLines = new Set(data.warning_lines || []);

      // Also parse lines from stderr/stdout
      const fullOutput = data.stdout || '';
      const lineMatches = fullOutput.match(/(?:line\s+|:)(\d+)(?::\d+)?/gi);
      if (lineMatches && data.status === 'ERROR') {
        lineMatches.forEach(m => {
          const num = parseInt(m.replace(/\D/g, ''), 10);
          if (num > 0 && num <= lines.length) {
            apiErrLines.add(num);
          }
        });
      }

      setErrorLines(apiErrLines);
      setWarningLines(apiWarnLines);

      let errBrief = '';
      if (apiErrLines.size > 0) {
        errBrief = `Compiler Error on line ${Array.from(apiErrLines).join(', ')}`;
      }
      setDiagnosticsMsg({
        error: errBrief,
        warning: apiWarnLines.size > 0 ? `Warning flagged on line ${Array.from(apiWarnLines).join(', ')}` : ''
      });

      setConsoleOutput(
        `[${data.runtime}] Status: ${data.status}\nExecution Time: ${data.execution_time} | Memory: ${data.memory_used || '14.2 MB'}\n\nSTDOUT:\n${data.stdout}`
      );
      setTestResult({
        passed: data.tests_passed,
        total: data.tests_total,
        status: data.status
      });
    } catch (err) {
      setConsoleOutput('Execution error: compiler service unreachable.');
      setErrorLines(new Set([1]));
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="flex flex-col h-full rounded-3xl liquid-glass border border-white/20 backdrop-blur-2xl shadow-glass-specular overflow-hidden">
      
      {/* Problem Tabs Navigation */}
      {problemsList.length > 1 && (
        <div className="px-5 py-2.5 border-b border-white/[0.1] bg-white/[0.02] flex items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <span className="text-[11px] font-mono text-slate-400 font-bold uppercase tracking-wider">
              Challenges:
            </span>
            {problemsList.map((prob, idx) => (
              <button
                key={prob.id || idx}
                onClick={() => {
                  setActiveIdx(idx);
                  setConsoleOutput('');
                  setTestResult(null);
                  setErrorLines(new Set());
                  setWarningLines(new Set());
                }}
                className={`px-4 py-1.5 rounded-xl font-mono text-xs font-bold transition flex items-center gap-2 ${
                  activeIdx === idx
                    ? 'bg-neon-cyan/25 border border-neon-cyan text-white shadow-neon-cyan'
                    : 'liquid-pill text-slate-300 hover:text-white border-white/10'
                }`}
              >
                <span>Problem {idx + 1}:</span>
                <span className="max-w-[180px] truncate">{prob.title}</span>
              </button>
            ))}
          </div>

          <div className="hidden sm:flex items-center gap-2 text-[11px] font-mono text-slate-400">
            <span>Tab: <b className="text-neon-cyan">4 Spaces</b></span>
            <span>•</span>
            <span className="flex items-center gap-1 text-rose-400">
              <span className="w-2 h-2 rounded-full bg-rose-500" /> Errors
            </span>
            <span>•</span>
            <span className="flex items-center gap-1 text-amber-400">
              <span className="w-2 h-2 rounded-full bg-amber-500" /> Warnings
            </span>
          </div>
        </div>
      )}

      {/* Problem Details Banner */}
      <div className="p-4 sm:p-5 border-b border-white/[0.1] bg-white/[0.03]">
        <div className="flex items-center justify-between gap-3 mb-2">
          <h3 className="text-sm sm:text-base font-bold text-white flex items-center gap-2">
            <span className="text-neon-cyan font-mono">Problem {activeIdx + 1}:</span>
            <span>{activeProblem.title}</span>
          </h3>
          <span className="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full liquid-pill text-neon-mint border border-neon-emerald/30 shadow-neon-emerald">
            Live Compilable Sandbox
          </span>
        </div>
        <p className="text-xs text-slate-300 leading-relaxed font-medium">
          {activeProblem.description}
        </p>

        {activeProblem.test_cases && activeProblem.test_cases.length > 0 && (
          <div className="mt-3 flex flex-wrap items-center gap-2 pt-2 border-t border-white/[0.08] text-[11px] font-mono">
            <span className="text-neon-gold font-bold">Sample Assertion:</span>
            <span className="bg-void/70 px-2.5 py-0.5 rounded text-slate-300 border border-white/10">
              Input: {activeProblem.test_cases[0].input}
            </span>
            <span className="bg-void/70 px-2.5 py-0.5 rounded text-neon-mint border border-white/10">
              Expected: {activeProblem.test_cases[0].expected}
            </span>
          </div>
        )}
      </div>

      {/* IDE Top Toolbar */}
      <div className="flex flex-wrap items-center justify-between px-5 py-2.5 border-b border-white/[0.1] bg-white/[0.02] text-xs">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 font-bold text-white">
            <span className="p-1.5 rounded-xl bg-neon-cyan/15 border border-neon-cyan/30 text-neon-cyan shadow-neon-cyan">
              <Code2 className="w-3.5 h-3.5" />
            </span>
            <span className="font-mono tracking-wider">Editor</span>
          </div>

          {/* Language Dropdown */}
          <select
            value={language}
            onChange={(e) => handleLanguageChange(e.target.value)}
            className="px-3.5 py-1.5 rounded-2xl liquid-pill bg-[#0a0f1d] border border-neon-cyan/40 text-neon-cyan font-mono text-xs font-bold focus:outline-none focus:border-neon-cyan transition cursor-pointer shadow-sm"
          >
            <option value="python" className="bg-[#0a0f1d] text-white">Python 3.12</option>
            <option value="javascript" className="bg-[#0a0f1d] text-white">JavaScript (Node.js)</option>
            <option value="typescript" className="bg-[#0a0f1d] text-white">TypeScript 5.3</option>
            <option value="java" className="bg-[#0a0f1d] text-white">Java 21 (OpenJDK)</option>
            <option value="cpp" className="bg-[#0a0f1d] text-white">C++20 (GCC)</option>
            <option value="c" className="bg-[#0a0f1d] text-white">C17 (GCC)</option>
            <option value="go" className="bg-[#0a0f1d] text-white">Go 1.22</option>
            <option value="rust" className="bg-[#0a0f1d] text-white">Rust 1.76</option>
          </select>
        </div>

        <div className="flex items-center gap-3">
          {/* Anti-Paste Shield Badge */}
          <span className="hidden sm:inline-flex items-center gap-1.5 text-[10px] uppercase font-mono font-black text-neon-gold bg-neon-amber/15 px-3 py-1 rounded-2xl border border-neon-amber/40 shadow-neon-amber">
            <CopyX className="w-3.5 h-3.5" /> Anti-Paste Locked
          </span>

          {/* Reset to Initial Stub */}
          <button
            onClick={() => {
              if (window.confirm('Reset code back to initial skeleton? Your current typing will be replaced.')) {
                const tmpl = activeProblem.starter_templates?.[language] || DEFAULT_TEMPLATES[language] || '';
                updateCode(tmpl);
                setConsoleOutput('');
                setTestResult(null);
              }
            }}
            className="p-2 rounded-xl liquid-pill text-slate-300 hover:text-white transition"
            title="Reset to Initial Skeleton"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>

          {/* Run Code Button */}
          <button
            onClick={runCode}
            disabled={isRunning}
            className="px-5 py-2 rounded-2xl bg-gradient-to-r from-neon-emerald via-neon-teal to-neon-mint hover:opacity-90 active:scale-95 text-void font-black text-xs transition flex items-center gap-2 shadow-neon-emerald uppercase tracking-wider font-mono disabled:opacity-50"
          >
            {isRunning ? <Cpu className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5 fill-current" />}
            <span>{isRunning ? 'Compiling...' : 'Run Code'}</span>
          </button>
        </div>
      </div>

      {/* Clipboard Warning Banner */}
      {copyToast && (
        <div className="bg-neon-rose/30 border-b border-neon-rose px-5 py-2 flex items-center gap-2.5 text-white text-xs font-bold animate-in slide-in-from-top duration-200 shadow-neon-rose backdrop-blur-md">
          <CopyX className="w-4 h-4 text-white" />
          <span>CLIPBOARD BLOCKED: Copying and Pasting code is strictly prohibited by ProctorLens Security.</span>
        </div>
      )}

      {/* Code Editor & Console Split Body */}
      <div className="flex-1 flex flex-col lg:flex-row min-h-[440px]">
        
        {/* Professional Code Editor Area */}
        <div className="flex-1 relative bg-slate-950 font-mono text-xs flex overflow-hidden">
          
          {/* Synchronized Line Numbers Gutter with Red Errors and Yellow Warnings */}
          <div
            ref={lineNumbersRef}
            className="w-14 select-none py-4 px-2 text-right border-r border-white/[0.08] bg-slate-950/80 text-[11px] font-mono font-bold overflow-hidden"
            style={{ lineHeight: '22px' }}
          >
            {lines.map((_, i) => {
              const lineNum = i + 1;
              const hasError = errorLines.has(lineNum);
              const hasWarning = warningLines.has(lineNum);
              const isActive = activeLine === lineNum;

              let textColor = 'text-slate-600';
              let badge = null;

              if (hasError) {
                textColor = 'text-rose-400 font-black';
                badge = <span className="inline-block w-2 h-2 rounded-full bg-rose-500 mr-1 shadow-[0_0_6px_#f43f5e]" />;
              } else if (hasWarning) {
                textColor = 'text-amber-400 font-black';
                badge = <span className="inline-block w-2 h-2 rounded-full bg-amber-400 mr-1 shadow-[0_0_6px_#f59e0b]" />;
              } else if (isActive) {
                textColor = 'text-neon-cyan font-black';
              }

              return (
                <div key={i} className={`h-[22px] flex items-center justify-end ${textColor}`}>
                  {badge}
                  <span>{lineNum}</span>
                </div>
              );
            })}
          </div>

          {/* Editor Canvas with Red/Yellow Line Highlighting Overlay */}
          <div className="flex-1 relative h-full">
            {/* Background Highlighting Layer */}
            <div
              className="absolute inset-0 pointer-events-none py-4 px-4 font-mono text-xs overflow-hidden"
              style={{ lineHeight: '22px' }}
            >
              {lines.map((_, i) => {
                const lineNum = i + 1;
                const hasError = errorLines.has(lineNum);
                const hasWarning = warningLines.has(lineNum);
                const isActive = activeLine === lineNum;

                let rowBg = 'h-[22px] transition-colors';
                if (hasError) {
                  rowBg += ' bg-rose-500/20 border-l-2 border-rose-500';
                } else if (hasWarning) {
                  rowBg += ' bg-amber-500/15 border-l-2 border-amber-500';
                } else if (isActive) {
                  rowBg += ' bg-white/[0.02]';
                }

                return <div key={i} className={rowBg} />;
              })}
            </div>

            {/* Interactive Typing Textarea */}
            <textarea
              ref={textareaRef}
              value={currentCode}
              onChange={(e) => {
                updateCode(e.target.value);
                updateCursorPosition();
              }}
              onKeyDown={handleKeyDown}
              onKeyUp={updateCursorPosition}
              onClick={updateCursorPosition}
              onScroll={handleScroll}
              onCopy={blockClipboard}
              onPaste={blockClipboard}
              onCut={blockClipboard}
              onContextMenu={(e) => e.preventDefault()}
              spellCheck="false"
              autoComplete="off"
              autoCorrect="off"
              autoCapitalize="off"
              className="absolute inset-0 p-4 bg-transparent text-slate-100 resize-none focus:outline-none font-mono selection:bg-neon-cyan/30 placeholder:text-slate-600 custom-scrollbar z-10"
              style={{
                lineHeight: '22px',
                tabSize: 4
              }}
            />
          </div>
        </div>

        {/* Terminal / Test Case Output */}
        <div className="lg:w-96 border-t lg:border-t-0 lg:border-l border-white/[0.12] bg-slate-950/60 flex flex-col font-mono">
          <div className="px-4 py-2.5 border-b border-white/[0.1] bg-white/[0.04] flex items-center justify-between text-xs font-bold text-white">
            <div className="flex items-center gap-2">
              <Terminal className="w-3.5 h-3.5 text-neon-mint" />
              <span>Sandbox Console</span>
            </div>
            {testResult && (
              <span
                className={`text-[10px] px-2.5 py-0.5 rounded-full border font-bold font-mono ${
                  testResult.status === 'SUCCESS'
                    ? 'text-neon-mint bg-neon-emerald/20 border-neon-emerald/40'
                    : 'text-rose-300 bg-neon-rose/20 border-neon-rose/40'
                }`}
              >
                {testResult.status === 'SUCCESS' ? 'All Assertions Passed' : 'Compilation / Test Failed'}
              </span>
            )}
          </div>

          <pre className="flex-1 p-4 text-[11px] text-slate-200 overflow-y-auto whitespace-pre-wrap leading-relaxed select-text font-mono custom-scrollbar">
            {consoleOutput ||
              'Click "Run Code" to compile your solution in the isolated execution sandbox.\nCompiler diagnostics and test assertions will display here.'}
          </pre>
        </div>
      </div>

      {/* Diagnostics Alert Bar (Red for Error, Yellow for Warning) */}
      {(errorLines.size > 0 || warningLines.size > 0 || diagnosticsMsg.error || diagnosticsMsg.warning) && (
        <div className="px-5 py-2 border-t border-white/[0.1] bg-slate-950/90 flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
          <div className="flex items-center gap-4">
            {errorLines.size > 0 && (
              <div className="flex items-center gap-2 text-rose-400 font-bold">
                <AlertCircle className="w-4 h-4 text-rose-500 flex-shrink-0" />
                <span>
                  {diagnosticsMsg.error || `Error detected on line ${Array.from(errorLines).join(', ')}`}
                </span>
              </div>
            )}
            {warningLines.size > 0 && (
              <div className="flex items-center gap-2 text-amber-400 font-bold">
                <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0" />
                <span>
                  {diagnosticsMsg.warning || `Warning flagged on line ${Array.from(warningLines).join(', ')}`}
                </span>
              </div>
            )}
          </div>
          <span className="text-[10px] text-slate-400">
            Cursor: Line {activeLine}
          </span>
        </div>
      )}

      {/* Stage Progression Bottom Bar */}
      <div className="px-6 py-3 border-t border-white/[0.12] bg-white/[0.03] flex flex-wrap items-center justify-between gap-3">
        <span className="text-xs text-slate-300 font-mono">
          {activeIdx < problemsList.length - 1 ? `Challenge 1 of ${problemsList.length} Active` : 'All Coding Challenges Addressed'}
        </span>
        <div className="flex flex-wrap items-center gap-3">
          {onSubmitExam && (
            <button
              onClick={onSubmitExam}
              className="px-4 py-2 rounded-2xl liquid-pill text-rose-300 hover:text-white border border-rose-500/40 hover:bg-rose-500/15 text-xs font-bold transition flex items-center gap-1.5 font-mono"
              title="Submit exam directly"
            >
              <CheckCircle2 className="w-3.5 h-3.5 text-rose-400" />
              <span>Submit Exam Early</span>
            </button>
          )}
          {activeIdx < problemsList.length - 1 && (
            <button
              onClick={() => {
                setActiveIdx(1);
                setConsoleOutput('');
                setTestResult(null);
                setErrorLines(new Set());
                setWarningLines(new Set());
              }}
              className="px-5 py-2 rounded-2xl liquid-pill text-neon-cyan border border-neon-cyan/40 hover:bg-neon-cyan/15 text-xs font-bold transition flex items-center gap-2 font-mono"
            >
              <span>Problem 2</span> <ChevronRight className="w-4 h-4" />
            </button>
          )}
          {onProceedToInterview && (
            <button
              onClick={onProceedToInterview}
              className="px-6 py-2 rounded-2xl bg-gradient-to-r from-neon-fuchsia to-neon-violet hover:opacity-90 active:scale-95 text-white font-black text-xs transition flex items-center gap-2 shadow-neon-fuchsia font-mono"
            >
              <span>Proceed to Stage 3: Zam AI Interview</span> <ChevronRight className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
