import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GreenCompute",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
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

# ---------------- TITLE ----------------
st.markdown('<p class="big-title">🌱 GreenCompute</p>',
            unsafe_allow_html=True)

st.subheader("A Carbon Conscious Cloud Job Scheduler")
st.caption("Optimizing cloud workloads for sustainability-aware deployment")

col_title, col_button = st.columns([6, 1])

with col_button:
    if st.button("🚀 Submit Job"):
        st.switch_page("pages/submit_job.py")

st.write("""
GreenCompute intelligently routes workloads to cloud regions with **lower carbon emissions**, 
**higher renewable energy availability**, and **acceptable latency** — enabling sustainable 
cloud computing without compromising performance.
""")

st.divider()

# ---------------- KPI + TREND SIDE-BY-SIDE LAYOUT ----------------

col_left, col_right = st.columns([1, 2])


# -------- LEFT: KPI SUMMARY PANEL --------

with col_left:

    st.markdown("### 📊 Climate Impact Snapshot")

    kpi_data = [
        ("🌍 Global CO₂ Emissions", "37.4 Billion Tons"),
        ("⚡ Data Center Energy Use", "3% of Global Electricity"),
        ("☁️ Cloud Growth Rate", "18% YoY"),
        ("📉 Reduction via Smart Scheduling", "Up to 30%")
    ]

    for title, value in kpi_data:

        st.markdown(f"""
        <div style="
            background:linear-gradient(145deg,#0f172a,#111827);
            padding:16px;
            border-radius:12px;
            margin-bottom:12px;
            font-size:16px;">
            <b>{title}</b><br>
            <span style="font-size:22px;">{value}</span>
        </div>
        """, unsafe_allow_html=True)


# -------- RIGHT: TREND CHART --------

with col_right:

    st.markdown("### 🌍 Global Carbon Emissions Trend (2018–2024)")

    carbon_data = pd.DataFrame({
        "Year": [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        "CO2": [33.5, 34.1, 31.5, 36.3, 37.1, 37.4, 37.8]
    })

    fig = px.line(
        carbon_data,
        x="Year",
        y="CO2",
        markers=True
    )

    fig.update_traces(
        line=dict(width=3, color="#22c55e"),
        marker=dict(size=8, color="#22c55e")
    )

    fig.update_layout(
        height=420,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(
            tickmode="linear",
            dtick=1
        ),
        yaxis=dict(range=[31, 39]),
        xaxis_title="Year",
        yaxis_title="Global CO₂ Emissions (Gt)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("*2024 estimated global emissions based on projections.")

# ---------------- WORLD MAP CARBON COMPARISON ----------------

st.subheader("🗺️ Global Electricity Carbon Intensity by Region")

map_data = pd.DataFrame({
    "Country": [
        "France","Norway","Sweden","Brazil","Canada",
        "United Kingdom","Germany","United States",
        "India","China","Australia","South Africa",
        "Japan","Russia","Saudi Arabia"
    ],
    "ISO": [
        "FRA","NOR","SWE","BRA","CAN",
        "GBR","DEU","USA",
        "IND","CHN","AUS","ZAF",
        "JPN","RUS","SAU"
    ],
    "CarbonIntensity": [
        50, 30, 40, 90, 120,
        200, 350, 400,
        650, 700, 540, 900,
        450, 500, 750
    ]
})


# -------- LARGE RESPONSIVE MAP --------

fig = px.choropleth(
    map_data,
    locations="ISO",
    color="CarbonIntensity",
    hover_name="Country",
    color_continuous_scale=[
        "green",
        "yellow",
        "red"
    ]
)

fig.update_layout(
    height=600,
    margin=dict(l=0, r=0, t=0, b=0),
    coloraxis_colorbar=dict(
        title="gCO₂/kWh"
    )
)

st.plotly_chart(fig, use_container_width=True)


st.divider()


# ---------------- GREEN vs RED REGION PANELS ----------------

col_green, col_red = st.columns(2)


# -------- GREENER REGIONS --------

with col_green:

    st.markdown("### 🟢 Greener Regions")

    green_regions = map_data.nsmallest(5, "CarbonIntensity")

    for _, row in green_regions.iterrows():

        st.markdown(f"""
        <div style="
            background:#166534;
            padding:10px 14px;
            border-radius:8px;
            margin-bottom:6px;
            font-size:15px;">
            {row['Country']} — {row['CarbonIntensity']} gCO₂/kWh
        </div>
        """, unsafe_allow_html=True)


# -------- HIGH EMISSION REGIONS --------

with col_red:

    st.markdown("### 🔴 High Emission Regions")

    red_regions = map_data.nlargest(5, "CarbonIntensity")

    for _, row in red_regions.iterrows():

        st.markdown(f"""
        <div style="
            background:#7a1f1f;
            padding:10px 14px;
            border-radius:8px;
            margin-bottom:6px;
            font-size:15px;">
            {row['Country']} — {row['CarbonIntensity']} gCO₂/kWh
        </div>
        """, unsafe_allow_html=True)

# ---------------- GREENCOMPUTE ADVANTAGES ----------------
st.subheader("🚀 GreenCompute Advantages")

col1, col2, col3, col4 = st.columns(4)

features = [
    ("🌍","Carbon-Aware Scheduling"),
    ("⚡","Renewable-Optimized Deployment"),
    ("📡","Latency-Safe Execution"),
    ("📊","Real-Time Sustainability Scoring")
]

for col, (icon, text) in zip([col1,col2,col3,col4], features):
    col.markdown(f"""
    <div class="feature-card">
        <div style="font-size:44px">{icon}</div>
        <div>{text}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- CTA BUTTON ----------------
st.subheader("Start Scheduling a Sustainable Job")

if st.button("🚀 Submit New Job"):
    st.switch_page("pages/submit_job.py")


st.markdown("""
---
<center style="color:#d1d5db;">
GreenCompute • Carbon-Aware Cloud Scheduling Dashboard 🌱
</center>
""", unsafe_allow_html=True)