import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Submit Job | GreenCompute",
    page_icon="📂",
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


# ---------------- HEADER ----------------
st.title("Job Submission Console")
st.caption(
    "Upload workload and configure sustainability-aware scheduling priorities"
)


# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## Scheduler Control Panel")

alpha = st.sidebar.slider("Carbon Priority (α)", 0.0, 1.0, 0.6)
beta = st.sidebar.slider("Latency Priority (β)", 0.0, 1.0, 0.25)
gamma = st.sidebar.slider("Performance Priority (γ)", 0.0, 1.0, 0.15)

total_weight = round(alpha + beta + gamma, 2)

st.sidebar.write(f"Total Weight = {total_weight}")

if total_weight != 1:
    st.sidebar.warning("Weights ideally sum to 1.0")
else:
    st.sidebar.success("Balanced priority distribution")

score = round(alpha * 0.4 + beta * 0.3 + gamma * 0.3, 2)

st.sidebar.metric("Sustainability Score", score)


# ---------------- MAIN LAYOUT ----------------
left, right = st.columns([2, 1])


# ---------------- LEFT PANEL ----------------
with left:

    st.subheader("Upload ML Script")

    file = st.file_uploader(
        "Upload Python ML / Batch Script",
        type=["py"]
    )

    if file:
        st.success("Script ready for scheduling analysis")

        preview = file.getvalue().decode("utf-8")[:400]
        st.code(preview, language="python")

    else:
        st.info(
            "Upload a script to begin sustainability-aware scheduling"
        )


    # ---------------- FORMULA PANEL ----------------
    st.divider()

    st.subheader("Scheduling Score Model")

    st.latex(r"S = \alpha C + \beta L + \gamma P")

    st.write(f"""
Carbon weight (α) = **{alpha}**  
Latency weight (β) = **{beta}**  
Performance weight (γ) = **{gamma}**
""")

    st.caption(
        "Cloud regions are ranked using weighted sustainability scoring."
    )


    # ---------------- DECISION MODE PANEL ----------------
    st.divider()

    st.subheader("Scheduler Decision Mode")

    if alpha > beta and alpha > gamma:
        st.success("Carbon-aware optimization dominates")

    elif beta > alpha and beta > gamma:
        st.warning("Latency-sensitive execution mode")

    else:
        st.error("Performance-priority execution mode")


# ---------------- RIGHT PANEL ----------------
with right:

    st.subheader("Parameter Distribution")

    df = pd.DataFrame(
        {"Weight": [alpha, beta, gamma]},
        index=["Carbon", "Latency", "Performance"]
    )

    st.bar_chart(df)


    st.divider()

    st.subheader("Estimated Carbon Optimization")

    estimated_savings = round(alpha * 28, 2)

    st.metric(
        "Potential Emission Reduction",
        f"{estimated_savings}%"
    )


    st.divider()

    st.subheader("Scheduler Score Interpretation")

    if score > 0.6:
        st.success("Low-carbon regions prioritized")

    elif score > 0.3:
        st.info("Balanced scheduling strategy active")

    else:
        st.warning("Performance-oriented scheduling active")


# ---------------- NEXT STEP ----------------
st.divider()

st.subheader("Proceed to Region Scheduling Analysis")

if st.button("Run Scheduling Analysis"):
    st.switch_page("pages/scheduling.py")


# ---------------- FOOTER ----------------
st.markdown("""
---
<center style="color:gray;">
GreenCompute • Carbon-Aware Cloud Scheduling Dashboard
</center>
""", unsafe_allow_html=True)