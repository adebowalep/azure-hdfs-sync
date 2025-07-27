# Data Engineering Challenge: Simulation Pipeline with Azure Blob Storage

## Overview
This project demonstrates a practical data pipeline to support geophysical simulations involving the transfer of large HDF5 files between a local machine and the cloud. The workflow uses **Azure Blob Storage** to store and retrieve simulation files, organized by simulation run. The pipeline ensures that only missing files are downloaded and organizes them cleanly by folder.

## Architecture Diagram
```
Local Machine
       ↓
Azure Blob Storage (processed outputs)
       ↓
Local Machine (downloads organized by run)
```

*Interaction is handled via the Azure SDK (Python) with secure authentication.*

## Contents
- `generate_hdfs.py`: Generates synthetic HDF5 simulation data for testing.
- `upload_to_azure.py`: Uploads HDF5 files from local machine to Azure Blob Storage.
- `download_from_azure.py`: Downloads only missing files and organizes them by simulation run.
- `.env`: Environment file to securely store your Azure connection string and container name.
- `requirements.txt`: Python packages needed to run the scripts.
- `logs/`: Directory containing `upload.log` and `download.log` (optional).

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create a `.env` File
```env
AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here
AZURE_STORAGE_CONTAINER_NAME=simulation-data
```

> ⚠️ Make sure `.env` is listed in `.gitignore`.

### 3. Generate Test Data
```bash
python generate_hdfs.py
```

### 4. Upload Files
```bash
python upload_to_azure.py
```

### 5. Download Files
```bash
python download_from_azure.py
```

## Folder Structure Example
```
mock_hdf5_runs/
├── run_01/
│   ├── sample_01.h5
│   └── sample_02.h5
├── run_02/
│   ├── sample_01.h5
│   └── sample_02.h5

.env                 # Not committed to version control
logs/                # Contains upload.log and download.log
```

## Notes
- Azure SDK for Python is used for secure blob interaction.
- Logging is included in upload and download steps.
- Files are checked before download to avoid duplication.
- Downloaded files are organized into folders by simulation run.

## Author
Suleiman Ojo
