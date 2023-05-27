from fastapi import FastAPI, File, UploadFile
import pandas as pd
from starlette.responses import JSONResponse
import uuid

app = FastAPI()

datasets = {}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/datasets/")
def list_datasets():
    return {"datasets": list(datasets)}


@app.post("/datasets/")
async def create_dataset(file: UploadFile = File(...)):
    try:
        # Read uploaded csv file and store it as a pandas dataframe
        df = pd.read_csv(file.file)
        # Generate a unique ID for the dataset
        dataset_id = uuid.uuid1()
        # Store the dataset in memory
        datasets[dataset_id] = df
        return {"dataset_id": dataset_id}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})