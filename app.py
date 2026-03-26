import streamlit as st
import requests
import boto3

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
        return "⏳ Job is still running... please wait 1–2 minutes and click refresh.", False


# ---------------- Page Config ----------------
st.set_page_config(
    page_title="GreenCompute Dashboard",
    layout="centered"
)

# ---------------- Session Init ----------------
if "job_id" not in st.session_state:
    st.session_state["job_id"] = None

if "result" not in st.session_state:
    st.session_state["result"] = None


# ---------------- Title ----------------
st.title("🌱 GreenCompute Dashboard")
st.markdown("Upload your ML task and configure parameters")

# ---------------- Sliders ----------------
st.subheader("⚙️ Configure Parameters (Sum = 1)")

alpha = st.slider("Alpha (Carbon)", 0.0, 1.0, 0.5)

remaining = 1.0 - alpha
beta = st.slider("Beta (Latency)", 0.0, remaining, 0.3)

gamma = round(1.0 - alpha - beta, 2)

st.info(f"Gamma (Renewable) auto-set to: {gamma}")

# ---------------- File Upload ----------------
st.subheader("📂 Upload Python File")

uploaded_file = st.file_uploader(
    "Upload your ML Python file (.py)",
    type=["py"]
)

# ---------------- File Preview ----------------
if uploaded_file:
    st.markdown("### 📄 File Preview")
    st.code(uploaded_file.read().decode("utf-8"), language="python")

# ---------------- Submit ----------------
st.markdown("---")

if st.button("🚀 Submit Job"):

    if uploaded_file is None:
        st.warning("⚠️ Please upload a file first")
    else:
        try:
            with st.spinner("Submitting to backend..."):

                response = requests.post(
                    "http://127.0.0.1:8000/submit/",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue())},
                    params={
                        "alpha": alpha,
                        "beta": beta,
                        "gamma": gamma
                    }
                )

            if response.status_code != 200:
                st.error("❌ Backend error. Check terminal logs.")
            else:
                res = response.json()

                if res["status"] == "success":
                    st.success("✅ Job submitted successfully!")

                    # Save in session
                    st.session_state["job_id"] = res.get("job_id")
                    st.session_state["result"] = res

                else:
                    st.error(res.get("message", "❌ Failed"))

        except Exception as e:
            st.error(f"⚠️ Backend connection error: {e}")


# ---------------- Show Results (Persisted) ----------------
result = st.session_state.get("result")
job_id = st.session_state.get("job_id")

if result:

    # -------- Best Region --------
    st.subheader("🏆 Best Region")
    st.write(result["best_region"])

    # -------- Scores --------
    st.subheader("📊 All Region Scores")
    st.dataframe(result["all_scores"])

    # -------- Output Section --------
    st.subheader("📤 Job Output")

    if job_id:
        st.info(f"Job ID: {job_id}")

        output, ready = fetch_output_from_s3(job_id)

        if ready:
            st.success("✅ Output Ready")
            st.code(output, language="text")
        else:
            st.warning(output)

        # Refresh Button
        if st.button("🔄 Refresh Output"):
            st.rerun()

    else:
        st.warning("⚠️ No job ID found")


# ---------------- Footer ----------------
st.markdown("---")
st.caption("GreenCompute | Smart ML Scheduler 🌱")