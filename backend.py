#  ###########  SANIKA CODE  ############


# from fastapi import FastAPI, UploadFile, File
# import os
# import shutil
# import json
# from datetime import datetime
# import requests
# import pandas as pd
# from final_ec2_runner import run_job
# import threading

# app = FastAPI()

# UPLOAD_DIR = "uploads"
# LOG_FILE = "logs.json"

# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # 🔑 API Key
# API_KEY = "U7aZyJUPsEGr7wsTPemW"

# # 🌍 Regions
# regions = {
#     "France": "FR",
#     # "Zurich": "CH",
#     "Frankfurt": "DE",
#     "Stockholm": "SE3",
#     "Western India": "IN-WE"
# }

# aws_region_map = {
#     "France": "eu-west-3",
#     # "Zurich": "eu-central-2",
#     "Frankfurt": "eu-central-1",
#     "Stockholm": "eu-north-1",
#     "Western India": "ap-south-1"
# }

# # ⚡ Mock Latency (ms)
# latency_map = {
#     "France": 120,
#     # "Zurich": 110,
#     "Frankfurt": 100,
#     "Stockholm": 130,
#     "Western India": 80
# }

# @app.post("/submit/")
# async def submit_job(
#     file: UploadFile = File(...),
#     alpha: float = 0.5,
#     beta: float = 0.3,
#     gamma: float = 0.2
# ):

#     # -------- Save File --------
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     headers = {"auth-token": API_KEY}

#     # -------- Fetch Raw Data --------
#     raw_data = []

#     for region_name, zone in regions.items():
#         try:
#             ci_res = requests.get(
#                 "https://api.electricitymaps.com/v3/carbon-intensity/latest",
#                 headers=headers,
#                 params={"zone": zone}
#             )
#             ci_res.raise_for_status()
#             carbon = ci_res.json().get("carbonIntensity")

#             pb_res = requests.get(
#                 "https://api.electricitymaps.com/v3/power-breakdown/latest",
#                 headers=headers,
#                 params={"zone": zone}
#             )
#             pb_res.raise_for_status()
#             renewable = pb_res.json().get("renewablePercentage")

#             if carbon is None or renewable is None:
#                 print(f"Skipping {region_name} due to missing data")
#                 continue

#             latency = latency_map.get(region_name, 100)

#             raw_data.append({
#                 "Region": region_name,
#                 "Carbon": carbon,
#                 "Latency": latency,
#                 "Renewable": renewable
#             })

#         except Exception as e:
#             print(f"Error in {region_name}: {e}")
#             continue

#     # ❌ No data case
#     if not raw_data:
#         return {
#             "status": "error",
#             "message": "No data fetched. Check API key or zones."
#         }

#     df = pd.DataFrame(raw_data)

#     # -------- Min-Max Normalization --------
#     def normalize(series):
#         min_val = series.min()
#         max_val = series.max()
#         if max_val - min_val == 0:
#             return [0.5] * len(series)
#         return (series - min_val) / (max_val - min_val)

#     df["Carbon_norm"] = normalize(df["Carbon"])
#     df["Latency_norm"] = normalize(df["Latency"])
#     df["Renewable_norm"] = normalize(df["Renewable"])

#     # -------- Compute Scores --------
#     scores = []

#     for _, row in df.iterrows():

#         # Optional: convert renewable to "cost"
#         renewable_cost = 1 - row["Renewable_norm"]

#         score = (
#             alpha * row["Carbon_norm"]
#             + beta * row["Latency_norm"]
#             + gamma * renewable_cost
#         )

#         scores.append({
#             "Region": row["Region"],
#             "Carbon": row["Carbon"],
#             "Latency": row["Latency"],
#             "Renewable": row["Renewable"],
#             "Carbon_norm": round(row["Carbon_norm"], 3),
#             "Latency_norm": round(row["Latency_norm"], 3),
#             "Renewable_norm": round(row["Renewable_norm"], 3),
#             "Score": round(score, 4)
#         })

#     # -------- Best Region --------
#     best_region = min(scores, key=lambda x: x["Score"])

#     # -------- Run Job on EC2 (NON-BLOCKING) --------
#     job_id = None
#     try:
#         selected_region_name = best_region["Region"]
#         aws_region = aws_region_map.get(selected_region_name, "ap-south-1")

#         print(f"🌍 Selected AWS Region: {aws_region}")
       
#         job_id = run_job(aws_region, file_path)
        
#         print("🚀 EC2 Job Triggered in Background")

#     except Exception as e:
#         print(f"❌ EC2 Execution Failed: {e}")

#     # -------- Store Logs --------
#     job_data = {
#         "filename": file.filename,
#         "alpha": alpha,
#         "beta": beta,
#         "gamma": gamma,
#         "best_region": best_region,
#         "all_scores": scores,
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }

#     if os.path.exists(LOG_FILE):
#         with open(LOG_FILE, "r") as f:
#             data = json.load(f)
#     else:
#         data = []

#     data.append(job_data)

#     with open(LOG_FILE, "w") as f:
#         json.dump(data, f, indent=4)

#     return {
#         "status": "success",
#         "best_region": best_region,
#         "all_scores": scores,
#         "job_id": job_id
#     }


