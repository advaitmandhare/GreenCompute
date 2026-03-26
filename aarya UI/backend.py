from fastapi import FastAPI, UploadFile, File
import os
import shutil
import json
from datetime import datetime

app = FastAPI()

UPLOAD_DIR = "uploads"
LOG_FILE = "logs.json"

# Create folder if not exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

    # -------- Store Parameters --------
    job_data = {
        "filename": file.filename,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Append to JSON log
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(job_data)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "status": "success",
        "message": "File and parameters stored successfully"
    }