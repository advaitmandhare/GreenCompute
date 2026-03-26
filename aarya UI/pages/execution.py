import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Execution | GreenCompute",
    layout="wide"
)

# ---------------- GLOBAL STYLE ----------------
st.markdown("""
<style>

/* Navbar */
.navbar {
    background-color:#0f172a;
    padding:14px 30px;
    border-radius:12px;
    margin-bottom:25px;
}

.navbar a {
    color:white;
    margin-right:30px;
    text-decoration:none;
    font-weight:600;
    font-size:17px;
}

.navbar a:hover {color:#22c55e;}

/* Upload Card */
.upload-card {
    background:linear-gradient(145deg,#0f172a,#111827);
    padding:28px;
    border-radius:18px;
    box-shadow:0px 4px 18px rgba(0,0,0,0.4);
}

/* Decision Card */
.decision-card {
    background:linear-gradient(90deg,#14532d,#166534);
    padding:20px;
    border-radius:14px;
    font-size:17px;
    color:white;
}

/* Info Card */
.metric-card {
    background:linear-gradient(145deg,#0f172a,#111827);
    padding:16px;
    border-radius:14px;
    text-align:center;
    margin-bottom:12px;
}

.highlight {
    font-size:22px;
    font-weight:600;
    color:#22c55e;
}

</style>


<div class="navbar">
<a href="/">🏠 Home</a>
<a href="/submit_job">📤 Submit Job</a>
<a href="/scheduling">🧠 Scheduling</a>
<a href="/execution">⚙️ Execution</a>
<a href="/impact">📊 Impact</a>
</div>
""", unsafe_allow_html=True)


# ---------------- PAGE TITLE ----------------
st.title("Execution Monitoring Console")


# ---------------- EXECUTION STATUS CARD ----------------
st.markdown("""
<div class="status-card">

<b>Deployment Status:</b> Running Successfully<br><br>

Region: UK (eu-west-2)<br>
Instance Type: GPU Optimized Node<br>
Carbon Intensity: 40 gCO₂/kWh<br><br>

Estimated Completion Time: 12 minutes

</div>
""", unsafe_allow_html=True)


# ---------------- KPI ROW ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Execution Progress", "68%")
col2.metric("Energy Consumed", "2.4 kWh")
col3.metric("CO₂ Emitted", "0.096 kg")
col4.metric("Carbon Saved vs Baseline", "31%")


# ---------------- EXECUTION TIMELINE ----------------
st.subheader("Execution Timeline")

timeline_data = pd.DataFrame({
    "Stage": ["Queued", "Scheduled", "Provisioned", "Running", "Optimizing"],
    "Completion": [100, 100, 100, 68, 40]
})

fig_timeline = px.bar(
    timeline_data,
    x="Stage",
    y="Completion",
    color="Completion",
    color_continuous_scale="Greens"
)

fig_timeline.update_layout(height=350)

st.plotly_chart(fig_timeline, use_container_width=True)


# ---------------- ENERGY USAGE CHART ----------------
st.subheader("Energy Consumption Trend")

energy_data = pd.DataFrame({
    "Minute": [1,2,3,4,5,6,7,8],
    "Energy_kWh": [0.2,0.35,0.48,0.7,1.1,1.6,2.0,2.4]
})

fig_energy = px.line(
    energy_data,
    x="Minute",
    y="Energy_kWh",
    markers=True
)

fig_energy.update_layout(height=350)

st.plotly_chart(fig_energy, use_container_width=True)


# ---------------- RESOURCE UTILIZATION ----------------
st.subheader("Resource Utilization")

resource_df = pd.DataFrame({
    "Resource": ["CPU", "GPU", "Memory", "Network"],
    "Usage (%)": [72, 64, 58, 46]
})

fig_resource = px.bar(
    resource_df,
    x="Resource",
    y="Usage (%)",
    color="Usage (%)",
    color_continuous_scale="Blues",
    text_auto=True
)

fig_resource.update_layout(height=350)

st.plotly_chart(fig_resource, use_container_width=True)


# ---------------- CARBON SAVINGS PANEL ----------------
st.subheader("Execution Sustainability Insight")

st.success(
    "Execution in a low-carbon region reduced emissions by approximately 31% compared to default deployment region."
)


# ---------------- NEXT STEP ----------------
st.divider()

st.subheader("Proceed to Sustainability Impact Report")

if st.button("View Impact Analysis"):
    st.switch_page("pages/impact.py")


# ---------------- FOOTER ----------------
st.markdown("""
---
<center style="color:gray;">
GreenCompute • Carbon-Aware Cloud Scheduling Dashboard
</center>
""", unsafe_allow_html=True)