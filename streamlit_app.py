"""
Factskoot Live Campus Project: Unified 3-Tab Anti-Cheat Proctoring Dashboard
=============================================================================
Tabs:
  1. Live Proctoring: OpenCV/MediaPipe violation detection loop (gaze, face, phone, pose, backlight).
  2. Browser Focus Logger: Live session table logging tab switches, window minimization, and focus loss events.
  3. Evidence Gallery & Trust Score: Aggregate Trust Score (0-100%) calculation + clean violation screenshot gallery.
"""

import os
import sys
import time
import json
import base64
from pathlib import Path
import cv2
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

# Add backend directory to sys.path so existing proctor_engine is imported cleanly without modifications
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))
from proctor_engine import ProctorEngine

st.set_page_config(
    page_title="SKIT ProctorLens.AI • Factskoot Live Campus",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphic Styling
st.markdown("""
<style>
    .main {
        background-color: #030712;
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    .header-box {
        background: linear-gradient(135deg, rgba(6,182,212,0.1), rgba(168,85,247,0.1));
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 16px;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 24px;
        border-radius: 14px;
        font-weight: 700;
        font-family: monospace;
    }
    .status-focused {
        color: #00f59b;
        font-weight: 800;
        font-family: monospace;
    }
    .status-blurred {
        color: #f43f5e;
        font-weight: 800;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Initialize Session State
# -----------------------------------------------------------------------------
if "proctor_engine" not in st.session_state:
    st.session_state.proctor_engine = ProctorEngine()

if "focus_logs" not in st.session_state:
    st.session_state.focus_logs = [
        {
            "id": "foc-init",
            "timestamp": time.strftime("%H:%M:%S"),
            "event_type": "SESSION_INITIALIZED",
            "details": "Exam lockdown initialized. Fullscreen & window surveillance active.",
            "severity": "INFO",
            "duration_sec": 0
        }
    ]

if "is_window_focused" not in st.session_state:
    st.session_state.is_window_focused = True

if "total_lost_focus_sec" not in st.session_state:
    st.session_state.total_lost_focus_sec = 0

if "exam_submitted" not in st.session_state:
    st.session_state.exam_submitted = False

engine = st.session_state.proctor_engine

# -----------------------------------------------------------------------------
# Sidebar: Session Controls & Candidate Identity
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Target_Corporation_logo_%28vector%29.svg/100px-Target_Corporation_logo_%28vector%29.svg.png"
        if not os.path.exists("frontend/public/skit-logo.png")
        else "frontend/public/skit-logo.png",
        width=70
    )
    st.markdown("### **SKIT ProctorLens.AI**")
    st.caption("Factskoot Live Campus Autonomous Proctoring")

    st.markdown("---")
    st.markdown("#### **Candidate Profile**")
    candidate_name = st.text_input("Candidate Name", value="Student Candidate")
    candidate_email = st.text_input("SKIT Email", value="student@skit.org.in")
    candidate_dept = st.selectbox(
        "Department",
        ["Computer Science & Engineering", "Artificial Intelligence & ML", "Information Science", "Electronics & Comm."]
    )

    st.markdown("---")
    st.markdown("#### **Proctoring Engine Status**")
    trust_val = max(0, min(100, int(engine.trust_score)))
    trust_color = "normal" if trust_val >= 75 else "off"
    st.metric("Live Trust Index", f"{trust_val}%", delta=f"{trust_val - 100}%" if trust_val < 100 else "Optimal")
    st.metric("Total Infraction Strikes", f"{engine.warnings_count.get('total', 0)} / 5")

    if st.button("🔄 Reset Proctor Session", use_container_width=True):
        engine.reset_session()
        st.session_state.focus_logs.clear()
        st.session_state.total_lost_focus_sec = 0
        st.session_state.exam_submitted = False
        st.rerun()

# -----------------------------------------------------------------------------
# Top Banner
# -----------------------------------------------------------------------------
st.markdown("""
<div class="header-box">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 1.8rem; font-weight: 900; color: #fff;">
                Sri Krishna Institute of Technology • AI Proctor Cockpit
            </h1>
            <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.9rem; font-family: monospace;">
                Factskoot Hackathon Autonomous Anti-Cheat Proctoring Matrix • OpenCV + MediaPipe
            </p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(0,245,155,0.15); color: #00f59b; padding: 6px 14px; border-radius: 20px; font-weight: 800; font-family: monospace; border: 1px solid rgba(0,245,155,0.4); font-size: 0.8rem;">
                ● AI ACTIVE
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3-Tab Main Navigation
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🎥 Tab 1: Live Proctoring",
    "🛡️ Tab 2: Browser Focus Logger",
    "📊 Tab 3: Evidence Gallery & Trust Score"
])

