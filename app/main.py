from fastapi import FastAPI, File, UploadFile
from starlette.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import uuid
import os
import shutil

app = FastAPI()

datasets = {}
UPLOAD_FOLDER = "uploads"


class Dataset(BaseModel):
    id: str
    filename: str
    size: int


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/datasets/")
def list_datasets():
    datasets = []

    for file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file)
        if os.path.isfile(file_path):
            dataset = Dataset(
                id=str(file.split('.')[0]),
                filename=file,
                size=os.path.getsize(file_path)
            )
            datasets.append(dataset)
    return datasets


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
        return Dataset(
            id=str(file_name.split('.')[0]),
            filename=file_name,
            size=os.path.getsize(file_path)
        )
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.get("/datasets/{id}")
async def get_dataset_info(id: str):
    file_name = f"{id}.csv"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    # check if the given id is a file or not
    if not os.path.isfile(file_path):
        return JSONResponse(status_code=404, content={"error": "dataset file not found"})

    file_size = os.path.getsize(file_path)
    return Dataset(
        id=str(file_name.split('.')[0]),
        filename=file_name,
        size=os.path.getsize(file_path)
    )


@app.delete("/datasets/{id}")
async def remove_dataset(id: str):
    file_path = os.path.join(UPLOAD_FOLDER, f"{id}.csv")
    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
        return JSONResponse(status_code=200, content={"success": "dataset removed"})
    else:
        return JSONResponse(status_code=404, content={"error": "dataset file not found"})
