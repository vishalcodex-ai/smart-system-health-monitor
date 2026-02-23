# 🚀 Smart System Health Monitor

An AI-Based Smart System Health Monitoring & Failure Prediction Dashboard built using Python, Streamlit, and Machine Learning.

This project monitors real-time system performance (CPU, RAM, Disk), detects critical health conditions, generates intelligent alerts, and predicts potential future system failures.

📌 Features

📊 Real-time Monitoring of:
CPU Usage
RAM Usage
Disk Usage
🧠 Intelligent Health Score Calculation
⚠️ Smart Alert System with Cooldown Mechanism
🔮 Machine Learning-Based Failure Prediction
🧹 Automatic RAM Optimization (Critical Mode)
📁 CSV Data Logging
🌐 Interactive Web Dashboard (Streamlit)
☁️ Cloud Deployment Ready (Railway / Streamlit Cloud)

🛠️ Tech Stack
Programming Language: Python
Frontend & Dashboard: Streamlit
Machine Learning: Scikit-learn
System Monitoring: psutil
Data Handling: Pandas, NumPy
Model Persistence: Joblib
Deployment: Railway
Version Control: Git & GitHub

Smart-System-Health-Monitor/
│
├── core/                # Monitoring, Alerts, Analyzer, Prediction logic
├── dashboard/           # Streamlit UI
│   └── app.py
├── ml/                  # Model training & prediction scripts
├── utils/               # Health score, logging, file handling
├── config/              # System thresholds & settings
├── requirements.txt     # Dependencies
├── Procfile             # Railway deployment file
├── runtime.txt          # Python version
└── README.md
