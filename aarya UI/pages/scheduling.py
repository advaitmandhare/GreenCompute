import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Scheduling | GreenCompute",
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



# ---------------- SIDEBAR ----------------
st.sidebar.header("Scheduler Configuration")

alpha = st.sidebar.slider("Carbon Weight (α)", 0.0, 1.0, 0.5)
beta = st.sidebar.slider("Latency Weight (β)", 0.0, 1.0, 0.3)
gamma = st.sidebar.slider("Renewable Weight (γ)", 0.0, 1.0, 0.2)


# ---------------- REGION DATA ----------------
regions = pd.DataFrame({

    "Region": [
        "France (eu-west-3)",
        "Germany (eu-central-1)",
        "UK (eu-west-2)",
        "Spain (eu-south-2)",
        "Italy (eu-south-1)"
    ],

    "Carbon": [50, 350, 40, 270, 220],
    "Latency": [110, 95, 102, 120, 130],
    "Renewable": [72, 45, 68, 52, 60]
})


# ---------------- NORMALIZATION ----------------
regions["CarbonScore"] = 1 - (regions["Carbon"] / regions["Carbon"].max())
regions["LatencyScore"] = 1 - (regions["Latency"] / regions["Latency"].max())
regions["RenewableScore"] = regions["Renewable"] / 100


regions["Score"] = (
    alpha * regions["CarbonScore"]
    + beta * regions["LatencyScore"]
    + gamma * regions["RenewableScore"]
)

best = regions.sort_values("Score", ascending=False).iloc[0]


# ---------------- PAGE TITLE ----------------
st.title("Scheduler Decision Engine")


# ---------------- DECISION CARD ----------------
st.markdown(f"""
<div class="decision-card">

<b>Selected Region:</b> {best['Region']}<br><br>

Carbon Intensity: {best['Carbon']} gCO₂/kWh<br>
Latency: {best['Latency']} ms<br>
Renewable Share: {best['Renewable']}%<br><br>

<b>Final Sustainability Score:</b> {round(best['Score'],3)}

</div>
""", unsafe_allow_html=True)


# ---------------- KPI ROW ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Lowest Carbon Region", regions.loc[regions["Carbon"].idxmin()]["Region"])
col2.metric("Fastest Region", regions.loc[regions["Latency"].idxmin()]["Region"])
col3.metric("Highest Renewable Region", regions.loc[regions["Renewable"].idxmax()]["Region"])


# ---------------- REGION SCORE BAR CHART ----------------
st.subheader("Region Sustainability Score Comparison")

fig = px.bar(
    regions,
    x="Region",
    y="Score",
    color="Score",
    color_continuous_scale="Greens",
    text_auto=True
)

fig.update_layout(height=420)

st.plotly_chart(fig, use_container_width=True)


# ---------------- WORLD CARBON MAP ----------------
st.subheader("Global Electricity Carbon Intensity Map")

map_df = pd.DataFrame({

    "Country": ["France","Germany","United Kingdom","Spain","Italy","India","China","USA","Canada"],
    "ISO": ["FRA","DEU","GBR","ESP","ITA","IND","CHN","USA","CAN"],
    "CarbonIntensity": [50,350,40,270,220,650,700,400,120]
})

fig_map = px.choropleth(
    map_df,
    locations="ISO",
    color="CarbonIntensity",
    hover_name="Country",
    color_continuous_scale=["green","yellow","red"]
)

fig_map.update_layout(height=520)

st.plotly_chart(fig_map, use_container_width=True)




# ---------------- REGION RANKING TABLE ----------------
st.subheader("Region Ranking Table")

st.dataframe(
    regions.sort_values("Score", ascending=False),
    use_container_width=True
)


# ---------------- STRATEGY INSIGHT PANEL ----------------
st.subheader("Scheduling Insight")

if alpha > beta and alpha > gamma:

    st.success("Carbon-aware scheduling dominated region selection")

elif beta > alpha:

    st.warning("Latency-sensitive workload influenced scheduling decision")

else:

    st.info("Renewable energy availability influenced selection")