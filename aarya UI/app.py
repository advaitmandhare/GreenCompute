import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GreenCompute Dashboard",
    page_icon="🌱",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("🌱 GreenCompute Scheduler Dashboard")
st.caption("Carbon-Aware Job Scheduling Interface")

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Scheduling Controls")

alpha = st.sidebar.slider(
    "Alpha (Carbon Priority)", 0.0, 1.0, 0.5
)

beta = st.sidebar.slider(
    "Beta (Latency Priority)", 0.0, 1.0, 0.3
)

gamma = st.sidebar.slider(
    "Gamma (Performance Priority)", 0.0, 1.0, 0.2
)

st.sidebar.markdown("---")
st.sidebar.success("Scheduler weights updated")

# ---------------- PARAMETER METRICS ----------------
st.subheader("📊 Parameter Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Carbon Priority (α)", round(alpha, 2))
col2.metric("Latency Priority (β)", round(beta, 2))
col3.metric("Performance Priority (γ)", round(gamma, 2))


# ---------------- PARAMETER VISUALIZATION ----------------
st.subheader("📈 Weight Distribution")

param_df = pd.DataFrame({
    "Parameter": ["Carbon", "Latency", "Performance"],
    "Weight": [alpha, beta, gamma]
})

st.bar_chart(param_df.set_index("Parameter"))

# ---------------- SUSTAINABILITY SCORE ----------------
st.subheader("🌍 Sustainability Score")

score = (alpha * 0.4) + (beta * 0.3) + (gamma * 0.3)

score_col1, score_col2 = st.columns([2,1])

with score_col1:
    st.progress(score)

with score_col2:
    st.metric("Score", round(score, 2))

if score >= 0.7:
    st.success("Recommended: Low-carbon execution region ✅")
elif score >= 0.4:
    st.warning("Balanced scheduling region suggested ⚖️")
else:
    st.error("Performance-priority region suggested 🚀")

st.markdown("---")


# ---------------- REGION COMPARISON TABLE ----------------
st.subheader("🌐 Region Comparison (Simulated)")

region_data = pd.DataFrame({
    "Region": ["India (ap-south-1)", "Europe (eu-west-1)", "US East (us-east-1)"],
    "Carbon Intensity": ["High", "Low", "Medium"],
    "Latency": ["Low", "Medium", "Medium"],
    "Score": [0.52, 0.68, 0.60]
})

st.dataframe(region_data, use_container_width=True)


# ---------------- SCHEDULER DECISION PREVIEW ----------------
st.subheader("🧠 Scheduler Decision Preview")

if score >= 0.6:
    region = "Europe (eu-west-1)"
elif score >= 0.45:
    region = "US East (us-east-1)"
else:
    region = "India (ap-south-1)"

decision_col1, decision_col2 = st.columns(2)

decision_col1.info(f"Selected Region: {region}")
decision_col2.success("Decision Confidence: High")


st.markdown("---")


# ---------------- JOB HISTORY SUMMARY ----------------
st.subheader("📂 Job Submission Summary")

LOG_FILE = "logs.json"

if os.path.exists(LOG_FILE):

    with open(LOG_FILE) as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    total_jobs = len(df)

    avg_alpha = round(df["alpha"].mean(), 2)
    avg_beta = round(df["beta"].mean(), 2)
    avg_gamma = round(df["gamma"].mean(), 2)

    hist_col1, hist_col2, hist_col3, hist_col4 = st.columns(4)

    hist_col1.metric("Total Jobs", total_jobs)
    hist_col2.metric("Avg α", avg_alpha)
    hist_col3.metric("Avg β", avg_beta)
    hist_col4.metric("Avg γ", avg_gamma)

else:
    st.info("No job submissions yet")


# ---------------- RECENT JOBS TABLE ----------------
st.subheader("📋 Recent Submissions")

if os.path.exists(LOG_FILE):

    df = pd.read_json(LOG_FILE)

    st.dataframe(df.tail(5), use_container_width=True)

else:
    st.warning("No job history available")


# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("GreenCompute | Carbon-Aware Cloud Scheduler Dashboard 🌱")