######### Latency Code ##########

from fastapi import FastAPI, UploadFile, File
import os
import shutil
import json
from datetime import datetime
import requests
import pandas as pd
from final_ec2_runner import run_job
import socket
import time
import numpy as np

app = FastAPI()

UPLOAD_DIR = "uploads"
LOG_FILE = "logs.json"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🔑 API Key
API_KEY = "U7aZyJUPsEGr7wsTPemW"

# 🌍 Regions (Electricity Maps Zones)
regions = {
    "France": "FR",
    "Frankfurt": "DE",
    "Stockholm": "SE3",
    "Western India": "IN-WE"
}

# 🌍 AWS Region Mapping
aws_region_map = {
    "France": "eu-west-3",
    "Frankfurt": "eu-central-1",
    "Stockholm": "eu-north-1",
    "Western India": "ap-south-1"
}

# 🌐 Hosts for TCP latency
region_hosts = {
    "France": "ec2.eu-west-3.amazonaws.com",
    "Frankfurt": "ec2.eu-central-1.amazonaws.com",
    "Stockholm": "ec2.eu-north-1.amazonaws.com",
    "Western India": "ec2.ap-south-1.amazonaws.com"
}


# TCP LATENCY FUNCTION

def tcp_latency(host, port=443, timeout=2):
    try:
        start = time.time()
        socket.create_connection((host, port), timeout=timeout)
        return (time.time() - start) * 1000  # ms
    except Exception:
        return np.nan


# NORMALIZATION FUNCTION

def normalize(series):
    series = series.fillna(series.mean())
    min_val = series.min()
    max_val = series.max()
    if max_val - min_val == 0:
        return [0.5] * len(series)
    return (series - min_val) / (max_val - min_val)


# MAIN API

@app.post("/submit/")
async def submit_job(
    file: UploadFile = File(...),
    alpha: float = 0.5,
    beta: float = 0.3,
    gamma: float = 0.2
):

    # -------- Save File --------
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    headers = {"auth-token": API_KEY}

    raw_data = []

    # -------- Fetch Data + Latency --------
    for region_name, zone in regions.items():
        try:
            # 🌿 Carbon Intensity
            ci_res = requests.get(
                "https://api.electricitymaps.com/v3/carbon-intensity/latest",
                headers=headers,
                params={"zone": zone},
                timeout=5
            )
            ci_res.raise_for_status()
            carbon = ci_res.json().get("carbonIntensity")

            # 🌱 Renewable %
            pb_res = requests.get(
                "https://api.electricitymaps.com/v3/power-breakdown/latest",
                headers=headers,
                params={"zone": zone},
                timeout=5
            )
            pb_res.raise_for_status()
            renewable = pb_res.json().get("renewablePercentage")

            # ⚡ Latency (REAL)
            host = region_hosts.get(region_name)
            latency = tcp_latency(host)

            if carbon is None or renewable is None or np.isnan(latency):
                print(f"Skipping {region_name} due to missing data")
                continue

            raw_data.append({
                "Region": region_name,
                "Carbon": carbon,
                "Latency": latency,
                "Renewable": renewable
            })

        except Exception as e:
            print(f"Error in {region_name}: {e}")
            continue

    # No valid data
    if not raw_data:
        return {
            "status": "error",
            "message": "No data fetched. Check API key, zones, or network."
        }

    df = pd.DataFrame(raw_data)

    # -------- Normalization --------
    df["Carbon_norm"] = normalize(df["Carbon"])
    df["Latency_norm"] = normalize(df["Latency"])
    df["Renewable_norm"] = normalize(df["Renewable"])

    # -------- Compute Scores --------
    scores = []

    for _, row in df.iterrows():

        renewable_cost = 1 - row["Renewable_norm"]

        score = (
            alpha * row["Carbon_norm"]
            + beta * row["Latency_norm"]
            + gamma * renewable_cost
        )

        scores.append({
            "Region": row["Region"],
            "Carbon": row["Carbon"],
            "Latency": round(row["Latency"], 2),
            "Renewable": row["Renewable"],
            "Carbon_norm": round(row["Carbon_norm"], 3),
            "Latency_norm": round(row["Latency_norm"], 3),
            "Renewable_norm": round(row["Renewable_norm"], 3),
            "Score": round(score, 4)
        })

    # -------- Best Region --------
    best_region = min(scores, key=lambda x: x["Score"])

    # -------- Trigger EC2 Job --------
    job_id = None
    try:
        selected_region_name = best_region["Region"]
        aws_region = aws_region_map.get(selected_region_name, "ap-south-1")

        print(f"🌍 Selected AWS Region: {aws_region}")

        job_id = run_job(aws_region, file_path)

        print("🚀 EC2 Job Triggered")

    except Exception as e:
        print(f"❌ EC2 Execution Failed: {e}")

    # -------- Store Logs --------
    job_data = {
        "filename": file.filename,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "best_region": best_region,
        "all_scores": scores,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(job_data)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

    # -------- Response --------
    return {
        "status": "success",
        "best_region": best_region,
        "all_scores": scores,
        "job_id": job_id
    }