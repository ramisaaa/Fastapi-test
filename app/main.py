from fastapi import FastAPI, File, UploadFile
from starlette.responses import JSONResponse
import pandas as pd
import uuid
import os
import shutil

app = FastAPI()

datasets = {}
UPLOAD_FOLDER = "uploads"


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/datasets/")
def list_datasets():
    file_lists = []
    for file_name in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        if os.path.isfile(file_path):
            file_lists.append(file_name)
    return {"datasets": file_lists}


@app.post("/datasets/")
async def create_dataset(file: UploadFile = File(...)):
    try:
        # create the defined upload folder if it does not exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        # Generate a unique ID for the dataset
        dataset_id = uuid.uuid4()
        file_name = f"{dataset_id.hex}.csv"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # Read CSV file and store it as a pandas dataframe
        df = pd.read_csv(file_path)
        # Store the dataset in memory
        datasets[dataset_id] = df
        return {"dataset_id": dataset_id}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