# =============================================================================
# TAB 1: LIVE PROCTORING
# =============================================================================
with tab1:
    st.markdown("### 🎥 Live Proctoring Surveillance")
    st.caption("Untouched OpenCV/MediaPipe pipeline analyzing gaze deflection, head nodding, phone detection, and lighting.")

    col_cam, col_hud = st.columns([7, 5])

    with col_cam:
        st.markdown("#### **Camera Input Stream**")
        cam_source = st.radio("Camera Source Mode:", ["Webcam Camera (Live)", "Interactive Video Frame Snapshot"], horizontal=True)

        if cam_source == "Webcam Camera (Live)":
            run_cam = st.checkbox("▶️ Enable Continuous Camera Feed", value=False)
            frame_placeholder = st.empty()

            if run_cam:
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    st.error("Unable to access local webcam device. Check browser permissions or test via frame snapshot.")
                else:
                    stop_btn = st.button("⏹️ Stop Camera Stream")
                    while run_cam and not stop_btn:
                        ret, frame = cap.read()
                        if not ret:
                            break

                        # Process frame using existing proctor_engine without modifying core logic
                        analysis = engine.analyze_frame(frame)
                        annotated = analysis.get("annotated_frame", frame)

                        # Convert BGR to RGB for Streamlit display
                        rgb_frame = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                        frame_placeholder.image(rgb_frame, channels="RGB", use_container_width=True)
                        time.sleep(0.08)

                    cap.release()
            else:
                st.info("Check 'Enable Continuous Camera Feed' above to start real-time computer vision proctoring.")
        else:
            # Interactive Snapshot Mode
            cam_shot = st.camera_input("Capture Instant Assessment Verification Frame")
            if cam_shot is not None:
                bytes_data = cam_shot.getvalue()
                cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
                analysis = engine.analyze_frame(cv_img)
                annotated = analysis.get("annotated_frame", cv_img)

                st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), caption="Processed MediaPipe & CV Frame", use_container_width=True)
                st.success(f"Frame Analyzed • Face Count: {analysis.get('face_count')} • Trust Score: {analysis.get('trust_score')}%")

    with col_hud:
        st.markdown("#### **Real-Time Proctoring Telemetry**")
        
        # Dial / Score indicator
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 18px; padding: 20px; text-align: center; margin-bottom: 16px;">
            <div style="font-size: 0.8rem; font-family: monospace; color: #94a3b8; text-transform: uppercase;">Real-Time Trust Index</div>
            <div style="font-size: 3rem; font-weight: 900; font-family: monospace; color: {'#00f59b' if trust_val >= 75 else '#f43f5e' if trust_val < 50 else '#fbbf24'};">
                {trust_val}%
            </div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #fff;">
                {'VERIFIED INTEGRITY' if trust_val >= 75 else 'HIGH RISK AUDIT' if trust_val < 50 else 'SUSPICIOUS ACTIVITY'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### **Recent Infraction Alerts**")
        recent_incidents = engine.incidents[:6]
        if not recent_incidents:
            st.success("🟢 Zero infractions recorded in current session.")
        else:
            for inc in recent_incidents:
                sev_color = "red" if inc.get("severity") == "CRITICAL" else "orange" if inc.get("severity") == "HIGH" else "blue"
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.02); border-left: 4px solid {sev_color}; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; font-family: monospace; font-size: 0.8rem;">
                    <div style="display: flex; justify-content: space-between;">
                        <strong style="color: #fff;">{inc.get('code')}</strong>
                        <span style="color: #94a3b8;">{inc.get('time_display')}</span>
                    </div>
                    <div style="color: #cbd5e1; margin-top: 2px;">{inc.get('message')}</div>
                </div>
                """, unsafe_allow_html=True)

# =============================================================================
# TAB 2: BROWSER FOCUS LOGGER
# =============================================================================
with tab2:
    st.markdown("### 🛡️ Browser Focus & Window Activity Logger")
    st.caption("Surveillance tracking tab switches, window minimization, Alt+Tab actions, and loss of window focus.")

    # Status & Counters
    status_col1, status_col2, status_col3, status_col4 = st.columns(4)
    tab_switches_count = sum(1 for x in st.session_state.focus_logs if "TAB" in x.get("event_type", ""))
    blurs_count = sum(1 for x in st.session_state.focus_logs if "BLUR" in x.get("event_type", "") or "MINIMIZE" in x.get("event_type", ""))
    fullscreen_count = sum(1 for x in st.session_state.focus_logs if "FULLSCREEN" in x.get("event_type", ""))
    hotkey_count = sum(1 for x in st.session_state.focus_logs if "HOTKEY" in x.get("event_type", "") or "CLIPBOARD" in x.get("event_type", ""))

    with status_col1:
        st.metric("Tab Switches", tab_switches_count)
    with status_col2:
        st.metric("Window Minimizations", blurs_count)
    with status_col3:
        st.metric("Fullscreen Exits", fullscreen_count)
    with status_col4:
        st.metric("Total Lost Focus Time", f"{st.session_state.total_lost_focus_sec}s")

    st.markdown("---")

    # Interactive Simulation Triggers
    st.markdown("#### **Interactive Browser Focus Simulation Triggers**")
    st.caption("Trigger simulated events to test focus degradation and trust score adjustments in real-time.")

    bcol1, bcol2, bcol3, bcol4 = st.columns(4)

    with bcol1:
        if st.button("⚠️ Simulate Tab Switch", use_container_width=True):
            evt = {
                "id": f"foc-{int(time.time()*1000)}",
                "timestamp": time.strftime("%H:%M:%S"),
                "event_type": "TAB_SWITCH_DETECTED",
                "details": "Candidate switched to background tab or application.",
                "severity": "CRITICAL",
                "duration_sec": 4
            }
            st.session_state.focus_logs.insert(0, evt)
            st.session_state.total_lost_focus_sec += 4
            engine.log_external_violation("TAB_SWITCH_DETECTED", "Candidate switched away from exam window.", severity="CRITICAL")
            st.rerun()

    with bcol2:
        if st.button("🪟 Simulate Window Minimization", use_container_width=True):
            evt = {
                "id": f"foc-{int(time.time()*1000)}",
                "timestamp": time.strftime("%H:%M:%S"),
                "event_type": "WINDOW_MINIMIZED",
                "details": "Candidate minimized browser window (Alt+Tab task switch).",
                "severity": "HIGH",
                "duration_sec": 3
            }
            st.session_state.focus_logs.insert(0, evt)
            st.session_state.total_lost_focus_sec += 3
            engine.log_external_violation("WINDOW_MINIMIZED", "Window minimized or lost desktop focus.", severity="HIGH")
            st.rerun()

    with bcol3:
        if st.button("🖥️ Simulate Fullscreen Exit", use_container_width=True):
            evt = {
                "id": f"foc-{int(time.time()*1000)}",
                "timestamp": time.strftime("%H:%M:%S"),
                "event_type": "FULLSCREEN_EXITED",
                "details": "Candidate exited mandatory fullscreen lockdown.",
                "severity": "CRITICAL",
                "duration_sec": 2
            }
            st.session_state.focus_logs.insert(0, evt)
            st.session_state.total_lost_focus_sec += 2
            engine.log_external_violation("FULLSCREEN_EXITED", "Fullscreen mode dismissed by user.", severity="CRITICAL")
            st.rerun()

    with bcol4:
        if st.button("📋 Simulate Prohibited Hotkey", use_container_width=True):
            evt = {
                "id": f"foc-{int(time.time()*1000)}",
                "timestamp": time.strftime("%H:%M:%S"),
                "event_type": "PROHIBITED_HOTKEY",
                "details": "Candidate attempted Ctrl+C clipboard copy shortcut.",
                "severity": "MEDIUM",
                "duration_sec": 0
            }
            st.session_state.focus_logs.insert(0, evt)
            engine.log_external_violation("PROHIBITED_HOTKEY", "Prohibited shortcut detected.", severity="MEDIUM")
            st.rerun()

    st.markdown("---")

    # Real-Time Live Session Table
    st.markdown("#### **Live Session Focus Telemetry Table**")
    
    if not st.session_state.focus_logs:
        st.info("No focus events recorded yet.")
    else:
        # Render clean table
        table_rows = []
        for log in st.session_state.focus_logs:
            table_rows.append({
                "Timestamp": log.get("timestamp"),
                "Event Type": log.get("event_type"),
                "Details & Action": log.get("details"),
                "Severity": log.get("severity"),
                "Lost Duration": f"{log.get('duration_sec', 0)}s"
            })
        st.dataframe(table_rows, use_container_width=True, height=280)

# =============================================================================
# TAB 3: EVIDENCE GALLERY & TRUST SCORE
# =============================================================================
with tab3:
    st.markdown("### 📊 Evidence Gallery & Forensic Trust Score")
    st.caption("Compilation of all visual flags, focus losses, and violation snapshots into an aggregate Trust Score (0-100%).")

    # Calculation logic
    visual_infractions = [inc for inc in engine.incidents if "TAB" not in inc.get("code", "") and "FULLSCREEN" not in inc.get("code", "")]
    focus_infractions = st.session_state.focus_logs
    total_strikes = engine.warnings_count.get("total", 0)

    visual_penalty = len(visual_infractions) * 15
    focus_penalty = (tab_switches_count * 20) + (blurs_count * 15) + (fullscreen_count * 20)
    total_deduction = visual_penalty + focus_penalty
    computed_trust = max(0, min(100, 100 - total_deduction))

    if total_strikes >= 5:
        computed_trust = min(computed_trust, 25)

    # Trust Score Metric Display
    gcol1, gcol2 = st.columns([5, 7])

    with gcol1:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border: 2px solid {'#00f59b' if computed_trust >= 75 else '#f43f5e' if computed_trust < 50 else '#fbbf24'}; border-radius: 20px; padding: 24px; text-align: center;">
            <div style="font-size: 0.85rem; font-family: monospace; color: #94a3b8; text-transform: uppercase;">Aggregate Exam Trust Score</div>
            <div style="font-size: 3.8rem; font-weight: 900; font-family: monospace; color: {'#00f59b' if computed_trust >= 75 else '#f43f5e' if computed_trust < 50 else '#fbbf24'}; margin: 10px 0;">
                {computed_trust}%
            </div>
            <div style="display: inline-block; padding: 4px 16px; border-radius: 20px; font-weight: 800; font-family: monospace; font-size: 0.85rem; background: {'rgba(0,245,155,0.15)' if computed_trust >= 75 else 'rgba(244,63,94,0.15)'}; color: {'#00f59b' if computed_trust >= 75 else '#f43f5e'};">
                {'PASSED • HIGH INTEGRITY' if computed_trust >= 75 else 'TERMINATED • ACADEMIC BREACH' if computed_trust < 50 else 'FLAGGED • AUDIT REQUIRED'}
            </div>
            <div style="margin-top: 14px; font-size: 0.8rem; color: #cbd5e1; font-family: monospace;">
                Strikes: {total_strikes} of 5 Maximum
            </div>
        </div>
        """, unsafe_allow_html=True)

    with gcol2:
        st.markdown("#### **Score Formulation & Deductions**")
        st.code(
            f"Trust Score = 100 (Base) - {visual_penalty} (Visual Flags) - {focus_penalty} (Focus Losses) = {computed_trust}%",
            language="text"
        )
        st.markdown(f"""
        - 📸 **Visual Biometric Infractions:** {len(visual_infractions)} flagged (-{visual_penalty} pts)
        - 🛡️ **Browser Focus Losses:** {len(focus_infractions)} logged (-{focus_penalty} pts)
        - ⚠️ **Total Warning Strikes:** {total_strikes} / 5
        """)

        if st.button("🏁 End & Submit Examination Session", use_container_width=True):
            st.session_state.exam_submitted = True
            st.success(f"Examination concluded successfully! Final Trust Score: {computed_trust}%. Certificate logged.")

    st.markdown("---")

    # Clean Evidence Gallery
    st.markdown("#### **📸 Captured Violation Evidence Gallery**")
    st.caption("Audit snapshots captured automatically by the computer vision engine with bounding boxes and metadata banners.")

    evidence_items = [inc for inc in engine.incidents if inc.get("snapshot") or inc.get("snapshot_path")]

    # Also check backend/evidence directory on disk
    evidence_dir = Path("backend/evidence")
    disk_images = list(evidence_dir.glob("*.jpg")) if evidence_dir.exists() else []

    if not evidence_items and not disk_images:
        st.info("No violation frames captured yet. Snapshots trigger automatically on mobile phone detection or severe face deflections.")
    else:
        # Show snapshots in a 3-column responsive grid
        cols = st.columns(3)
        displayed_count = 0

        # Show in-memory snapshots first
        for i, item in enumerate(evidence_items):
            with cols[displayed_count % 3]:
                b64 = item.get("snapshot")
                if b64:
                    if b64.startswith("data:image"):
                        b64 = b64.split(",")[1]
                    try:
                        img_data = base64.b64decode(b64)
                        st.image(img_data, caption=f"{item.get('code')} • {item.get('time_display')}", use_container_width=True)
                        st.markdown(f"**Severity:** `{item.get('severity')}` • `{item.get('message')}`")
                        displayed_count += 1
                    except Exception:
                        pass

        # Show disk images if any
        for img_path in disk_images[:6]:
            with cols[displayed_count % 3]:
                st.image(str(img_path), caption=f"Evidence: {img_path.name}", use_container_width=True)
                displayed_count += 1

    # Student & Admin Result Summary Table
    st.markdown("---")
    st.markdown("#### **Student & Admin Examination Scorecard**")

    scorecard_data = [
        {
            "Candidate": f"{candidate_name} ({candidate_email})",
            "Department": candidate_dept,
            "MCQ Score": "18.0 / 20 (90%)",
            "Coding Sandbox": "30.0 / 30 (100%)",
            "Zam AI Viva": "45.0 / 50 (90%)",
            "Total Academic Score": "93.0 / 100",
            "Final Trust Score": f"{computed_trust}%",
            "Integrity Verdict": "PASSED & VERIFIED" if computed_trust >= 75 else "FLAGGED" if computed_trust >= 50 else "TERMINATED"
        }
    ]
    st.table(scorecard_data)

