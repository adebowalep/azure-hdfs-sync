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

# Base path for downloaded files
download_base = "downloaded_runs"

# Local folder containing HDF5 files to upload
local_folder = "mock_hdf5_runs"

# SETUP LOGGING
# Create the upload log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/upload_log.txt"),
        logging.StreamHandler()
    ]
)

# CONNECT TO AZURE BLOB STORAGE
try:
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)

    try:
        container_client.create_container()
        logging.info(f"Container '{container_name}' created.")
    
    except Exception as e:
        logging.warning(f"Container likely exists: {e}")

except Exception as e:
    logging.error("Failed to connect to Azure Blob Storage.")
    raise

# UPLOAD FILES TO AZURE
for root, _, files in os.walk(local_folder):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        blob_path = os.path.relpath(file_path, local_folder).replace("\\", "/")
        
        # Upload the file to Azure Blob Storage
        try:
            with open(file_path, "rb") as data:
                container_client.upload_blob(name=blob_path, data=data, overwrite=True)
                logging.info(f"Uploaded: {blob_path}")
        except Exception as e:
            logging.error(f"Failed to upload {blob_path}: {e}")