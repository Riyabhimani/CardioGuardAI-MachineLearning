import streamlit as st
import time
import random
import pandas as pd
import numpy as np
import pickle

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


ALGO_RESULTS = {
    "Decision Tree": {"Train": 73.00, "Test": 73.45},
    "Random Forest": {"Train": 72.76, "Test": 72.95},
    "Logistic Regression": {"Train": 72.31, "Test": 73.13},
    "KNN": {"Train": 81.31, "Test": 66.96},
    "XGBoost": {"Train": 73.45, "Test": 73.48}
}


st.set_page_config(
    page_title="CardioGuard AI",
    page_icon="🫀",
    layout="wide"
)

# ---------------- THEME ----------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"


# ---------------- CSS ----------------
def load_css():
    theme = st.session_state.theme

    if theme == "dark":
        css = {
            "bg": "#0f172a",
            "card": "#1e293b",
            "text": "#f1f5f9",
            "subtext": "#94a3b8",
            "primary": "#3b82f6",
            "border": "#334155",
            "success": "#22c55e",
            "danger": "#ef4444"
        }
    else:
        css = {
            "bg": "#f8fafc",
            "card": "#ffffff",
            "text": "#1e293b",
            "subtext": "#64748b",
            "primary": "#2563eb",
            "border": "#e2e8f0",
            "success": "#10b981",
            "danger": "#ef4444"
        }

    st.markdown(f"""
    <style>
    :root {{
        --bg: {css["bg"]};
        --card: {css["card"]};
        --text: {css["text"]};
        --subtext: {css["subtext"]};
        --primary: {css["primary"]};
        --border: {css["border"]};
        --success: {css["success"]};
        --danger: {css["danger"]};
    }}

    html, body, [class*="css"] {{
        background: var(--bg);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }}

    .block-container {{
        padding-top: 2rem;
        max-width: 1200px;
    }}

    header, footer, #MainMenu {{
        visibility: hidden;
    }}

    .card {{
        background: var(--card);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid var(--border);
    }}

    .title {{
        font-size: 2rem;
        font-weight: bold;
    }}

    .subtext {{
        color: var(--subtext);
    }}

    div.stButton > button {{
        background: var(--primary);
        color: white;
        border-radius: 25px;
        padding: 0.6rem 1.2rem;
        border: none;
    }}

    div.stButton > button:hover {{
        opacity: 0.9;
    }}

    </style>
    """, unsafe_allow_html=True)


# ---------------- NAVBAR ----------------
def navbar():
    col1, col2, col3, col4 = st.columns([3,1,1,1])

    with col1:
        st.markdown("## 🫀 CardioGuard AI")

    with col2:
        if st.button("Predict"):
            st.session_state.page = "predict"

    with col3:
        if st.button("Insights"):
            st.session_state.page = "insights"

    with col4:
        if st.button("🌙" if st.session_state.theme=="light" else "☀️"):
            toggle_theme()
            st.rerun()


# ---------------- MOCK MODEL ----------------
def mock_predict(data):
    score = 0

    if data['age'] > 50:
        score += 20

    if data['ap_hi'] > 140:
        score += 20

    if data['cholesterol'] > 1:
        score += 20

    if data['smoke'] == 1:
        score += 10

    return min(score/100, 0.95)


# ---------------- PREDICT ----------------
def predict_page():
    st.markdown("### Enter Details")

    col1, col2, col3 = st.columns(3)

    age = col1.number_input("Age", 10, 100, 50)
    ap_hi = col2.number_input("Systolic BP", 80, 200, 120)
    cholesterol = col3.selectbox("Cholesterol", [1,2,3])

    smoke = st.selectbox("Smoking", [0,1])

    if st.button("Predict"):
        prob = mock_predict({
            "age": age,
            "ap_hi": ap_hi,
            "cholesterol": cholesterol,
            "smoke": smoke
        })

        st.markdown(f"## Risk: {prob*100:.2f}%")

        if PLOTLY_AVAILABLE:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob*100,
                gauge={'axis': {'range': [0,100]}}
            ))
            st.plotly_chart(fig, use_container_width=True)


# ---------------- INSIGHTS ----------------
def insights_page():
    st.markdown("### Model Comparison")

    df = pd.DataFrame(ALGO_RESULTS).T

    if PLOTLY_AVAILABLE:
        fig = px.bar(df, barmode='group')
        st.plotly_chart(fig, use_container_width=True)


# ---------------- MAIN ----------------
load_css()
navbar()

if "page" not in st.session_state:
    st.session_state.page = "predict"

if st.session_state.page == "predict":
    predict_page()
elif st.session_state.page == "insights":
    insights_page()
