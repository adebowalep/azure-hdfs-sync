import os
import logging
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# CONFIGURATION
# Connection string
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
# Container name
container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

# Validate configuration
if not connect_str or not container_name:
    raise ValueError("Azure Storage connection string and container name must be set in environment variables.")
download_base = "downloaded_runs"

# SETUP LOGGING
# Create the download log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/download_log.txt"),
        logging.StreamHandler()
    ]
)

# CONNECT TO AZURE BLOB STORAGE
try:
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)
    logging.info(f"Connected to container: {container_name}")
    # If the container already exists, we can proceed without creating it
except Exception as e:
    logging.error("Failed to connect to Azure Blob Storage.")
    raise

# DOWNLOAD FILES FROM AZURE BLOB STORAGE
for blob in container_client.list_blobs():

    # Local path for downloaded file
    local_path = os.path.join(download_base, blob.name.replace("/", os.sep))
    
    # Directories
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    if not os.path.exists(local_path):
        try:
            with open(local_path, "wb") as file:
                blob_data = container_client.download_blob(blob)
                file.write(blob_data.readall())
            logging.info(f"Downloaded: {blob.name}")
        except Exception as e:
            logging.error(f"Failed to download {blob.name}: {e}")
    else:
        logging.info(f"Skipped (exists): {blob.name}")
