"""Utils to download datasets and models from drive.
"""
import requests
from scisum.config import DATA_DIR, DATASETS, DOWNLOAD, FILENAME, MODELS, MODELS_DIR
import os
from pathlib import Path
import logging


def download_data():
    """Download datasets from drive. Save them in DATA_DIR directory.
    """
    for dataset in DATASETS.values():
        filename = dataset[FILENAME]
        download_id = dataset[DOWNLOAD][dataset[FILENAME]]
        destination = os.path.join(DATA_DIR, filename)
        download_file_from_google_drive(download_id, destination)

def download_models():
    """Download trained models from drive. Save them in MODELS_DIR directory.
    """
    logging.info("Downloading all models")
    for model in MODELS.values():
        dir_name = model[FILENAME]
        dir_path = Path(MODELS_DIR) / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        files = model[DOWNLOAD].items()
        logging.info(f" > {dir_name} model: {len(files)} files to download")
        for filename, google_id in files:
            logging.info(f"-- Start download of {filename}")
            destination = dir_path / filename
            download_file_from_google_drive(google_id, destination)
        logging.info(f"-- Completed!")
    logging.info("End of download.")

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == '__main__':
    download_data()
    download_models()
