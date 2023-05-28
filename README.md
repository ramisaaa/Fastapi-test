# Datapane
Datapane is an API-driven product that provides client libraries / commandline applications that talk to an API server to handle and process datasets.

-----------------------------------------------------------------------

## API Server

### Installation

git clone ramisaaa/Fastapi-test

Install the required dependencies using pip:
> pip install -r requirements.txt


## Usage
start the API server with:

>  python3 -m uvicorn app.main:app --reload

* The API server will start running at http://localhost:8000.
* You can see the documentation at http://localhost:8000/docs.
* You can see the alternative automatic documentation at http://localhost:8000/redoc.
* To View the list the uploaded datasets, send a GET request to /datasets/.
* To upload a new dataset, send a POST request to /datasets/ with the CSV file as the request body.
* To get information about a specific dataset, send a GET request to /datasets/{id}/, where {id} is the ID of the dataset.
* To export a dataset as an Excel file, send a GET request to /datasets/{id}/excel/, where {id} is the ID of the dataset. The response will be the Excel file.
* To generate statistics for a dataset, send a GET request to /datasets/{id}/stats/, where {id} is the ID of the dataset. The response will be a JSON object containing the dataset statistics.
* To generate PDF plots for a dataset, send a GET request to /datasets/{id}/plot/, where {id} is the ID of the dataset. The response will be a PDF file containing histograms of all the numerical columns in the dataset.
* To delete a dataset, send a DELETE request to /datasets/{id}/, where {id} is the ID of the dataset.



-----------------------------------------------------------------------
## Dataset Client 

The Dataset API Client is a command-line Python application that interacts with the API server to perform various actions on datasets.


## Usage

To run the Dataset Client, use the following command:

> python3 app/client.py [arguments]


Replace `[arguments]` with one or more of the available command-line arguments listed below.

## Available Arguments

- `--list`: List of datasets.
- `--create <CSV_FILE>`: Create a dataset from a CSV file.
- `--info <ID>`: Get information about given dataset.
- `--excel <ID>`: Export a dataset to Excel.
- `--stats <ID>`: Generate statistics for a dataset.
- `--plot <ID>`: Generate histograms for a dataset.
- `--delete <ID>`: Delete a dataset.

**Note:** Replace `<CSV_FILE>` with the path to the CSV file you want to upload and `<ID>` with the ID of the dataset you want to perform actions on.

## Examples


> python3 app/client.py --list

> python3 app/client.py --create path/sample_data_1.csv

> python3 app/client.py --info c618bdb86ed141ba99a7355052322546

> python3 app/client.py --excel c618bdb86ed141ba99a7355052322546

>  python3 app/client.py --stats c618bdb86ed141ba99a7355052322546

>  python3 app/client.py --plots c618bdb86ed141ba99a7355052322546

> python3 app/client.py --delete c618bdb86ed141ba99a7355052322546