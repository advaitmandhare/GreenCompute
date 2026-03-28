import streamlit as st
import requests
import boto3
import time
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="GreenCompute", layout="wide")

# ---------------- PREMIUM CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(180deg, #020617, #020617);
    color: white;
}

/* Header */
.header {
    padding: 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 10px;
}

/* Navbar pills */
div[role="radiogroup"] > label {
    background: rgba(255,255,255,0.05);
    padding: 6px 14px;
    border-radius: 20px;
    margin-right: 8px;
}

div[role="radiogroup"] > label[data-checked="true"] {
    background: linear-gradient(90deg, #22c55e, #16a34a);
    color: white;
}

/* Cards */
.card {
    background: linear-gradient(145deg, rgba(15,23,42,0.9), rgba(2,6,23,0.95));
    padding: 22px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 35px rgba(0,0,0,0.7);
    margin-bottom: 18px;
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 45px rgba(0,0,0,0.85);
}

/* Titles */
.card-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 14px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- S3 Fetch Function ----------------
def fetch_output_from_s3(job_id):
    s3 = boto3.client("s3")

    bucket = "green-compute-demo-sanika"
    key = f"{job_id}/output/output.txt"

    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        content = obj["Body"].read().decode("utf-8")
        return content, True
    except Exception:
        return "⏳ Job still running... refresh shortly.", False


# ---------------- REGION MAP ----------------
aws_region_map = {
    "France": "eu-west-3",
    "Frankfurt": "eu-central-1",
    "Stockholm": "eu-north-1",
    "Western India": "ap-south-1"
}

# ---------------- SESSION ----------------
if "job_id" not in st.session_state:
    st.session_state.job_id = None

if "result" not in st.session_state:
    st.session_state.result = None

if "alpha" not in st.session_state:
    st.session_state.alpha = 0.4

if "beta" not in st.session_state:
    st.session_state.beta = 0.3


# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
<h2>💻 GreenCompute </h2>
</div>
""", unsafe_allow_html=True)


# ---------------- NAVBAR ----------------
page = st.radio(
    "",
    ["Submit Job", "Execution Insights", "Sustainability Impact"],
    horizontal=True
)


# =====================================================
# PAGE 1 — SUBMIT JOB
# =====================================================
if page == "Submit Job":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">⚙️ Job Configuration</div>', unsafe_allow_html=True)

    inner1, inner2 = st.columns([1, 1.2])

    with inner1:
        alpha = st.slider("Carbon Intensity (α)", 0.0, 1.0, st.session_state.alpha, step=0.05)

        max_beta = round(1.0 - alpha, 2)
        if st.session_state.beta > max_beta:
            st.session_state.beta = max_beta

        beta = st.slider("Latency (β)", 0.0, max_beta, st.session_state.beta, step=0.05)

        gamma = round(1.0 - alpha - beta, 2)

        st.session_state.alpha = alpha
        st.session_state.beta = beta

        st.caption(f"Renewable factor (γ) = {gamma}")

        st.markdown("---")

        uploaded_file = st.file_uploader("Upload ML Script (.py)", type=["py"])

        if st.button("🚀 Run Scheduler", use_container_width=True):

            if uploaded_file is None:
                st.warning("Upload file first")
            else:
                response = requests.post(
                    "http://127.0.0.1:8000/submit/",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue())},
                    params={"alpha": alpha, "beta": beta, "gamma": gamma}
                )

                if response.status_code == 200:
                    res = response.json()
                    if res["status"] == "success":
                        st.session_state.job_id = res["job_id"]
                        st.session_state.result = res

    with inner2:
        df = pd.DataFrame({
            "Metric": ["Carbon", "Latency", "Renewable"],
            "Value": [alpha, beta, gamma]
        })

        fig = px.pie(df, names="Metric", values="Value", hole=0.4)

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    result = st.session_state.result

    if result:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        best_region = result["best_region"]["Region"]
        aws_region = aws_region_map[best_region]

        st.markdown("### 🏆 Selected Region")
        st.json(result["best_region"])

        st.success(f"Scheduled in {best_region} ({aws_region})")

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- SHOW OUTPUT (UNCHANGED) ----------------
    result = st.session_state.result
    job_id = st.session_state.job_id

    if result:

        st.subheader("📤 Job Output")

        output, ready = fetch_output_from_s3(job_id)

        if ready:

            execution_time = round(
                time.time() - st.session_state.start_time, 2
            )

            st.success("Execution completed successfully")

            st.metric("⏱ Execution Time", f"{execution_time} sec")

            st.code(output)

        else:

            st.warning(output)

        if st.button("🔄 Refresh Output"):
            st.rerun()


# =====================================================
# PAGE 2 — EXECUTION INSIGHTS
# =====================================================
elif page == "Execution Insights":

    st.markdown("## ⚡ Execution Insights")

    result = st.session_state.result

    if result:
        best = result["best_region"]

        st.markdown('<div class="card">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        col1.metric("Region", best["Region"])
        col1.metric("Latency", f'{best["Latency"]} ms')

        col2.metric("Carbon", f'{best["Carbon"]} gCO₂/kWh')
        col2.metric("Renewable", f'{best["Renewable"]}%')

        df = pd.DataFrame(result["all_scores"])
        st.dataframe(df, use_container_width=True)

        selected_region = best["Region"]

        df["Highlight"] = df["Region"].apply(
            lambda x: "Selected ✅" if x == selected_region else "Other"
        )

        colA, colB = st.columns(2)

        with colA:
            fig_bar = px.bar(
                df.sort_values("Score"),
                x="Region",
                y="Score",
                color="Highlight",
                text="Score",
                title="🏆 Decision Score Across Regions"
            )

            fig_bar.update_traces(textposition="outside")

            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                transition_duration=800
            )

            for trace in fig_bar.data:
                if trace.name == "Selected ✅":
                    trace.marker.line.width = 3
                else:
                    trace.opacity = 0.4

            st.plotly_chart(fig_bar, use_container_width=True)

        with colB:
            fig_scatter = px.scatter(
                df,
                x="Latency",
                y="Carbon",
                size="Renewable",
                color="Highlight",
                hover_name="Region",
                title="⚖️ Carbon vs Latency Trade-off",
            )

            fig_scatter.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                transition_duration=800
            )

            for trace in fig_scatter.data:
                if trace.name == "Selected ✅":
                    trace.marker.line.width = 3
                else:
                    trace.opacity = 0.4

            st.plotly_chart(fig_scatter, use_container_width=True)

        best_score = df["Score"].max()
        selected_score = df[df["Region"] == selected_region]["Score"].values[0]
        potential_gain = round(best_score - selected_score, 4)

        st.markdown("---")

        colX, colY = st.columns(2)
        colX.metric("Selected Score", round(selected_score, 4))
        colY.metric("Missed Optimization", potential_gain if potential_gain > 0 else "Optimal ✅")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ⚙ AI Decision Explanation")

        lowest_carbon = df.loc[df["Carbon"].idxmin()]
        fastest = df.loc[df["Latency"].idxmin()]

        explanation = f"""
The scheduler selected **{selected_region}** as the optimal region.

• Balanced **carbon ({best['Carbon']})** and **latency ({best['Latency']})**  
• Lower emissions than fastest region (**{fastest['Region']}**)  
• Faster than greenest region (**{lowest_carbon['Region']}**)  
• Renewable share: **{best['Renewable']}%**

This reflects an efficient multi-objective optimization.
"""

        st.markdown(f"<div style='opacity:0.85'>{explanation}</div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Submit job first")


# =====================================================
# PAGE 3 — SUSTAINABILITY IMPACT (HACKATHON UI)
# =====================================================
elif page == "Sustainability Impact":

    st.markdown("## 🌱 Sustainability Impact")

    result = st.session_state.result

    if result:

        scores = result["all_scores"]
        best = result["best_region"]

        df = pd.DataFrame(scores)

        avg_carbon = df["Carbon"].mean()
        avg_renewable = df["Renewable"].mean()

        carbon_saved = avg_carbon - best["Carbon"]
        renewable_gain = best["Renewable"] - avg_renewable

        selected_region = best["Region"]

        df["Highlight"] = df["Region"].apply(
            lambda x: "Selected ✅" if x == selected_region else "Other"
        )

        # ================= TOP METRICS =================
        st.markdown('<div class="card">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("🌍 Carbon Reduction", f"{round(carbon_saved,2)} gCO₂/kWh")
        col2.metric("🌿 Renewable Gain", f"{round(renewable_gain,2)} %")
        col3.metric("⚡ Latency", f"{best['Latency']} ms")

        st.markdown('</div>', unsafe_allow_html=True)

        # ================= TRADEOFF CHARTS =================
        colA, colB = st.columns(2)

        with colA:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            fig_renew = px.bar(
                df.sort_values("Renewable", ascending=False),
                x="Region",
                y="Renewable",
                color="Highlight",
                text="Renewable",
                title="🌿 Renewable Share Across Regions"
            )

            fig_renew.update_traces(textposition="outside")

            fig_renew.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                transition_duration=800
            )

            for trace in fig_renew.data:
                if trace.name == "Selected ✅":
                    trace.marker.line.width = 3
                else:
                    trace.opacity = 0.4

            st.plotly_chart(fig_renew, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with colB:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            fig_tradeoff = px.scatter(
                df,
                x="Carbon",
                y="Renewable",
                size="Latency",
                color="Highlight",
                hover_name="Region",
                title="⚖️ Carbon vs Renewable Trade-off"
            )

            fig_tradeoff.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                transition_duration=800
            )

            for trace in fig_tradeoff.data:
                if trace.name == "Selected ✅":
                    trace.marker.line.width = 3
                else:
                    trace.opacity = 0.4

            st.plotly_chart(fig_tradeoff, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ================= IMPACT VISUALS (SIDE-BY-SIDE) =================
        col1, col2 = st.columns([1, 1.2])  # slightly emphasize right chart

        # -------- Carbon Savings --------
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            comp_df = pd.DataFrame({
                "Type": ["Average Region", "Selected Region"],
                "Carbon": [avg_carbon, best["Carbon"]]
            })

            fig_carbon = px.bar(
                comp_df,
                x="Type",
                y="Carbon",
                text="Carbon",
                title="📉 Carbon Savings Visualization"
            )

            fig_carbon.update_traces(textposition="outside")

            fig_carbon.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                transition_duration=800
            )

            st.plotly_chart(fig_carbon, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # -------- Decision Contribution --------
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            norm_df = df.copy()

            norm_df["Carbon_norm"] = norm_df["Carbon"] / norm_df["Carbon"].max()
            norm_df["Latency_norm"] = norm_df["Latency"] / norm_df["Latency"].max()
            norm_df["Renewable_norm"] = norm_df["Renewable"] / 100

            melted = norm_df.melt(
                id_vars=["Region"],
                value_vars=["Carbon_norm", "Latency_norm", "Renewable_norm"],
                var_name="Metric",
                value_name="Value"
            )

            fig_stack = px.bar(
                melted,
                x="Region",
                y="Value",
                color="Metric",
                title="🔄 Decision Factor Contribution"
            )

            fig_stack.update_layout(
                barmode="stack",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                transition_duration=800
            )

            st.plotly_chart(fig_stack, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ================= AI EXPLANATION =================
        st.markdown('<div class="card">', unsafe_allow_html=True)

        lowest_carbon = df.loc[df["Carbon"].idxmin()]
        highest_renewable = df.loc[df["Renewable"].idxmax()]

        explanation = f"""
The scheduler selected **{selected_region}** as the most sustainable execution region.

• Achieves **{round(carbon_saved,2)} gCO₂/kWh lower emissions** than average  
• Offers **{best['Renewable']}% renewable energy**, among top regions  
• Maintains balanced latency (**{best['Latency']} ms**)  

Compared to alternatives:  
• Greenest region → **{lowest_carbon['Region']}** (but slower)  
• Highest renewable → **{highest_renewable['Region']}**  

This reflects a **multi-objective optimization balancing carbon, latency, and renewable energy (γ)**.
"""

        st.markdown(f"<div style='opacity:0.85'>{explanation}</div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Submit job first")