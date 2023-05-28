from fastapi.testclient import TestClient
from .main import app
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



