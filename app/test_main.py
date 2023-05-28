from fastapi.testclient import TestClient
from .main import app
import os

client = TestClient(app)


def test_list_datasets():
    response = client.get("/datasets/")
    assert response.status_code == 200
    datasets = response.json()
    assert isinstance(datasets, list)
    for dataset in datasets:
        assert "id" in dataset
        assert "filename" in dataset
        assert "size" in dataset
        assert dataset["filename"].endswith(".csv")


def test_create_dataset():
    # Create a sample CSV file for testing
    temp_csv_file = "test_dataset.csv"
    with open(temp_csv_file, "w") as f:
        f.write("col1,col2\nvalue1,value2\n")

    with open(temp_csv_file, "rb") as csv_file:
        response = client.post("/datasets/", files={"file": csv_file})

    assert response.status_code == 200
    dataset = response.json()
    assert "id" in dataset
    assert "filename" in dataset
    assert "size" in dataset
    assert dataset["filename"].endswith(".csv")

    # remove test CSV file
    os.remove(temp_csv_file)


def test_get_dataset_info():
    # Create a sample CSV file for testing
    temp_csv_file = "test_dataset.csv"
    with open(temp_csv_file, "w") as f:
        f.write("col1,col2\nvalue1,value2\n")

    with open(temp_csv_file, "rb") as csv_file:
        res = client.post("/datasets/", files={"file": csv_file})
        res_json = res.json()
        id=res_json['id']

    response = client.get(f"/datasets/{id}")
    assert response.status_code == 200
    dataset = response.json()
    assert "id" in dataset
    assert "filename" in dataset
    assert "size" in dataset
    assert dataset["id"] == id
    assert dataset["filename"] == f"{id}.csv"
    assert isinstance(dataset["size"], int)

    # remove test CSV file
    os.remove(temp_csv_file)
