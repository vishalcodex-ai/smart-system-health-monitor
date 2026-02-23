# ==========================================
# Smart System Health Monitor
# Streamlit Dashboard (LOCAL / DEMO)
# File: dashboard/app.py
# ==========================================

import os
import sys
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# -------------------------------
# Fix Python Path (IMPORTANT)
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
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="Smart System Health Monitor",
    layout="wide"
)

st.title("🖥️ Smart System Health Monitor")
st.caption("Real-time system monitoring & failure prediction (Demo)")

# 🔁 Auto refresh every 5 sec (safe)
st_autorefresh(interval=5000, key="refresh")

logger = get_logger("dashboard")

# -------------------------------
# Initialize Core (ONE TIME)
# -------------------------------
monitor = SystemMonitor()
analyzer = SystemAnalyzer()
predictor = FailurePredictor()

# -------------------------------
# Health Logic
# -------------------------------
def enrich_analysis(metrics, analysis):
    cpu = metrics.get("cpu", 0)
    ram = metrics.get("ram", {}).get("percent", 0)
    disk = metrics.get("disk", {}).get("percent", 0)

    score = 100
    problems, suggestions = [], []

    if cpu > 85:
        score -= 40
        problems.append("CPU Overloaded")
        suggestions.append("Close unused applications")

    if ram > 90:
        score -= 40
        problems.append("RAM Almost Full")
        suggestions.append("Restart system / reduce startup apps")

    if disk > 85:
        score -= 20
        problems.append("Disk Usage High")
        suggestions.append("Delete unused files")

    if score <= 40:
        status = "Critical"
        message = "⚠️ High risk of system failure"
        auto_clean_ram()
    elif score <= 70:
        status = "Warning"
        message = "⚠️ System under pressure"
    else:
        status = "Healthy"
        message = "✅ System is healthy"

    analysis["health"] = {
        "score": max(score, 0),
        "status": status,
        "message": message,
        "problems": problems,
        "suggestions": suggestions
    }

    return analysis

# -------------------------------
# Collect Data (SINGLE CYCLE)
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
    st.metric("CPU Usage (%)", metrics.get("cpu", 0))

with col2:
    st.metric("RAM Usage (%)", metrics.get("ram", {}).get("percent", 0))

with col3:
    st.metric("Disk Usage (%)", metrics.get("disk", {}).get("percent", 0))

st.divider()

# -------------------------------
# HEALTH STATUS
# -------------------------------
health = analysis.get("health")

if health:
    st.subheader("🩺 System Health")
    st.progress(health["score"] / 100)

    if health["status"] == "Critical":
        st.error(health["message"])
    elif health["status"] == "Warning":
        st.warning(health["message"])
    else:
        st.success(health["message"])

    if health["problems"]:
        st.subheader("⚠️ Problems")
        for p in health["problems"]:
            st.write("•", p)

    if health["suggestions"]:
        st.subheader("💡 Suggestions")
        for s in health["suggestions"]:
            st.write("•", s)

st.divider()

# -------------------------------
# FAILURE PREDICTION
# -------------------------------
st.subheader("🔮 Failure Prediction")
st.json(prediction)

st.success("Dashboard running (demo mode) 🚀")
