from fastapi.testclient import TestClient
from .main import app
import os
import pytest

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
    id = create_sample()

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


def test_remove_dataset():
    # Create a sample CSV file for testing
    temp_csv_file = "test_dataset.csv"
    id = create_sample()

    # Send a DELETE request to remove the dataset
    response = client.delete(f"/datasets/{id}")

    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] == "dataset removed"

    os.remove(temp_csv_file)


def test_export_dataset_excel():
    # Create a sample CSV file for testing
    temp_csv_file = "test_dataset.csv"
    id = create_sample()

    # request to export the dataset as an Excel file
    response = client.get(f"/datasets/{id}/excel/")

    assert response.status_code == 200
    assert response.headers["content-type"] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    # Verify that the response content is not empty
    assert response.content

    # Clean up the temporary files
    os.remove(temp_csv_file)


def test_get_stats():
    # Create a sample CSV file for testing
    temp_csv_file = "test_dataset.csv"
    id = create_sample()

    # Send a GET request to retrieve the dataset stats
    response = client.get(f"/datasets/{id}/stats/")

    assert response.status_code == 200
    stats = response.json()
    assert stats["col1"]["count"] == 3
    assert stats["col2"]["mean"] == pytest.approx(4.0, abs=1e-2)
    assert stats["col2"]["25%"] == 3
    assert stats["col1"]["25%"] == 2

    # Clean up the temporary CSV file
    os.remove(temp_csv_file)

def create_sample():
    temp_csv_file = "test_dataset.csv"
    with open(temp_csv_file, "w") as f:
        f.write("col1,col2\n1,2\n3,4\n5,6\n")
    with open(temp_csv_file, "rb") as csv_file:
        res = client.post("/datasets/", files={"file": csv_file})
        res_json = res.json()
        id = res_json['id']
    return id
