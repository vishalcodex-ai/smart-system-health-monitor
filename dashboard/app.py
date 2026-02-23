# ==========================================
# Smart System Health Monitor
# Streamlit Dashboard (Optimized Version)
# File: dashboard/app.py
# ==========================================

import os
import sys
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# -------------------------------
# Fix Python Path
# -------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# -------------------------------
# Project Imports
# -------------------------------
from core.monitor import SystemMonitor
from core.analyzer import SystemAnalyzer
from core.predictor import FailurePredictor
from core.auto_cleaner import auto_clean_ram
from utils.file_handler import append_system_log
from utils.logger import get_logger

# -------------------------------
# Streamlit Config
# -------------------------------
st.set_page_config(
    page_title="Smart System Health Monitor",
    layout="wide"
)

st.title("🖥️ Smart System Health Monitor")
st.caption("Real-time system monitoring & AI-based failure prediction")

# Auto refresh every 5 sec
st_autorefresh(interval=5000, key="refresh")

logger = get_logger("dashboard")

# -------------------------------
# Initialize Core
# -------------------------------
monitor = SystemMonitor()
analyzer = SystemAnalyzer()
predictor = FailurePredictor()

# -------------------------------
# SMART HEALTH LOGIC (Improved)
# -------------------------------
def enrich_analysis(metrics, analysis):
    cpu = metrics.get("cpu", 0)
    ram = metrics.get("ram", {}).get("percent", 0)
    disk = metrics.get("disk", {}).get("percent", 0)

    problems = []
    suggestions = []

    # Weighted Risk Score (Professional Approach)
    risk_score = (cpu * 0.4) + (ram * 0.4) + (disk * 0.2)

    # ---------------- CPU ----------------
    if cpu > 95:
        problems.append("CPU Extremely High")
        suggestions.append("Close heavy applications immediately")
    elif cpu > 85:
        problems.append("CPU Usage High")

    # ---------------- RAM ----------------
    if ram > 92:
        problems.append("RAM Critically High")
        suggestions.append("Restart system or upgrade RAM")
    elif ram > 85:
        problems.append("RAM Usage High")
        suggestions.append("Close unused background apps")

    # ---------------- DISK ----------------
    if disk > 95:
        problems.append("Disk Almost Full")
        suggestions.append("Delete unused files immediately")
    elif disk > 85:
        problems.append("Disk Usage Increasing")

    # ---------------- Final Status ----------------
    if risk_score > 85:
        status = "Critical"
        message = "🚨 High Risk of System Failure"

        # Auto clean only if RAM > 95 (Not 85!)
        if ram > 95:
            auto_clean_ram()

    elif risk_score > 65:
        status = "Warning"
        message = "⚠️ System Under Moderate Load"

    else:
        status = "Healthy"
        message = "✅ System Stable"

    analysis["health"] = {
        "score": round(max(100 - risk_score, 0), 2),
        "risk_score": round(risk_score, 2),
        "status": status,
        "message": message,
        "problems": problems,
        "suggestions": suggestions
    }

    return analysis


# -------------------------------
# Collect Data
# -------------------------------
metrics, analysis, prediction = {}, {}, {}

try:
    metrics = monitor.collect_metrics()
    append_system_log(metrics)

    analysis = analyzer.analyze_metrics(metrics)
    analysis = enrich_analysis(metrics, analysis)

    prediction = predictor.predict({
        "cpu": metrics.get("cpu", 0),
        "ram": metrics.get("ram", {}).get("percent", 0),
        "disk": metrics.get("disk", {}).get("percent", 0)
    })

except Exception as e:
    logger.exception(e)
    st.error(f"Monitoring error: {e}")

# -------------------------------
# UI METRICS
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CPU Usage (%)", round(metrics.get("cpu", 0), 2))

with col2:
    st.metric("RAM Usage (%)", round(metrics.get("ram", {}).get("percent", 0), 2))

with col3:
    st.metric("Disk Usage (%)", round(metrics.get("disk", {}).get("percent", 0), 2))

st.divider()

# -------------------------------
# HEALTH SECTION
# -------------------------------
health = analysis.get("health")

if health:
    st.subheader("🩺 System Health")

    # Health progress (based on 100 - risk)
    st.progress(health["score"] / 100)

    # Dynamic Message
    if health["status"] == "Critical":
        st.error(health["message"])
    elif health["status"] == "Warning":
        st.warning(health["message"])
    else:
        st.success(health["message"])

    # Show Risk Score (Professional Touch)
    st.caption(f"Risk Score: {health['risk_score']}")

    # Problems
    if health["problems"]:
        st.subheader("⚠️ Detected Issues")
        for p in health["problems"]:
            st.write("•", p)

    # Suggestions
    if health["suggestions"]:
        st.subheader("💡 Recommended Actions")
        for s in health["suggestions"]:
            st.write("•", s)

st.divider()

# -------------------------------
# FAILURE PREDICTION
# -------------------------------
st.subheader("🔮 AI Failure Prediction")

if prediction:
    st.json(prediction)
else:
    st.info("No prediction data available")

st.success("Dashboard running successfully 🚀")