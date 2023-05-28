from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from starlette.responses import JSONResponse
from pydantic import BaseModel
import matplotlib.pyplot as plt
import pandas as pd
import uuid
import os
import shutil
import glob

app = FastAPI()

datasets = {}
UPLOAD_FOLDER = "uploads"


class Dataset(BaseModel):
    id: str
    filename: str
    size: int


@app.get("/")
async def root():
    return "Ramisa Heidari :)"


@app.get("/datasets/")
def list_datasets():
    datasets = []
    csv_files = glob.glob(os.path.join(UPLOAD_FOLDER, "*.csv"))
    for file_path in csv_files:
        if os.path.isfile(file_path):
            dataset = Dataset(
                id=str(os.path.basename(file_path).split('.')[0]),
                filename=os.path.basename(file_path),
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


@app.get("/datasets/{id}/excel/")
async def export_dataset_excel(id: str):
    file_path = os.path.join(UPLOAD_FOLDER, f"{id}.csv")
    # check if the file exists
    if os.path.exists(file_path) and os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        excel_path = os.path.join(UPLOAD_FOLDER, f"{id}.xlsx")
        df.to_excel(excel_path)
        return FileResponse(excel_path)
    else:
        return JSONResponse(status_code=404, content={"error": "dataset file not found"})


@app.get("/datasets/{id}/stats/")
async def get_stats(id: str):
    file_path = os.path.join(UPLOAD_FOLDER, f"{id}.csv")
    # check if the file exists
    if os.path.exists(file_path) and os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        stats = df.describe()
        return stats
    else:
        return JSONResponse(status_code=404, content={"error": "dataset file not found"})


@app.get("/datasets/{id}/plots/")
async def generate_plots(id: str):
    file_path = os.path.join(UPLOAD_FOLDER, f"{id}.csv")
    # check if the file exists
    if os.path.exists(file_path) and os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        # first check for all the numerical columns
        numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns

        # Generate histograms
        fig, axes = plt.subplots(len(numerical_columns), 1, figsize=(8, 4 * len(numerical_columns)))
        for i, column in enumerate(numerical_columns):
            ax = axes[i]
            ax.hist(df[column], bins=10)
            ax.set_xlabel(column)
            ax.set_ylabel('Frequency')

        # Save the plot as a PDF
        plot_path = os.path.join(UPLOAD_FOLDER, f"{id}_histograms.pdf")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()

        return FileResponse(plot_path, media_type='application/pdf')
    else:
        return JSONResponse(status_code=404, content={"error": "dataset file not found"})
