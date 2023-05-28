import argparse
import requests
import os

BASE_URL = "http://localhost:8000"


parser = argparse.ArgumentParser(description="Dataset API Client")

# List datasets
parser.add_argument("--list", action="store_true", help="List uploaded datasets")

# Create dataset
parser.add_argument("--create", metavar="CSV_FILE", help="Create a dataset from a CSV file")

# Get dataset info
parser.add_argument("--info", metavar="ID", type=str, help="Get information about a dataset")

# Export dataset to Excel
parser.add_argument("--excel", metavar="ID", type=str, help="Export a dataset to Excel")

# Generate dataset statistics
parser.add_argument("--stats", metavar="ID", type=str, help="Generate statistics for a dataset")

# Generate histograms
parser.add_argument("--plot", metavar="ID", type=str, help="Generate histograms for a dataset")

# Delete dataset
parser.add_argument("--delete", metavar="ID", type=str, help="Delete a dataset")

args = parser.parse_args()

if args.list:
    response = requests.get(f"{BASE_URL}/datasets/")
    datasets = response.json()
    print("Uploaded datasets:")
    for dataset in datasets:
        print(f"- ID: {dataset['id']}, Filename: {dataset['filename']}, Size: {dataset['size']} bytes")

if args.create:
    csv_file = args.create
    if os.path.exists(csv_file) and os.path.isfile(csv_file):
        with open(csv_file, "rb") as file:
            response = requests.post(f"{BASE_URL}/datasets/", files={"file": file})
            if response.status_code == 200:
                created_dataset = response.json()
                print("Dataset created successfully:")
                print(
                    f"- ID: {created_dataset['id']}, Filename: {created_dataset['filename']}, Size: {created_dataset['size']} bytes")
            else:
                print("Failed to create dataset.")
    else:
        print("CSV file not found.")

if args.info:
    dataset_id = args.info
    response = requests.get(f"{BASE_URL}/datasets/{dataset_id}/")
    if response.status_code == 200:
        dataset_info = response.json()
        print("Dataset information:")
        print(f"- ID: {dataset_info['id']}, Filename: {dataset_info['filename']}, Size: {dataset_info['size']} bytes")
    else:
        print("Failed to retrieve dataset information.")

if args.excel:
    dataset_id = args.excel
    response = requests.get(f"{BASE_URL}/datasets/{dataset_id}/excel/")
    if response.status_code == 200 and response.headers.get('content-type') == 'application/pdf':
        with open(f"{dataset_id}_dataset.xlsx", 'wb') as file:
            file.write(response.content)
        print("Dataset exported to Excel successfully.")
    else:
        print("Failed to export dataset to Excel.")

if args.stats:
    dataset_id = args.stats
    response = requests.get(f"{BASE_URL}/datasets/{dataset_id}/stats/")
    if response.status_code == 200:
        dataset_stats = response.json()
        print("Dataset statistics:")
        for key, value in dataset_stats.items():
            print(f"- {key}: {value}")
    else:
        print("Failed to retrieve dataset statistics.")

if args.plot:
    dataset_id = args.plot
    response = requests.get(f"{BASE_URL}/datasets/{dataset_id}/plot/")
    if response.status_code == 200 and response.headers.get('content-type') == 'application/pdf':
        with open(f"{dataset_id}_histograms.pdf", 'wb') as file:
            file.write(response.content)
        print("Histograms generated and saved as PDF successfully.")
    else:
        print("Failed to generate histograms.")

if args.delete:
    dataset_id = args.delete
    response = requests.delete(f"{BASE_URL}/datasets/{dataset_id}/")
    if response.status_code == 200:
        print("Dataset deleted successfully.")
    else:
        print("Failed to delete dataset.")

