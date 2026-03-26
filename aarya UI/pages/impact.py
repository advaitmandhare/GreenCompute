import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import random
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Impact | GreenCompute",
    layout="wide"
)

# ---------------- HIDE SIDEBAR ----------------
st.markdown("""
<style>

/* Hide sidebar */
[data-testid="stSidebar"] {display:none;}
[data-testid="collapsedControl"] {display:none;}

/* Navbar */
.navbar {
    background-color:#0f172a;
    padding:14px 30px;
    border-radius:12px;
    margin-bottom:20px;
}
.navbar a {
    color:white;
    margin-right:30px;
    text-decoration:none;
    font-weight:600;
    font-size:17px;
}
.navbar a:hover {color:#22c55e;}

.big-title {
    font-size:48px;
    font-weight:700;
}

/* KPI Cards */
.kpi-card {
    background:linear-gradient(145deg,#0f172a,#111827);
    padding:22px;
    border-radius:16px;
    text-align:center;
    color:white;
    box-shadow:0px 4px 18px rgba(0,0,0,0.4);
}
.kpi-title {
    font-size:16px;
    color:#9ca3af;
}
.kpi-value {
    font-size:34px;
    font-weight:bold;
}

/* Feature cards */
.feature-card {
    background:#111827;
    padding:20px;
    border-radius:14px;
    text-align:center;
    font-size:18px;
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


# ================= SAMPLE DATA =================
baseline_carbon = random.randint(650, 820)
optimized_carbon = random.randint(350, 480)

carbon_saved = baseline_carbon - optimized_carbon
reduction_percent = round((carbon_saved / baseline_carbon) * 100, 2)

renewable_percent = random.randint(55, 75)
fossil_percent = 100 - renewable_percent

baseline_cost = random.randint(40, 60)
optimized_cost = baseline_cost - random.randint(8, 18)

cost_saved = baseline_cost - optimized_cost

baseline_time = random.randint(12, 18)
optimized_time = baseline_time - random.randint(2, 5)

time_saved = baseline_time - optimized_time


# ================= PAGE TITLE =================
st.title("Sustainability Impact Report")


# ================= SUMMARY CARD =================
st.markdown(f"""
<div class="summary-card">

Deployment completed using carbon-aware region selection.

Carbon Reduced: {reduction_percent}%  
Renewable Energy Used: {renewable_percent}%  
Cost Saved: ₹{cost_saved}  
Execution Time Reduced: {time_saved} minutes

</div>
""", unsafe_allow_html=True)


# ================= KPI STRIP =================
k1, k2, k3, k4 = st.columns(4)

k1.metric("Carbon Saved", f"{carbon_saved} gCO₂")
k2.metric("Emission Reduction", f"{reduction_percent}%")
k3.metric("Cost Saved", f"₹{cost_saved}")
k4.metric("Time Saved", f"{time_saved} min")


# ================= EMISSION COMPARISON =================
st.subheader("Carbon Emission Comparison")

carbon_df = pd.DataFrame({
    "Scenario": ["Traditional Deployment", "GreenCompute Deployment"],
    "Carbon": [baseline_carbon, optimized_carbon]
})

fig_bar = px.bar(
    carbon_df,
    x="Scenario",
    y="Carbon",
    color="Scenario",
    text_auto=True
)

st.plotly_chart(fig_bar, use_container_width=True)


# ================= DONUT CHART ROW =================
col1, col2 = st.columns(2)


with col1:

    st.subheader("Renewable Energy Contribution")

    fig1, ax1 = plt.subplots()

    ax1.pie(
        [renewable_percent, fossil_percent],
        labels=["Renewable", "Fossil"],
        autopct="%1.1f%%",
        wedgeprops={"width":0.45},
        startangle=90
    )

    ax1.axis("equal")

    st.pyplot(fig1)


with col2:

    st.subheader("SLA Improvement Distribution")

    sla_labels = [
        "Latency Improved",
        "Queue Delay Reduced",
        "Throughput Increased"
    ]

    sla_values = [35, 40, 25]

    fig2, ax2 = plt.subplots()

    ax2.pie(
        sla_values,
        labels=sla_labels,
        autopct="%1.1f%%",
        wedgeprops={"width":0.45},
        startangle=90
    )

    ax2.axis("equal")

    st.pyplot(fig2)


# ================= EXECUTION TIMELINE =================
st.subheader("Execution Workflow Timeline")

timeline = pd.DataFrame({
    "Stage": [
        "Submitted",
        "Scheduled",
        "Allocated",
        "Running",
        "Completed"
    ],
    "Progress": [10, 35, 55, 80, 100]
})

fig_line = px.line(
    timeline,
    x="Stage",
    y="Progress",
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)


# ================= IMPACT SCORE =================
st.subheader("Impact Efficiency Score")

impact_score = (
    reduction_percent * 0.5
    + renewable_percent * 0.3
    + time_saved * 2
)

normalized_score = min(round(impact_score / 10, 2), 1)

st.progress(normalized_score)

st.metric("Overall Sustainability Efficiency", normalized_score)


# ================= FINAL SUMMARY =================
st.success(
    f"""
GreenCompute successfully optimized workload deployment.

Carbon emissions reduced by {reduction_percent}%  
Renewable energy usage increased to {renewable_percent}%  
Execution cost reduced by ₹{cost_saved}  
Execution latency reduced by {time_saved} minutes
"""
)